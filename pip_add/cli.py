import os
import sys
import subprocess
import pkg_resources
import argparse
from pkg_resources import working_set
from .utils import find_requirements as utils_find_requirements

def find_requirements(custom_path=None):
    """Find requirements.txt using utils or use custom path"""
    if custom_path:
        # If custom path provided, ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(custom_path)), exist_ok=True)
        if not os.path.exists(custom_path):
            with open(custom_path, 'w') as f:
                f.write('# Python dependencies\n')
        return custom_path
    
    # Use utils.find_requirements() to search for requirements files
    req_file, found_files = utils_find_requirements()
    if len(found_files) > 1:
        print("\nℹ️  Found multiple requirements files:")
        for f in found_files:
            print(f"  - {f}")
        print(f"\nUsing: {req_file}")
        print("To use a specific file, run the command with -f/--requirements-file option:")
        print(f"Example: pip-add -f {found_files[0]} <package>")
    
    return req_file

def get_package_dependencies(package_name):
    """Get all dependencies of a package"""
    try:
        dist = pkg_resources.get_distribution(package_name)
        deps = {package_name: dist.version}  # Start with the main package
        
        for req in dist.requires():
            try:
                dep_dist = pkg_resources.get_distribution(req.key)
                deps[req.key] = dep_dist.version
            except pkg_resources.DistributionNotFound:
                continue
                
        return deps
    except Exception as e:
        print(f"Warning: Could not fetch dependencies: {str(e)}", file=sys.stderr)
        return {package_name: pkg_resources.get_distribution(package_name).version}

def find_dependent_packages(package_name, excluding_package):
    """
    Find all installed packages that depend on the given package,
    excluding the package we're removing and its dependencies
    """
    dependents = {}
    for dist in working_set:
        # Skip the package we're removing and its dependencies
        if dist.key == excluding_package or dist.key == package_name:
            continue
        for req in dist.requires():
            if req.key == package_name:
                dependents[package_name] = dependents.get(package_name, [])
                dependents[package_name].append(dist.key)
    return dependents

def analyze_dependencies(package_name):
    """Analyze which dependencies can be removed and which are still needed"""
    try:
        # Get all dependencies of the package we're removing
        all_deps = get_package_dependencies(package_name)
        safe_to_remove = set()
        kept_deps = {}
        
        # First, mark the main package for removal
        main_pkg_version = all_deps.pop(package_name)
        safe_to_remove.add((package_name, main_pkg_version))
        
        # Then check each dependency
        for dep, version in all_deps.items():
            # Check if anything besides the package we're removing needs this dependency
            dependents = find_dependent_packages(dep, package_name)
            if not dependents.get(dep):
                safe_to_remove.add((dep, version))
            else:
                kept_deps[dep] = dependents[dep]
        
        return safe_to_remove, kept_deps
    except Exception as e:
        print(f"Warning: Could not analyze dependencies: {str(e)}", file=sys.stderr)
        version = pkg_resources.get_distribution(package_name).version
        return {(package_name, version)}, {}

def remove_from_requirements(packages, req_file):
    """Remove packages from requirements.txt"""
    try:
        with open(req_file, 'r') as f:
            requirements = f.readlines()
    except FileNotFoundError:
        return set()
    
    # Keep track of removed packages
    removed = set()
    
    # Filter out the packages while keeping comments
    new_reqs = []
    for line in requirements:
        if line.strip() and not line.strip().startswith('#'):
            # Check if this line is one of our packages
            pkg = line.split('>=')[0].split('==')[0].strip()
            if pkg not in {name for name, _ in packages}:
                new_reqs.append(line)
            else:
                removed.add(pkg)
        else:
            new_reqs.append(line)
    
    # Write back the filtered requirements
    with open(req_file, 'w') as f:
        f.writelines(new_reqs)
    
    return removed

