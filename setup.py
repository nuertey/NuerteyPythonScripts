# A good way to get moving is to turn the codebase into an installable 
# Python distribution like this:
from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
]

setup(
    name='nuertey_flask_project_1',
    version='0.0',
    description='Nuertey\'s first project built with Flask',
    author='Nuertey Odzeyem',
    author_email='nuertey_odzeyem@hotmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)
