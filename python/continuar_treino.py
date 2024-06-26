from ultralytics import YOLO

model = YOLO('./runs/detect/train/weights/last.pt')

results = model.train(data='data_custom.yaml', epochs=50, batch=0.90, resume=True)