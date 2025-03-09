from setuptools import setup

setup(
    name="calculator",
    version="0.1.0",
    py_modules=["calculator"],
    package_dir={"": "."},
    exclude_package_data={"": ["test_*.py"]},
) 