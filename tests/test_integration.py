"""Integration layer tests."""

from cyberhosp.integration.fhir import FHIRAdapter


class TestEHRAdapter:
    def test_fhir_adapter_instantiable(self) -> None:
        assert FHIRAdapter() is not None
