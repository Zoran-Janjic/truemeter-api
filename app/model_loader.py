"""
Machine Learning model loader and manager.

This module handles loading and storing the ML models used for
mileage prediction and fraud detection.
"""

import joblib
from typing import Optional, Tuple, Any
from app.config import REGRESSOR_PATH, CLASSIFIER_PATH, DEFAULT_FRAUD_THRESHOLD


class ModelManager:
    """
    Manages the loading and storage of machine learning models.
    
    This class implements a singleton pattern to ensure models are loaded
    only once and shared across the application.
    """
    
    def __init__(self):
        """Initialize the ModelManager with empty model slots."""
        self.regressor_model: Optional[Any] = None
        self.classifier_model: Optional[Any] = None
        self.fraud_threshold: float = DEFAULT_FRAUD_THRESHOLD
    
    def load_models(self) -> Tuple[bool, str]:
        """
        Load the regression and classification models from disk.
        
        The regression model predicts expected mileage based on car features.
        The classification model detects potential odometer fraud.
        
        Returns:
            Tuple[bool, str]: (success_status, message)
                - success_status: True if models loaded successfully
                - message: Success or error message
        """
        try:
            # Load the regression model (predicts expected mileage)
            print(f"Loading regression model from: {REGRESSOR_PATH}")
            self.regressor_model = joblib.load(REGRESSOR_PATH)
            
            # Load the classification model (detects fraud)
            print(f"Loading classification model from: {CLASSIFIER_PATH}")
            classifier_dict = joblib.load(CLASSIFIER_PATH)
            
            # Extract the pipeline and threshold from the classifier dictionary
            self.classifier_model = classifier_dict['pipeline']
            self.fraud_threshold = classifier_dict.get('threshold', DEFAULT_FRAUD_THRESHOLD)
            
            success_msg = f"✅ Models loaded successfully! Threshold: {self.fraud_threshold}"
            print(success_msg)
            return True, success_msg
            
        except FileNotFoundError as e:
            error_msg = f"❌ Model file not found: {e}"
            print(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"❌ Error loading models: {e}"
            print(error_msg)
            return False, error_msg
    
    def are_models_loaded(self) -> bool:
        """
        Check if both models are loaded and ready for predictions.
        
        Returns:
            bool: True if both models are loaded, False otherwise
        """
        return (
            self.regressor_model is not None and 
            self.classifier_model is not None
        )
    
    def get_regressor(self) -> Optional[Any]:
        """
        Get the regression model.
        
        Returns:
            The regression model or None if not loaded
        """
        return self.regressor_model
    
    def get_classifier(self) -> Optional[Any]:
        """
        Get the classification model.
        
        Returns:
            The classification model or None if not loaded
        """
        return self.classifier_model
    
    def get_threshold(self) -> float:
        """
        Get the fraud detection threshold.
        
        Returns:
            float: The threshold value (0.0 - 1.0)
        """
        return self.fraud_threshold


# Global singleton instance
model_manager = ModelManager()
