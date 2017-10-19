from setuptools import setup , find_packages

requires=[]

setup(
    author='Max M Rasmussen',
    author_email='maxm@mxm.dk',
    name='mxm.midifile',
    description='A python 3 library for reading, writing and modifying midi files',
    version='1.1',
    # packages=find_packages(),
    packages=[
        'mxm.midifile',
        'mxm.midifile.src',
        'mxm.midifile.docs',
        'mxm.midifile.tests',
        'mxm.midifile.examples',
    ],
    include_package_data=True,
    install_requires=requires,
    tests_require=requires+['nose==1.3.7'],
    test_suite = 'nose.collector',
    license='MIT License',
    url='https://github.com/maxmcorp/mxm.midifile',
    long_description=open('README.md').read(),

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Artistic Software',
    ],
    keywords=[
        'midi', 'music', 'algorithmic composition', 'midi parser', 'midi reader'
    ],
)


