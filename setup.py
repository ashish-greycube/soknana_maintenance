from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in soknana_maintenance/__init__.py
from soknana_maintenance import __version__ as version

setup(
	name="soknana_maintenance",
	version=version,
	description="Customization for Soknana",
	author="GreyCube Technologies",
	author_email="admin@greycube.in",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
