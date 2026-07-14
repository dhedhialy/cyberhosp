"""Audit and monitoring tests."""

from cyberhosp.monitor.analyzer import BehaviorAnalyzer
from cyberhosp.monitor.audit import AuditPipeline


class TestAuditPipeline:
    def test_audit_pipeline_instantiable(self) -> None:
        assert type(AuditPipeline()) is AuditPipeline


class TestBehaviorAnalyzer:
    def test_behavior_analyzer_instantiable(self) -> None:
        assert type(BehaviorAnalyzer()) is BehaviorAnalyzer
