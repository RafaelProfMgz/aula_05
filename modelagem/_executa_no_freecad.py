"""Helper: executa codigo no FreeCAD pelo servidor MCP."""
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CMD = "/home/angel/tep/aula05/.venv/bin/freecad-mcp"

async def _run(codes):
    p = StdioServerParameters(command=CMD, args=["--only-text-feedback"])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            for code in codes:
                res = await s.call_tool("execute_code", {"code": code})
                for c in res.content:
                    print(getattr(c, "text", ""))

def run(*codes):
    asyncio.run(_run(list(codes)))

if __name__ == "__main__":
    run(open(sys.argv[1]).read())
