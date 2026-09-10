# Scripts da modelagem

Os scripts que o agente executou, na ordem. **Não são o caminho da seção 4.7** — a Tarefa
A foi conduzida pelo servidor MCP (seção 4.3). Estão versionados porque tornam o resultado
reproduzível e porque documentam exatamente o que rodou dentro de cada programa.

Os dois arquivos com prefixo `_` são os utilitários que enviam o código ao programa pelo
servidor MCP, por stdio:

```
.venv/bin/python modelagem/_executa_no_freecad.py modelagem/freecad-etapas-1-a-6.py
.venv/bin/python modelagem/_executa_no_blender.py modelagem/blender-tarefa-b-cena.py
```

| Ordem | Script | O que faz |
|---|---|---|
| 1 | `freecad-etapas-1-a-6.py` | as seis etapas da seção 5.2, cada uma medida e capturada |
| 2 | `freecad-etapa-6-nervura-corrigida.py` | refaz a nervura — a cota `DistanceY` é orientada e o sinal invertido jogou o vértice para Z = −15 |
| 3 | `freecad-passo-7-cota-do-furo.py` | Ø25 → Ø30 pelo histórico, cronometrado, com conferência de que nada mais mudou |
| 4 | `freecad-passo-8-exportacao.py` | STEP e STL, nas duas versões do furo |
| 5 | `blender-tarefa-b-cena.py` | importa o STL, dois materiais, três pontos de luz, câmera e render |
| 6 | `blender-passo-10-furo-na-malha.py` | o mesmo furo na malha, cronometrado, com o erro de facetamento medido |

> O script 1 traz a nervura na versão com a cota invertida; o script 2 é a correção que
> ficou valendo. Os dois estão aqui de propósito: o erro e a correção são material do
> Anexo B do `comparacao.md`.
