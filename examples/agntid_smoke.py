"""Model-free protected calls using the official AgntID SDK task lifecycle.

Only enable --allow-deny after setting the documented demo.add_numbers policy:
first_number 10..20 and second_number 20..30, inclusive.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from urllib.parse import urlsplit

import agntid


async def protected_call(client, first: int, second: int) -> dict:
    agent_id = os.environ.get("AGNTID_AGENT_ID", "hackathon-smoke-agent")
    user_id = os.environ.get("AGNTID_USER_ID", "local-smoke-user")
    prompt = f"Use demo.add_numbers to add {first} and {second}."
    visible = await agntid.get_tools_list(client)
    task_id = agntid.create_task(agent_id, user_id, prompt)
    wrapped = agntid.wrap_client(client, task_id)
    async with agntid.task_context(client, task_id):
        opened = await agntid.send_task_open_details(client, task_id, agent_id, user_id, prompt)
        shortlisted = agntid.filter_tools_for_task(visible, opened)
        if "demo_add_numbers" not in {tool.name for tool in shortlisted}:
            raise RuntimeError("Expected demo tool is unavailable for this task.")
        result = await wrapped.call_tool_async(
            "demo_add_numbers", {"first_number": first, "second_number": second}
        )
        denied = bool(getattr(result, "denied", False))
        return {"inputs": [first, second], "denied": denied, "result": None if denied else result.get("result")}


async def run(allow_deny: bool) -> None:
    url = os.environ.get("AGNTID_MCP_URL", "http://127.0.0.1:18082/mcp")
    parsed = urlsplit(url)
    if parsed.username or parsed.password or parsed.query:
        raise RuntimeError("Use a clean MCP URL and transport-only OAuth credentials.")
    if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}):
        raise RuntimeError("Use HTTPS or local loopback HTTP.")
    async with agntid.AgntidMCPClient(url, access_token=os.getenv("AGNTID_ACCESS_TOKEN") or None) as client:
        tools = await agntid.get_tools_list(client)
        print(json.dumps({"enforcement": "agntid-runtime", "visible_tool_count": len(tools)}))
        allowed = await protected_call(client, 11, 21)
        print(json.dumps(allowed))
        if allowed["denied"] or allowed["result"] != 32:
            raise RuntimeError("Allowed case did not return 32.")
        if allow_deny:
            denied = await protected_call(client, 50, 21)
            print(json.dumps(denied))
            if not denied["denied"]:
                raise RuntimeError("Expected denial did not occur. Review the input policy.")
        print("Verify the matching task-open, tool execution, and task-close events in AgntID Reporting.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Official AgntID model-free SDK smoke")
    parser.add_argument("--allow-deny", action="store_true", help="Check both cases after configuring the Quick Start policy")
    options = parser.parse_args()
    try:
        asyncio.run(asyncio.wait_for(run(options.allow_deny), timeout=45))
    except Exception:
        print("AgntID smoke failed. Check provisioning, Applied sync, demo tool review, policy, and OAuth. Raw server errors and credentials are suppressed.")
        raise SystemExit(1) from None
