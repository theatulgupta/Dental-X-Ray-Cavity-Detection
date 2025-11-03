"""
Validation and conversion script for YOLO format annotations.
Since annotations are already in YOLO format, this script validates them.
"""

import os
import sys
from pathlib import Path
from typing import Tuple, List


sys.path.append(str(Path(__file__).parent.parent))

from data_prep.utils import get_file_pairs


def validate_yolo_annotation(label_path: str) -> Tuple[bool, str, List[int]]:
    """
    Validate a single YOLO format annotation file.
    
    Args:
        label_path: Path to the label file
    
    Returns:
        Tuple of (is_valid, error_message, class_ids)
    """
    class_ids = []
    
    try:
        with open(label_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Split into components
                parts = line.split()
                if len(parts) != 5:
                    return False, f"Line {line_num}: Expected 5 values, got {len(parts)}", []
                
                # Parse values
                try:
                    class_id = int(parts[0])
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])
                except ValueError:
                    return False, f"Line {line_num}: Invalid numeric values", []
                
                # Validate class ID (0-3 for this dataset)
                if class_id < 0 or class_id > 3:
                    return False, f"Line {line_num}: Class ID {class_id} out of range [0-3]", []
                
                # Validate normalized coordinates (should be between 0 and 1)
                for coord_name, coord_value in [('x_center', x_center), ('y_center', y_center), 
                                                ('width', width), ('height', height)]:
                    if not (0.0 <= coord_value <= 1.0):
                        return False, f"Line {line_num}: {coord_name} {coord_value} out of range [0-1]", []
                
                # Validate box boundaries
                x_min = x_center - width / 2
                x_max = x_center + width / 2
                y_min = y_center - height / 2
                y_max = y_center + height / 2
                
                if not (0.0 <= x_min <= 1.0 and 0.0 <= x_max <= 1.0):
                    return False, f"Line {line_num}: Invalid x bounds [{x_min:.3f}, {x_max:.3f}]", []
                
                if not (0.0 <= y_min <= 1.0 and 0.0 <= y_max <= 1.0):
                    return False, f"Line {line_num}: Invalid y bounds [{y_min:.3f}, {y_max:.3f}]", []
                
                class_ids.append(class_id)
    
    except FileNotFoundError:
        return False, "File not found", []
    except Exception as e:
        return False, f"Error reading file: {str(e)}", []
    
    # All validations passed
    return True, "", class_ids


def validate_all_annotations(images_dir: str, labels_dir: str) -> dict:
    """
    Validate all annotation files in the dataset.
    
    Args:
        images_dir: Directory containing images
        labels_dir: Directory containing labels
    
    Returns:
        Dictionary with validation statistics
    """
    pairs = get_file_pairs(images_dir, labels_dir)
    
    stats = {
        'total_files': len(pairs),
        'valid_files': 0,
        'invalid_files': 0,
        'total_annotations': 0,
        'class_distribution': {0: 0, 1: 0, 2: 0, 3: 0},
        'errors': []
    }
    
    print(f"\nValidating {len(pairs)} annotation files...")
    
    for img_path, label_path in pairs:
        is_valid, error_msg, class_ids = validate_yolo_annotation(label_path)
        
        if is_valid:
            stats['valid_files'] += 1
            stats['total_annotations'] += len(class_ids)
            for class_id in class_ids:
                stats['class_distribution'][class_id] += 1
        else:
            stats['invalid_files'] += 1
            filename = Path(label_path).name
            stats['errors'].append({
                'file': filename,
                'error': error_msg
            })
            print(f"  [ERROR] {filename}: {error_msg}")
    
    return stats


def fix_small_coordinates(label_path: str, min_size: float = 0.001) -> bool:
    """
    Fix very small bounding boxes that might cause issues.
    This is optional and only applied if needed.
    
    Args:
        label_path: Path to the label file
        min_size: Minimum size for width/height
    
    Returns:
        True if file was modified
    """
    with open(label_path, 'r') as f:
        lines = f.readlines()
    
    modified = False
    fixed_lines = []
    
    for line in lines:
        if not line.strip():
            fixed_lines.append(line)
            continue
        
        parts = line.strip().split()
        if len(parts) != 5:
            fixed_lines.append(line)
            continue
        
        x_center, y_center, width, height = map(float, parts[1:5])
        
        # Fix if too small
        if width < min_size or height < min_size:
            width = max(width, min_size)
            height = max(height, min_size)
            modified = True
            fixed_line = f"{parts[0]} {x_center} {y_center} {width} {height}\n"
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    
    # Write back if modified
    if modified:
        with open(label_path, 'w') as f:
            f.writelines(fixed_lines)
    
    return modified


def main():
    """
    Main function to validate YOLO annotations.
    """
    # Configuration
    RAW_DATA_DIR = "data/raw/dental"
    IMAGES_DIR = os.path.join(RAW_DATA_DIR, "images")
    LABELS_DIR = os.path.join(RAW_DATA_DIR, "object_detection_labels")
    
    print("=" * 60)
    print("YOLO Annotation Validation")
    print("=" * 60)
    
    # Step 1: Validate all annotations
    stats = validate_all_annotations(IMAGES_DIR, LABELS_DIR)
    
    # Step 2: Print results
    print("\n" + "=" * 60)
    print("Validation Results")
    print("=" * 60)
    print(f"\nTotal files: {stats['total_files']}")
    print(f"Valid files: {stats['valid_files']} [OK]")
    print(f"Invalid files: {stats['invalid_files']}")
    
    if stats['total_annotations'] > 0:
        print(f"\nTotal annotations: {stats['total_annotations']}")
        print("\nClass distribution:")
        for class_id, count in sorted(stats['class_distribution'].items()):
            print(f"  Class {class_id}: {count} instances")
    
    # Step 3: Print errors if any
    if stats['errors']:
        print(f"\n[ERROR] Found {len(stats['errors'])} invalid files:")
        for error in stats['errors']:
            print(f"  - {error['file']}: {error['error']}")
    else:
        print("\n[OK] All annotation files are valid!")
    
    # Step 4: Check for empty files
    print("\n[Optional] Checking for empty annotation files...")
    empty_count = 0
    pairs = get_file_pairs(IMAGES_DIR, LABELS_DIR)
    for _, label_path in pairs:
        with open(label_path, 'r') as f:
            content = f.read().strip()
            if not content:
                empty_count += 1
                print(f"  Warning: {Path(label_path).name} is empty (no annotations)")
    
    if empty_count == 0:
        print("[OK] No empty annotation files found")
    else:
        print(f"  Found {empty_count} empty annotation files")
    
    # Step 5: Summary
    print("\n" + "=" * 60)
    if stats['invalid_files'] == 0:
        print("[OK] All annotations validated successfully!")
        print("Dataset is ready for YOLO training.")
    else:
        print("[WARNING] Some annotation files need to be fixed.")
        print("Please review the errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main()

