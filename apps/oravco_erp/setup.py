from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
	long_description = f.read()

setup(
	name="oravco_erp",
	version="1.0.0",
	description="Oravco ERP - Custom ERP Solution",
	author="Oravco",
	author_email="info@oravco.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[],
)

