import yaml

with open(r'yolov5m\data\myData.yaml', 'r') as file:
    labelsIndex = yaml.safe_load(file)

print(labelsIndex)