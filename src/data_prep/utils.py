import os
import shutil
import random
from pathlib import Path
from typing import List, Tuple


def create_dirs(base_path: str, dir_names: List[str]) -> None:
    for dir_name in dir_names:
        dir_path = Path(base_path) / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")


def count_files(directory: str, extension: str = None) -> int:
    path = Path(directory)
    if extension:
        files = list(path.glob(f"*.{extension}"))
    else:
        files = list(path.iterdir())
    return len(files)


def get_file_pairs(images_dir: str, labels_dir: str) -> List[Tuple[str, str]]:
    images_path = Path(images_dir)
    labels_path = Path(labels_dir)
    
    image_files = sorted(images_path.glob("*.png"))
    pairs = []
    
    for img_file in image_files:
        label_file = labels_path / f"{img_file.stem}.txt"
        if label_file.exists():
            pairs.append((str(img_file), str(label_file)))
        else:
            print(f"Warning: No matching label file for {img_file.name}")
    
    return pairs


def copy_files_to_split(src_files: List[Tuple[str, str]], 
                       dest_dir: str, 
                       split_name: str) -> None:
    
    dest_path = Path(dest_dir) / split_name
    
    images_dest = dest_path / "images"
    labels_dest = dest_path / "labels"
    images_dest.mkdir(parents=True, exist_ok=True)
    labels_dest.mkdir(parents=True, exist_ok=True)
    
    for img_path, label_path in src_files:
        img_name = Path(img_path).name
        label_name = Path(label_path).name
        
        shutil.copy2(img_path, images_dest / img_name)
        shutil.copy2(label_path, labels_dest / label_name)
    
    print(f"Copied {len(src_files)} files to {split_name} split")


def split_dataset(pairs: List[Tuple[str, str]], 
                 train_ratio: float = 0.7,
                 val_ratio: float = 0.15,
                 test_ratio: float = 0.15,
                 seed: int = 42) -> Tuple[List[Tuple[str, str]], 
                                          List[Tuple[str, str]], 
                                          List[Tuple[str, str]]]:
    """
    Split dataset into train, validation, and test sets.
    
    Args:
        pairs: List of (image_path, label_path) tuples
        train_ratio: Ratio for training set (default: 0.7)
        val_ratio: Ratio for validation set (default: 0.15)
        test_ratio: Ratio for test set (default: 0.15)
        seed: Random seed for reproducibility
    
    Returns:
        Tuple of (train_pairs, val_pairs, test_pairs)
    """
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 0.001:
        raise ValueError("Ratios must sum to 1.0")
    
    random.seed(seed)
    random.shuffle(pairs)
    
    total = len(pairs)
    train_end = int(total * train_ratio)
    val_end = int(total * (train_ratio + val_ratio))
    
    train_pairs = pairs[:train_end]
    val_pairs = pairs[train_end:val_end]
    test_pairs = pairs[val_end:]
    
    return train_pairs, val_pairs, test_pairs


def create_yolo_dataset_config(output_path: str,
                              class_names: List[str],
                              train_dir: str,
                              val_dir: str,
                              test_dir: str = None) -> None:
    """
    Create YOLO dataset configuration YAML file. 
    Args:
        output_path: Path to save the YAML file
        class_names: List of class names
        train_dir: Training images directory
        val_dir: Validation images directory
        test_dir: Test images directory (optional)
    """
    config_content = f"""# Dental X-Ray Cavity Detection Dataset
# Generated for YOLO training

# Dataset paths
path: data/processed  # Root dataset directory

train: {train_dir}  # Training images
val: {val_dir}      # Validation images
"""
    
    if test_dir:
        config_content += f"test: {test_dir}    # Test images\n"
    
    config_content += f"""
# Class names
names:
"""
    for idx, name in enumerate(class_names):
        config_content += f"  {idx}: {name}\n"
    
    config_content += f"""
# Number of classes
nc: {len(class_names)}
"""
    
    # Write to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(config_content)
    
    print(f"Created dataset config: {output_path}")


def print_dataset_statistics(pairs: List[Tuple[str, str]], 
                            split_name: str = "Dataset") -> None:
    """
    Print statistics about the dataset.
    
    Args:
        pairs: List of (image_path, label_path) tuples
        split_name: Name of the split
    """
    print(f"\n{split_name} Statistics:")
    print(f"  Total samples: {len(pairs)}")
    
    # Count classes
    class_counts = {}
    for _, label_path in pairs:
        with open(label_path, 'r') as f:
            for line in f:
                if line.strip():
                    class_id = int(line.split()[0])
                    class_counts[class_id] = class_counts.get(class_id, 0) + 1
    
    print(f"  Total annotations: {sum(class_counts.values())}")
    print(f"  Classes found: {sorted(class_counts.keys())}")
    for class_id in sorted(class_counts.keys()):
        print(f"    Class {class_id}: {class_counts[class_id]} instances")


if __name__ == "__main__":
    # Test the utility functions
    print("Testing utils.py...")
    print("All utility functions loaded successfully!")
