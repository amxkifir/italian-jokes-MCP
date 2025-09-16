#!/usr/bin/env python3
"""
MCPB Builder Script
Creates an MCPB (MCP Bundle) package from the Italian Jokes MCP project
"""

import os
import json
import zipfile
import shutil
from pathlib import Path
from typing import List, Dict, Any

def validate_manifest(manifest_path: str) -> Dict[str, Any]:
    """Validate and load the manifest.json file"""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Required fields validation
        required_fields = ['name', 'version', 'description', 'mcpServers']
        for field in required_fields:
            if field not in manifest:
                raise ValueError(f"Missing required field: {field}")
        
        print(f"✓ Manifest validation passed for {manifest['name']} v{manifest['version']}")
        return manifest
        
    except Exception as e:
        print(f"✗ Manifest validation failed: {e}")
        raise

def get_files_to_include(manifest: Dict[str, Any], project_dir: str) -> List[str]:
    """Get list of files to include in the MCPB package"""
    files_to_include = []
    
    # Files explicitly listed in manifest
    if 'files' in manifest:
        files_to_include.extend(manifest['files'])
    
    # Always include manifest.json
    if 'manifest.json' not in files_to_include:
        files_to_include.append('manifest.json')
    
    # Check if files exist
    existing_files = []
    for file_path in files_to_include:
        full_path = os.path.join(project_dir, file_path)
        if os.path.exists(full_path):
            existing_files.append(file_path)
            print(f"✓ Found: {file_path}")
        else:
            print(f"⚠ Missing: {file_path}")
    
    return existing_files

def create_mcpb_package(
    project_dir: str,
    output_dir: str = None,
    package_name: str = None
) -> str:
    """Create MCPB package from project directory"""
    
    project_path = Path(project_dir)
    manifest_path = project_path / 'manifest.json'
    
    if not manifest_path.exists():
        raise FileNotFoundError("manifest.json not found in project directory")
    
    # Validate manifest
    manifest = validate_manifest(str(manifest_path))
    
    # Determine output directory and package name
    if output_dir is None:
        output_dir = project_dir
    
    if package_name is None:
        package_name = f"{manifest['name']}-{manifest['version']}.mcpb"
    
    output_path = os.path.join(output_dir, package_name)
    
    # Get files to include
    files_to_include = get_files_to_include(manifest, project_dir)
    
    print(f"\nCreating MCPB package: {package_name}")
    print(f"Output path: {output_path}")
    
    # Create the ZIP file (MCPB is essentially a ZIP)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as mcpb_file:
        for file_path in files_to_include:
            full_path = os.path.join(project_dir, file_path)
            
            # Add file to ZIP with proper path structure
            mcpb_file.write(full_path, file_path)
            print(f"  + {file_path}")
    
    # Verify the package
    verify_mcpb_package(output_path)
    
    print(f"\n✓ MCPB package created successfully: {output_path}")
    return output_path

def verify_mcpb_package(mcpb_path: str) -> bool:
    """Verify the created MCPB package"""
    try:
        with zipfile.ZipFile(mcpb_path, 'r') as mcpb_file:
            # Check if manifest.json exists
            if 'manifest.json' not in mcpb_file.namelist():
                raise ValueError("manifest.json not found in MCPB package")
            
            # Validate manifest content
            manifest_content = mcpb_file.read('manifest.json')
            manifest = json.loads(manifest_content.decode('utf-8'))
            
            # Basic validation
            if 'name' not in manifest or 'version' not in manifest:
                raise ValueError("Invalid manifest structure")
            
            print(f"✓ MCPB package verification passed")
            print(f"  Package: {manifest['name']} v{manifest['version']}")
            print(f"  Files: {len(mcpb_file.namelist())}")
            
            return True
            
    except Exception as e:
        print(f"✗ MCPB package verification failed: {e}")
        return False

def install_mcpb_locally(mcpb_path: str, install_dir: str = None) -> str:
    """Install MCPB package locally for testing"""
    if install_dir is None:
        install_dir = os.path.expanduser("~/.mcp/bundles")
    
    # Create install directory if it doesn't exist
    os.makedirs(install_dir, exist_ok=True)
    
    # Extract package name from path
    package_name = os.path.splitext(os.path.basename(mcpb_path))[0]
    extract_path = os.path.join(install_dir, package_name)
    
    # Remove existing installation
    if os.path.exists(extract_path):
        shutil.rmtree(extract_path)
    
    # Extract MCPB package
    with zipfile.ZipFile(mcpb_path, 'r') as mcpb_file:
        mcpb_file.extractall(extract_path)
    
    print(f"✓ MCPB package installed locally: {extract_path}")
    return extract_path

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build MCPB package for Italian Jokes MCP")
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Project directory containing manifest.json (default: current directory)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for MCPB package (default: project directory)"
    )
    parser.add_argument(
        "--package-name",
        help="Custom package name (default: auto-generated from manifest)"
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install the package locally after building"
    )
    parser.add_argument(
        "--verify-only",
        help="Only verify an existing MCPB package"
    )
    
    args = parser.parse_args()
    
    try:
        if args.verify_only:
            # Verify existing package
            verify_mcpb_package(args.verify_only)
        else:
            # Build new package
            mcpb_path = create_mcpb_package(
                args.project_dir,
                args.output_dir,
                args.package_name
            )
            
            # Install locally if requested
            if args.install:
                install_mcpb_locally(mcpb_path)
        
        print("\n🎉 Success!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()