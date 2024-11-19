# pip-add

A command-line tool that combines package installation and requirements.txt management. Install, update, or remove Python packages and their dependencies with automatic requirements.txt handling.

Compatible with Python 3.11, 3.12, and 3.13.

## Features

- Single command for package management and requirements.txt updates
- Smart dependency handling for installation and removal
- Dependency analysis to prevent breaking other packages
- Flexible version specifications (`>=` by default)
- Optional exact version pinning (`==`)
- Clean, informative output with version information
- Preserves requirements.txt comments and formatting
- Creates requirements.txt if it doesn't exist
- Support for custom requirements file paths
- Smart detection of multiple requirements files
- Full support for Python 3.11, 3.12, and 3.13

## Installation

It's recommended to install pip-add within a virtual environment to avoid conflicts with system packages:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install from PyPI
pip install pip-add

# Or install latest version
pip install --upgrade pip-add
```

For global installation (use with caution), you can install with pipx:

```bash
# Install globally using pipx
pipx install pip-add
```

## Usage

### Package Installation

```bash
# Basic package installation
pip-add requests
# Output:
# Installing requests...
# ✓ Successfully installed requests (2.32.3)
# ✓ Updated requirements.txt

# Install with exact version
pip-add -e requests
# Adds: requests==2.32.3 to requirements.txt

# Install with dependencies
pip-add -d requests
# Output:
# Installing requests...
# ✓ Successfully installed:
#   - certifi (2024.8.30)
#   - charset-normalizer (3.4.0)
#   - idna (3.10)
#   - requests (2.32.3)
#   - urllib3 (2.2.3)
# ✓ Updated requirements.txt

# Install using custom requirements file
pip-add -f requirements/dev.txt requests
# Output:
# Installing requests...
# ✓ Successfully installed requests (2.32.3)
# ✓ Updated requirements/dev.txt
```

### Multiple Requirements Files

When multiple requirements files are found in your project:

```bash
# Tool will show available files:
pip-add requests
# Output:
# ℹ️  Found multiple requirements files:
#   - requirements.txt
#   - requirements/dev.txt
#   - requirements/prod.txt
#
# Using: requirements.txt
# To use a specific file, run the command with -f/--requirements-file option:
# Example: pip-add -f requirements/dev.txt requests

# Specify which file to use:
pip-add -f requirements/dev.txt requests
```

### Removal

```bash
# Remove single package
pip-add -r requests
# Output:
# Removing packages...
# ✓ Successfully uninstalled requests (2.32.3)
# ✓ Updated requirements.txt

# Remove package and its unused dependencies
pip-add -d -r requests
# Output:
# Removing packages...
# ✓ Successfully uninstalled:
#   - certifi (2024.8.30)
#   - charset-normalizer (3.4.0)
#   - requests (2.32.3)
#   - urllib3 (2.2.3)
#
# ℹ️  Dependencies kept (required by other packages):
#   - idna (needed by: email-validator, cryptography)
#
# ✓ Updated requirements.txt

# Remove from specific requirements file
pip-add -r -f requirements/dev.txt requests
# Output:
# Removing packages...
# ✓ Successfully uninstalled requests (2.32.3)
# ✓ Updated requirements/dev.txt
```

## Command Line Options

```bash
pip-add [-h] [-d] [-e] [-r] [-f REQUIREMENTS_FILE] package

positional arguments:
  package               Package to install or remove

options:
  -h, --help           show this help message and exit
  -d, --dependencies   Include dependencies when installing or removing
  -e, --exact         Use == instead of >= for version specification
  -r, --remove        Remove package(s) and their entries from requirements.txt
  -f, --requirements-file
                      Path to custom requirements.txt file
```

## How It Works

### Installation Process

1. Installs the specified package using pip
2. Retrieves installed version information
3. With `-d`: tracks and installs all dependencies
4. Updates requirements.txt (or specified requirements file) with new package(s)
5. Uses `>=` by default or `==` with `-e` flag

### Removal Process

1. Analyzes package dependencies
2. Identifies which dependencies are safe to remove
3. Checks if any dependencies are needed by other packages
4. Safely removes unused packages
5. Updates requirements.txt (or specified requirements file)
6. Reports kept dependencies and their dependents

### Requirements File Handling

1. By default, looks for requirements.txt in the current directory
2. Creates requirements.txt if it doesn't exist
3. With `-f`: uses specified requirements file path
4. Creates directories if needed for custom file paths
5. Preserves comments and formatting in existing files
6. When multiple files are found:
   - Lists all available requirements files
   - Shows which file will be used by default
   - Provides example command to specify a particular file

## Safe Dependency Handling

The tool is designed to safely handle dependencies:

- **Installation**: Records all dependencies when using `-d`
- **Removal**: Only removes dependencies that aren't needed by other packages
- **Analysis**: Shows which dependencies were kept and why
- **Protection**: Prevents breaking other installed packages

## Requirements

- Python 3.11, 3.12, or 3.13
- pip
- setuptools

## Common Scenarios

### New Project

```bash
# First time setup
pip-add flask
# Creates requirements.txt and adds Flask

pip-add -d flask
# Creates requirements.txt and adds Flask with dependencies

# Multiple requirements files
pip-add -f requirements/dev.txt pytest
pip-add -f requirements/prod.txt gunicorn
# Manages separate requirement files for different environments
```

### Updating Dependencies

```bash
# Update with newer versions
pip-add requests
# Updates to newest version with >= specification
```

### Clean Uninstall

```bash
# Remove package and unused dependencies
pip-add -d -r flask
# Removes Flask and dependencies not used by other packages
```

## Troubleshooting

1. **Package not found in requirements.txt**
   - The file will be created automatically
   - Existing comments are preserved
   - Use `-f` to specify a different requirements file

2. **Dependency conflicts**
   - Uses `>=` by default to minimize conflicts
   - Use `-e` for exact versions when needed

3. **Dependencies not removing**
   - Check the output for dependencies kept
   - Tool will show which packages need them

4. **Multiple requirements files**
   - Tool will list all available requirements files
   - Shows which file will be used by default
   - Provides example command to specify a particular file
   - Use `-f` to specify which file to use
