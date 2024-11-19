from setuptools import setup, find_packages

setup(
    name="pip-add",
    version="0.2.5",
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
    author_email="pac@pacnp.al",
    description="A modern Python package manager that combines pip install with requirements.txt management. Supports Python 3.11, 3.12, and 3.13.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PacNPal/pip-add",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    python_requires=">=3.11",
)
