# Projeto — Modelagem 3D com agentes

## Programas
- Fusion 360, servidor MCP local em http://127.0.0.1:27182/mcp
- Blender 5.2.1 LTS, complemento MCP na porta 9876

## Unidades
- Eu falo sempre em milímetro. Você converte.
- API do Fusion: centímetro. 80 mm se escreve 8.0.
- Cena do Blender: metro. 80 mm se escreve 0.08.
- Toda medida devolvida a mim vem em milímetro, com uma casa decimal.

## Convenções
- Toda operação do Fusion parte de esboço com cota, nunca de primitiva direta.
- Objetos do Blender recebem nome descritivo em minúsculas, sem acento.
- Renderizações vão para renders/, com o caminho definido em scene.render.filepath
  antes de renderizar — as ferramentas de render do servidor gravam em pasta temporária.

## Comandos
- Verificar as conexões: `opencode mcp list`
- Listar as ferramentas na sessão: `/mcp`

## Sempre
- Depois de cada operação, imprima a medida do resultado e me informe o valor.
- Antes de escrever código para o Blender, consulte a API com `search_api_docs`.
- Antes de capturar o Blender, enquadre o objeto e capture a área VIEW_3D, não a janela.
- Nos scripts do Fusion, não capture exceções: o erro é o que permite corrigir.

## Nunca
- Não altere cota já aceita sem me avisar qual e por quê.
- Não apague objetos que você não criou nesta sessão.
