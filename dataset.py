import json
import os
from PIL import Image

# Define paths
base_path = '/content/drive/MyDrive/CottonWeedDet3'
annotations_dir = os.path.join(base_path, 'annotations')  # Folder containing all JSON files
images_dir = os.path.join(base_path, 'images')  # Folder containing all image files
output_images_dir = os.path.join(base_path, 'processed/images')  # Directory to save images
output_annotations_dir = os.path.join(base_path, 'processed/annotated')  # Directory to save YOLO format labels

# Create output directories for images and YOLO annotations if they don't exist
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_annotations_dir, exist_ok=True)

# Mapping class names to IDs
class_mapping = {
    'morningglory': 0,
    'palmer_amaranth': 1,
    'carpetweed': 2,
}

# Function to convert VIA annotations to YOLO format
def convert_to_yolo(regions, img_width, img_height):
    yolo_annotations = []
    for region in regions:
        shape_attributes = region['shape_attributes']
        x = shape_attributes['x']
        y = shape_attributes['y']
        width = shape_attributes['width']
        height = shape_attributes['height']

        # Convert to YOLO format (normalized)
        x_center = (x + width / 2) / img_width
        y_center = (y + height / 2) / img_height
        norm_width = width / img_width
        norm_height = height / img_height

        # Get class name and map to ID
        class_name = region['region_attributes']['class']
        class_id = class_mapping.get(class_name, -1)  # Default to -1 if not found

        if class_id != -1:  # Only add if class ID is valid
            yolo_annotations.append(f"{class_id} {x_center} {y_center} {norm_width} {norm_height}")

    return yolo_annotations

# Iterate through each JSON file in the annotations directory
for json_file in os.listdir(annotations_dir):
    if json_file.endswith(".json"):
        json_path = os.path.join(annotations_dir, json_file)
        
        # Load the JSON file
        with open(json_path, 'r') as f:
            via_data = json.load(f)
        
        # Extract the image filename from the JSON
        image_key = list(via_data.keys())[0]
        img_file = via_data[image_key]['filename']
        img_path = os.path.join(images_dir, img_file)
        
        if os.path.exists(img_path):
            img = Image.open(img_path)
            img_width, img_height = img.size
            
            # Convert annotations to YOLO format
            regions = via_data[image_key]['regions']
            yolo_annotations = convert_to_yolo(regions, img_width, img_height)
            
            # Save the image in the output images directory
            img.save(os.path.join(output_images_dir, img_file))
            
            # Save YOLO annotations in the annotated folder
            annotation_filename = os.path.splitext(img_file)[0] + '.txt'
            annotation_filepath = os.path.join(output_annotations_dir, annotation_filename)
            with open(annotation_filepath, 'w') as f:
                f.write("\n".join(yolo_annotations))

print("Conversion completed for all JSON files!")
