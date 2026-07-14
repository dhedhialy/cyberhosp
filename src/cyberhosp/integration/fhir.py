"""FHIR R4/R5 adapter for SMART-on-FHIR compliant EHRs."""

import asyncio
import logging
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from cyberhosp.integration.base import EHRAdapter, EHRConfig

logger = logging.getLogger(__name__)


@dataclass
class OAuth2Config:
    token_url: str
    client_id: str
    client_secret: str
    scopes: str = "system/*.read"


class FHIRAdapter(EHRAdapter):
    def __init__(self, config: EHRConfig, oauth2: OAuth2Config | None = None) -> None:
        super().__init__(config)
        self.oauth2 = oauth2
        self._client: httpx.AsyncClient | None = None
        self._token: str | None = None
        self._base_url = config.base_url.rstrip("/")

    async def connect(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=10),
        )
        if self.oauth2:
            resp = await self._client.post(
                self.oauth2.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.oauth2.client_id,
                    "client_secret": self.oauth2.client_secret,
                    "scope": self.oauth2.scopes,
                },
            )
            resp.raise_for_status()
            self._token = resp.json()["access_token"]
            logger.info("FHIRAdapter authenticated with %s", self.config.vendor)

    async def disconnect(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
            self._token = None

    async def stream_audit_events(  # type: ignore[override]
        self, since: datetime | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        if not self._client:
            raise RuntimeError("Not connected. Call connect() first.")

        params: dict[str, str] = {
            "_sort": "_lastUpdated",
            "_count": "200",
        }
        if since:
            params["_lastUpdated"] = f"gt{since.isoformat()}"

        url: str | None = f"{self._base_url}/AuditEvent"
        retries = 0

        while url:
            try:
                headers = {}
                if self._token:
                    headers["Authorization"] = f"Bearer {self._token}"

                params = {} if url and "?" in url else params
                resp = await self._client.get(url, params=params, headers=headers)
                resp.raise_for_status()
                bundle: dict[str, Any] = resp.json()
                retries = 0

                for entry in bundle.get("entry", []):
                    yield entry.get("resource", {})

                next_link = self._next_page(bundle)
                if next_link and "://" in next_link:
                    url = next_link
                elif next_link:
                    url = f"{self._base_url}/{next_link}"
                else:
                    url = None
                params = {}

            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 502, 503) and retries < 5:
                    wait = 2**retries
                    logger.warning(
                        "FHIR API error %d, retrying in %ds",
                        e.response.status_code,
                        wait,
                    )
                    await asyncio.sleep(wait)
                    retries += 1
                else:
                    raise

    def _next_page(self, bundle: dict[str, Any]) -> str | None:
        for link in bundle.get("link", []):
            if link.get("relation") == "next":
                return link.get("url", "")
        return None

    async def __aenter__(self) -> "FHIRAdapter":
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.disconnect()
