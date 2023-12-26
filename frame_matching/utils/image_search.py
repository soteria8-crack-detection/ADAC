import numpy as np

class ImageSearch:
    """
    A class for performing image search based on query and search features.

    Parameters:
        - query_index_dict (dict): Dictionary containing query features.
        - search_index_dict (dict): Dictionary containing search features.

    Methods:
        - __init__(query_index_dict, search_index_dict): Initializes the ImageSearch class.
        - euclidean(a, b): Calculates the Euclidean distance between two vectors.
        - perform_search(queryFeatures, search_index_dict, maxResults): Performs search based on query features and search index.
        - get_match_result(): Gets matching results based on query and search features.

    Example:
        searcher = ImageSearch(query_index_dict={'features': query_features},
                               search_index_dict={'features': search_features})
        results = searcher.get_match_result()
    """
    
    def __init__(self, query_index_dict, search_index_dict):
        """
        Initialize the ImageSearch class.
        
        Args:
        - query_index_dict (dict): Dictionary containing query features
        - search_index_dict (dict): Dictionary containing search features
        """
        self.query_index_dict = query_index_dict
        self.search_index_dict = search_index_dict   

    def euclidean(self, a, b):
        """
        Calculate the Euclidean distance between two vectors a and b.
        
        Args:
        - a (numpy.ndarray): First vector
        - b (numpy.ndarray): Second vector
        
        Returns:
        - float: Euclidean distance between vectors a and b
        """
        return np.linalg.norm(a - b)
           
    def perform_search(self, queryFeatures, search_index_dict, maxResults):
        """
        Perform search based on query features and search index dictionary.
        
        Args:
        - queryFeatures (numpy.ndarray): Query features for searching
        - search_index_dict (dict): Dictionary containing search index
        
        Returns:
        - list: List of matching results
        """
        results = []
        for i in range(0, len(search_index_dict["features"])):
            d = self.euclidean(queryFeatures, search_index_dict["features"][i])
            results.append([d, i])
        results = sorted(results)[:maxResults]
        return results
    
    def get_match_result(self):
        """
        Get matching results based on query and search features.
        
        Returns:
        - list: Matching results
        """
        matching_result = []
        for i in range(len(self.query_index_dict['features'])):
            MAX_RESULTS = 1
            queryIdx = i
            queryFeatures = self.query_index_dict['features'][queryIdx]
            results = self.perform_search(queryFeatures, self.search_index_dict, maxResults=MAX_RESULTS)
            matching_result += results
        return matching_result
