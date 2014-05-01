try: 
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	
config = {
	'description': 'vgmc7 project',
	'author': 'meisnewbie',
	'url': 'PLACEHOLDER.',
	'download_url': 'ALSO PLACEHOLDER PROBABLY GITHUB',
	'author_email': 'ahchang012@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['scraper'],
	'scripts': [],
	'name': 'Nomination changer'
}

setup(**config)
