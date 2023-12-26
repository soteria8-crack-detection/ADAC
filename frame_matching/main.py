import os
import pickle
import natsort
import pandas as pd

from utils.image_search import ImageSearch
from utils.latent_features import LatentFeaturesDict

class Main:
    """
    Main class for matching frames using latent features.

    Parameters:
        - query_path (str): Path to the query frames.
        - query_input_list (str): Path to the query input list.
        - search_path (str): Path to the search frames.
        - file_name (str): Name of the file to save the matching results.

    Methods:
        - main(): Main method for performing frame matching and saving the results to a text file.

    Example:
        main_instance = Main(query_path='./dataset/image_extraction/video_01',
                             query_input_list='./dataset/result_txt/_label_info.txt',
                             search_path='./dataset/image_extraction/video_02',
                             file_name='./dataset/result_txt/_pair_info.txt')
        main_instance.main()
    """
    
    def __init__(self, query_path, query_input_list, search_path, file_name):
        """
        Initializes the Main class.

        Parameters:
            - query_path (str): Path to the query frames.
            - query_input_list (str): Path to the query input list.
            - search_path (str): Path to the search frames.
            - file_name (str): Name of the file to save the matching results.
        """
        self.query_path = query_path
        self.query_input_list = query_input_list
        self.search_path = search_path
        self.file_name = file_name
        
    def runner(self):
        """
        Main method for performing frame matching and saving the results to a text file.
        """
        query_features = LatentFeaturesDict(path=self.query_path, batch_size=4, input_list=self.query_input_list)
        query_feature_dictionary = query_features.make_feature_dictionary()
        
        search_features = LatentFeaturesDict(path=self.search_path, batch_size=4, input_list=None)
        search_feature_dictionary = search_features.make_feature_dictionary()
        
        image_search = ImageSearch(query_feature_dictionary, search_feature_dictionary)
        matching_result = image_search.get_match_result()
        
        temp = pd.DataFrame()
        query_= []
        search_ = []

        for idx, result in enumerate(matching_result):
            _, j = result 
            query_.append(query_feature_dictionary['name'][idx][:-4])
            search_.append(search_feature_dictionary['name'][j])
            
        temp['origin_frame'] =  query_
        temp['matching_frame'] = search_

        temp_dict = dict(zip(query_,search_,))
        sorted_keys = natsort.natsorted(temp_dict.keys())
        sorted_temp = {key: temp_dict[key] for key in sorted_keys}
        temp_df = pd.DataFrame(sorted_temp.items(), columns=['origin_frame', 'matching_frame'])

        matching_frame_list = temp_df['matching_frame'].tolist()
        with open(self.file_name, 'wb') as file:
            pickle.dump(matching_frame_list, file)

def main():
    PATH = os.getcwd()
    
    query_path = os.path.join(PATH, 'dataset/image_extraction/video_01')
    query_input_list = os.path.join(PATH, 'dataset/result_txt', '_image_info.txt')
    search_path = os.path.join(PATH, 'dataset/image_extraction/video_02')
    file_name = os.path.join(PATH, 'dataset/result_txt', '_pair_info.txt')

    runner = Main(query_path, query_input_list, search_path, file_name)
    runner.runner()
    
    
if __name__ == "__main__":
    main()
    