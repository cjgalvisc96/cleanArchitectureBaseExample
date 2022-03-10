from abc import ABC, abstractmethod

from interfaces.error_messages import interface_repo_errors as errors


class IRepo(ABC):
    @abstractmethod
    def _create_room_objects():
        raise NotImplementedError(errors["method_not_implemented"])

    @abstractmethod
    def list():
        raise NotImplementedError(errors["method_not_implemented"])
