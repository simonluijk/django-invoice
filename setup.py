try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from invoice import __version__, __license__

setup(
    author='Simon Luijk',
    author_email='simon@simonluijk.com',
    name='django-invoice',
    version=__version__,
    license=__license__,
    description='Django invoicing app',
    url='https://github.com/simonluijk/django-invoice/',
    packages=find_packages(),
    install_requires=[
        'django-addresses',
        'django-extensions',
        'reportlab',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ]
)
