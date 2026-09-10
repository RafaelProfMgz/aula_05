# Comparação — Fusion 360 e Blender

## 0. Como a Tarefa A foi conduzida
- [ ] Pelo servidor MCP do Fusion (seção 4.3)
- [ ] Pela execução manual dos scripts (seção 4.7) — `UTILITIES → ADD-INS → Scripts and Add-Ins`

_Registrar aqui qual dos dois caminhos foi usado, e por quê._

---

## 1. Medição de contexto

Medido em 10/09/2026, com o servidor `blender-mcp` 1.0.2 e o complemento MCP 1.0.0
no Blender 5.2.1 LTS.

| Servidor | Ferramentas | Caracteres (nome + descrição + parâmetros) | Tokens aprox. |
|---|---|---|---|
| Blender (medido nesta instalação) | 26 | 13.231 | ~3.310 |
| Blender (apostila, seção 6.1) | 26 | 15.565 | ~3.900 |
| Fusion 360 (apostila, seção 6.1) | 4 | 20.598 | ~5.150 |
| os dois conectados (apostila) | 30 | 36.163 | ~9.050 |

**Divergência.** O número de ferramentas confere exatamente (26), mas o volume de texto
medido aqui é ~15% menor que o da apostila: 13.231 caracteres contra 15.565. A apostila
declara que os números foram medidos nas versões de setembro de 2026 e que mudam entre
versões — a diferença é compatível com uma revisão das descrições entre a versão usada na
preparação da apostila e a 1.0.2 instalada aqui. A ordem de grandeza se mantém.

As três ferramentas mais caras concentram boa parte do custo, e todas são de consulta à
documentação: `get_python_api_docs` (2.638 caracteres), `search_api_docs` (1.467) e
`search_manual_docs` (1.464) — juntas, 5.569 caracteres, 42% do total. Doze das 26
ferramentas são pares `_for_cli` de outras, o que infla a contagem sem acrescentar
capacidade nova à sessão interativa.

**Janela restante:** _a preencher — com os dois conectados e com um deles desabilitado._

_Falta a medição do Fusion nesta instalação (ver seção 4 abaixo)._

---

## 2. A alteração de cota no Fusion (passo 7)

- **O que foi pedido:** alterar a cota do diâmetro do furo da parede de Ø25 para Ø30 mm
- **O que o histórico recalculou:** _a preencher_
- **Tempo gasto:** _a preencher_
- **Precisou refazer alguma coisa a jusante?** _a preencher_

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

## Anexo — impedimentos encontrados

- **Fusion 360 não roda em Linux.** Esta máquina é Linux (kernel 6.17), e a Autodesk não
  distribui o Fusion 360 para Linux. Como o servidor MCP do Fusion é local e sobe junto com
  o programa (seção 4.2), nem o caminho da seção 4.3 nem o da seção 4.7 são executáveis
  aqui. A entrada `fusion` está registrada corretamente no `opencode.json`, com
  `"type": "remote"` e a URL `http://127.0.0.1:27182/mcp`, mas com `"enabled": false`.
  A Tarefa A depende de uma máquina com Windows ou macOS.
- **O desenho técnico ainda não foi obtido.** `desenho-tecnico-suporte.pdf` precisa ser
  baixado do ambiente virtual para completar o `leitura-do-desenho.md`.

---

## Anexo — como a medição foi feita

`medir-contexto.py`, na raiz do repositório, abre o servidor por stdio, chama
`list_tools` e soma os caracteres de nome, descrição e esquema de parâmetros de cada
ferramenta — que é exatamente o texto apresentado ao modelo em toda chamada:

```
.venv/bin/python medir-contexto.py
```

Para medir o Fusion, o mesmo script serve apontando para o executável do servidor;
como o Fusion é `remote`, a medição de lá exige um cliente HTTP em vez de stdio.
