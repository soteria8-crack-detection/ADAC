import os
import pickle
import natsort

from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

class ComparativeAnalysis:
    """
    A class for comparative analysis of instance segmentation results using YOLO labels.

    Methods:
        - __init__(file_info, search_folder, option): Initializes the ComparativeAnalysis class.
        - txt_file_sort(txts_path, without_file_type=False): Sorts and returns the list of YOLO label files.
        - calculate_polygon_area(coordinates): Calculates the area of a polygon given its coordinates.
        - read_yolo_labels(file_path): Reads YOLO labels from a file.
        - process_results_folder(): Processes YOLO label files in the results folder and calculates the total area for each class.
    """
    
    def __init__(self, file_info, search_folder, option):
        """
        Initializes the ComparativeAnalysis class.

        Parameters:
            - file_info (str): Path to the file containing information about YOLO label files.
            - search_folder (str): Path to the folder containing YOLO label files.
            - option (str): Additional option for the output file name.
        """
        self.file_info = file_info
        self.search_folder = search_folder
        self.image_width = 1280
        self.image_height = 720
        self.option = option

    def txt_file_sort(self, txts_path, without_file_type=False):
        """
        Sorts and returns the list of YOLO label files.

        Parameters:
            - txts_path (str): Path to the folder containing YOLO label files.
            - without_file_type (bool): Whether to sort without file type. Default is False.

        Returns:
            - txt_files (list): Sorted list of YOLO label files.
        """
        txt_files = [f for f in os.listdir(txts_path) if f.endswith('.txt')]
        txt_files = [float(item.split('s')[0])for item in txt_files]
        txt_files = natsort.natsorted(txt_files)
        
        if without_file_type:
            txt_files = [str(name)+'s.txt' for name in txt_files]
        else:
            txt_files = [str(name)+'s' for name in txt_files]
        return txt_files

    def calculate_polygon_area(self, coordinates):
        """
        Calculates the area of a polygon given its coordinates.

        Parameters:
            - coordinates (list): List of coordinates defining the polygon.

        Returns:
            - area (float): Area of the polygon.
        """
        polygon = Polygon(coordinates)
        return polygon.area

    def read_yolo_labels(self, file_path):
        """
        Reads YOLO labels from a file.

        Parameters:
            - file_path (str): Path to the YOLO label file.

        Returns:
            - labels (list): List of YOLO labels.
        """
        labels = []

        with open(file_path, 'r') as file: 
            for line in file:
                parts = line.strip().split() 

                if len(parts) < 1:
                    print(f"Skipping invalid line: {line}") 
                    continue

                class_id = int(parts[0])
                coordinates = [(float(parts[i]), float(parts[i+1])) for i in range(1, len(parts)-1, 2)]

                labels.append((class_id, coordinates))
        return labels 

    def process_results_folder(self):
        """
        Processes YOLO label files in the results folder and calculates the total area for each class.
        Saves the result to a pickle file.

        Returns:
            None
        """
        try:
            with open(self.file_info, 'rb') as file:
                label_files = pickle.load(file)
        except:
            with open(self.file_info, 'rb') as file:
                label_files = file.readlines()
                label_files = [(line.decode().strip()).split('.jpg')[0] for line in label_files]
        search_list = [f.split('.txt')[0] for f in os.listdir(self.search_folder) if f.endswith('.txt')]
            
        tmp = []

        for file_path in label_files:
            total_areas = {0: 0, 1: 0, 2: 0}
            
            if file_path in search_list:
                yolo_labels = self.read_yolo_labels(self.search_folder+file_path+'.txt')
                class_polygons = {}

                for class_id, normalized_coordinates in yolo_labels:
                    absolute_coordinates = [(x * self.image_width, y * self.image_height) for x, y in normalized_coordinates]
                    
                    if class_id not in class_polygons:
                        class_polygons[class_id] = []
                    class_polygons[class_id].append(absolute_coordinates)

                for class_id, polygons in class_polygons.items():
                    total_area = 0.0
                    for poly_coords in polygons:
                        
                        if len(poly_coords) < 3:
                            print("Skipping polygon with insufficient coordinates")
                            continue

                        poly_coords = orient(Polygon(poly_coords)).exterior.coords.xy
                        area = self.calculate_polygon_area(list(zip(poly_coords[0], poly_coords[1])))
                        total_area += area

                    total_areas[class_id] = total_area
            else: 
                pass

            file_name = os.path.basename(file_path)
            tmp.append([file_name, total_areas])
            
            out_folder = os.path.join(os.getcwd(), 'dataset/result_txt')
            
            with open(out_folder+f'/_mask_info_{self.option}.txt', 'wb') as f:
                pickle.dump(tmp, f)
    