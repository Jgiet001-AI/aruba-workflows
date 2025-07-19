"""
HPE Aruba Network Automation Suite

A comprehensive toolkit for automating HPE Aruba network infrastructure
using n8n workflows, API integrations, and monitoring systems.
"""

__version__ = "1.0.0"
__author__ = "HPE Aruba Automation Team"

from .api_client import ArubaAPIClient
from .workflow_manager import WorkflowManager
from .data_extractor import PostmanDataExtractor, EndpointCategorizer

__all__ = [
    "ArubaAPIClient",
    "WorkflowManager", 
    "PostmanDataExtractor",
    "EndpointCategorizer"
]