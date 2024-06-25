from PIL import Image

from ultralytics import YOLO

model = YOLO("./runs/detect/nano50epochs/weights/best.pt")

results = model("./teste1.jpg")
print(results)

for i, r in enumerate(results):
    
    im_bgr = r.plot()
    im_rgb = Image.fromarray(im_bgr[..., ::-1])

    r.show()