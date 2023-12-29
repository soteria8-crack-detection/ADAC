import os
import subprocess

class MainRunner:
    def __init__(self, folder):
        self.folder = folder

    def run_main_script(self):
        main_script_path = os.path.join(self.folder, "main.py")
        if os.path.exists(main_script_path):
            print(f"Running {main_script_path}...")
            subprocess.run(["python", main_script_path])
        else:
            print(f"No main.py found in {self.folder}")

def run_main_scripts_in_order(make_folder_list, folders):
    """
    Runs main.py scripts in the specified folders in order.

    Parameters:
        - folders (list): List of folder paths containing main.py scripts.
    """
    for path in make_folder_list:
        os.makedirs(path, exist_ok=True)
    
    for folder in folders:
        runner = MainRunner(folder)
        runner.run_main_script()
        
make_folder_list = ['./dataset/image_extraction/video_01', './dataset/image_extraction/video_02', './dataset/result_txt']
folders_to_run = ["YOLO", "frame_matching", "comparative_analysis"]
run_main_scripts_in_order(make_folder_list, folders_to_run)
