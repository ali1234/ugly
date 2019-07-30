from setuptools import setup

setup(
    name='ugly',
    version='0.0.0',
    author='Alistair Buxton',
    author_email='a.j.buxton@gmail.com',
    url='https://github.com/ali1234/ugly',
    packages=['ugly', 'ugly.drivers', 'ugly.drivers.hardware', 'ugly.drivers.legacy', 'ugly.drivers.virtual', 'ugly.demos'],
    entry_points={
        'console_scripts': [
            'uglydemo = ugly.demos.demo:main',
        ]
    },
    install_requires=['numpy'],
)
