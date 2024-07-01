from ultralytics import YOLO

model = YOLO('./runs/detect/train3/weights/last.pt')

results = model.train(data='data_custom.yaml', epochs=200, batch=0.90, resume=True)