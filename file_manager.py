#!/usr/bin/env python3
"""
File Manager Utility
A comprehensive file management tool demonstrating advanced Python concepts.
"""

import os
import shutil
import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union
import json


class FileManager:
    """
    A comprehensive file management utility class.
    
    This class provides various file operations including:
    - File and directory listing
    - File copying and moving
    - Directory creation and deletion
    - File information retrieval
    - Search functionality
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize FileManager with a base path.
        
        Args:
            base_path (str): The base directory path to work with
        """
        self.base_path = Path(base_path).resolve()
        self.ensure_directory_exists(self.base_path)
    
    def ensure_directory_exists(self, path: Union[str, Path]) -> None:
        """
        Ensure that a directory exists, create if it doesn't.
        
        Args:
            path: Directory path to check/create
        """
        Path(path).mkdir(parents=True, exist_ok=True)
    
    def list_files(self, directory: Optional[str] = None, 
                   include_hidden: bool = False) -> List[Dict[str, Union[str, int, float]]]:
        """
        List files in a directory with detailed information.
        
        Args:
            directory: Directory to list (defaults to base_path)
            include_hidden: Whether to include hidden files
            
        Returns:
            List of dictionaries containing file information
        """
        target_dir = Path(directory) if directory else self.base_path
        
        if not target_dir.exists():
            raise FileNotFoundError(f"Directory '{target_dir}' not found")
        
        files_info = []
        
        try:
            for item in target_dir.iterdir():
                if not include_hidden and item.name.startswith('.'):
                    continue
                
                stat = item.stat()
                file_info = {
                    'name': item.name,
                    'path': str(item),
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': stat.st_size,
                    'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'permissions': oct(stat.st_mode)[-3:]
                }
                files_info.append(file_info)
        
        except PermissionError:
            raise PermissionError(f"Permission denied accessing '{target_dir}'")
        
        return sorted(files_info, key=lambda x: (x['type'] == 'file', x['name'].lower()))
    
    def create_file(self, filename: str, content: str = "", 
                   overwrite: bool = False) -> bool:
        """
        Create a new file with optional content.
        
        Args:
            filename: Name of the file to create
            content: Content to write to the file
            overwrite: Whether to overwrite existing file
            
        Returns:
            True if file was created successfully
        """
        file_path = self.base_path / filename
        
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"File '{filename}' already exists. Use overwrite=True to replace.")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            raise IOError(f"Failed to create file '{filename}': {str(e)}")
    
    def copy_file(self, source: str, destination: str, 
                  overwrite: bool = False) -> bool:
        """
        Copy a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            overwrite: Whether to overwrite existing destination file
            
        Returns:
            True if file was copied successfully
        """
        src_path = Path(source)
        dest_path = self.base_path / destination
        
        if not src_path.exists():
            raise FileNotFoundError(f"Source file '{source}' not found")
        
        if dest_path.exists() and not overwrite:
            raise FileExistsError(f"Destination '{destination}' already exists")
        
        try:
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest_path)
            return True
        except Exception as e:
            raise IOError(f"Failed to copy file: {str(e)}")
    
    def move_file(self, source: str, destination: str) -> bool:
        """
        Move a file from source to destination.
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if file was moved successfully
        """
        src_path = Path(source)
        dest_path = self.base_path / destination
        
        if not src_path.exists():
            raise FileNotFoundError(f"Source file '{source}' not found")
        
        try:
            # Ensure destination directory exists
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dest_path))
            return True
        except Exception as e:
            raise IOError(f"Failed to move file: {str(e)}")
    
    def delete_file(self, filename: str, confirm: bool = False) -> bool:
        """
        Delete a file.
        
        Args:
            filename: Name of file to delete
            confirm: Safety confirmation flag
            
        Returns:
            True if file was deleted successfully
        """
        if not confirm:
            raise ValueError("Deletion requires explicit confirmation (confirm=True)")
        
        file_path = self.base_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' not found")
        
        try:
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            return True
        except Exception as e:
            raise IOError(f"Failed to delete '{filename}': {str(e)}")
    
    def search_files(self, pattern: str, search_content: bool = False) -> List[Dict[str, str]]:
        """
        Search for files by name pattern or content.
        
        Args:
            pattern: Search pattern (supports wildcards)
            search_content: Whether to search inside file content
            
        Returns:
            List of matching files with details
        """
        matches = []
        
        try:
            if search_content:
                # Search in file content
                for file_path in self.base_path.rglob('*'):
                    if file_path.is_file():
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if pattern.lower() in content.lower():
                                    matches.append({
                                        'name': file_path.name,
                                        'path': str(file_path),
                                        'match_type': 'content'
                                    })
                        except (UnicodeDecodeError, PermissionError):
                            continue
            else:
                # Search by filename pattern
                for file_path in self.base_path.rglob(pattern):
                    matches.append({
                        'name': file_path.name,
                        'path': str(file_path),
                        'match_type': 'filename'
                    })
        
        except Exception as e:
            raise IOError(f"Search failed: {str(e)}")
        
        return matches
    
    def get_file_info(self, filename: str) -> Dict[str, Union[str, int, float]]:
        """
        Get detailed information about a file.
        
        Args:
            filename: Name of the file
            
        Returns:
            Dictionary containing file information
        """
        file_path = self.base_path / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"File '{filename}' not found")
        
        stat = file_path.stat()
        
        return {
            'name': file_path.name,
            'path': str(file_path),
            'type': 'directory' if file_path.is_dir() else 'file',
            'size': stat.st_size,
            'size_human': self._human_readable_size(stat.st_size),
            'created': datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'accessed': datetime.datetime.fromtimestamp(stat.st_atime).isoformat(),
            'permissions': oct(stat.st_mode)[-3:],
            'owner': stat.st_uid,
            'group': stat.st_gid
        }
    
    def _human_readable_size(self, size: int) -> str:
        """
        Convert file size to human-readable format.
        
        Args:
            size: Size in bytes
            
        Returns:
            Human-readable size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def export_file_list(self, output_file: str = "file_list.json") -> bool:
        """
        Export file list to JSON format.
        
        Args:
            output_file: Name of output file
            
        Returns:
            True if export was successful
        """
        try:
            file_list = self.list_files(include_hidden=True)
            output_path = self.base_path / output_file
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(file_list, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            raise IOError(f"Failed to export file list: {str(e)}")


def demonstrate_file_manager() -> None:
    """
    Demonstrate the FileManager functionality.
    """
    print("=== File Manager Utility Demo ===")
    
    # Initialize file manager
    fm = FileManager()
    
    try:
        # List current files
        print("\n1. Current files in workspace:")
        files = fm.list_files()
        for file_info in files[:5]:  # Show first 5 files
            print(f"  {file_info['type'].upper()}: {file_info['name']} "
                  f"({file_info['size_human'] if 'size_human' in file_info else fm._human_readable_size(file_info['size'])})")
        
        # Create a sample file
        print("\n2. Creating a sample configuration file...")
        config_content = '''{
    "app_name": "File Manager",
    "version": "1.0.0",
    "settings": {
        "auto_backup": true,
        "max_file_size": "10MB"
    }
}'''
        fm.create_file("config.json", config_content)
        print("   ✓ config.json created successfully")
        
        # Get file information
        print("\n3. File information for config.json:")
        info = fm.get_file_info("config.json")
        print(f"   Size: {info['size_human']}")
        print(f"   Modified: {info['modified'][:19]}")
        print(f"   Permissions: {info['permissions']}")
        
        # Search for Python files
        print("\n4. Searching for Python files:")
        python_files = fm.search_files("*.py")
        for file_info in python_files:
            print(f"   Found: {file_info['name']}")
        
        # Export file list
        print("\n5. Exporting file list to JSON...")
        fm.export_file_list("workspace_inventory.json")
        print("   ✓ File list exported successfully")
        
    except Exception as e:
        print(f"Error during demonstration: {str(e)}")


def main() -> None:
    """
    Main function to run the file manager utility.
    """
    print("File Manager Utility")
    print("===================")
    
    while True:
        print("\nAvailable operations:")
        print("1. List files")
        print("2. Create file")
        print("3. Get file info")
        print("4. Search files")
        print("5. Run demonstration")
        print("6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                fm = FileManager()
                files = fm.list_files()
                print(f"\nFound {len(files