from setuptools import setup, find_packages

import xbox

readme = open('README.md')

setup(
    name='python-xbox',
    version=xbox.__VERSION__,
    url='https://github.com/buttscicles/xbox/',
    author='Joe Alcorn',
    author_email='joealcorn123@gmail.com',
    description="A wrapper around Microsoft's undocumented Xbox One APIs",
    long_description=readme.read(),
    packages=find_packages(exclude=["tests"]),
    keywords='xbox one microsoft',
    tests_require=['pytest==2.6.2', 'tox==1.7.3'],
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)

readme.close()
