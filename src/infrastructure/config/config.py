import yaml
import os
from pathlib import Path
from copy import deepcopy


with open('./config.yml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Параметры изображений.
PATH_TO_IMG_DIR = Path(config['images']['path_to_dir'])

# Параметры captioning-моделей.
BLIP_MODEL_NAME = config['cap_model']['blip_name']
# BLIP2_MODEL_NAME = config['cap_model']['blip2_name']
CAP_MODEL_SETTINGS = {
    BLIP_MODEL_NAME: {
        'download_path': config['cap_model']['download_blip_path'],
        'save_dir': config['cap_model']['save_blip_dir'],
        'cache_dir': config['cap_model']['cache_blip_dir']
    },
    # BLIP2_MODEL_NAME: {
    #     'download_path': config['cap_model']['download_blip2_path'],
    #     'save_dir': config['cap_model']['save_blip2_dir'],
    #     'cache_dir': config['cap_model']['cache_blip2_dir']
    # }
}

MAX_LENGTH_DESCRIPTION = config['cap_model']['max_length']
MIN_LENGTH_DESCRIPTION = config['cap_model']['min_length']
DEFAULT_LENGTH_DESCRIPTION = config['cap_model']['default_length']
STEP_LENGTH_DESCRIPTION = config['cap_model']['step_length']

# Параметры переводчиков.
APPTRANS_TRANS_NAME = config['translator']['apptrans_name']
GOOGLE_TRANS_NAME = config['translator']['google_name']
TRANS_MODEL_SETTINGS = {
    APPTRANS_TRANS_NAME: {'lang': config['translator']['lang']},
    GOOGLE_TRANS_NAME: {'lang': config['translator']['lang']}
}

# Параметры логов.
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": config['logs']['level_to_console'],
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": config['logs']['level_to_file'],
            "formatter": "standard",
            "filename": str(Path(
                config['logs']['path_to_dir'],
                config['logs']['filename']
            )),
            "maxBytes": config['logs']['max_bytes'],
            "backupCount": config['logs']['backup_count'],
            "encoding": "utf-8",
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console", "file"]
        }
    }
}

# Параметры реализации на Gradio
GRADIO_LOGS_PATH = str(Path(
    config['logs']['path_to_dir'],
    config['logs']['gradio_folder'],
    config['logs']['filename']
))
GRADIO_LOGGING_CONFIG = deepcopy(LOGGING_CONFIG)
GRADIO_LOGGING_CONFIG['handlers']['file']['filename'] = GRADIO_LOGS_PATH

GRADIO_CAP_MODEL_NAME_MAP = {
    "BLIP": BLIP_MODEL_NAME,
    # "BLIP2": BLIP2_MODEL_NAME
}
GRADIO_TRANS_NAME_MAP = {
    "Без перевода": None,
    "App Translator": APPTRANS_TRANS_NAME,
    "Google Translate (работает через раз)": GOOGLE_TRANS_NAME
}


# Параметры реализации на FastAPI
FASTAPI_LOGS_PATH = str(Path(
    config['logs']['path_to_dir'],
    config['logs']['fastapi_folder'],
    config['logs']['filename']
))
FASTAPI_LOGGING_CONFIG = deepcopy(LOGGING_CONFIG)
FASTAPI_LOGGING_CONFIG['handlers']['file']['filename'] = FASTAPI_LOGS_PATH

# Параметры Базы данных.
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Хосты и порты.
GRADIO_HOST = os.getenv("GRADIO_HOST", "0.0.0.0")
GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))

FASTAPI_HOST = os.getenv("FASTAPI_HOST", "0.0.0.0")
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 8000))

# Создание папок.
os.makedirs(PATH_TO_IMG_DIR, exist_ok=True)
os.makedirs(CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['save_dir'], exist_ok=True)
os.makedirs(CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['cache_dir'], exist_ok=True)
# os.makedirs(CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['save_dir'], exist_ok=True)
# os.makedirs(CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['cache_dir'], exist_ok=True)
os.makedirs(
    Path(config['logs']['path_to_dir'], config['logs']['gradio_folder']),
    exist_ok=True
)
os.makedirs(
    Path(config['logs']['path_to_dir'],
         config['logs']['fastapi_folder']),
    exist_ok=True
)
