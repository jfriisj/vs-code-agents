#!/usr/bin/env python3
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any


class MCPError(RuntimeError):
    pass


def _parse_mcp_payload(body: str) -> dict[str, Any]:
    text = body.strip()
    if not text:
        raise MCPError("Empty MCP response body")

    if text.startswith("{"):
        return json.loads(text)

    data_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("data:"):
            data_lines.append(line[5:].lstrip())

    if not data_lines:
        raise MCPError(f"Unable to parse MCP SSE payload: {body[:200]}")

    return json.loads("\n".join(data_lines))


class MCPClient:
    def __init__(
        self,
        url: str,
        timeout_seconds: int = 20,
        max_retries: int = 2,
        backoff_seconds: float = 0.25,
    ) -> None:
        self.url = url
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(0, int(max_retries))
        self.backoff_seconds = max(0.0, float(backoff_seconds))
        self.session_id: str | None = None
        self.request_id = 1

    def initialize(self) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "planka-workflow-cli", "version": "1.0.0"},
            },
        }
        return self._post(payload)

    def list_tools(self) -> Any:
        self._ensure_initialized()
        result = self._post({"jsonrpc": "2.0", "id": self._next_id(), "method": "tools/list"})
        return result.get("tools")

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        self._ensure_initialized()
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments or {},
            },
        }
        result = self._post(payload)
        content = result.get("content", [])

        if not content:
            return result

        text_chunks = [item.get("text", "") for item in content if item.get("type") == "text"]
        combined_text = "\n".join([chunk for chunk in text_chunks if chunk]).strip()

        if not combined_text:
            return result

        try:
            return json.loads(combined_text)
        except json.JSONDecodeError:
            return combined_text

    def _ensure_initialized(self) -> None:
        if self.session_id is None:
            self.initialize()

    def _next_id(self) -> int:
        value = self.request_id
        self.request_id += 1
        return value

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        retryable_http_codes = {408, 429, 500, 502, 503, 504}
        max_attempts = self.max_retries + 1

        for attempt in range(max_attempts):
            request = urllib.request.Request(
                url=self.url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )

            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    raw_body = response.read().decode("utf-8", errors="replace")
                    returned_session = response.headers.get("mcp-session-id")
                    if returned_session:
                        self.session_id = returned_session
            except urllib.error.HTTPError as error:
                error_body = error.read().decode("utf-8", errors="replace")
                if error.code in retryable_http_codes and attempt < self.max_retries:
                    time.sleep(self.backoff_seconds * (2 ** attempt))
                    continue
                raise MCPError(
                    f"HTTP {error.code} from MCP endpoint: {error_body[:400]}"
                ) from error
            except urllib.error.URLError as error:
                if attempt < self.max_retries:
                    time.sleep(self.backoff_seconds * (2 ** attempt))
                    continue
                raise MCPError(f"Unable to reach MCP endpoint {self.url}: {error}") from error

            parsed = _parse_mcp_payload(raw_body)
            if "error" in parsed:
                raise MCPError(f"MCP error: {parsed['error']}")

            result = parsed.get("result")
            if result is None:
                raise MCPError(f"MCP response missing result: {parsed}")

            return result

        raise MCPError("MCP transport retry loop exited unexpectedly")
