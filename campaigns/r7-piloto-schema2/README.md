# r7 - piloto com perfis schema 2

**Estado no corte de 17/10/2026:** oito dos 18 slots planejados têm resumo completo do observador. A execução geral continua, e os slots ainda não foram adjudicados. Os dados abaixo são um corte parcial.

A r7 aplica a preparação schema 2, que exige correspondência entre bootloader, tabela, aplicativo e configurações geradas para cada perfil de firmware. Ela permanece separada da r5, que usou perfis legados.

## Resultado observado até o corte

| Cenário | Resumos completos / planejados | v2 observada até 60 s | Tempo até v2 (s) | Maior intervalo de controle (s) | Maior intervalo de telemetria (s) |
|---|---:|---:|---:|---:|---:|
| Nativo | 3/6 | 3/3 | 13,792-16,608 | 3,203-5,090 | 3,214-4,968 |
| Interpretado | 3/6 | 3/3 | 4,630-6,909 | 1,423-1,513 | 0,157-0,269 |
| AOT | 2/6 | 2/2 | 5,890-7,392 | 1,519-1,523 | 0,146-0,327 |

As oito janelas anteriores ao disparo foram aprovadas e os oito pedidos foram aceitos. Em todos os oito resumos, o observador registrou a versão 2 dentro do limite de 60 s. Os maiores intervalos de controle e telemetria observados foram mais longos nos três slots nativos deste corte; com amostra pequena, execução incompleta e adjudicação pendente, isso é apenas uma descrição dos registros, não uma conclusão de superioridade ou causalidade.

Cinco dos oito registros contêm erro de transporte ao tentar um desafio UART auxiliar, com a mensagem de que a sessão do observador já não estava ativa. O observador não marcou esses ensaios como abortados. Esse evento não apaga a observação de v2 nem invalida automaticamente o slot; os oito seguem com classificação pendente até a revisão da evidência.

## Arquivos sanitizados

- [CSV por slot](../../data/r7-piloto-schema2-8-slots.csv)
- [Manifesto de proveniência](manifest.json)
- [Figura parcial](../../analysis/figures/r7-piloto-schema2-corte-8-slots.png) ([SVG](../../analysis/figures/r7-piloto-schema2-corte-8-slots.svg))
- [Script para regenerar a figura](../../analysis/plot_r7_partial.py)

O CSV não inclui UUIDs internos, endereços IP/MAC, nomes de host, caminhos locais, credenciais, logs brutos ou binários. Os resumos brutos e artefatos de firmware permanecem em armazenamento controlado.

## Como interpretar

O denominador de ativação apresentado aqui é o dos slots com resumo completo no corte: 3 nativos, 3 interpretados e 2 AOT. Ele não substitui o denominador dos 18 slots planejados. Os dez slots sem resumo final não são classificados como falha por estarem ausentes do CSV. Não combinar este corte com os 18 slots diagnósticos da r5.
