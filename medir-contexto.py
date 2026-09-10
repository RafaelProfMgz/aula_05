#!/usr/bin/env python3
"""Mede o custo de contexto de um servidor MCP local.

Conta as ferramentas expostas e soma os caracteres de nome, descricao e
esquema de parametros — que e o texto apresentado ao modelo em toda chamada,
conforme a secao 6.1 da apostila.

Uso:
    .venv/bin/python medir-contexto.py [caminho-do-executavel]
"""
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PADRAO = "/home/angel/tep/aula05/.venv/bin/blender-mcp"


async def medir(comando: str) -> None:
    params = StdioServerParameters(command=comando, args=[])
    async with stdio_client(params) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            await sessao.initialize()
            ferramentas = (await sessao.list_tools()).tools
            total = 0
            print(f"ferramentas: {len(ferramentas)}\n")
            for ferramenta in ferramentas:
                tamanho = (
                    len(ferramenta.name)
                    + len(ferramenta.description or "")
                    + len(json.dumps(ferramenta.inputSchema or {}))
                )
                total += tamanho
                print(f"  {ferramenta.name:50s} {tamanho:6d}")
            print(f"\ncaracteres (nome + descricao + parametros): {total}")
            print(f"tokens aproximados (/4): {total / 4:.0f}")


if __name__ == "__main__":
    asyncio.run(medir(sys.argv[1] if len(sys.argv) > 1 else PADRAO))
