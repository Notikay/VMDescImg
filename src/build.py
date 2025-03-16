import time
import logging.config

from transformers import (
    BlipForConditionalGeneration,
    BlipProcessor,
    # Blip2ForConditionalGeneration,
    # Blip2Processor
)

from infrastructure.config import (
    BLIP_MODEL_NAME,
    # BLIP2_MODEL_NAME,
    CAP_MODEL_SETTINGS
)
from infrastructure.config import LOGGING_CONFIG


def download_blip_processor():
    processor = BlipProcessor.from_pretrained(
        CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['download_path'],
        cache_dir=CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['cache_dir']
    )
    processor.save_pretrained(CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['save_dir'])


def download_blip_model():
    model = BlipForConditionalGeneration.from_pretrained(
        CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['download_path'],
        cache_dir=CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['cache_dir']
    )
    model.save_pretrained(CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['save_dir'])


# def download_blip2_processor():
#     processor = Blip2Processor.from_pretrained(
#         CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['download_path'],
#         cache_dir=CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['cache_dir']
#     )
#     time.sleep(10)
#     processor.save_pretrained(CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['save_dir'])
#
#
# def download_blip2_model():
#     model = Blip2ForConditionalGeneration.from_pretrained(
#         CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['download_path'],
#         cache_dir=CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['cache_dir']
#     )
#     time.sleep(10)
#     model.save_pretrained(CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['save_dir'])


if __name__ == '__main__':
    # TODO: Доделать корректную загрузку моделей.

    # Бред, но пока так
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)

    logger.info("Загрузка моделей...")

    download_blip_processor()
    logger.debug("Загрузка BLIP процессора модели прошла успешно!")

    time.sleep(10)

    download_blip_model()
    logger.debug("Загрузка BLIP модели прошла успешно!")

    # download_blip2_processor()
    # logger.debug("Загрузка BLIP2 процессора модели прошла успешно!")

    # time.sleep(10)

    # download_blip2_model()
    # logger.debug("Загрузка BLIP2 модели прошла успешно!")

    logger.info("Загрузка моделей завершена!")


