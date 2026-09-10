"""Helper: executa codigo no Blender pelo servidor MCP."""
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
CMD = "/home/angel/tep/aula05/.venv/bin/blender-mcp"

async def _run(code):
    p = StdioServerParameters(command=CMD, args=[])
    async with stdio_client(p) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool("execute_blender_code", {"code": code})
            for c in res.content:
                print(getattr(c, "text", ""))

if __name__ == "__main__":
    asyncio.run(_run(open(sys.argv[1]).read()))
