from PIL import Image

from ultralytics import YOLO

model = YOLO("./fire_s.pt")

results = model(["./teste1.jpg", "./teste2.jpg"], iou=0.7, conf=0.4)
print(results)

for i, r in enumerate(results):
    
    im_bgr = r.plot()
    im_rgb = Image.fromarray(im_bgr[..., ::-1])

    r.show()