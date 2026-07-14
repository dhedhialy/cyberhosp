"""Audit and monitoring tests."""

from cyberhosp.monitor.analyzer import BehaviorAnalyzer
from cyberhosp.monitor.audit import AuditPipeline
from cyberhosp.monitor.base import MonitorComponent


class TestAuditPipeline:
    def test_audit_pipeline_inherits_monitor_component(self) -> None:
        assert isinstance(AuditPipeline(), MonitorComponent)

    def test_behavior_analyzer_inherits_monitor_component(self) -> None:
        assert isinstance(BehaviorAnalyzer(), MonitorComponent)
