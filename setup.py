from setuptools import setup, find_packages

setup(
    name='pluto-data',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=["litellm==1.7.12"]
)