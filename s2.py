import os
import shutil
import random

# Paths
base_path = '/content/drive/MyDrive/CottonWeedDet3/processed'
images_dir = os.path.join(base_path, 'images')
annotations_dir = os.path.join(base_path, 'annotated')
val_images_dir = os.path.join(base_path, 'val_images')
val_annotations_dir = os.path.join(base_path, 'val_annotations')

# Create validation directories
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_annotations_dir, exist_ok=True)

# Split dataset
image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
num_val = int(len(image_files) * 0.2)  # Use 20% for validation
val_files = random.sample(image_files, num_val)

for val_file in val_files:
    # Move to validation images directory
    shutil.move(os.path.join(images_dir, val_file), os.path.join(val_images_dir, val_file))
    # Move the corresponding annotation file
    annotation_file = os.path.splitext(val_file)[0] + '.txt'
    shutil.move(os.path.join(annotations_dir, annotation_file), os.path.join(val_annotations_dir, annotation_file))

print("Dataset split into training and validation sets!")
