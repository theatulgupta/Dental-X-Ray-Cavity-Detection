
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from data_prep.utils import (
    create_dirs,
    get_file_pairs,
    split_dataset,
    copy_files_to_split,
    print_dataset_statistics,
    create_yolo_dataset_config
)


def main():
    RAW_DATA_DIR = "data/raw/dental"
    PROCESSED_DATA_DIR = "data/processed"
    IMAGES_DIR = os.path.join(RAW_DATA_DIR, "images")
    LABELS_DIR = os.path.join(RAW_DATA_DIR, "object_detection_labels")
    
    TRAIN_RATIO = 0.7
    VAL_RATIO = 0.15
    TEST_RATIO = 0.15
    
    RANDOM_SEED = 42
    
    CLASS_NAMES = [
        "cavity_class_0",  
        "cavity_class_1",  
        "cavity_class_2",  
        "cavity_class_3"   
    ]
    
    print("=" * 60)
    print("Dental X-Ray Dataset Preparation")
    print("=" * 60)
    
    # Step 1
    print("\n[Step 1] Checking raw data...")
    if not os.path.exists(IMAGES_DIR):
        print(f"ERROR: Images directory not found: {IMAGES_DIR}")
        sys.exit(1)
    if not os.path.exists(LABELS_DIR):
        print(f"ERROR: Labels directory not found: {LABELS_DIR}")
        sys.exit(1)
    
    # Step 2
    print("\n[Step 2] Getting image-label pairs...")
    pairs = get_file_pairs(IMAGES_DIR, LABELS_DIR)
    print(f"[OK] Found {len(pairs)} valid image-label pairs")
    
    # Step 3
    print("\n[Step 3] Original dataset statistics:")
    print_dataset_statistics(pairs, split_name="Raw Dataset")
    
    # Step 4
    print(f"\n[Step 4] Splitting dataset...")
    print(f"  Train: {TRAIN_RATIO*100}%")
    print(f"  Validation: {VAL_RATIO*100}%")
    print(f"  Test: {TEST_RATIO*100}%")
    
    train_pairs, val_pairs, test_pairs = split_dataset(
        pairs,
        train_ratio=TRAIN_RATIO,
        val_ratio=VAL_RATIO,
        test_ratio=TEST_RATIO,
        seed=RANDOM_SEED
    )
    
    print(f"\n[OK] Split completed:")
    print(f"  Train: {len(train_pairs)} samples")
    print(f"  Validation: {len(val_pairs)} samples")
    print(f"  Test: {len(test_pairs)} samples")
    
    # Step 5
    print("\n[Step 5] Creating directory structure...")
    create_dirs(PROCESSED_DATA_DIR, ['train', 'val', 'test'])
    create_dirs(os.path.join(PROCESSED_DATA_DIR, 'train'), ['images', 'labels'])
    create_dirs(os.path.join(PROCESSED_DATA_DIR, 'val'), ['images', 'labels'])
    create_dirs(os.path.join(PROCESSED_DATA_DIR, 'test'), ['images', 'labels'])
    print("[OK] Directory structure created")
    
    # Step 6
    print("\n[Step 6] Copying files to splits...")
    copy_files_to_split(train_pairs, PROCESSED_DATA_DIR, 'train')
    copy_files_to_split(val_pairs, PROCESSED_DATA_DIR, 'val')
    copy_files_to_split(test_pairs, PROCESSED_DATA_DIR, 'test')
    print("[OK] Files copied successfully")
    
    # Step 7
    print("\n[Step 7] Split statistics:")
    print_dataset_statistics(train_pairs, "Train Set")
    print_dataset_statistics(val_pairs, "Validation Set")
    print_dataset_statistics(test_pairs, "Test Set")
    
    # Step 8
    print("\n[Step 8] Creating YOLO dataset configuration...")
    config_path = os.path.join(PROCESSED_DATA_DIR, "dataset.yaml")
    create_yolo_dataset_config(
        output_path=config_path,
        class_names=CLASS_NAMES,
        train_dir="train/images",
        val_dir="val/images",
        test_dir="test/images"
    )
    print("[OK] Dataset configuration created")

    print("\n[OK] Ready for YOLO training!")


if __name__ == "__main__":
    main()

