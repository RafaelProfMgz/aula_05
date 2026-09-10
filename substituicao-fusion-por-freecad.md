# Por que o FreeCAD no lugar do Fusion 360

Registro da substituição de ferramenta na Tarefa A da Aula 05, com o motivo, o que a
troca preserva e o que ela muda.

---

## 1. O motivo: o Fusion 360 não é executável nesta máquina

A estação de trabalho usada nesta disciplina roda **Ubuntu 25.10** (kernel 6.17). O
Fusion 360 não tem versão para Linux, e as três saídas possíveis foram examinadas antes
de recorrer à substituição:

| Saída | Situação | Por que não serve |
|---|---|---|
| Cliente nativo Linux | não existe | A Autodesk suporta oficialmente Windows, macOS e navegador. Não há e não houve cliente Linux. |
| Versão em navegador | roda no Linux | **Não hospeda o servidor MCP.** A seção 4.2 da apostila é explícita: o servidor sobe junto com o programa e "não há como usá-lo com o Fusion fechado nem com a versão web". O caminho alternativo da seção 4.7 (`UTILITIES → ADD-INS → Scripts and Add-Ins`) também é recurso do aplicativo de mesa. Os dois caminhos previstos para a Tarefa A ficam indisponíveis. |
| Wine / Bottles | possível, instável | O projeto de referência da comunidade, `cryinkfly/Autodesk-Fusion-360-for-Linux`, **foi arquivado em fevereiro de 2026** e está sem manutenção. Mesmo quando o programa abre, o servidor MCP é o componente mais recente e menos testado nesse ambiente. |
| Máquina virtual Windows | funciona | Exige DirectX 11 e aceleração gráfica na VM. Viável, mas fora do alcance desta estação no prazo da entrega. |

Não se trata de preferência por software livre nem de dificuldade de licença: a licença
educacional está disponível. O impedimento é de plataforma.

## 2. O critério da escolha

O substituto tinha de preservar aquilo que a Aula 05 usa o Fusion **para demonstrar** —
não a marca, e sim o paradigma. Pela tabela da seção 1.3 da apostila, o que o Fusion traz
e o Blender não traz é:

1. Geometria **B-Rep** — fronteiras analíticas, e não facetas
2. **Histórico de operações** editável, que recalcula a jusante
3. Esboço com **restrições e cotas** como base das operações sólidas
4. Saída em **STEP** e **STL** com dimensão controlada
5. Trabalho em **milímetro**, com tolerância de fabricação

O **FreeCAD 1.1.3** atende aos cinco. É B-Rep sobre o mesmo núcleo geométrico
(OpenCascade), tem árvore de operações paramétrica, tem o ambiente Sketcher com
restrições geométricas e cotas, exporta STEP e STL, e a sua API trabalha em milímetro.

E — o que decidiu a escolha para esta aula — existe complemento MCP para ele com a
mesma arquitetura do Blender: um servidor dentro do programa aberto, mais um processo
ponte que fala MCP com o OpenCode.

## 3. O que foi instalado

| Componente | Versão | Papel |
|---|---|---|
| FreeCAD | 1.1.3 (AppImage, jul/2026) | o programa |
| Complemento `FreeCADMCP` | `neka-nat/freecad-mcp` | servidor XML-RPC **dentro** do FreeCAD, porta **9875** |
| Servidor ponte `freecad-mcp` | 0.1.22 | processo separado, fala **stdio** com o OpenCode |

A simetria com o Blender é exata, e é o que a seção 2.2 da apostila descreve para o
caminho `local`:

```
OPENCODE  --stdio-->  freecad-mcp  --XML-RPC 9875-->  FREECAD (complemento)
OPENCODE  --stdio-->  blender-mcp  --socket   9876-->  BLENDER  (complemento)
```

Registro no `opencode.json`, com `"type": "local"`, porque o OpenCode precisa executar um
programa — mesmo critério da seção 3.2.

A entrada do `fusion` **foi mantida no arquivo**, com `"type": "remote"`, a URL
`http://127.0.0.1:27182/mcp` e `"enabled": false`. Ela não conecta nesta máquina, mas
documenta o exercício de registro dos dois tipos, que é o conteúdo da seção 4.3.

