from ultralytics import YOLO

model = YOLO('yolov8x.pt')

# Caso esteja recebendo um erro de memória, tente diminuir a quantidade de batch para não ultrapassar o limite de VRAM da sua GPU
# Caso esteja travando e/ou fechando o terminal, tente diminuir o número de workers para reduzir a carga na memória RAM
model.train(
   data="data_custom.yaml",
   epochs=50,
   batch=0.90,
   #amp=True # Habilitar amp apenas caso a utilização de memória RAM esteja alta demais, amp reduz precisão do modelo e deixa mais lento o treino
)
