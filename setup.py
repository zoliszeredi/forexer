import setuptools


setuptools.setup(
    name='forexer',
    version='0.1.0',
    author='Szeredi Tibor Zoltan',
    author_email='zoltan@szeredi.ro',
    description='Forex Trading for Dummies',
    packages=setuptools.find_packages('src'),
    install_requires=[
        'Django',
        'requests',
        'djangorestframework'
    ],
    package_dir={'': 'src'},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    license='MIT',
)


