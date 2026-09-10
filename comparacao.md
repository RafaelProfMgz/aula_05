# Comparação — FreeCAD e Blender

> **Substituição de ferramenta.** A Tarefa A foi feita no **FreeCAD 1.1.3**, e não no
> Fusion 360, porque o Fusion não é executável nesta máquina (Ubuntu 25.10). O motivo
> completo, as alternativas examinadas e o que a troca preserva e o que ela muda estão em
> [`substituicao-fusion-por-freecad.md`](substituicao-fusion-por-freecad.md).

## 0. Como a Tarefa A foi conduzida
- [x] Pelo servidor MCP (equivalente à seção 4.3) — complemento `FreeCADMCP` na porta
      9875 e servidor ponte `freecad-mcp` 0.1.22, registrado como `"type": "local"`
- [ ] Pela execução manual dos scripts (seção 4.7)

O caminho da seção 4.7 não foi necessário: o servidor conectou e as ferramentas
responderam na primeira tentativa.

---

## 1. Medição de contexto

Medido em 10/09/2026, com `medir-contexto.py`, somando os caracteres de nome, descrição e
esquema de parâmetros de cada ferramenta — que é o texto apresentado ao modelo em toda
chamada, conforme a seção 6.1 da apostila.

| Servidor | Ferramentas | Caracteres | Tokens aprox. |
|---|---|---|---|
| Blender 5.2.1 (`blender-mcp` 1.0.2) | 26 | 13.231 | ~3.310 |
| FreeCAD 1.1.3 (`freecad-mcp` 0.1.22) | 15 | 18.232 | ~4.560 |
| **os dois conectados** | **41** | **31.463** | **~7.870** |

Para referência, a tabela da seção 6.1 da apostila, medida com o Fusion:

| Servidor | Ferramentas | Caracteres | Tokens aprox. |
|---|---|---|---|
| Blender | 26 | 15.565 | ~3.900 |
| Fusion 360 | 4 | 20.598 | ~5.150 |
| os dois | 30 | 36.163 | ~9.050 |

### Divergências

**No Blender**, o número de ferramentas confere exatamente (26), mas o texto medido aqui
é ~15% menor: 13.231 caracteres contra 15.565. A apostila declara que os números mudam
entre versões — a diferença é compatível com uma revisão das descrições entre a versão
usada na preparação e a 1.0.2 instalada aqui. A ordem de grandeza se mantém.

**A conclusão da seção 6.1 se confirma com outro servidor.** A apostila usa o par
Blender/Fusion para mostrar que **número de ferramentas não mede custo de contexto**: o
Fusion, com 4 ferramentas, custa mais que o Blender, com 26. O par Blender/FreeCAD
reproduz o mesmo efeito de forma independente — **15 ferramentas do FreeCAD custam ~38%
mais contexto que as 26 do Blender**. A causa é a mesma que a apostila aponta: as
ferramentas do FreeCAD são genéricas, e cada uma carrega na descrição o catálogo dos
tipos de objeto e de propriedade que aceita. `create_object` sozinha responde por boa
parte do total.

No Blender, as três ferramentas mais caras são todas de consulta à documentação —
`get_python_api_docs` (2.638 caracteres), `search_api_docs` (1.467) e `search_manual_docs`
(1.464): juntas, 5.569 caracteres, 42% do total. Doze das 26 são pares `_for_cli` de
outras, o que infla a contagem sem acrescentar capacidade à sessão interativa.

**Janela restante:** _a preencher — com os dois conectados e com um deles desabilitado._

---

## 2. A alteração de cota no FreeCAD (passo 7)

- **O que foi pedido:** _a preencher_ — alterar a cota do diâmetro do furo da parede de
  Ø25 para Ø30 mm, editando a operação no histórico
- **O que o histórico recalculou:** _a preencher_
- **Tempo gasto:** _a preencher_
- **Precisou refazer alguma coisa a jusante?** _a preencher_

### Já verificado no ensaio de conexão

Antes da Tarefa A, a peça de teste da seção 4.5 da apostila foi reproduzida para conferir
o ciclo completo. O resultado foi idêntico ao que a apostila prevê para o Fusion:

| Ação | Medição devolvida |
|---|---|
| Esboço retangular 80 x 40 mm, extrusão de 10 mm | `80.00 x 40.00 x 10.00` |
| Alterar o comprimento para 100 mm e recalcular | `100.00 x 40.00 x 10.00` |

O histórico recalculou a extrusão sobre o esboço alterado, e o corpo manteve as duas
operações (`esboco`, `extrusao`). É esse comportamento que a modelagem paramétrica
oferece e a poligonal não.

---

## 3. A mesma alteração no Blender (passo 10)

- **O que foi pedido:** alterar o mesmo furo, de 25 para 30 mm, direto na malha
- **O que precisou ser refeito:** _a preencher (material? UV? posição da câmera? luzes?)_
- **Tempo gasto:** _a preencher_

---

## 4. Conclusão

_Cinco linhas sobre em qual dos dois programas eu começaria um projeto de peça
fabricada, e por quê._

---

## Anexo A — um tropeço que não está na apostila

**O complemento do Blender não sobe com "Allow Online Access" desligado.** A tabela da
seção 3.5 não registra este caso. O sintoma é a porta 9876 nunca abrir, sem mensagem de
erro visível na janela: `opencode mcp list` responde `connected`, porque quem responde é o
processo intermediário, e a falha só aparece na primeira chamada de ferramenta. A causa é
que o complemento abre um socket TCP e verifica `bpy.app.online_access` antes de iniciar;
com a permissão negada, ele registra o erro apenas no painel de preferências do próprio
complemento.

**Solução:** `Preferências → Sistema → Allow Online Access`, e salvar as preferências.

Acrescento sugerido à tabela da seção 3.5:

| Sintoma | Causa | Solução |
|---|---|---|
| conecta, mas a porta 9876 nunca abre e nenhuma ferramenta responde | "Allow Online Access" desligado no Blender | marcar a opção em Preferências → Sistema e salvar |

---

## Anexo B — como a medição foi feita

`medir-contexto.py`, na raiz do repositório, abre o servidor por stdio, chama `list_tools`
e soma os caracteres de nome, descrição e esquema de parâmetros de cada ferramenta:

```
.venv/bin/python medir-contexto.py                              # Blender (padrão)
.venv/bin/python medir-contexto.py .venv/bin/freecad-mcp        # FreeCAD
```

Para medir um servidor `remote`, como seria o do Fusion, o mesmo cálculo exige um cliente
HTTP em vez de stdio.
