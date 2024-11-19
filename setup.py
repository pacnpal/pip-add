from setuptools import setup, find_packages

setup(
    name="pip-add",
    version="0.1.2",
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
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
)
