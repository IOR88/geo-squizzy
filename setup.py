from setuptools import setup, find_packages

setup(
    name='geo-squizzy',
    version='0.1',
    packages=find_packages(exclude=['tests*', 'research*', 'build_big_data*']),
    license='MIT',
    description='GeoJSON-unknown-documents-model-creation',
    long_description=open('README.md').read(),
    # install_requires=['numpy'],
    url='https://github.com/LowerSilesians/geo-squizzy',
    author='Igor Miazek, Jakub Miazek',
    author_email='t-32@o2.pl, the@grillazz.com'
)