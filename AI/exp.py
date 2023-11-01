import controller as con

image_path = r'C:\Users\anas3\Desktop\metal1.jpg'
output_path = r'C:\Users\anas3\Desktop\metal1_out.jpg'

det = con.modelController.ModelController.make_inference(img=image_path,
                                                    normalization_dims=(512, 384),
                                                    yaml_filepath=r"C:\Users\anas3\Desktop\trash_detection.yaml",
                                                    model_filepath=r"C:\Users\anas3\Desktop\best.pt",
                                                    conf_threshold=0.1)

print(det)

import cv2
import numpy as np

def draw_bounding_box(image_path, points, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert points to NumPy array
    points = np.array(points, dtype=int)

    # Draw the bounding box
    cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    # Save the image with the bounding box
    cv2.imwrite(output_path, image)

# Example usage:
loc = det[0]['location']
x_min, y_min, x_max, y_max = loc[0], loc[1], loc[2], loc[3]

points = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]  # Replace with your own points
draw_bounding_box(image_path, points, output_path)