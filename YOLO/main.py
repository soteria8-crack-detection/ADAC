import os
import time
import shutil

from utils.video_slicing import VideoProcessor
from utils.ultralytics import InstanceSegmentation
from utils.convert_inference_to_video import InstanceSegmentationImageComposer

class Main:
    """
    Main class for processing videos, performing instance segmentation, and creating result videos.

    Parameters:
        - video_path (str): Path to the input video file.
        - output_folder (str): Output folder for storing extracted frames.
        - model_path (str): Path to the YOLO model.
        - source_dir (str): Directory containing input images for instance segmentation.
        - inference_results_name (str): Name of the directory to save instance segmentation results.
        - pred (str): Path to the directory containing instance segmentation prediction results.
        - result_name (str): Name of the directory to save the final result video.

    Methods:
        - runner(): Execute the video processing, instance segmentation, and result video creation.

    Example:
        main_instance = Main(
            video_path='path/to/video.mp4',
            output_folder='path/to/output',
            model_path='path/to/best.pt',
            source_dir='path/to/source/images',
            inference_results_name='inference_results',
            pred='path/to/predictions',
            result_name='final_result'
        )
        main_instance.runner()
    """
    
    def __init__(self, video_path, output_folder, model_path, source_dir, inference_results_name, label_dir, pred, result_name):
        """
        Initializes the Main class with input parameters.

        Parameters:
            - video_path (str): Path to the input video file.
            - output_folder (str): Output folder for storing extracted frames.
            - model_path (str): Path to the YOLO model.
            - source_dir (str): Directory containing input images for instance segmentation.
            - inference_results_name (str): Name of the directory to save instance segmentation results.
            - pred (str): Path to the directory containing instance segmentation prediction results.
            - result_name (str): Name of the directory to save the final result video.
        """
        self.video_path = video_path
        self.output_folder = output_folder
        self.model_path = model_path
        self.source_dir = source_dir
        self.inference_results_name = inference_results_name
        self.label_dir = label_dir
        self.pred = pred
        self.result_name = result_name
        
    def main(self):
        """
        Execute the video processing, instance segmentation, and result video creation.
        """
        processor = VideoProcessor(self.video_path, self.output_folder)
        processor.extract_frames_from_video()
        
        instance_seg = InstanceSegmentation(model_path = self.model_path, 
                                            source_dir = self.source_dir, 
                                            inference_results_name = self.inference_results_name,
                                            label_dir = self.label_dir)
        instance_seg.predictor()
        instance_seg.make_label_image_info()
        
        composer = InstanceSegmentationImageComposer(self.pred, 60, self.result_name)
        composer.frame_to_video()
        
if __name__ == "__main__":
    PATH = os.getcwd()
    
    # 첫번째 입력할 경로
    videos_01 = os.path.join(PATH, 'data/video', 'video_01.MP4')
    outfolder_01 = os.path.join(PATH, 'dataset/image_extraction/video_01')
    
    model_path = os.path.join(PATH, 'data', 'best.pt')
    
    source_dir_01 = os.path.join(PATH, 'dataset/image_extraction/video_01')
    inference_results_name_01 = 'inference_video_01'
    
    label_dir_01 = os.path.join(PATH, 'runs/segment', 'inference_video_01')
    
    pred_01 = os.path.join(PATH, 'runs/segment', 'inference_video_01')
    result_name_01 = 'pred_result_video_01'  
    
    # 두번째 입력할 경로
    videos_02 = os.path.join(PATH, 'data/video', 'video_02.MP4')
    outfolder_02 = os.path.join(PATH, 'dataset/image_extraction/video_02')
    
    source_dir_02 = os.path.join(PATH, 'dataset/image_extraction/video_02')
    inference_results_name_02 = 'inference_video_02'

    # label_dir_02 = os.path.join(PATH, 'runs/segment', 'inference_video_02')

    pred_02 = os.path.join(PATH, 'runs/segment', 'inference_video_02')
    result_name_02 = 'pred_result_video_02'  
    
    run_01 = Main(videos_01, outfolder_01, model_path, source_dir_01, inference_results_name_01, label_dir_01, pred_01, result_name_01)
    run_01.main()
    
    run_02 = Main(videos_02, outfolder_02, model_path, source_dir_02, inference_results_name_02, label_dir_01, pred_02, result_name_02)
    run_02.main()
    
    pred_result_video_01_path = os.path.join(pred_01, 'pred_result_video_01.mp4')
    destination_pred_result_video_01_path = os.path.join(PATH, 'results')
    shutil.move(pred_result_video_01_path, destination_pred_result_video_01_path)

    pred_result_video_02_path = os.path.join(pred_02, 'pred_result_video_02.mp4')
    destination_pred_result_video_02_path = os.path.join(PATH, 'results')
    shutil.move(pred_result_video_02_path, destination_pred_result_video_02_path)
    