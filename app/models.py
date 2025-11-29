"""
Pydantic models for request and response data validation.

This module defines the data structures used for API requests and responses,
ensuring type safety and automatic validation.
"""

from pydantic import BaseModel, Field
from typing import List


class CarInput(BaseModel):
    """
    Request model for car fraud detection.
    
    Attributes:
        make: Car manufacturer (e.g., "BMW", "Volkswagen")
        model: Car model name (e.g., "Golf", "320")
        year: Manufacturing year
        reported_km: Odometer reading in kilometers
        fuelType: Fuel type ("Diesel", "Petrol", "Electric", etc.)
        gearbox: Transmission type ("Manual", "Automatic")
        horsepower: Engine power in horsepower
        price: Listing price in local currency
        offerType: Type of offer ("Used", "New")
    """
    make: str = Field(..., description="Car manufacturer")
    model: str = Field(..., description="Car model name")
    year: int = Field(..., ge=1900, le=2100, description="Manufacturing year")
    reported_km: int = Field(..., ge=0, description="Reported mileage in kilometers")
    fuelType: str = Field(..., description="Type of fuel")
    gearbox: str = Field(..., description="Transmission type")
    horsepower: int = Field(..., ge=0, description="Engine power in HP")
    price: int = Field(..., ge=0, description="Listing price")
    offerType: str = Field(default="Used", description="Offer type")

    class Config:
        """Configuration for the model"""
        json_schema_extra = {
            "example": {
                "make": "Volkswagen",
                "model": "Golf",
                "year": 2019,
                "reported_km": 92000,
                "fuelType": "Diesel",
                "gearbox": "Manual",
                "horsepower": 115,
                "price": 14500,
                "offerType": "Used"
            }
        }


class FraudCheckResponse(BaseModel):
    """
    Response model for fraud detection results.
    
    Attributes:
        fraud_score: Fraud probability as percentage (0-100)
        is_suspicious: Boolean flag indicating if the car is suspicious
        expected_km: Expected mileage based on similar cars
        reasons: List of explanations in Bosnian for why the car is flagged
    """
    fraud_score: int = Field(..., ge=0, le=100, description="Fraud probability (0-100)")
    is_suspicious: bool = Field(..., description="Whether the car is flagged as suspicious")
    expected_km: int = Field(..., ge=0, description="Expected mileage for this car")
    reasons: List[str] = Field(..., description="List of reasons in Bosnian")

    class Config:
        """Configuration for the model"""
        json_schema_extra = {
            "example": {
                "fraud_score": 85,
                "is_suspicious": True,
                "expected_km": 150000,
                "reasons": [
                    "Kilometraža je sumnjiva: Samo 48% od očekivanih 150,000 km."
                ]
            }
        }


class HealthCheckResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    Attributes:
        status: Service status ("healthy" or "initializing")
        models_loaded: Whether ML models are successfully loaded
        service: Service name
        creator: Creator name
        website: Creator website URL
        dataset: Dataset source used for training
    """
    status: str = Field(..., description="Service status")
    models_loaded: bool = Field(..., description="Whether models are loaded")
    service: str = Field(..., description="Service name")
    creator: str = Field(..., description="Creator name")
    website: str = Field(..., description="Creator website")
    dataset: str = Field(..., description="Dataset source")

    class Config:
        """Configuration for the model"""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "models_loaded": True,
                "service": "API za detekciju prevare s kilometražom",
                "creator": "Zoran Janjic",
                "website": "https://www.linkedin.com/in/janjiczoran/",
                "dataset": "autoscout24-germany-dataset.csv"
            }
        }
