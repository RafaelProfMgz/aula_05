# Comparação — FreeCAD e Blender

> **Substituição de ferramenta.** A Tarefa A foi feita no **FreeCAD 1.1.3**, e não no
> Fusion 360, porque o Fusion não é executável nesta máquina (Ubuntu 25.10). O motivo
> completo, as alternativas examinadas e o que a troca preserva e o que ela muda estão em
> [`substituicao-fusion-por-freecad.md`](substituicao-fusion-por-freecad.md).

## 0. Como a Tarefa A foi conduzida

- [x] **Pelo servidor MCP** (equivalente à seção 4.3) — complemento `FreeCADMCP` na porta
      9875 e servidor ponte `freecad-mcp` 0.1.22, registrado como `"type": "local"`
- [ ] Pela execução manual dos scripts (seção 4.7)

O caminho da seção 4.7 não foi necessário: o servidor conectou e as ferramentas
responderam. Toda a modelagem passou por `execute_code`, e **toda medição foi impressa
pelo próprio script que executou a operação**, conforme a seção 2.3.

---

## 1. Medição de contexto

Medido em 10/09/2026 com `medir-contexto.py`, somando os caracteres de nome, descrição e
esquema de parâmetros de cada ferramenta — o texto apresentado ao modelo em toda chamada.

| Servidor | Ferramentas | Caracteres | Tokens aprox. | % de uma janela de 200k |
|---|---|---|---|---|
| Blender 5.2.1 (`blender-mcp` 1.0.2) | 26 | 13.231 | ~3.310 | 1,7 % |
| FreeCAD 1.1.3 (`freecad-mcp` 0.1.22) | 15 | 18.232 | ~4.560 | 2,3 % |
| **os dois conectados** | **41** | **31.463** | **~7.870** | **3,9 %** |
| só o FreeCAD, com o Blender desabilitado | 15 | 18.232 | ~4.560 | 2,3 % |
| só o Blender, com o FreeCAD desabilitado | 26 | 13.231 | ~3.310 | 1,7 % |

Desabilitar o servidor fora de uso devolveu entre **1.250 e 4.560 tokens** por tarefa —
entre 16% e 58% do custo dos dois somados. O campo `"enabled": false` desliga sem apagar
a configuração, e é o que o `opencode.json` entregue traz para o `fusion`.

Para referência, a tabela da seção 6.1 da apostila, medida com o Fusion:

| Servidor | Ferramentas | Caracteres | Tokens aprox. |
|---|---|---|---|
| Blender | 26 | 15.565 | ~3.900 |
| Fusion 360 | 4 | 20.598 | ~5.150 |
| os dois | 30 | 36.163 | ~9.050 |

### Divergências

**No Blender**, o número de ferramentas confere exatamente (26), mas o texto medido aqui é
**~15% menor**: 13.231 caracteres contra 15.565. A apostila declara que os números mudam
entre versões, e a diferença é compatível com uma revisão das descrições entre a versão
usada na preparação e a 1.0.2 instalada aqui. A ordem de grandeza se mantém.

**A conclusão da seção 6.1 se confirma com um servidor que a apostila não mediu.** A
apostila usa o par Blender/Fusion para mostrar que número de ferramentas não mede custo de
contexto: o Fusion, com 4 ferramentas, custa mais que o Blender, com 26. O par
Blender/FreeCAD **reproduz o mesmo efeito de forma independente** — 15 ferramentas do
FreeCAD custam **38% mais** contexto que as 26 do Blender. A causa é a que a apostila
aponta: as ferramentas do FreeCAD são genéricas, e cada uma carrega na descrição o
catálogo dos tipos de objeto e de propriedade que aceita.

No Blender, as três ferramentas mais caras são todas de consulta à documentação —
`get_python_api_docs` (2.638 caracteres), `search_api_docs` (1.467) e `search_manual_docs`
(1.464): juntas, 5.569 caracteres, **42% do total**. Doze das 26 são pares `_for_cli` de
outras, o que infla a contagem sem acrescentar capacidade à sessão interativa.

---

## 2. A alteração de cota no FreeCAD (passo 7)

**O que foi pedido:** alterar o diâmetro do furo da parede de Ø25 para Ø30 mm, editando a
cota no histórico — não refazendo a peça.

**Como foi feito:** uma única chamada, sobre a cota nomeada no esboço do furo:

```python
esboco_furo.setDatum("diametro_furo", "30 mm")
doc.recompute()
```

