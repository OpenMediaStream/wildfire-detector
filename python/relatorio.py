import mysql.connector as cnn
from dotenv import load_dotenv
import os
from io import BytesIO
import numpy as np
import cv2

# Connect to DB
load_dotenv()
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

connection = cnn.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

cursor = connection.cursor()

# Obtain image binary data from longblob and coords string
cursor.execute("SELECT image FROM wildfire WHERE id = 1")
image_data = cursor.fetchone()[0]

cursor.execute("SELECT coords from wildfire WHERE id = 1")
coords_string = cursor.fetchone()[0]

cursor.close()
connection.close()

# Turns coords into a list and decodes the binary image data
image_array = np.frombuffer(image_data, dtype=np.uint8)
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

coords = coords_string.split('|')
while '' in coords:
    coords.remove('')


# Draws the boxes on the image to save the final result
parsed_coordinates = []
for coord in coords:
    x1, y1, x2, y2 = map(float, coord.split(','))
    parsed_coordinates.append((int(x1), int(y1), int(x2), int(y2)))

for (x1, y1, x2, y2) in parsed_coordinates:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 255), 4)

cv2.imwrite('result.jpg', image)

# Adicionar tags nas caixas para ficar igual ao plot do YOLO