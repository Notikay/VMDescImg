from abc import ABC, abstractmethod
from typing import Any


class AbstractViewer(ABC):

    @abstractmethod
    def present(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def present_error(self, *args, **kwargs) -> Any:
        pass
