
# minimal local MCP server (harmless, no network)
import sys
def main():
    # MCP stdio JSON-RPC protocol, minimal echo tool
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        sys.stdout.write('{"jsonrpc":"2.0","result":{"content":[{"type":"text","text":"pong"}]},"id":1}\n')
        sys.stdout.flush()
if __name__ == "__main__":
    main()
