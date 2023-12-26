import os
import cv2
import natsort

class InstanceSegmentationImageComposer:
    """
    A class for creating a video using instance segmentation images.

    Parameters:
        - imgs_path (str): Path to the folder containing input images.
        - fps (int): Frame rate of the generated video.
        - out_file_name (str): Name of the generated video file. Default is 'pred_result'.

    Methods:
        - img_file_sort(without_file_type=False): Sorts and returns the image files.
        - frame_to_video(): Generates a video using the sorted image files.

    Example:
        composer = InstanceSegmentationImageComposer(imgs_path='input_images',
                                                     fps=30,
                                                     out_file_name='output_video')
        composer.frame_to_video()
    """
    
    def __init__(self, imgs_path, fps, out_file_name='pred_result'):
        """
        Initializes the InstanceSegmentationImageComposer.

        Parameters:
            - imgs_path (str): Path to the folder containing input images.
            - fps (int): Frame rate of the generated video.
            - out_file_name (str): Name of the generated video file. Default is 'pred_result'.
        """
        self.imgs_path = imgs_path
        self.fps = fps
        self.out_file_name = out_file_name

    def img_file_sort(self, without_file_type=False):
        """
        Sorts and returns the image files.

        Parameters:
            - without_file_type (bool): Whether to sort without file type. Default is False.

        Returns:
            - img_files (list): Sorted list of image files.
        """
        img_files = [f for f in os.listdir(self.imgs_path) if f.endswith('.jpg') or f.endswith('.png')]
        img_files = [float((item.split('s')[0]).split('_')[1]) for item in img_files]
        img_files = natsort.natsorted(img_files)

        if without_file_type:
            img_files = ['frame_'+str(name)+'s' for name in img_files]
        else:
            img_files = ['frame_'+str(name)+'s.jpg' for name in img_files]
        return img_files

    def frame_to_video(self):
        """
        Generates a video using the sorted image files.
        """
        img_files = self.img_file_sort()

        video_file = os.path.join(self.imgs_path, f'{self.out_file_name}.mp4')

        first_image = cv2.imread(os.path.join(self.imgs_path, img_files[0]))
        height, width = first_image.shape[:2] 

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_file, fourcc, self.fps, (width, height))
        print('video width:', width, ', height:', height)

        for image_file in img_files:
            img = cv2.imread(os.path.join(self.imgs_path, image_file)) 
            video_writer.write(img)

        video_writer.release()
        print(f'비디오가 생성되었습니다: {video_file}')
        