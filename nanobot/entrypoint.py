#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config.json at runtime,
then execs into nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    app_dir = Path("/app/nanobot")
    config_path = app_dir / "config.json"
    # Write resolved config to /tmp since mounted volumes may not be writable
    resolved_path = Path("/tmp/nanobot.config.resolved.json")
    workspace_dir = app_dir / "workspace"

    # Read base config
    with open(config_path) as f:
        config = json.load(f)

    # Override LLM provider settings from env vars
    llm_api_key = os.environ.get("LLM_API_KEY", "").strip()
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL", "").strip()
    llm_api_model = os.environ.get("LLM_API_MODEL", "").strip()

    # Determine provider from API base URL
    provider = "openrouter" if "openrouter" in llm_api_base_url.lower() else "custom"
    
    if provider not in config["providers"]:
        config["providers"][provider] = {}
    
    if llm_api_key:
        config["providers"][provider]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"][provider]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model
        config["agents"]["defaults"]["provider"] = provider

    # Override gateway settings from env vars
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "").strip()
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "").strip()

    if gateway_host:
        config.setdefault("gateway", {})["host"] = gateway_host
    if gateway_port:
        config.setdefault("gateway", {})["port"] = int(gateway_port)

    # Override MCP server env vars for LMS
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "").strip()
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY", "").strip()

    if "tools" not in config:
        config["tools"] = {}
    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}

    if "lms" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["lms"] = {
            "command": "python",
            "args": ["-m", "mcp_lms"],
        }

    lms_config = config["tools"]["mcpServers"]["lms"]
    if "env" not in lms_config:
        lms_config["env"] = {}

    if lms_backend_url:
        lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
    if lms_api_key:
        lms_config["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Configure webchat channel if enabled
    webchat_enabled = os.environ.get("NANOBOT_WEBCHAT_ENABLED", "").strip().lower()
    if webchat_enabled == "true":
        if "channels" not in config:
            config["channels"] = {}

        webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0").strip()
        webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8081").strip()

        config["channels"]["webchat"] = {
            "enabled": True,
            "host": webchat_host,
            "port": int(webchat_port),
            "allowFrom": ["*"],
        }

        # Task 2B: Configure mcp-webchat MCP server for UI messages (disabled for now)
        # webchat_ui_relay_url = os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_URL", "").strip()
        # webchat_ui_token = os.environ.get("NANOBOT_WEBCHAT_UI_TOKEN", "").strip()

        # if "mcp_webchat" not in config["tools"]["mcpServers"]:
        #     config["tools"]["mcpServers"]["mcp_webchat"] = {
        #         "command": "python",
        #         "args": ["-m", "mcp_webchat"],
        #         "env": {},
        #     }

        # mcp_webchat_env = config["tools"]["mcpServers"]["mcp_webchat"]["env"]
        # if webchat_ui_relay_url:
        #     mcp_webchat_env["NANOBOT_WEBCHAT_UI_RELAY_URL"] = webchat_ui_relay_url
        # if webchat_ui_token:
        #     mcp_webchat_env["NANOBOT_WEBCHAT_UI_TOKEN"] = webchat_ui_token

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_path}", file=sys.stderr)

    # Exec into nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace_dir),
        ],
    )


if __name__ == "__main__":
    main()