**O que o histórico recalculou:** o `PartDesign::Pocket` do furo e, a jusante dele, a
nervura — as duas operações posteriores no histórico. As cinco operações anteriores não
foram tocadas.

**Tempo gasto:** **0,042 s** de recálculo.

| Medição | Antes | Depois |
|---|---|---|
| Volume do sólido | 63.857,3 mm³ | 61.697,5 mm³ |
| Volume esperado pelo cálculo | — | 61.697,5 mm³ (erro 0,0000) |
| Caixa envolvente | 100,00 × 50,00 × 69,99 | 100,00 × 50,00 × 69,99 (inalterada) |
| Operações no histórico | 12 | 12 — **nenhuma acrescentada** |
| Diâmetro medido na geometria | Ø25,00 | **Ø30,00** |

**Precisou refazer alguma coisa a jusante?** Não. A conferência das demais cotas depois do
recálculo devolveu todas intactas: `comprimento_base=100`, `largura_base=50`,
`raio_rasgo=7,5`, `distancia_centros=25`, `rasgo_ate_aresta_frontal=40`,
`largura_parede=40`, `altura_parede_reta=50`, `raio_topo=20`, `comprimento_nervura=20`,
`altura_nervura=25`. O sólido continuou único e válido.

---

## 3. A mesma alteração no Blender (passo 10)

**O que foi pedido:** o mesmo furo, de 25 para 30 mm, direto na malha.

**Como foi feito.** Não existe cota para editar. Foi preciso, antes de mexer em qualquer
coisa, **descobrir na geometria** o que no FreeCAD já estava escrito: onde está o eixo do
furo (X = 0, Z = +0,015 nas coordenadas locais), qual o seu raio (0,0125 m) e quais
vértices pertencem a ele. Só então a alteração:

```python
for v in malha.vertices:
    if -0.0251 < v.co.y < -0.0149:                  # dentro da espessura da parede
        r = hypot(v.co.x, v.co.z - 0.015)
        if abs(r - 0.0125) < 0.0004:                # esta no cilindro do furo
            v.co.x *= 1.2                            # 30/25
            v.co.z = 0.015 + (v.co.z - 0.015) * 1.2
```

252 vértices deslocados radialmente.

**Tempo gasto:** **0,001 s** de execução — e é justamente esse número que engana. O custo
não está na execução, está em tudo o que veio antes dela: localizar o eixo, medir o raio,
escolher a tolerância de seleção e verificar que nenhum vértice vizinho entrou junto. Na
primeira tentativa a medição de conferência **pegou vértices que não eram do furo** e
devolveu Ø31,04 mm; foi preciso refazer a seleção pelas faces do material do furo para
obter a medida correta.

**O que precisou ser refeito:** neste caso específico, pouco — os dois materiais e a
suavização sobreviveram, porque as faces continuaram sendo as mesmas, só com os vértices
em outro lugar. **E isso é sorte da alteração escolhida**, não uma propriedade da malha: a
mudança era um escalonamento radial puro de um cilindro que já existia. Qualquer alteração
que mudasse a topologia — mover o furo até romper a borda da parede, transformar o rasgo em
dois furos, alterar o raio do topo — não teria solução por deslocamento de vértices, e
exigiria remodelar. A renderização, essa, teve de ser refeita integralmente (4,97 s).

| Medição | Antes | Depois |
|---|---|---|
| Diâmetro medido na malha | Ø25,00 | **Ø30,01** |
| Polígonos | 1.312 | 1.312 — os mesmos |
| Lados do polígono do furo | 126 | 126 — **os mesmos, agora sobre um círculo maior** |
| Erro de facetamento (flecha) | 0,0039 mm | 0,0047 mm — **+20%** |

Três coisas que a malha não sabe e o histórico sabia:

1. **O diâmetro não é 30, é 30,01.** A malha não guarda cota; guarda vértices. O valor sai
   de uma medição, com o erro do próprio facetamento embutido.
2. **A precisão piorou com a alteração.** O furo maior é descrito pelo mesmo número de
   facetas, então o erro de aproximação cresceu 20%. No FreeCAD o furo continua sendo um
   cilindro analítico, exato em qualquer escala.
3. **Nada se propaga.** Depois do passo 10 existem três versões independentes da peça: o
   modelo do FreeCAD (Ø30, com histórico), o `suporte.stl` exportado (Ø25) e a malha do
   Blender (Ø30,01). Nenhuma sabe da outra.

