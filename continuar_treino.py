from ultralytics import YOLO

model = YOLO('./runs/detect/train/weights/last.pt')

results = model.train(data='data_custom.yaml', epochs=100, batch=0.70, resume=True)