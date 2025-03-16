import logging.config

import click
from dotenv import load_dotenv

from infrastructure.ui.api import app as fastapi_app
from infrastructure.ui.web import app as gradio_app
from infrastructure.config import (
    LOGGING_CONFIG,
    GRADIO_LOGGING_CONFIG,
    FASTAPI_LOGGING_CONFIG
)


@click.command()
@click.option('--app', help="Реализация приложения")
def main(app: str):
    match app:
        case 'fastapi':
            logging.config.dictConfig(FASTAPI_LOGGING_CONFIG)
            logger = logging.getLogger(__name__)
            logger.info(f"Старт приложения {app}!")
            fastapi_app.main()
            logger.info(f"Завершение приложения {app}!")
        case 'gradio':
            logging.config.dictConfig(GRADIO_LOGGING_CONFIG)
            logger = logging.getLogger(__name__)
            logger.info(f"Старт приложения {app}!")
            gradio_app.main()
            logger.info(f"Завершение приложения {app}!")
        case _:
            logging.config.dictConfig(LOGGING_CONFIG)
            logger = logging.getLogger(__name__)
            logger.info(f"Нет реализации приложения {app}!")


if __name__ == '__main__':
    load_dotenv(".env")
    main()