---

## 4. Conclusão

Começaria no FreeCAD, e a razão está nos dois números lado a lado: a mesma alteração custou
uma chamada com o valor pretendido de um lado, e uma investigação geométrica com tolerância
escolhida à mão do outro. Em uma peça fabricada o requisito muda várias vezes, e no modelo
paramétrico cada mudança é uma cota reescrita, com o programa recalculando o resto e
respondendo com a medida — foram 0,042 s e nenhuma outra cota tocada. Na malha, a alteração
só foi barata porque era um escalonamento de cilindro; a precisão piorou 20% e o resultado
saiu 30,01 e não 30, o que num contexto de tolerância de fabricação é a diferença entre ter
e não ter uma peça. O Blender entra depois, quando a geometria já está fechada e o que se
quer é a imagem — que é exatamente o que a Tarefa B fez.

---

## Anexo A — dois tropeços que não estão na apostila

### A.1 O complemento do Blender não sobe com "Allow Online Access" desligado

A tabela da seção 3.5 não registra este caso. O sintoma é a porta 9876 nunca abrir, sem
mensagem de erro visível: `opencode mcp list` responde `connected`, porque quem responde é
o processo intermediário, e a falha só aparece na primeira chamada de ferramenta. O
complemento abre um socket TCP e verifica `bpy.app.online_access` antes de iniciar; com a
permissão negada, registra o erro apenas no painel de preferências dele.

**Solução:** `Preferências → Sistema → Allow Online Access`, e salvar as preferências.

| Sintoma | Causa | Solução |
|---|---|---|
| conecta, mas a porta 9876 nunca abre e nenhuma ferramenta responde | "Allow Online Access" desligado no Blender | marcar a opção em Preferências → Sistema e salvar |

### A.2 Operadores do Blender falham por contexto quando chamados pelo MCP

`bpy.ops.wm.stl_import` respondeu `poll() failed, context is incorrect`, e
`bpy.context.selected_objects` não existe no contexto em que o complemento executa o
código. O servidor roda o código em um *timer*, fora de uma área de viewport.

**Solução:** envolver os operadores em `bpy.context.temp_override(window=..., area=...,
region=...)` com uma área `VIEW_3D`, e **não depender de seleção** — obter o objeto
importado pela diferença de `bpy.data.objects` antes e depois da chamada.

| Sintoma | Causa | Solução |
|---|---|---|
| `poll() failed, context is incorrect` num operador | o código roda fora de uma área de viewport | `bpy.context.temp_override` com uma área `VIEW_3D` |
| `'Context' object has no attribute 'selected_objects'` | não há seleção no contexto do timer | pegar o objeto pela diferença em `bpy.data.objects` |

---

## Anexo B — o que a medição de cada etapa pegou

O procedimento da seção 5.2 — medir cada etapa antes de pedir a seguinte — encontrou três
erros que a captura de tela não teria mostrado, porque **em todos os três a peça continuava
parecendo certa**:

| Etapa | O que a captura mostrava | O que a medição mostrou |
|---|---|---|
| 2 — rasgo oblongo | a peça, aparentemente normal | volume **inalterado**: o corte não aconteceu. O perfil estava inválido por restrições de tangência sobrepostas às coincidências |
| 4 — topo arredondado | a parede com o topo reto | o filete R20 sobre uma parede de 40 mm é **degenerado** (os dois raios se encontram no centro) e o OpenCascade o recusou. Refeito como arco no perfil |
| 6 — nervura | uma aleta em algum lugar | caixa envolvente **85 mm** em vez de 70: a restrição `DistanceY` é orientada, e o sinal invertido jogou o vértice para Z = −15 |

E um quarto, no esboço da parede: com o esboço **sub-restringido**, mudar a cota de altura
de 70 para 50 mm **deformou o perfil num trapézio** em vez de baixar o topo. É a
justificativa prática da regra do `AGENTS.md` — toda operação parte de esboço com cota e
restrição. Os esboços foram refeitos e cinco dos seis fecham como
`FullyConstrained = True`.

---

## Anexo C — como reproduzir as medições

```
.venv/bin/python medir-contexto.py                          # Blender
.venv/bin/python medir-contexto.py .venv/bin/freecad-mcp    # FreeCAD
```

Para um servidor `remote`, como seria o do Fusion, o mesmo cálculo exige um cliente HTTP
em vez de stdio.
