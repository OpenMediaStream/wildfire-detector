import mysql.connector as cnn
from dotenv import load_dotenv
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

class Data:
    def get_contrasting_colors(label_list):
        color_map = plt.get_cmap('Dark2')
        num_colors = color_map.N
        results = []
        for i in range(len(label_list)):
            color_index = i+1 % num_colors
            bg_color = color_map(color_index)
            
            # Convert the background color to RGB tuple
            bg_color_rgb = tuple(int(255 * c) for c in bg_color[:3])
            
            # Determine text color (white or black) based on luminance
            luminance = 0.299 * bg_color_rgb[0] + 0.587 * bg_color_rgb[1] + 0.114 * bg_color_rgb[2]
            text_color_rgb = (0, 0, 0) if luminance > 186 else (255, 255, 255)
            results.append((bg_color_rgb, text_color_rgb))

        return results
    
    def draw_box(coords, confs, labels, labels_list, image,):
        colors = Data.get_contrasting_colors(labels_list)

        for i in range(4):
            # Gets coords for the box to be drawn
            x1, y1, x2, y2 = map(float, coords[i].split(','))
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            # Transforms string value to float
            conf = f"{float(confs[i])*100:.0f}%"

            # Renames the label to the correct annotation
            if labels[i] == '0':
                label = "smoke"
                color_bg = colors[0][0]
                color_text = colors[0][1]
            else:
                label = "fire"
                color_bg = colors[1][0]
                color_text = colors[1][1]

            # Text settings
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{label}: {conf}"
            font_scale = 0.7
            thickness = 1
            text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
            text_x = x1
            text_y = y1 - 10 if y1 - 10 > 10 else y1 + text_size[1] + 10
            rect_start = (text_x, text_y - text_size[1] - 5)
            rect_end = (text_x + text_size[0], text_y + 5)

            # Draws the background for the text
            cv2.rectangle(image, rect_start, rect_end, (color_bg), cv2.FILLED)

            # Writes text on image
            cv2.putText(image, text, (text_x, text_y), font, font_scale, (color_text), thickness, cv2.LINE_AA)

            # Draws the prediction box
            cv2.rectangle(image, (x1, y1), (x2, y2), (color_bg), 2)

        cv2.imwrite('result.jpg', image)

    def get_wildfire(id):
        # Connect to DB
        load_dotenv()
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        db_name = os.getenv('DB_NAME')

        connection = DB.connection_factory(host, user, password, db_name)
        

        # Obtain coords, confs, labels strings and image binary data from longblob
        data = DB.retrieve_data(connection, tuple([id]))
        coords_string = data[0]
        confs_string = data[1]
        labels_string = data[2]
        image_data = data[3]
      

        # Turns coords, confs and labels into a list and filters out the garbage used to separate the string
        coords = coords_string.split('|')
        while '' in coords:
            coords.remove('')

        confs = confs_string.split('|')
        while '' in confs:
            confs.remove('')

        labels = labels_string.split('|')
        while '' in labels:
            labels.remove('')

        # Decodes the binary image data
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        labels_list = ["smoke", "fire"]

        Data.draw_box(coords, confs, labels, labels_list, image)

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
    
    def retrieve_data(connection, id):
        cursor = connection.cursor()
        results = []
        try:
            query = "SELECT coords, confs, labels, image FROM wildfire WHERE id = %s"
            data = (id)
            cursor.execute(query, data)
            print("Select OK")
            row = cursor.fetchone()
            if row != None:
                for i in range(4):
                    results.append(row[i])
            return results
        except cnn.Error as e:
            print(f"Error: '{e}'")


# Main

Data.get_wildfire(1)