from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

def get_requirements():
    """
    lists the requirements to install.
    """
    pkgs = []
    links = []
    requirements = []
    try:
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
        for r in requirements:
            if "git+git" in r:
                links.append(r)
            else:
                pkgs.append(r)
    except Exception as ex:
        raise Exception("Error parsing requirements.txt. Check its availability.")
    return pkgs, links

pkgs, links = get_requirements()

setup(
    name='sicuro',
	version='0.1.0',
	description='Secure your shit',
	long_description=readme(),
	url='http://github.com/beenum22/sicuro',
	author='Muneeb Ahmad',
	author_email='muneeb.gandapur@gmail.com',
	entry_points = {
		'console_scripts': ['sicuro=sicuro.main:main']
	},
	packages=setuptools.find_packages(),
    package_data= {
        "sicuro": [
            "LICENSE",
            "pyproject.toml",
            "MANIFEST.in",
            "README.rst",
            "requirements.txt",
            "sicuro/main.py",
            "sicuro/src/*"
        ]},
	install_requires=[
                'pycrypto',
                'ipaddress',
                'zizou'
        ],
	zip_safe=False)

