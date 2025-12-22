from configparser import ConfigParser
import os

from embeddings import GeminiEmbedder, LocalEmbedder

config = ConfigParser()

# Create config file with defaults if it doesn't exist
if not os.path.exists('config.ini'):
    config['embeddings'] = {
        'model': 'local',
        'api_key': ''
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read('config.ini')

def set_model():
    model = config['embeddings']['model']
    if model == "local":
        return LocalEmbedder()
    elif model == "gemini":
        return GeminiEmbedder(api_key=get_key())
    else:
        raise ValueError(f"Unknown model type: {model}") 

def get_key(): 
    if key := os.getenv("codevec_api_key"):
        return key
    else:
        return config['embeddings']['api_key']

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