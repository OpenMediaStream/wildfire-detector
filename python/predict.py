from PIL import Image

from ultralytics import YOLO

model = YOLO("./runs/detect/fire_s.pt")

results = model("./teste2.jpg", iou=0.2, conf=0.4)
print(results)

for i, r in enumerate(results):
    
    im_bgr = r.plot()
    im_rgb = Image.fromarray(im_bgr[..., ::-1])

    r.show()