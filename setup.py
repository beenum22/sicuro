from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='sicuro',
	version='3.0',
	description='Secure your shit',
	long_description=readme(),
	url='http://github.com/beenum22/sicuro',
	author='Muneeb Ahmad',
	author_email='muneeb.gandapur@gmail.com',
	entry_points = {
		'console_scripts': ['sicuro=sicuro.main:main']
	},
	packages=setuptools.find_packages(),
	install_requires=[
		'pycrypto', 'ipaddress'
		],
	zip_safe=False)

