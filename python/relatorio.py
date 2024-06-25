import mysql.connector as cnn
from dotenv import load_dotenv
import os
from io import BytesIO
import numpy as np
import cv2

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

cursor.execute("SELECT image FROM wildfire WHERE id = 1")
image_data = cursor.fetchone()[0]

cursor.close()
connection.close()

image_array = np.frombuffer(image_data, dtype=np.uint8)

image_cv2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

cv2.imwrite('imagem_db.jpg', image_cv2)
