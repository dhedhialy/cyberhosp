from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EHRConfig:
    vendor: str
    base_url: str
    auth_method: str
    api_version: str


class EHRAdapter(ABC):
    def __init__(self, config: EHRConfig) -> None:
        self.config = config

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def stream_audit_events(self) -> None: ...
