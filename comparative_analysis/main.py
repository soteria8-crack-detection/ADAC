import os
import time
import pickle

from utils.comparing_the_inference_results import ComparativeAnalysis

class Main:
    """
    Main class for running ComparativeAnalysis and generating a final report.

    Attributes:
        - path (str): Path to the result file.
        - label (str): Label path.

    Methods:
        - __init__(path, label): Constructor for the Main class.
        - runner(): Method to run the ComparativeAnalysis and process the results.
    """
    
    def __init__(self, path, label, option):
        """
        Constructor for the Main class.

        Parameters:
            - path (str): Path to the result file.
            - label (str): Label path.
        """
        self.path = path
        self.label = label
        self.option = option
        
    def runner(self):
        """
        Method to run the ComparativeAnalysis and process the results.
        """
        results = ComparativeAnalysis(self.path, self.label, self.option)
        results.process_results_folder()
        
def main():
    """
    Main function that processes a list of results and runs the ComparativeAnalysis.
    """
    PATH = os.getcwd()
    
    run_01 = Main(os.path.join(PATH, 'dataset/result_txt', '_image_info.txt'), os.path.join(PATH, 'runs/segment', 'inference_video_01', 'labels/'), '01')
    run_01.runner()
    
    run_02 = Main(os.path.join(PATH, 'dataset/result_txt', '_pair_info.txt'), os.path.join(PATH, 'runs/segment', 'inference_video_02', 'labels/'), '02')
    run_02.runner()

def generate_final_report():
    """
    Function to generate the final report based on the processed results.
    """
    load_path = os.path.join(os.getcwd(), 'dataset/result_txt')
    
    with open(os.path.join(load_path, '_mask_info_01.txt'), 'rb') as lf:
        right_01 = pickle.load(lf)
    
    with open(os.path.join(load_path, '_mask_info_02.txt'), 'rb') as lf:
        right_02 = pickle.load(lf)
        
    file_tmp = []
    save_path = os.path.join(os.getcwd(), 'results')
    
    for num in range(len(right_01)):
        info_tmp = []
        
        for i in right_01[num][1].keys():
            if right_01[num][1][i] != 0:
                info_tmp.append(str(round((right_01[num][1][i] - right_02[num][1][i])/right_01[num][1][i]*100, 2))+'% 변화')
            else:
                info_tmp.append('변화 없음')
        frame_tmp = (right_02[num][0].split('_')[1]).split('.')[0]
        txt = ' '.join([
            f'video_02 {frame_tmp}s :',
            f'reinforcement {info_tmp[0]} |',
            f'white_bleeding {info_tmp[1]} |',
            f'red_bleeding {info_tmp[2]}'
        ])
        file_tmp.append(txt)
        
    with open(save_path + '/final_report.txt', 'wb') as f:
        pickle.dump(file_tmp, f)
        
    with open(save_path +'/final_report.txt', 'rb') as lf:
        report = pickle.load(lf)

if __name__ == "__main__":
    main()
    generate_final_report()
