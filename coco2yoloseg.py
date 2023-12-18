"""
Author: Zubin Bhuyan
Date: June 21, 2023

MIT License

"""

import json
import os

def convert_coco_to_yolo_segmentation(json_file, folder_name = "labels"):

    folder_name = folder_name
    # Load the JSON file
    with open(json_file, 'r') as file:
        coco_data = json.load(file)

    # Create a "labels" folder to store YOLO segmentation annotations
    output_folder = os.path.join(os.path.dirname(json_file), folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # Extract annotations from the COCO JSON data
    categories = coco_data["categories"]
    print(categories)

    annotations = coco_data['annotations']
    for annotation in annotations:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        segmentation = annotation['segmentation']
        bbox = annotation['bbox']

        # 指定对应类别
        # if category_id == 1 :#person
        #     category_id = 1
        # elif category_id == 3: #car
        #     category_id = 2
        # elif category_id == 8 :#truck
        #     category_id = 3
        # elif category_id == 6 :#bus
        #     category_id = 4
        # elif category_id == 7 :#train
        #     category_id = 5
        # elif category_id == 2 :#bicycle
        #     category_id = 6
        # elif category_id == 4 :#motorcycle
        #     category_id = 7
        # elif category_id == 10 :#traffic light
        #     category_id = 8
        # else:
        #     continue
        # print(category_id)


        # Find the image filename from the COCO data
        for image in coco_data['images']:
            if image['id'] == image_id:
                image_filename = os.path.basename(image['file_name'])
                image_filename = os.path.splitext(image_filename)[0] # Removing the extension. (In our case, it is the .jpg or .png part.)
                image_width = image['width']
                image_height = image['height']
                break

        # Calculate the normalized center coordinates and width/height
        x_center = (bbox[0] + bbox[2] / 2) / image_width
        y_center = (bbox[1] + bbox[3] / 2) / image_height
        bbox_width = bbox[2] / image_width
        bbox_height = bbox[3] / image_height

        try:
            # Convert COCO segmentation to YOLO segmentation format
            yolo_segmentation = [f"{(x) / image_width:.5f} {(y) / image_height:.5f}" for x, y in zip(segmentation[0][::2], segmentation[0][1::2])]
            #yolo_segmentation.append(f"{(segmentation[0][0]) / image_width:.5f} {(segmentation[0][1]) / image_height:.5f}")
            yolo_segmentation = ' '.join(yolo_segmentation)

            # Generate the YOLO segmentation annotation line
            yolo_annotation = f"{category_id} {yolo_segmentation}"

            # Save the YOLO segmentation annotation in a file
            output_filename = os.path.join(output_folder, f"{image_filename}.txt")
            with open(output_filename, 'a+') as file:
                file.write(yolo_annotation + '\n')
        except:
            continue

    print("Conversion completed. YOLO segmentation annotations saved in 'labels' folder.")


# Example usage
json_file = r"G:\Edge_downloads\raildb\anno_new\fixed_day\annotations.json" #JSON file
split = r"G:\Edge_downloads\raildb\anno_new\fixed_day\yololabels" #Folder
convert_coco_to_yolo_segmentation(json_file, split)
