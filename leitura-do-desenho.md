# Leitura do desenho — suporte em L

Fonte: [`desenho-tecnico-suporte.pdf`](desenho-tecnico-suporte.pdf) — *Exercise-71*, três vistas
ortográficas mais isométrico, cotas em milímetro.

## Sistema de coordenadas adotado

- Origem no canto inferior da base
- **X** = largura (0 a 50) · **Y** = comprimento (0 a 100) · **Z** = altura (0 a 50)
- A parede e a nervura ficam na extremidade **Y = 100**; o rasgo fica na outra metade

## Tabela de leitura

| Elemento | Cota | Vista |
| --- | --- | --- |
| Base — comprimento | 100 mm | superior e a das 100 |
| Base — largura | 50 mm | superior |
| Base — espessura | 10 mm | as duas inferiores |
| Rasgo oblongo — raio | R7,5 mm | superior |
| Rasgo oblongo — distância entre os centros dos arcos | 25 mm | superior (cadeia 15 + 25) |
| Rasgo oblongo — 1º centro, a partir da aresta frontal (Y=0) | 15 mm | superior |
| Rasgo oblongo — 2º centro | Y = 40 mm | superior |
| Rasgo oblongo — posição na largura | X = 25 mm, centrado | superior (cota 25 de 50) |
| Rasgo oblongo — profundidade | passante | superior |
| Parede — espessura | 15 mm (X de 0 a 15) | superior e lateral |
| Parede — comprimento | 50 mm (Y de 50 a 100) | a das 100 |
| Parede — altura | 40 mm acima da base; **50 mm** no total | a das 100 e lateral |
| Canto arredondado — raio | R20, tangente à face Y=50 e ao topo Z=50 | a das 100 |
| Furo — diâmetro | Ø25 mm, eixo ao longo de X | a das 100 |
| Furo — centro, a partir da extremidade Y=100 | 30 mm (cadeia 20 + 10) → Y = 70 | a das 100 |
| Furo — centro, altura sobre o topo da base | 20 mm → Z = 30 | a das 100 |
| Nervura — espessura | 10 mm (Y de 90 a 100) | superior |
| Nervura — cateto na base | 35 mm (X de 15 a 50) | superior (15 + 35) e lateral |
| Nervura — cateto vertical | 40 mm (Z de 10 a 50) | lateral |

## Observações da leitura

- **Concentricidade.** O centro do furo e o centro do arco R20 coincidem em (Y = 70,
  Z = 30). As duas cadeias de cotas fecham no mesmo ponto: 20 + 10 = 30 a partir de
  Y = 100, e 20 acima do topo da base. A parede remanescente entre o furo Ø25 e o arco é
  de 20 − 12,5 = **7,5 mm**.
- **Tangência.** O R20 é um **filete de canto**, não uma meia-lua: encosta na face
  vertical Y = 50 e no topo Z = 50. Com o centro em (70, 30), as duas tangências saem
  exatas.
- **Perpendicularidade.** A parede é uma placa fina em X (15 mm); a nervura é uma placa
  fina em Y (10 mm). As duas são **perpendiculares entre si**, e não paralelas — é o que a
  vista superior mostra ao trazer a nervura como uma faixa de 35 × 10 ao lado do bloco de
  15 × 50 da parede.
- **A vista superior tem duas cadeias horizontais:** 15 + 35 = 50, que separa a espessura
  da parede (15) do cateto da nervura (35).
- Escala declarada no desenho: não indicada.
- Tolerância geral: não indicada.

---

## O que a leitura corrigiu

O desenho só chegou depois da primeira modelagem, que foi feita com premissas tiradas do
texto da apostila. **Cinco delas estavam erradas**, e o registro fica aqui porque a
diferença entre o que se supõe e o que o desenho diz é exatamente o ponto da seção 5.1.

| Elemento | Premissa usada antes | O desenho diz |
|---|---|---|
| Parede | placa de 10 mm atravessando a largura, 40 mm de largura | placa de **15 mm** de espessura em X, 50 mm de comprimento em Y |
| Topo da parede | meia-lua semicircular R20 sobre a largura | **filete de canto** R20 no canto superior do perfil Y-Z |
| Furo | centro no meio da meia-lua | centro em (Y=70, Z=30), 30 da extremidade e 20 acima da base |
| Rasgo | eixo ao longo da largura, centro a 40 mm da aresta frontal | eixo ao longo do **comprimento**, centros em Y=15 e Y=40 |
| Nervura | 8 mm de espessura, catetos 20 × 25 | **10 mm** de espessura, catetos **35 × 40** |

A frase da apostila "com o centro do conjunto a 40 mm da aresta frontal" (seção 5.2,
etapa 2) descreve o **segundo centro de arco**, em Y = 40, e não o centro do conjunto, que
fica em Y = 27,5. O texto da apostila é um exemplo de pedido, não a cota do desenho — e a
tabela de leitura existe justamente para que a cota venha do desenho.

O modelo foi refeito do zero a partir desta tabela. O volume de cada uma das seis etapas
confere com o cálculo analítico com erro menor que 0,05 mm³.
