# app/services/registry.py
import logging
from app.services.user_service import UserService
from app.services.product_service import ProductService

# Set up a logger for this module
logger = logging.getLogger(__name__)

# Service registry mapping model names to service classes
SERVICES = {
    "User": UserService,
    "Product": ProductService,
    # add additional models as needed
}


def get_service_for_model(model_name):
    logger.debug("Retrieving service for model: %s", model_name)
    service = SERVICES.get(model_name)
    if service is None:
        logger.warning("No service found for model: %s", model_name)
    else:
        logger.info("Service found for model %s: %s", model_name, service.__name__)
    return service
