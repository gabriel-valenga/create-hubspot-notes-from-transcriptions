from typing import Protocol

class ParameterStoreProtocol(Protocol):

    def get_parameter(self, name: str) -> str:
        ...
        