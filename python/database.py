from ultralytics import YOLO
import mysql.connector as cnn
from dotenv import load_dotenv
import os

class Coords:
    # The converted tensor from box.xyxy leaves a bunch of white spaces, so we want to remove them and replace with a comma to make it easier to collect the individual coordinates
    def remove_white_space(string):
        pos = string.split()
        string = ",".join(pos)
        return string

    def transform_tensor_to_string(tensor):
        numpy_array = tensor.cpu().numpy()
        tensor_string = str(numpy_array)
        coordinates_string = tensor_string.replace('[', '').replace(']', '')
        coordinates_string = Coords.remove_white_space(coordinates_string)
        return coordinates_string
    
    def get_results(img):
        model = YOLO("./runs/detect/fire_s.pt")
        results = model(img, iou=0.2, conf=0.4)

        return results
    
    def get_coords(results):
        coords = []
        boxes = results[0].boxes
        for box in boxes:
            tensor = Coords.transform_tensor_to_string(box.xyxy)
            coords.append(tensor)
        
        return coords
    
    def get_label(results):
        labels = []
        boxes = results[0].boxes
        for box in boxes:
            tensor = Coords.transform_tensor_to_string(box.cls)
            labels.append(tensor)
    
        return labels
    
    def get_conf(results):
        confs = []
        boxes = results[0].boxes
        for box in boxes:
            tensor = Coords.transform_tensor_to_string(box.conf)
            confs.append(tensor)
    
        return confs
    
    def get_info(img):
        # Load environment variables and attempt connection to database
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        connection = DB.connection_factory(host, user, password, db_name)
        results = Coords.get_results(img)

        # Get image and coords to insert into database
        with open(img, 'rb') as file:
            img_data = file.read()

        coords = Coords.get_coords(results)
        coords_string = "|"
        for i in range(len(coords)):
            coords_string += coords[i] + '|'
        
        confs = Coords.get_conf(results)
        confs_string = "|"
        for i in range(len(confs)):
            confs_string += confs[i] + '|'
        
        labels = Coords.get_label(results)
        labels_string = "|"
        for i in range(len(labels)):
            labels_string += labels[i] + '|'

        DB.insert_data(connection, coords_string, confs_string, labels_string, img_data)
        connection.close()

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
    
    def insert_data(connection, coords, confs, labels, img):
        cursor = connection.cursor()
        try:
            query = "INSERT INTO wildfire (coords, confs, labels, image) VALUES (%s, %s, %s, %s)"
            data = (coords, confs, labels, img)
            cursor.execute(query, data)
            connection.commit()
            print("Insert OK")
            cursor.close()
        except cnn.Error as e:
            print(f"Error: '{e}'")


# Main
img = "./teste2.jpg"
Coords.get_info(img)