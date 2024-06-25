from ultralytics import YOLO
import mysql.connector as cnn
from dotenv import load_dotenv
import os

class Coords:
    # The converted tensor from box.xyxy leaves a bunch of white spaces, so we want to remove them and replace with a comma to make it easier to collect the individual coordinates
    @staticmethod
    def remove_white_space(string):
        pos = string.split()
        string = ",".join(pos)
        return string

    @staticmethod
    def transform_tensor_to_string(tensor):
        numpy_array = tensor.cpu().numpy()
        tensor_string = str(numpy_array)
        coordinates_string = tensor_string.replace('[', '').replace(']', '')
        coordinates_string = Coords.remove_white_space(coordinates_string)
        return coordinates_string
    
    @staticmethod
    def get_coords(img):
        model = YOLO("./runs/detect/nano50epochs/weights/best.pt")
        results = model(img)

        coords = []
        boxes = results[0].boxes
        for box in boxes:
            tensor = Coords.transform_tensor_to_string(box.xyxy)
            coords.append(tensor)
        
        return coords

class DB:
    def connection_factory(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = cnn.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("Connection to mauasat DB successful")
        except cnn.Error as e:
            print(f"Error: '{e}'")
        return connection

    def insert_data(connection, coords, img):
        cursor = connection.cursor()
        try:
            query = "INSERT INTO wildfire (coords, image) VALUES (%s, %s)"
            data = (coords, img)
            cursor.execute(query, data)
            connection.commit()
            print("Insert OK")
            cursor.close()
        except cnn.Error as e:
            print(f"Error: '{e}'")


# Main
# Load environment variables and attempt connection to database
load_dotenv()
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

connection = DB.connection_factory(host, user, password, db_name)

# Get image and coords to insert into database
img = "./teste1.jpg"
with open(img, 'rb') as file:
    img_data = file.read()

coords = Coords.get_coords(img)
coords_string = "|"
for i in range(len(coords)):
    coords_string += coords[i] + '|'
print(coords_string)
DB.insert_data(connection, coords_string, img_data)
connection.close()