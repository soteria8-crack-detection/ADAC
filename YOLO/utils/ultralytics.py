import os
import pickle

from ultralytics import YOLO

class InstanceSegmentation:
    """
    A class for performing instance segmentation using the YOLO model.

    Parameters:
        - model_path (str): Path to the YOLO model.
        - source_dir (str): Directory containing input images for inference.
        - inference_results_name (str): Name of the directory to save the inference results.

    Attributes:
        - model: YOLO model instance.
        - source (str): Directory containing input images for inference.
        - name (str): Name of the directory to save the inference results.

    Methods:
        - predictor(): Perform instance segmentation on input images and save the results.
        - make_label_image_info(): Create a file containing information about labeled images.

    Example:
        instance_segmentation = InstanceSegmentation(model_path='path/to/yolo_model.pth',
                                                     source_dir='path/to/source_images',
                                                     inference_results_name='inference_results')
        instance_segmentation.predictor()
        instance_segmentation.make_label_image_info()
    """
    
    def __init__(self, model_path, source_dir, inference_results_name, label_dir):
        """
        Initializes the InstanceSegmentation class.

        Parameters:
            - model_path (str): Path to the YOLO model.
            - source_dir (str): Directory containing input images for inference.
            - inference_results_name (str): Name of the directory to save the inference results.
        """
        self.model = YOLO(model_path)
        self.source = source_dir
        self.name = inference_results_name
        self.label_dir = label_dir
        
    def predictor(self):
        """
        Perform instance segmentation on input images and save the results.

        Returns:
            - results: Dictionary containing inference results.
        """
        results = self.model.predict(
            source = self.source,
            save = True,
            classes = [0, 1, 2],
            save_txt = True,
            save_conf = True,
            name = self.name,
            imgsz=(512, 512),
            device=0
        )
        return results
        
    def make_label_image_info(self):
        """
        Create a file containing information about labeled images.
        """
        txt_files = [f for f in os.listdir(os.path.join(self.label_dir, 'labels')) if f.endswith('.txt')]
        txt_files = sorted([float((item.split('s')[0]).split('_')[1]) for item in txt_files])
        txt_files = ['frame_'+str(name)+'s' for name in txt_files]
        with open(os.path.join(os.getcwd(), 'dataset/result_txt', '_image_info.txt'), 'wb') as f:
            pickle.dump(txt_files, f)
