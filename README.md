# Como prever um incêndio

Crie um ambiente virtual
```bash
python -m venv venv
```
Ative o ambiente virtual
```bash
source venv/bin/activate
```
Instale as dependências com pip
```bash
pip install -r requirements. txt
```
Para testar algum dos modelos, vá para predict.py e troque o caminho para o desejado, segue abaixo um exemplo: 
```python
model = YOLO("./runs/detect/nano5epochs/weights/best.pt")
```
Caso queira testar com outras imagens, precisa apenas mudar o caminho do results
```python
results = model("path/to/image")
```

# Como treinar um novo modelo

Crie um arquivo .yaml chamado data_custom.yaml com os caminhos nescessarios para o seu dataset. O projeto utiliza o seguinte dataset:  
<a href="https://drive.google.com/drive/folders/1DWgsQLVgkkLM8m-VcugHNpD5WYDbjYp5">D-Fire</a>

```yaml
train: /path/to/dataset/train
val: /path/to/dataset/val

names:
  0: smoke
  1: fire
```
Com o dataset e o seu caminho adicionados, execute o main.py. Algums problemas ao rodar estão com possíveis soluções comentadas no próprio arquivo.


# Referências

### Dataset D-Fire
Pedro Vinícius Almeida Borges de Venâncio, Adriano Chaves Lisboa, Adriano Vilela Barbosa: <a href="https://link.springer.com/article/10.1007/s00521-022-07467-z">An automatic fire detection system based on deep convolutional neural networks for low-power, resource-constrained devices.</a> In: Neural Computing and Applications, 2022.