def add_to_requirements(packages_dict, req_file, exact=False):
    """Add or update packages in requirements.txt"""
    try:
        with open(req_file, 'r') as f:
            requirements = f.readlines()
    except FileNotFoundError:
        requirements = []
    
    # Keep comments and empty lines
    filtered_reqs = [line for line in requirements if line.strip() and not line.strip().startswith('#')]
    comments = [line for line in requirements if not line.strip() or line.strip().startswith('#')]
    
    # Convert existing requirements to dict for easy updating
    existing_pkgs = {}
    for line in filtered_reqs:
        if '>=' in line or '==' in line:
            name = line.split('>=')[0].split('==')[0].strip()
            existing_pkgs[name] = line
    
    # Update or add new packages
    for package, version in packages_dict.items():
        operator = '==' if exact else '>='
        requirement_line = f"{package}{operator}{version}\n"
        existing_pkgs[package] = requirement_line
    
    # Combine comments and updated requirements
    final_requirements = comments + [existing_pkgs[pkg] for pkg in sorted(existing_pkgs.keys())]
    
    with open(req_file, 'w') as f:
        f.writelines(final_requirements)

def install_package(package_name):
    """Install a package using pip"""
    print(f"Installing {package_name}...")
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', package_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def uninstall_packages(packages):
    """Uninstall multiple packages silently"""
    print("Removing packages...")
    for package, version in packages:
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'uninstall', '-y', package],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Error uninstalling {package}: {str(e)}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description='Install/remove packages and manage requirements.txt')
    parser.add_argument('package', help='Package to install or remove')
    parser.add_argument('-d', '--with-dependencies', action='store_true',
                      help='Include dependencies when installing or removing')
    parser.add_argument('-e', '--exact', action='store_true',
                      help='Use == instead of >= for version specification')
    parser.add_argument('-r', '--remove', action='store_true',
                      help='Remove package(s) and their entries from requirements.txt')
    parser.add_argument('-f', '--requirements-file',
                      help='Path to custom requirements.txt file')
    
    args = parser.parse_args()
    package = args.package
    req_file = find_requirements(args.requirements_file)
    
    try:
        if args.remove:
            if args.with_dependencies:
                # Analyze dependencies
                to_remove, kept_deps = analyze_dependencies(package)
                
                # Remove from requirements.txt and uninstall
                removed = remove_from_requirements(to_remove, req_file)
                uninstall_packages(to_remove)
                
                # Report results
                if removed:
                    print("\n✓ Successfully uninstalled:")
                    for pkg, version in sorted(to_remove):
                        print(f"  - {pkg} ({version})")
                    
                    if kept_deps:
                        print("\nℹ️  Dependencies kept (required by other packages):")
                        for dep, dependents in sorted(kept_deps.items()):
                            print(f"  - {dep} (needed by: {', '.join(sorted(dependents))})")
                    
                    print(f"\n✓ Updated {req_file}")
                else:
                    print(f"\n✓ Successfully uninstalled {package} (no entries found in {req_file})")
            else:
                # Remove single package
                version = pkg_resources.get_distribution(package).version
                uninstall_packages({(package, version)})
                removed = remove_from_requirements({(package, version)}, req_file)
                if removed:
                    print(f"\n✓ Successfully uninstalled {package} ({version})")
                    print(f"✓ Updated {req_file}")
                else:
                    print(f"\n✓ Successfully uninstalled {package} ({version})")
                    print(f"ℹ️  Note: Package was not found in {req_file}")
        else:
            # Install package
            install_package(package)
            
            # Get package info and update requirements
            if args.with_dependencies:
                packages = get_package_dependencies(package)
                print("\n✓ Successfully installed:")
                for pkg, version in sorted(packages.items()):
                    print(f"  - {pkg} ({version})")
            else:
                version = pkg_resources.get_distribution(package).version
                packages = {package: version}
                print(f"\n✓ Successfully installed {package} ({version})")
            
            # Update requirements.txt
            add_to_requirements(packages, req_file, args.exact)
            print(f"✓ Updated {req_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error {'removing' if args.remove else 'installing'} {package}: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
