from setuptools import setup, find_packages

setup(
    name="flake8-django-view-returns",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["flake8>=5.0.0"],
    entry_points={
        "flake8.extension": [
            "DJV = flake8_django_view_returns:DjangoViewReturnChecker",
        ],
    },
)

