import train

train.run(data='myData.yaml', imgsz=320, weights='yolov5m.pt', epochs=20, batch_size=4)
print("Hello")