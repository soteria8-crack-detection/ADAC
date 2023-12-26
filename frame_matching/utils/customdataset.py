from PIL import Image

from torch.utils.data.dataset import Dataset
from torchvision import transforms

class CustomDataset(Dataset):
    """
    Custom Dataset class for image processing.

    Attributes:
    - dataFrame (pandas.DataFrame): DataFrame containing image paths
    - transformations (torchvision.transforms.Compose): Composed image transformations

    Methods:
    - __init__(dataFrame): Initializes the CustomDataset.
    - __getitem__(idx): Gets an item (image) from the dataset by index.
    - __len__(): Gets the length of the dataset.
    """
    
    def __init__(self, dataFrame):
        """
        Initializes the CustomDataset.

        Parameters:
        - dataFrame (pandas.DataFrame): DataFrame containing image paths
        """
        self.dataFrame = dataFrame
        self.transformations = transforms.Compose([
            transforms.Resize((380, 380)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        ])

    def __getitem__(self, idx):
        """
        Get an item (image) from the dataset by index.
        
        Args:
        - idx (int): Index of the item
        
        Returns:
        - torch.Tensor: Transformed image tensor
        """
        image_path = self.dataFrame['image'][idx]
        image = Image.open(image_path)
        image = self.transformations(image)
        return image

    def __len__(self):
        """
        Get the length of the dataset.
        
        Returns:
        - int: Length of the dataset
        """
        return len(self.dataFrame.index)
