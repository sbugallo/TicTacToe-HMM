from setuptools import setup, find_namespace_packages
import os

VERSION = '2019.08'
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
MODULE_NAME = "ttt"
PACKAGE_NAME = "ttt"

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    url="",
    download_url="",
    description='tic-tac-toe game',
    author='Sergio Bugallo Enjamio',
    tests_require=['pytest'],
    install_requires=["", 'loguru', 'numpy', 'fire'],
    author_email="sergiobugalloenjamio@gmail.com",

    license='Propietary',
    packages=find_namespace_packages(
        include=f"{MODULE_NAME}.*",
        exclude=["tests", "docs"]),
    py_modules=[],
    entry_points={
        "console_scripts":  [
            "ttt-human-vs-human = ttt.cli.human_vs_human:main",
            "ttt-human-vs-cpu = ttt.cli.human_vs_cpu:main",
            "ttt-cpu-vs-cpu = ttt.cli.cpu_vs_cpu:main",
            "ttt-train = ttt.cli.train:main"
        ]
    },
    include_package_data=True,
    platforms='any',
    classifiers=['Programming Language :: Python',
                 'Development Status :: 4 - Beta',
                 'Natural Language :: English',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache Software License',
                 'Operating System :: OS Independent',
                 ('Topic :: Software Development :: Libraries '
                  ':: Python Modules'),
                 ('Topic :: Software Development :: Libraries :: '
                  'Application Frameworks')
                 ],
    python_requires=">=3.0",
    setup_requires=[
        'setuptools',
        'setuptools-git',
        'wheel',
    ],
    extras_require={
        'testing': ['pytest'],
    }
)