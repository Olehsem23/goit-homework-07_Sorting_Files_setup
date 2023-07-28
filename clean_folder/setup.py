from setuptools import setup, find_namespace_packages

setup(
    name="Clean folder",
    version="0.0.1",
    description="Sorting of files due to their extensions",
    author="Olehsem",
    author_email="Olehsem23@gmail.com",
    url="https://github.com/Olehsem23/goit-homework-06_Sorting_Files",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    packages=find_namespace_packages(),
    include_package_data=True)
