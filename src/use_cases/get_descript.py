from enum import Enum
from typing import TYPE_CHECKING

from transformers import (
    BlipForConditionalGeneration,
    BlipProcessor,
    # Blip2ForConditionalGeneration,
    # Blip2Processor
)
from googletrans import Translator as GTranslator
from googletrans.constants import LANGUAGES
from translate import Translator

from entities.cap_model_director import CapModelDirector
from entities.cap_models import BLIPCapModelBuilder
from entities.translators import GoogleTranslator, AppTranslator
from use_cases.base import AbstractUseCase
from infrastructure.config import (
    BLIP_MODEL_NAME,
    # BLIP2_MODEL_NAME,
    CAP_MODEL_SETTINGS,
    TRANS_MODEL_SETTINGS,
    APPTRANS_TRANS_NAME,
    GOOGLE_TRANS_NAME
)

if TYPE_CHECKING:
    from uuid import UUID

    from entities import AbstractCapModelDirector
    from infrastructure.db import (
        AbstractImageRepository,
        AbstractDescriptionRepository
    )


class BuilderNameEnum(Enum):
    BLIP_DIR: 'AbstractCapModelDirector' = CapModelDirector(
        BLIPCapModelBuilder(
            model=BlipForConditionalGeneration,
            processor=BlipProcessor,
            download_path=CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['save_dir'],
            cache_dir=CAP_MODEL_SETTINGS[BLIP_MODEL_NAME]['cache_dir']
        )
    )
    # BLIP2_DIR: 'AbstractCapModelDirector' = CapModelDirector(
    #     BLIPCapModelBuilder(
    #         model=Blip2ForConditionalGeneration,
    #         processor=Blip2Processor,
    #         download_path=CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['save_dir'],
    #         cache_dir=CAP_MODEL_SETTINGS[BLIP2_MODEL_NAME]['cache_dir']
    #     )
    # )


class TranslatorNameEnum(Enum):
    APPTRANS = AppTranslator(
        Translator(
            to_lang=TRANS_MODEL_SETTINGS[APPTRANS_TRANS_NAME]['lang'],
            provider='mymemory'
        ),
        support_langs=[
            'af', 'sq', 'am', 'ar', 'hy', 'az', 'bjs',
            'rm', 'eu', 'bem', 'bn', 'be', 'bi', 'bs',
            'br', 'bg', 'my', 'ca', 'ceb', 'ch', 'zh',
            'zh', 'zdj', 'cop', 'aig', 'bah', 'gcl',
            'gyn', 'jam', 'svc', 'vic', 'ht', 'acf',
            'crs', 'pov', 'hr', 'cs', 'da', 'nl', 'dz',
            'en', 'eo', 'et', 'fn', 'fo', 'fi', 'fr',
            'gl', 'ka', 'de', 'el', 'grc', 'gu', 'ha',
            'haw', 'he', 'hi', 'hu', 'is', 'id', 'kl',
            'ga', 'it', 'ja', 'jv', 'kea', 'kab', 'kn',
            'kk', 'km', 'rw', 'rn', 'ko', 'ku', 'ckb',
            'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk',
            'mg', 'ms', 'dv', 'mt', 'gv', 'mi', 'mh',
            'men', 'mn', 'mfe', 'ne', 'niu', 'no', 'ny',
            'ur', 'pau', 'pa', 'pap', 'ps', 'fa', 'pis',
            'pl', 'pt', 'pot', 'qu', 'ro', 'ru', 'sm',
            'sg', 'gd', 'sr', 'sn', 'si', 'sk', 'sl',
            'so', 'st', 'es', 'srn', 'sw', 'sv', 'de',
            'syc', 'tl', 'tg', 'tmh', 'ta', 'te', 'tet',
            'th', 'bo', 'ti', 'tpi', 'tkl', 'to', 'tn',
            'tr', 'tk', 'tvl', 'uk', 'ppk', 'uz', 'vi',
            'wls', 'cy', 'wo', 'xh', 'yi', 'zu'
        ]
    )
    GOOGLE = GoogleTranslator(
        GTranslator(),
        to_lang=TRANS_MODEL_SETTINGS[GOOGLE_TRANS_NAME]['lang'],
        support_langs=(LANGUAGES.keys())
    )


_director_mapping = {
    'blip': BuilderNameEnum.BLIP_DIR.value,
    # 'blip2': BuilderNameEnum.BLIP2_DIR.value
}

_translator_mapping = {
    'google': TranslatorNameEnum.GOOGLE.value,
    'apptrans': TranslatorNameEnum.APPTRANS.value
}


class GetDescript(AbstractUseCase):
    """
    Получение описания изображения.

    :ivar __img_repos: Атрибут репозитория изображений, для доступа к
                       хранилищу.
    :type __img_repos: ImageRepository

    :ivar __desc_repos: Атрибут репозитория описаний, для доступа к
                        хранилищу.
    :type __desc_repos: DescriptionRepository
    """

    def __init__(
            self,
            img_repos: 'AbstractImageRepository',
            desc_repos: 'AbstractDescriptionRepository'
    ) -> None:
        """
        Инициализация описания изображения.

        :param img_repos: Репозиторий изображений, для доступа к
                          хранилищу.
        :type img_repos: ImageRepository

        ::param desc_repos: Репозиторий описаний, для доступа к
                            хранилищу.
        :type desc_repos: DescriptionRepository
        """

        self.__img_repos = img_repos
        self.__desc_repos = desc_repos

    def execute(
            self,
            uuid: 'UUID',
            name_cap_model: str,
            name_translator: str | None,
            max_length: int | None
    ) -> str:
        """
        Получение описания изображения.

        Получение изображения, по его пути, из репозитория, после чего,
        с помощью директора captioning-модели, идет описание
        изображения.

        :param uuid: UUID загруженного изображения.
        :type uuid: UUID

        :param name_cap_model: Название captioning-модели.
        :type name_cap_model: str

        :param name_translator: Название переводчика описания изображения.
        :type name_translator: str | None

        :param max_length: Максимальная длина описания изображения.
        :type max_length: int | None

        :return: Описание изображения.
        :rtype: str

        :raises ValueError: Если нет captioning-модели.
        :raises ValueError: Если нет переводчика.
        """

        # Получение изображения.
        img_path = self.__img_repos.get_path_by_uuid(uuid)
        if not img_path.exists():
            raise ValueError(f"Пути к файлу {img_path} не существует!")

        try:
            with open(img_path, 'rb') as f:
                img = f.read()
        except PermissionError:
            raise PermissionError("Нет прав для получения изображения!")
        except OSError:
            raise OSError("Невозможно получить изображение!")
        except Exception as e:
            raise Exception(f"Неизвестная ошибка при получении изображения:"
                            f" {e}!")

        # Инциализация Captioning-модели.
        if name_cap_model not in _director_mapping:
            raise ValueError(f'Нет такой captioning-модели: {name_cap_model}')
        director = _director_mapping[name_cap_model]

        if name_translator is not None:
            if name_translator not in _translator_mapping:
                raise ValueError(f'Нет такого переводчика: {name_translator}')
            translator = _translator_mapping[name_translator]
        else:
            translator = None

        director.set_translator(translator)

        # Получение результата и сохранение в хранилище.
        result = director.get_descript(img, max_length)
        self.__desc_repos.set_description_by_uuid(uuid, desc=result)

        return result
