"""
Mileage Fraud Detection API - Main Application Module

This FastAPI application provides endpoints for detecting potential odometer fraud
in used cars using machine learning. It uses two models:
1. A regression model to predict expected mileage
2. A classification model to detect fraud patterns

Author: Zoran Janjic
Repository: https://github.com/Zoran-Janjic/truemeter-api
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import configuration
from app.config import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    CREATOR_NAME,
    CREATOR_WEBSITE,
    DATASET_SOURCE,
    CORS_ORIGINS,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOW_METHODS,
    CORS_ALLOW_HEADERS
)

# Import data models
from app.models import CarInput, FraudCheckResponse, HealthCheckResponse

# Import model manager and service
from app.model_loader import model_manager
from app.prediction_service import fraud_service


# ==========================================
# LIFESPAN EVENT HANDLER
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown events.
    
    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown").
    The code before yield runs at startup, and code after yield runs at shutdown.
    """
    # Startup: Load machine learning models
    success, message = model_manager.load_models()
    if not success:
        print(f"⚠️  Warning: Application started but models failed to load: {message}")
    
    yield  # Application is running
    
    # Shutdown: Cleanup if needed (currently nothing to clean up)
    print("🔴 Application shutting down...")


# ==========================================
# APPLICATION INITIALIZATION
# ==========================================

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ==========================================
# CORS MIDDLEWARE CONFIGURATION
# ==========================================
# Enable Cross-Origin Resource Sharing (CORS) to allow frontend applications
# from different domains to access this API

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)


# ==========================================
# HEALTH CHECK ENDPOINT
# ==========================================

@app.get("/", response_model=HealthCheckResponse, tags=["Health"])
@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify API status.
    
    Returns the current status of the service and whether the ML models
    are successfully loaded and ready to make predictions.
    
    Returns:
        HealthCheckResponse: Service status information
        
    Example:
        GET http://localhost:8000/health
        
        Response:
        {
            "status": "healthy",
            "models_loaded": true,
            "service": "API za detekciju prevare s kilometražom",
            "creator": "Zoran Janjic",
            "website": "https://www.linkedin.com/in/janjiczoran/",
            "dataset": "autoscout24-germany-dataset.csv"
        }
    """
    models_loaded = model_manager.are_models_loaded()
    
    return HealthCheckResponse(
        status="healthy" if models_loaded else "initializing",
        models_loaded=models_loaded,
        service=API_TITLE,
        creator=CREATOR_NAME,
        website=CREATOR_WEBSITE,
        dataset=DATASET_SOURCE
    )


# ==========================================
# FRAUD DETECTION ENDPOINT
# ==========================================

@app.post("/api/check", response_model=FraudCheckResponse, tags=["Fraud Detection"])
async def check_car(car: CarInput) -> FraudCheckResponse:
    """
    Check a car for potential odometer fraud.
    
    This endpoint analyzes car details and returns a fraud score along with
    the expected mileage and explanations in Bosnian.
    
    Args:
        car: CarInput object containing car details (make, model, year, mileage, etc.)
        
    Returns:
        FraudCheckResponse: Fraud detection results including:
            - fraud_score: Fraud probability (0-100)
            - is_suspicious: Boolean flag
            - expected_km: Expected mileage for this car
            - reasons: List of explanations in Bosnian
            
    Raises:
        HTTPException 503: If models are not loaded
        HTTPException 400: If prediction fails
        
    Example:
        POST http://localhost:8000/api/check
        
        Request Body:
        {
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
        
        Response:
        {
            "fraud_score": 15,
            "is_suspicious": false,
            "expected_km": 95000,
            "reasons": []
        }
    """
    # Verify that models are loaded and ready
    if not model_manager.are_models_loaded():
        raise HTTPException(
            status_code=503,
            detail="Models are not loaded yet. Service is initializing. Please try again in a moment."
        )
    
    # Perform fraud detection
    try:
        result = fraud_service.check_fraud(car)
        return result
        
    except ValueError as e:
        # Handle validation or model errors
        raise HTTPException(
            status_code=400,
            detail=f"Prediction error: {str(e)}"
        )
        
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )