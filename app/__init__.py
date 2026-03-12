"""
Trinetra Agro AI - Application Package
Vision Beyond the Fields 🔱
"""

__version__ = "1.0.0"
__author__ = "Kartikeya Podicheti"
__email__ = "your-email@example.com"
__description__ = "AI-powered agricultural intelligence chatbot"

# Import main modules for easy access
from .chatbot.core_bot import TrinetraBot
from .utils.config import Config, load_config
from .utils.helpers import setup_logging

# Initialize logging when package is imported
setup_logging()

__all__ = [
    'TrinetraBot',
    'Config',
    'load_config',
    'setup_logging'
]