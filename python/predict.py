from PIL import Image

from ultralytics import YOLO

model = YOLO("./runs/detect/train/weights/best.pt")

results = model("/home/vinicius/data/teste.jpg", iou=0.1, conf=0.9)
print(results)

for i, r in enumerate(results):
    
    im_bgr = r.plot()
    im_rgb = Image.fromarray(im_bgr[..., ::-1])

    r.show()