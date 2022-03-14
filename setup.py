from setuptools import setup, find_packages

setup(
    name='setup',
    packages=find_packages(),
    url='https://github.com/W14A-Jelly/e-invoice_receiving',
    description='Install python libraries for repo',
    install_requires=[
            'coverage==6.3.1',
            'Flask==2.0.3',
            'Flask-Cors==3.0.10',
            'imbox==0.9.8',
            'jwt==1.3.1',
            'lxml==4.8.0',
            'peewee==3.14.9',
            'py==1.11.0',
            'pybase64==1.2.1',
            'pycparser==2.21',
            'PyJWT==2.3.0',
            'pylint==2.12.2',
            'pyparsing==3.0.6',
            'pytest==7.0.1',
            'pytest-cov==3.0.0',
            'requests==2.27.1',
            'Werkzeug==2.0.3',
            'wrapt==1.13.3'
            ]
)