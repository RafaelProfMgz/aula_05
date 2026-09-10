# Projeto — Modelagem 3D com agentes

> A Tarefa A usa **FreeCAD** no lugar do Fusion 360. O motivo está em
> `substituicao-fusion-por-freecad.md`.

## Programas
- FreeCAD 1.1.3, complemento MCP (XML-RPC) na porta 9875
- Blender 5.2.1 LTS, complemento MCP na porta 9876
- Fusion 360 — registrado no `opencode.json` como `remote`, mas desabilitado:
  não roda em Linux

## Unidades
- Eu falo sempre em milímetro. Você converte.
- API do FreeCAD: milímetro. 80 mm se escreve 80.
- Cena do Blender: metro. 80 mm se escreve 0.08.
- Toda medida devolvida a mim vem em milímetro, com uma casa decimal.

## Convenções
- Toda operação do FreeCAD parte de esboço com cota e restrição, dentro de um
  PartDesign::Body — nunca de primitiva direta.
- Objetos do FreeCAD e do Blender recebem nome descritivo em minúsculas, sem acento.
- Renderizações vão para renders/, com o caminho definido em scene.render.filepath
  antes de renderizar — as ferramentas de render do servidor gravam em pasta temporária.
- Exportações vão para saidas/: STEP por `Import.export`, STL por `Mesh.export`.

## Comandos
- Verificar as conexões: `opencode mcp list`
- Listar as ferramentas na sessão: `/mcp`

## Sempre
- Depois de cada operação, imprima a medida do resultado e me informe o valor.
- No FreeCAD, chame `doc.recompute()` antes de medir, e imprima a caixa envolvente
  com `body.Shape.BoundBox`.
- Antes de escrever código para o Blender, consulte a API com `search_api_docs`.
- Antes de capturar o Blender, enquadre o objeto e capture a área VIEW_3D, não a janela.
- Nos scripts do FreeCAD, não capture exceções: o erro é o que permite corrigir.

## Nunca
- Não altere cota já aceita sem me avisar qual e por quê.
- Não apague objetos nem documentos que você não criou nesta sessão.
- No FreeCAD, não refaça a peça para corrigir uma medida: edite a operação no
  histórico e recalcule.
