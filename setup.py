import setuptools


setuptools.setup(
    name='next-bug',
    version='1.0.0',
    description='Manage Launchpad bugs without any hassle.',
    author='Dolph Mathews',
    author_email='dolph.mathews@gmail.com',
    url='http://github.com/dolph/next-bug',
    scripts=['next_bug.py'],
    install_requires=['launchpadlib'],
    py_modules=['next_bug'],
    entry_points={'console_scripts': ['next-bug = next_bug:cli']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)
