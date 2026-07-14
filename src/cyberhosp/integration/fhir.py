"""FHIR R4/R5 adapter for SMART-on-FHIR compliant EHRs."""

from cyberhosp.integration.base import EHRAdapter, EHRConfig


class FHIRAdapter(EHRAdapter):
    def __init__(self, config: EHRConfig | None = None) -> None:
        super().__init__(
            config
            or EHRConfig(
                vendor="generic",
                base_url="http://localhost/fhir",
                auth_method="smart",
                api_version="R4",
            )
        )

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def stream_audit_events(self) -> None:
        pass
