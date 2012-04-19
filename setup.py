import os
from setuptools import setup
import cleantext

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='cleantext',
    version=cleantext.__version__,
    description='Tranform html compatible documents',
    author='Yohan Boniface & Amirouche Boubekki',
    author_email='y.boniface@liberation.fr',
    url='https://github.com/liberation/cleantext',
    keywords='xml html transformation',
    packages=['cleantext'],
    test_suite='tests',
    install_requires=read('requirements.txt'),
    long_description=read('README.rst'),
    license='WTF',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
