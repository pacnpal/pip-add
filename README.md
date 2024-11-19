# pip-add

A command-line tool that combines package installation and requirements.txt management. Install, update, or remove Python packages and their dependencies with automatic requirements.txt handling.

## Features

- Single command for package management and requirements.txt updates
- Smart dependency handling for installation and removal
- Dependency analysis to prevent breaking other packages
- Flexible version specifications (`>=` by default)
- Optional exact version pinning (`==`)
- Clean, informative output with version information
- Preserves requirements.txt comments and formatting
- Creates requirements.txt if it doesn't exist

## Installation

```bash
# Clone the repository
pip install pip-add

## Usage

### Installation

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
```

## Command Line Options

```
pip-add [-h] [-d] [-e] [-r] package

positional arguments:
  package               Package to install or remove

options:
  -h, --help           show this help message and exit
  -d, --dependencies   Include dependencies when installing or removing
  -e, --exact         Use == instead of >= for version specification
  -r, --remove        Remove package(s) and their entries from requirements.txt
```

## How It Works

### Installation Process

1. Installs the specified package using pip
2. Retrieves installed version information
3. With `-d`: tracks and installs all dependencies
4. Updates requirements.txt with new package(s)
5. Uses `>=` by default or `==` with `-e` flag

### Removal Process

1. Analyzes package dependencies
2. Identifies which dependencies are safe to remove
3. Checks if any dependencies are needed by other packages
4. Safely removes unused packages
5. Updates requirements.txt
6. Reports kept dependencies and their dependents

## Safe Dependency Handling

The tool is designed to safely handle dependencies:

- **Installation**: Records all dependencies when using `-d`
- **Removal**: Only removes dependencies that aren't needed by other packages
- **Analysis**: Shows which dependencies were kept and why
- **Protection**: Prevents breaking other installed packages

## File Structure

```
pip_add/
├── setup.py          # Package configuration
├── pip_add/
│   ├── __init__.py   # Package initialization
│   └── cli.py        # Main implementation
```

## Requirements

- Python 3.6+
- pip
- setuptools

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e .
```

## Common Scenarios

### New Project

```bash
# First time setup
pip-add -d flask
# Creates requirements.txt and adds Flask with dependencies
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

2. **Dependency conflicts**
   - Uses `>=` by default to minimize conflicts
   - Use `-e` for exact versions when needed

3. **Dependencies not removing**
   - Check the output for dependencies kept
   - Tool will show which packages need them
