from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="djangoasyncframework",
    version="0.3.2",
    packages=find_packages(),
    description=" Providing async views, ORM, and tasks for Django. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="mouhamaddev",
    author_email="mouhamaddev04@gmail.com",
    url="https://github.com/mouhamaddev/django-async-framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True   
)
