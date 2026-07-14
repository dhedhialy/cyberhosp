"""Integration layer tests."""

from cyberhosp.integration.base import EHRAdapter, EHRConfig
from cyberhosp.integration.fhir import FHIRAdapter


class TestEHRAdapter:
    def test_fhir_adapter_inherits_ehradapter(self) -> None:
        config = EHRConfig(
            vendor="test",
            base_url="https://example.com/fhir",
            auth_method="oauth2",
            api_version="R4",
        )
        assert isinstance(FHIRAdapter(config), EHRAdapter)
