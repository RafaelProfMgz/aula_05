# Leitura do desenho — suporte em L

Fonte pretendida: `desenho-tecnico-suporte.pdf` (arquivos/aula05-modelagem-3d)

> ⚠️ **O desenho não foi disponibilizado até o momento da modelagem.** As cotas abaixo
> marcadas como **[apostila]** vêm do texto das seções 5.1 e 5.2, que as cita
> literalmente. As marcadas como **[premissa]** foram fixadas por mim, por serem
> necessárias para fechar a geometria, e estão registradas aqui para serem substituídas
> pelos valores do desenho quando ele chegar. Trocar um valor nesta tabela e repetir a
> etapa correspondente é suficiente — o histórico recalcula o restante.

## Sistema de coordenadas adotado

- Origem no canto da base; **X** = comprimento (100), **Y** = profundidade (50), **Z** = altura
- **Aresta frontal** = a aresta em `Y = 0`
- A parede vertical fica na frente (`Y = 0` a `Y = 10`); o rasgo e a nervura ficam atrás dela

## Tabela de leitura

| Elemento | Cota | Vista | Origem |
| --- | --- | --- | --- |
| Base — comprimento | 100 mm | superior | [apostila] |
| Base — largura | 50 mm | superior | [apostila] |
| Base — espessura | 10 mm | frontal | [apostila] |
| Rasgo oblongo — raio | R7,5 mm | superior | [apostila] |
| Rasgo oblongo — distância entre os centros dos arcos | 25 mm | superior | [apostila] |
| Rasgo oblongo — posição | centrado na largura (X = 50), centro a 40 mm da aresta frontal | superior | [apostila] |
| Rasgo oblongo — profundidade | passante | superior | [apostila] |
| Parede vertical — largura | 40 mm, centrada em X (30 a 70) | frontal | **[premissa]** — imposta pela tangência do R20 (2 × 20 = 40) |
| Parede vertical — espessura | 10 mm | lateral | **[premissa]** |
| Parede vertical — altura total | 70 mm a partir da base | frontal | **[premissa]** |
| Topo da parede — raio | R20, tangente às duas laterais | frontal | [apostila] |
| Furo da parede — diâmetro | Ø25 mm | frontal | [apostila] |
| Furo da parede — centro | concêntrico com o arco do topo: X = 50, Z = 50 | frontal | [apostila] (concentricidade citada na seção 5.2, etapa 5) |
| Nervura — espessura | 8 mm, centrada em X | lateral | **[premissa]** |
| Nervura — comprimento na base | 20 mm (Y = 10 a Y = 30) | lateral | **[premissa]** — limitado para não invadir o rasgo, que começa em Y = 32,5 |
| Nervura — altura | 25 mm acima da base (Z = 10 a Z = 35) | lateral | **[premissa]** |

## Observações da leitura

- **Tangência do topo:** o R20 só é tangente às laterais se a parede tiver exatamente
  40 mm de largura. Essa é a razão da premissa da largura da parede, e não uma escolha
  arbitrária — a seção 5.2, etapa 4, exige "raio, e tangência com as laterais".
- **Concentricidade:** o centro do furo coincide com o centro do arco do topo, conforme a
  etapa 5 da seção 5.2. Com o arco em Z = 50, o furo fica em Z = 50.
- **Conflito evitado:** o rasgo oblongo ocupa Y de 32,5 a 47,5. A nervura foi limitada a
  Y = 30 para não nascer sobre o vazado.
- Escala declarada no desenho: _não disponível_
- Tolerância geral: _não disponível_
