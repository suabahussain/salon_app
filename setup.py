ffrom setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="salon_booking",
    version="0.0.1",
    description="Salon and beauty services booking platform for Frappe",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
