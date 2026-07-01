from abc import ABC, abstractmethod


class BaseProvider(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def chat(self, messages: list, temperature: float = 0.3) -> str:
        pass
