import os
import gc
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path

import torch
from utils.customdataset import CustomDataset
from torch.utils.data import DataLoader

from efficientnet_pytorch import EfficientNet

class LatentFeaturesDict:
    """
    A class for extracting and managing latent features of images using EfficientNet.

    Parameters:
        - path (str): Path to image files.
        - batch_size (int): Batch size for the data loader.
        - input_list (str, optional): Path to the image list file (default: None).

    Methods:
        - __init__(path, batch_size, input_list=None): Initializes the LatentFeaturesDict class.
        - make_dataframe(): Converts image files to a DataFrame.
        - make_dataloader(): Creates a data loader using the DataFrame.
        - get_latent_features(): Extracts latent features of images.
        - make_feature_dictionary(): Generates a feature dictionary containing latent features.

    Example:
        features_dict = LatentFeaturesDict(path='images_folder', batch_size=32, input_list='image_list.pkl')
        feature_dictionary = features_dict.make_feature_dictionary()
    """
    
    def __init__(self, path, batch_size, input_list=None):
        """
        Initializes the LatentFeaturesDict class.
        
        Args:
        - path (str): Path to image files
        - batch_size (int): Batch size for the data loader
        - input_list (str, optional): Path to the image list file (default: None)
        """
        self.path = path
        self.batch_size = batch_size
        self.model = EfficientNet.from_pretrained('efficientnet-b4')
        self.model = self.model.eval()
        self.device = torch.device("cuda")
        self.model = self.model.to(self.device)
        self.input_list = input_list
    
    def make_dataframe(self):
        """
        Convert image files to a DataFrame.
        
        Returns:
        - pandas.DataFrame: DataFrame containing information about image files
        """
        df = pd.DataFrame()
        if self.input_list: # If a query list exists
            query_list = []
            with open(self.input_list, 'rb') as f:
                file = pickle.load(f)
                for i in file:
                    query_list.append(i.strip())
            df['image'] = [f for f in query_list]
            df['image'] = self.path + '/' + df['image'].astype(str) + '.jpg'
        else:   
            df['image'] = [f for f in os.listdir(Path(self.path))]
            df['image'] = self.path + '/' + df['image'].astype(str)
        return df
    
    def make_dataloader(self):
        """
        Create a data loader using the DataFrame.
        
        Returns:
        - torch.utils.data.DataLoader: Image data loader
        """
        df = self.make_dataframe()
        dataset = CustomDataset(dataFrame=df)
        dataloader = DataLoader(dataset=dataset, batch_size=self.batch_size, shuffle=False)
        return dataloader
    
    def get_latent_features(self):
        """
        Extract latent features of images.
        
        Returns:
        - numpy.ndarray: Vector of latent features of images
        """
        df = self.make_dataframe()
        dataloader = self.make_dataloader()
        
        images = df.image.values
        latent_features = np.zeros((len(df), 1792))
        
        for i, image in enumerate(tqdm(dataloader)):
            features = self.model.extract_features(image.to(self.device))
            feature_vec = torch.nn.AdaptiveAvgPool2d(1)(features).cpu().view(-1, 1792).detach().numpy()
            latent_features[i * self.batch_size:(i+1) * self.batch_size] = feature_vec
        
        del feature_vec
        gc.collect()
        return latent_features
    
    def make_feature_dictionary(self):
        """
        Generate a feature dictionary containing latent features.
        
        Returns:
        - dict: Dictionary containing image features
        """
        df = self.make_dataframe()
        latent_features = self.get_latent_features()
        
        indexes = list(range(0, len(df)))
        images_path = df.image.values
        images_names = [f for f in os.listdir(Path(self.path))]
        feature_dict = {'indexes': indexes, 'name': images_names, 'path': images_path, 'features': latent_features}
        
        return feature_dict