## 4. O critério da seção 2.3 — ação e verificação

A apostila estabelece que um servidor MCP só torna a modelagem viável se oferecer
ferramentas de **ação** e de **verificação**. O servidor do FreeCAD atende:

| Grupo | Ferramentas |
|---|---|
| Ação | `create_document`, `create_object`, `edit_object`, `delete_object`, `execute_code`, `execute_code_async`, `insert_part_from_library`, `run_fem_analysis` |
| Verificação | `get_view` (captura do viewport), `get_objects`, `get_object`, `list_documents`, `get_rpc_status` |
| Consulta | `get_parts_list`, `reload_document` |

Como no Fusion, **a modelagem passa por `execute_code`**, e a verificação dimensional é
impressa pelo próprio script — o mesmo procedimento da seção 5.2, sem adaptação.

## 5. Verificado na prática

A peça de teste da seção 4.5 da apostila foi reproduzida no FreeCAD, com o mesmo pedido
e a mesma conferência:

| Etapa | Esperado pela apostila (Fusion) | Obtido no FreeCAD |
|---|---|---|
| Esboço retangular 80 x 40 mm, extrusão de 10 mm | `80.00 x 40.00 x 10.00` | `80.00 x 40.00 x 10.00` ✔ |
| Alterar a cota do comprimento para 100 mm e recalcular | `100.00 x 40.00 x 10.00` | `100.00 x 40.00 x 10.00` ✔ |
| Histórico registra as operações | esboço, extrusão, filete | `['esboco', 'extrusao']` ✔ |
| Exportar STEP e STL | ambos | `ISO-10303-21` (STEP) e STL, ambos gravados ✔ |

O comportamento que a seção 4.5 chama de "o que a modelagem paramétrica oferece e a
poligonal não" — o histórico recalculando a extrusão sobre o esboço alterado — foi
observado, com o mesmo número na saída.

## 6. O que a troca muda, e precisa ficar registrado

**O contraste `local` × `remote` do `opencode.json` enfraquece.** A seção 2.2 usa o Fusion
para mostrar um servidor `remote`, alcançado por HTTP. O FreeCAD é `local`, igual ao
Blender. A distinção continua estudada — a entrada do `fusion` segue no arquivo, e a
tabela da seção 4.8 continua válida como referência —, mas ela não é mais exercitada com
um servidor que conecta de fato. **Esta é a perda real da substituição.**

**A armadilha de unidade muda de natureza.** A apostila avisa (seção 4.5) que a API do
Fusion trabalha em centímetro, o que faz a peça sair dez vezes maior. **A API do FreeCAD
trabalha em milímetro**, então essa armadilha específica não existe aqui. A do Blender
continua existindo, e é a mais severa das duas: a cena é em metro, e o erro é de fator mil.
A exigência do `AGENTS.md` — toda medida devolvida em milímetro — continua valendo, e
continua sendo o que revela o erro na primeira etapa.

**O que o FreeCAD não cobre.** O Fusion integra CAD, CAM e CAE; a geração e simulação de
percurso de ferramenta do Fusion não tem equivalente direto no que foi instalado aqui.
Nada disso é exigido pela Tarefa A, que termina na exportação do STEP e do STL.

**O complemento é de comunidade, não do fabricante.** O do Blender é oficial, publicado
pela Blender Foundation; o do FreeCAD é de terceiro (`neka-nat`), em desenvolvimento
ativo — o último commit é do próprio dia desta instalação. Vale o que a seção 6.1 da
apostila diz sobre avaliar servidor de terceiro: a descrição das ferramentas é o que o
modelo lê a cada mensagem, e foi medida (ver `comparacao.md`).

## 7. O que a troca preserva

O objetivo declarado da aula — verificar por conta própria, e não aceitar de leitura, a
segunda linha da tabela da seção 1.3 — fica intacto. A peça é modelada em um programa
B-Rep com histórico, exportada, apresentada no Blender, e a **mesma cota é alterada duas
vezes**: uma pelo histórico paramétrico, outra na malha. A comparação entre os dois
esforços é a entrega, e ela não depende de a primeira ferramenta se chamar Fusion.
