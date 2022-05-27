"""All environment based configs for the project"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setting environment constants
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
ENV = os.getenv('ENV', 'development')
