"""Alert dispatch — Slack, email, SIEM integration."""

import logging
import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    type: str
    severity: str
    user: str
    timestamp: str
    description: str
    details: dict[str, Any] | None = None


class SlackNotifier:
    def __init__(self, webhook_url: str) -> None:
        self._url = webhook_url

    SEVERITY_COLORS = {
        "CRITICAL": "#ff0000",
        "HIGH": "#ff8c00",
        "MEDIUM": "#ffd700",
        "LOW": "#90ee90",
    }

    def dispatch(self, alert: Alert) -> None:
        color = self.SEVERITY_COLORS.get(alert.severity.upper(), "#cccccc")
        blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": f"\u26a0 {alert.type}"}},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Severity:*\n{alert.severity}"},
                    {"type": "mrkdwn", "text": f"*User:*\n{alert.user}"},
                    {"type": "mrkdwn", "text": f"*Time:*\n{alert.timestamp}"},
                ],
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": alert.description}},
        ]
        payload = {"attachments": [{"color": color, "blocks": blocks}]}
        resp = httpx.post(self._url, json=payload)
        resp.raise_for_status()
        logger.info("Slack alert sent: %s", alert.type)


class EmailNotifier:
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_pass: str,
        from_addr: str,
        to_addr: str,
    ) -> None:
        self._host = smtp_host
        self._port = smtp_port
        self._user = smtp_user
        self._pass = smtp_pass
        self._from = from_addr
        self._to = to_addr

    def dispatch(self, alert: Alert) -> None:
        color = "red" if alert.severity in ("CRITICAL", "HIGH") else "orange"
        html = f"""<!DOCTYPE html>
<html><body style="font-family: sans-serif; max-width: 600px;">
<h2 style="color: {color};">{alert.type}</h2>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
<tr><td><strong>Severity</strong></td><td>{alert.severity}</td></tr>
<tr><td><strong>User</strong></td><td>{alert.user}</td></tr>
<tr><td><strong>Time</strong></td><td>{alert.timestamp}</td></tr>
<tr><td><strong>Description</strong></td><td>{alert.description}</td></tr>
</table>
</body></html>"""
        msg = MIMEText(html, "html")
        msg["Subject"] = f"[CyberHosp] {alert.severity} - {alert.type}"
        msg["From"] = self._from
        msg["To"] = self._to

        with smtplib.SMTP(self._host, self._port) as server:
            if self._user:
                server.starttls()
                server.login(self._user, self._pass)
            server.send_message(msg)
        logger.info("Email alert sent: %s", alert.type)


class Notifier:
    def __init__(self, config: dict[str, Any]) -> None:
        self._channels: list[SlackNotifier | EmailNotifier] = []
        slack_url = config.get("slack_webhook", "")
        if slack_url:
            self._channels.append(SlackNotifier(slack_url))
        smtp_host = config.get("smtp_host", "")
        if smtp_host:
            self._channels.append(
                EmailNotifier(
                    smtp_host=smtp_host,
                    smtp_port=config.get("smtp_port", 587),
                    smtp_user=config.get("smtp_user", ""),
                    smtp_pass=config.get("smtp_pass", ""),
                    from_addr=config.get("from_addr", ""),
                    to_addr=config.get("to_addr", ""),
                )
            )

    def dispatch(self, alert: Alert) -> None:
        for ch in self._channels:
            try:
                ch.dispatch(alert)
            except Exception:
                logger.exception("Alert dispatch failed on %s", type(ch).__name__)
