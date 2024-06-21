from ultralytics import YOLO

model = YOLO('yolov8l.pt')

# Caso esteja recebendo um erro de memória, tente diminuir a quantidade de batch para não ultrapassar o limite de VRAM da sua GPU
# Caso esteja travando e/ou fechando o terminal, tente diminuir o número de workers para reduzir a carga na memória RAM
model.train(
   data="data_custom.yaml",
   task='detect',
   epochs=5,
   verbose=True,
   batch=16,
   imgsz=640,
   patience=20,
   save=True,
   device=0,
   workers=8,
   cos_lr=True,
   lr0=0.0001,
   lrf=0.00001,
   warmup_epochs=3,
   warmup_bias_lr=0.000001,
   optimizer='Adam',
   seed=42,
)
