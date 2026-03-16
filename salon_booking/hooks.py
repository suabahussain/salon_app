app_name = 'salon_booking'
app_title = 'Salon Booking'
app_publisher = 'Your Company'
app_description = 'Platform for booking home beauty and salon services.'
app_icon = 'octicon octicon-calendar'
app_color = 'pink'
app_email = 'support@example.com'
app_license = 'MIT'

fixtures = [
    {
        'dt': 'Role',
        'filters': [['name', 'in', ['Salon Customer', 'Service Provider Manager']]],
    }
]

doctype_js = {
    'Booking': 'public/js/booking.js',
}
