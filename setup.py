from setuptools import setup, find_packages

setup(
    name="pip-add",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pip",
        "setuptools",
    ],
    entry_points={
        'console_scripts': [
            'pip-add=pip_add.cli:main',
        ],
    },
    author="PacNPal",
    description="A CLI tool to install packages and add them to requirements.txt",
)