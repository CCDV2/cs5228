from abc import abstractmethod
from typing import Any, Tuple

class BaseModel:
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def predict(self, train_dataloader, test_dataloader) -> Tuple[Any, Any]:
        """
        Specified for task 1, return (pred, ground_truth) on test set.
        """
        pass


    @abstractmethod
    def recommend(self, *args, **kwargs):
        """
        Specified for task 2, still TODO
        """
        pass
    
