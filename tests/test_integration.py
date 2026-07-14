"""Integration layer tests."""

from cyberhosp.integration.base import EHRAdapter
from cyberhosp.integration.fhir import FHIRAdapter


class TestEHRAdapter:
    def test_fhir_adapter_inherits_ehradapter(self) -> None:
        assert isinstance(FHIRAdapter(), EHRAdapter)
