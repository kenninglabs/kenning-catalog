# chrome-devtools MCP (drive a real, logged-in browser)

Describes the *mechanism* for wiring the official `chrome-devtools-mcp` server to an agent so it can drive a real Chrome instance (navigate/click/fill/screenshot/inspect network + console).

## What it is

`chrome-devtools-mcp` (npm, maintained by the Chrome DevTools team) is an MCP server that exposes browser-automation tools over the Chrome DevTools Protocol (CDP). Two connection modes:

- **Launch its own Chrome** (default) — throwaway browser, no existing session.
- **Attach to a running Chrome** via `--browserUrl=http://127.0.0.1:<port>` — use this when the task needs an already-logged-in session (the login lives in that Chrome's profile, not in the MCP).

## Install

Running Install checks for `npx` and pre-fetches the `chrome-devtools-mcp` npm package (`npx -y chrome-devtools-mcp@latest --version`), so the first real MCP call doesn't pay the download cost. It does not do the Chrome-launch/profile/`.mcp.json` setup below — that's a one-time environment step, not a package install.

## Prerequisites

- `node` + `npx` on PATH (the server is fetched on first call via `npx -y chrome-devtools-mcp@latest`).
- Google Chrome installed.
- The agent host must be able to reach the CDP port (default `127.0.0.1:9222`).

## Chrome 136+ gotcha

Since Chrome 136 (May 2025), Chrome silently ignores `--remote-debugging-port` when launched on the *default* user-data-dir — a deliberate anti-cookie-theft hardening. A debug-enabled Chrome must use a separate `--user-data-dir`. Two ways to get a logged-in session in that separate profile:
1. **Fresh debug profile, log in once** (recommended) — the session persists in that dir across every restart, isolated from the daily browser.
2. **Clone the default profile** into the new dir to inherit the current login — a large copy that goes stale as the real profile keeps changing.

## Setup (attach-to-running mode)

1. Launch a debug Chrome on a dedicated profile (detached so it survives the agent's shell):
   ```bash
   open -na "Google Chrome" --args \
     --remote-debugging-port=9222 \
     --user-data-dir="$HOME/.chrome-debug" \
     "<the-url-to-open>"
   ```
   Verify the port is live: `curl -s http://127.0.0.1:9222/json/version` → should return a `webSocketDebuggerUrl`.
2. Log into the target environment once in that Chrome window (persists in the profile dir).
3. Register the MCP server — minimal `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl=http://127.0.0.1:9222"]
       }
     }
   }
   ```
4. Approve + load the server (a newly-added project-scoped server usually starts pending approval — confirm/approve, then restart/reconnect so the tools load).

## Verify it's wired

The agent can call tools like `navigate`, `take_snapshot`, `click`, `fill`, `take_screenshot`, `list_network_requests`, `list_console_messages`.

## Gotchas

- Keep the debug Chrome window open while working — the MCP attaches to it. If it closes, rerun the launch command (same profile dir → same login).
- Default profile won't work for the debug port (see above) — always use a separate dir.
- Prefer `take_snapshot` (accessibility tree with element uids) over screenshots for driving clicks/fills; use screenshots for visual confirmation.
- First tool call pays a one-time `npx` fetch of the server package.

## Uninstall / disable

Remove the `chrome-devtools` block from your MCP config and restart. Delete the debug profile dir to drop the stored login.
