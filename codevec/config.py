from configparser import ConfigParser
import os

config = ConfigParser()

# Create config file with defaults if it doesn't exist
if not os.path.exists('config.ini'):
    config['embeddings'] = {
        'model': 'local',
        'api_key': ''
    }
    config['reranking'] = {
        'rerank': 'True'
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read('config.ini')

def get_model_type() -> str:
    """Get the configured model type."""
    return config['embeddings']['model']

def get_api_key() -> str:
    """Get API key from environment variable or config file."""
    return os.getenv("codevec_api_key") or config['embeddings']['api_key']

def get_reranking() -> bool:
    """Get reranking status"""
    return config.getboolean('reranking', 'rerank', fallback=True)

def configure_model(model_name):
    """Write model name to config file"""
    config['embeddings']['model'] = model_name
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def configure_api_key(api_key):
    """Write API key to config file"""
    config['embeddings']['api_key'] = api_key
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def configure_reranking(bool):
    """Write reranking boolean to config file"""
    config['reranking']['rerank'] = bool
    with open('config.ini', 'w') as configfile:
        config.write(configfile)