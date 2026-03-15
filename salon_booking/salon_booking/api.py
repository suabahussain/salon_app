import frappe
from frappe import _
from frappe.utils import getdate, get_time


@frappe.whitelist()
def create_booking(customer, provider, service, booking_date, booking_time, address, latitude=None, longitude=None):
    """Create a booking record after checking provider availability."""
    is_available = check_provider_availability(provider=provider, booking_date=booking_date, booking_time=booking_time)
    if not is_available.get('available'):
        frappe.throw(_('Provider is not available for the selected slot.'))

    service_doc = frappe.get_doc('Service', service)
    booking = frappe.get_doc(
        {
            'doctype': 'Booking',
            'customer': customer,
            'provider': provider,
            'service': service,
            'booking_date': getdate(booking_date),
            'booking_time': get_time(booking_time),
            'address': address,
            'latitude': latitude,
            'longitude': longitude,
            'status': 'Pending',
            'price': service_doc.base_price,
        }
    )
    booking.insert(ignore_permissions=True)
    frappe.db.commit()

    return {'booking_id': booking.name, 'status': booking.status, 'price': booking.price}


@frappe.whitelist()
def get_nearby_providers(latitude, longitude, radius_km=10, service=None):
    """Find nearby providers using simple Euclidean approximation over lat/lng."""
    latitude = float(latitude)
    longitude = float(longitude)
    radius = float(radius_km)

    filters = {'is_active': 1}
    if service:
        filters['service'] = service

    providers = frappe.get_all(
        'Service Provider',
        fields=['name', 'provider_name', 'provider_type', 'latitude', 'longitude', 'average_rating', 'city'],
        filters=filters,
    )

    nearby = []
    for provider in providers:
        if provider.latitude is None or provider.longitude is None:
            continue

        distance = ((provider.latitude - latitude) ** 2 + (provider.longitude - longitude) ** 2) ** 0.5 * 111
        if distance <= radius:
            provider['distance_km'] = round(distance, 2)
            nearby.append(provider)

    return sorted(nearby, key=lambda x: x['distance_km'])


@frappe.whitelist()
def check_provider_availability(provider, booking_date, booking_time):
    """Check if provider has schedule and no overlapping booking."""
    weekday = getdate(booking_date).strftime('%A')
    slot_time = get_time(booking_time)

    availability = frappe.get_all(
        'Provider Availability',
        filters={'provider': provider, 'day_of_week': weekday, 'is_available': 1},
        fields=['name', 'start_time', 'end_time'],
    )

    in_schedule = any(slot.start_time <= slot_time <= slot.end_time for slot in availability)
    if not in_schedule:
        return {'available': False, 'reason': 'Outside configured availability'}

    conflict = frappe.db.exists(
        'Booking',
        {
            'provider': provider,
            'booking_date': getdate(booking_date),
            'booking_time': slot_time,
            'status': ['in', ['Pending', 'Confirmed', 'In Progress']],
        },
    )

    if conflict:
        return {'available': False, 'reason': 'Conflicting booking exists'}

    return {'available': True}


@frappe.whitelist()
def submit_review(booking, rating, review_text=None):
    """Submit review tied to a completed booking and update provider average rating."""
    booking_doc = frappe.get_doc('Booking', booking)
    if booking_doc.status != 'Completed':
        frappe.throw(_('Only completed bookings can be reviewed.'))

    if frappe.db.exists('Review Rating', {'booking': booking}):
        frappe.throw(_('Review already submitted for this booking.'))

    review = frappe.get_doc(
        {
            'doctype': 'Review Rating',
            'booking': booking,
            'customer': booking_doc.customer,
            'provider': booking_doc.provider,
            'rating': float(rating),
            'review_text': review_text,
        }
    )
    review.insert(ignore_permissions=True)

    avg = frappe.db.sql(
        """
        select avg(rating) as avg_rating
        from `tabReview Rating`
        where provider = %s
        """,
        (booking_doc.provider,),
        as_dict=True,
    )[0].avg_rating

    frappe.db.set_value('Service Provider', booking_doc.provider, 'average_rating', round(avg or 0, 2))
    frappe.db.commit()

    return {'review_id': review.name, 'provider_avg_rating': round(avg or 0, 2)}
