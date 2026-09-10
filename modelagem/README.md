# Scripts da modelagem

Os scripts que o agente executou, na ordem. **Não são o caminho da seção 4.7** — a Tarefa
A foi conduzida pelo servidor MCP (seção 4.3). Estão versionados porque tornam o resultado
reproduzível e porque documentam exatamente o que rodou dentro de cada programa.

Os dois arquivos com prefixo `_` enviam o código ao programa pelo servidor MCP, por stdio:

```
.venv/bin/python modelagem/_executa_no_freecad.py modelagem/freecad-etapas-1-a-6.py
.venv/bin/python modelagem/_executa_no_blender.py modelagem/blender-tarefa-b-cena.py
```

| Ordem | Script | O que faz |
|---|---|---|
| 1 | `freecad-etapas-1-a-6.py` | as seis etapas da seção 5.2, cada uma medida e capturada |
| 2 | `freecad-etapa-5-corrige-sentido-do-corte.py` | o furo não cortou: o `Pocket` corta no sentido oposto à normal do esboço. Corrigido com `Reversed = True`, **pelo histórico** |
| 3 | `freecad-passos-7-e-8.py` | exporta o Ø25, altera a cota para Ø30 cronometrando, confere que nada mais mudou e exporta de novo |
| 4 | `blender-tarefa-b-cena.py` | importa o STL, dois materiais, três pontos de luz, câmera e render |
| 5 | `blender-ajuste-camera-e-luz.py` | reenquadra para a nervura aparecer — de um ângulo dominado pelo eixo X ela fica escondida atrás da parede |
| 6 | `blender-passo-10-furo-na-malha.py` | o mesmo furo na malha, cronometrado, com o erro de facetamento medido |

> O script 1 traz o furo com o sentido de corte errado, e o 2 é a correção. Os dois estão
> aqui de propósito: o erro e a correção pelo histórico são material do Anexo B do
> `comparacao.md`.
