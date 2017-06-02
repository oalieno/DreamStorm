from distutils.core import setup
setup(
    name='DreamStorm',
    packages=['DreamStorm','DreamStorm.lib','DreamStorm.lib.modules'],  # this must be the same as the name above
    install_requires=[
        'beautifulsoup4',
    ],
    version='0.4',
    description='multi-thread tor crawler library',
    author='OAlienO',
    author_email='jeffrey6910@gmail.com',
    url='https://github.com/OAlienO/DreamStorm',  # use the URL to the github repo
    download_url='https://github.com/OAlienO/DreamStorm/archive/0.4.tar.gz',  # I'll explain this in a second
    keywords=['crawler', 'tor', 'multi-thread'],  # arbitrary keywords
    classifiers=[], )
