from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from interface_adapters.presenters import AbstractViewer
    from interface_adapters.presenters.dto import (
        UploadImgResponse,
        ErrorResponse
    )
    from use_cases import AbstractUseCase


class ImgHandler:
    """
    Обработчик изображения.

    :ivar __pres: Атрибут представления описания изображения.
    :type __pres: AbstractViewer

    :ivar __upload_img: Атрибут загрузки изображения.
    :type __upload_img: AbstractUseCase
    """

    def __init__(
            self,
            pres: 'AbstractViewer',
            upload_img: 'AbstractUseCase'
    ) -> None:
        """
        Инициализация обработчика изображения.

        :param pres: Представление описания изображения.
        :type pres: AbstractViewer

        :param upload_img: Загрузка изображения.
        :type upload_img: AbstractUseCase
        """

        self.__pres = pres
        self.__upload_img = upload_img


    def upload(
            self,
            img: bytes
    ) -> Union['UploadImgResponse', 'ErrorResponse']:
        """
        Загрузка изображения.

        :param img: Изображение.
        :type img: bytes

        :return: UUID загруженного изображения или ошибка.
        :rtype: UploadImgResponse | UploadImgErrorResponse
        """

        try:
            result = self.__upload_img.execute(img)
        except Exception as e:
            return self.__pres.present_error(error=str(e), code=500)

        return self.__pres.present(str(result))
