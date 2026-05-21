import sys, json, subprocess, os, time

# Read token from config.yaml (never hardcode)
config_path = os.path.expanduser("~/.hermes/config.yaml")
token = None
try:
    with open(config_path) as f:
        for line in f:
            if "HUAHUA_AGENT_TOKEN:" in line:
                token = line.split("HUAHUA_AGENT_TOKEN:", 1)[1].strip()
                break
except Exception:
    pass

if not token:
    token = os.environ.get("HUAHUA_AGENT_TOKEN", "")

if not token:
    print(json.dumps({"error": "No HUAHUA_AGENT_TOKEN found in config.yaml or env"}))
    sys.exit(1)

tool_name = sys.argv[1]
args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

env = {**os.environ, "HUAHUA_AGENT_TOKEN": token, "BAIYE_AGENT_TOKEN": token}

proc = subprocess.Popen(
    ["/home/agentuser/.local/bin/uvx", "--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    env=env
)

messages = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "hermes", "version": "1.0"}}},
    {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool_name, "arguments": args}}
]

for msg in messages:
    proc.stdin.write((json.dumps(msg) + "\n").encode())
    proc.stdin.flush()

# CRITICAL: sleep 8s before closing stdin to avoid deadlock
# MCP server may be slow to respond; closing stdin too early causes empty output
time.sleep(8)
try:
    proc.stdin.close()
except:
    pass

output = proc.stdout.read().decode()
result_found = False
for line in output.strip().split("\n"):
    try:
        d = json.loads(line)
        if d.get("id") == 2 and "result" in d:
            print(json.dumps(d["result"], ensure_ascii=False, indent=2))
            result_found = True
    except:
        pass

if not result_found:
    err = proc.stderr.read().decode().strip()
    if err:
        print(json.dumps({"error": "MCP no result", "stderr_tail": err[-500:]}))
    else:
        print(json.dumps({"error": "MCP returned empty output"}))
