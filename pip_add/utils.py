import os
from pathlib import Path
from typing import Optional, List, Tuple

def find_requirements(start_dir: Optional[str] = None) -> Tuple[str, List[str]]:
    """
    Find requirements files by searching up through parent directories.
    Returns tuple of (chosen_file, all_found_files).
    """
    requirements_files = [
        'requirements.txt',
        'requirements/base.txt',
        'requirements/dev.txt',
        'requirements/development.txt',
        'requirements/prod.txt',
        'requirements/production.txt'
    ]
    
    if start_dir is None:
        start_dir = os.getcwd()
    
    current_dir = Path(start_dir).resolve()
    found_files = []
    
    # Search up through parent directories
    while True:
        for req_file in requirements_files:
            req_path = current_dir / req_file
            if req_path.exists():
                found_files.append(str(req_path))
        
        # Stop if we found files or reached root
        if found_files or current_dir.parent == current_dir:
            break
            
        current_dir = current_dir.parent
    
    # If no files found, default to requirements.txt in current directory
    if not found_files:
        default_file = os.path.join(start_dir, 'requirements.txt')
        # Create the requirements directory if needed
        os.makedirs(os.path.dirname(default_file), exist_ok=True)
        # Create an empty requirements file
        if not os.path.exists(default_file):
            with open(default_file, 'w') as f:
                f.write('# Python dependencies\n')
        return default_file, [default_file]
    
    # Prefer requirements.txt in the closest directory
    for f in found_files:
        if os.path.basename(f) == 'requirements.txt':
            return f, found_files
    
    # Otherwise take the first found file
    return found_files[0], found_files

def add_to_requirements(package_name: str, version: str, requirements_file: str) -> None:
    """Add or update package in requirements file"""
    requirement_line = f"{package_name}=={version}\n"
    
    try:
        with open(requirements_file, 'r') as f:
            requirements = f.readlines()
    except FileNotFoundError:
        requirements = []
        
    # Check if package exists and update it
    package_exists = False
    for i, line in enumerate(requirements):
        if line.strip() and package_name == line.split('==')[0].strip():
            requirements[i] = requirement_line
            package_exists = True
            break
            
    # Add package if it doesn't exist
    if not package_exists:
        requirements.append(requirement_line)
        
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(requirements_file)), exist_ok=True)
    
    with open(requirements_file, 'w') as f:
        f.writelines(requirements)