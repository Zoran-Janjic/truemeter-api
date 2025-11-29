"""
Configuration module for the Mileage Fraud Detection API.

This module contains all configuration constants, paths, and settings
used throughout the application.
"""

import os

# ==========================================
# DIRECTORY PATHS
# ==========================================

# Base directory of the application (parent of 'app' folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the models directory
MODELS_DIR = os.path.join(BASE_DIR, "models")

# ==========================================
# MODEL PATHS
# ==========================================

# Path to the regression model (predicts expected mileage)
REGRESSOR_PATH = os.path.join(MODELS_DIR, "mileage_regressor_v2.joblib")

# Path to the classification model (detects fraud)
CLASSIFIER_PATH = os.path.join(MODELS_DIR, "fraud_classifier_xgb_v1.joblib")

# ==========================================
# API SETTINGS
# ==========================================

# API title displayed in documentation
API_TITLE = "API za detekciju prevare s kilometražom"

# API description
API_DESCRIPTION = "Detektira potencijalnu prevaru s kilometražom u polovnim automobilima koristeći AI modele."

# API version
API_VERSION = "1.0.0"

CREATOR_NAME = "Zoran Janjic"
CREATOR_WEBSITE = "https://www.linkedin.com/in/janjiczoran/"
DATASET_SOURCE = "autoscout24-germany-dataset.csv"

# ==========================================
# CORS SETTINGS
# ==========================================

# Allowed origins for CORS (use ["*"] for development, specify domains in production)
CORS_ORIGINS = ["*"]

# Allow credentials in CORS requests
CORS_ALLOW_CREDENTIALS = True

# Allowed HTTP methods
CORS_ALLOW_METHODS = ["*"]

# Allowed HTTP headers
CORS_ALLOW_HEADERS = ["*"]

# ==========================================
# FRAUD DETECTION THRESHOLDS
# ==========================================

# Default fraud probability threshold (0.0 - 1.0)
# If fraud_probability >= threshold, the car is flagged as suspicious
DEFAULT_FRAUD_THRESHOLD = 0.5

# Threshold for smart_ratio (reported_km / expected_km)
# If ratio < this value, the mileage is considered suspiciously low
SUSPICIOUS_RATIO_THRESHOLD = 0.70

# Threshold for market_km_diff (reported_km - expected_km)
# If difference < this value, it's significantly below market average
MARKET_DIFF_THRESHOLD = -30000
