from setuptools import setup, find_packages

with open('odoolightwf/version.py') as f:
    exec(f.read())

extra_setuptools_args = {}

setup(
    name="odoolightwf",
    version=__version__,
    description="An alternative, lightweight Odoo workflow implementation.",
    maintainer='Jérome Boisvert-Chouinard',
    maintainer_email='jerome.boisvertchouinard@savoirfairelinux.com',
    url='http://github.com/jbchouinard/odoolightwf',
    packages=find_packages(exclude=['tests', 'test_*']),
    package_data={'odoolightwf': ['data/*'],
                  'odoolightwf.tests': ['data/*']
                  },
    install_requires=['six'],
    license='LGPL-3.0',
    download_url='https://github.com/jbchouinard/odoolightwf/archive/%s.tar.gz' % __version__,
    classifiers=[
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LPGL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    **extra_setuptools_args
)
