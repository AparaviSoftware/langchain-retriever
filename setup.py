from setuptools import setup, find_packages

setup(
    name='Aparavi_PublicLangchainRetriever',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'logging',
    ],
)
