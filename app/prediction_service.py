"""
Fraud detection service containing the business logic.

This module implements the core fraud detection algorithm using
machine learning models to predict expected mileage and detect anomalies.
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, List
from app.models import CarInput, FraudCheckResponse
from app.model_loader import model_manager
from app.config import SUSPICIOUS_RATIO_THRESHOLD, MARKET_DIFF_THRESHOLD


class FraudDetectionService:
    """
    Service class for detecting odometer fraud in used cars.
    
    This service uses two machine learning models:
    1. Regression model: Predicts expected mileage based on car features
    2. Classification model: Detects fraud based on anomaly patterns
    """
    
    @staticmethod
    def calculate_expected_mileage(car: CarInput) -> int:
        """
        Calculate the expected mileage for a car using the regression model.
        
        The model uses features like year, price, horsepower, make, model,
        fuel type, gearbox, and calculated age to predict expected mileage.
        
        Args:
            car: CarInput object containing car details
            
        Returns:
            int: Expected mileage in kilometers
            
        Raises:
            ValueError: If prediction fails or returns invalid values
        """
        # Get the regression model
        reg_model = model_manager.get_regressor()
        
        # Calculate car age and age squared
        current_year = pd.Timestamp.now().year
        age = max(1, current_year - car.year)
        age_squared = age ** 2
        
        # Prepare input DataFrame with all required features
        # Feature order must match the training data
        reg_input = pd.DataFrame({
            'year': [car.year],
            'price': [car.price],
            'horsepower': [car.horsepower],
            'make': [car.make],
            'model': [car.model],
            'fuelType': [car.fuelType],
            'gearbox': [car.gearbox],
            'offerType': [car.offerType],
            'age': [age],
            'age_squared': [age_squared]
        })
        
        # Predict log-transformed mileage
        predicted_log = reg_model.predict(reg_input)[0]
        
        # Convert back to actual mileage using inverse log transformation
        expected_km = int(np.expm1(predicted_log))
        
        return expected_km
    
    @staticmethod
    def calculate_fraud_features(
        car: CarInput,
        expected_km: int,
        predicted_log: float
    ) -> pd.DataFrame:
        """
        Calculate fraud detection features for the classification model.
        
        These features capture the relationship between reported and
        expected mileage from multiple angles.
        
        Args:
            car: CarInput object containing car details
            expected_km: Expected mileage from regression model
            predicted_log: Log-transformed predicted mileage
            
        Returns:
            pd.DataFrame: Features for fraud classification
        """
        # Calculate car age
        current_year = pd.Timestamp.now().year
        age = max(1, current_year - car.year)
        
        # Calculate ratio: reported_km / expected_km
        # Low ratio indicates suspiciously low mileage
        smart_ratio = car.reported_km / max(1, expected_km)
        
        # Calculate absolute difference from market average
        # Large negative difference suggests rolled-back odometer
        market_km_diff = car.reported_km - expected_km
        
        # Calculate log difference
        # Captures the relative magnitude of discrepancy
        log_reported = math.log1p(car.reported_km)
        log_diff = log_reported - predicted_log
        
        # Create feature DataFrame for classification
        features = pd.DataFrame({
            'smart_ratio': [smart_ratio],
            'age': [age],
            'market_km_diff': [market_km_diff],
            'log_diff': [log_diff]
        })
        
        return features
    
    @staticmethod
    def generate_reasons(
        smart_ratio: float,
        market_km_diff: float,
        expected_km: int,
        is_suspicious: bool
    ) -> List[str]:
        """
        Generate human-readable explanations in Bosnian for fraud detection results.
        
        Args:
            smart_ratio: Ratio of reported to expected mileage
            market_km_diff: Difference from market average
            expected_km: Expected mileage value
            is_suspicious: Whether the car is flagged as suspicious
            
        Returns:
            List[str]: List of explanation strings in Bosnian
        """
        reasons = []
        
        # Check if mileage is significantly lower than expected
        if smart_ratio < SUSPICIOUS_RATIO_THRESHOLD:
            percentage = int(smart_ratio * 100)
            reasons.append(
                f"Kilometraža je sumnjiva: Samo {percentage}% od očekivanih {expected_km:,} km."
            )
        
        # Check if mileage is far below market average
        if market_km_diff < MARKET_DIFF_THRESHOLD:
            reasons.append(
                f"Automobil ima {abs(market_km_diff):,} km manje od sličnih oglasa na tržištu."
            )
        
        # If flagged but no specific reason, provide generic AI detection message
        if not reasons and is_suspicious:
            reasons.append(
                "Otkrivena složena anomalija od strane AI (kombinacija cijene, starosti i specifikacija)."
            )
        
        return reasons
    
    @staticmethod
    def check_fraud(car: CarInput) -> FraudCheckResponse:
        """
        Perform complete fraud detection analysis on a car.
        
        This is the main entry point for fraud detection. It:
        1. Predicts expected mileage using regression
        2. Calculates fraud detection features
        3. Uses classification model to detect anomalies
        4. Generates explanations
        
        Args:
            car: CarInput object with car details
            
        Returns:
            FraudCheckResponse: Complete fraud detection results
            
        Raises:
            ValueError: If models are not loaded or prediction fails
        """
        # Verify models are loaded
        if not model_manager.are_models_loaded():
            raise ValueError("Models are not loaded. Service is not ready.")
        
        # Get models
        reg_model = model_manager.get_regressor()
        class_model = model_manager.get_classifier()
        threshold = model_manager.get_threshold()
        
        # === STEP 1: Calculate Expected Mileage ===
        current_year = pd.Timestamp.now().year
        age = max(1, current_year - car.year)
        age_squared = age ** 2
        
        # Prepare regression input
        reg_input = pd.DataFrame({
            'year': [car.year],
            'price': [car.price],
            'horsepower': [car.horsepower],
            'make': [car.make],
            'model': [car.model],
            'fuelType': [car.fuelType],
            'gearbox': [car.gearbox],
            'offerType': [car.offerType],
            'age': [age],
            'age_squared': [age_squared]
        })
        
        # Predict expected mileage
        predicted_log = reg_model.predict(reg_input)[0]
        expected_km = int(np.expm1(predicted_log))
        
        # === STEP 2: Calculate Fraud Detection Features ===
        smart_ratio = car.reported_km / max(1, expected_km)
        market_km_diff = car.reported_km - expected_km
        log_reported = math.log1p(car.reported_km)
        log_diff = log_reported - predicted_log
        
        class_input = pd.DataFrame({
            'smart_ratio': [smart_ratio],
            'age': [age],
            'market_km_diff': [market_km_diff],
            'log_diff': [log_diff]
        })
        
        # === STEP 3: Detect Fraud Using Classification Model ===
        # Get fraud probability (0.0 to 1.0)
        fraud_prob = float(class_model.predict_proba(class_input)[0, 1])
        
        # Convert to percentage score (0 to 100)
        fraud_score = int(round(fraud_prob * 100))
        
        # Determine if suspicious based on threshold
        is_suspicious = fraud_prob >= threshold
        
        # === STEP 4: Generate Human-Readable Explanations ===
        reasons = FraudDetectionService.generate_reasons(
            smart_ratio=smart_ratio,
            market_km_diff=market_km_diff,
            expected_km=expected_km,
            is_suspicious=is_suspicious
        )
        
        # Return complete response
        return FraudCheckResponse(
            fraud_score=fraud_score,
            is_suspicious=is_suspicious,
            expected_km=expected_km,
            reasons=reasons
        )


# Global service instance
fraud_service = FraudDetectionService()
