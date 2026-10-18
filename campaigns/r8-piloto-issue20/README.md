# r8 — piloto HIL concluído da issue #20

**Concluído em 18/10/2026.** A campanha usou o protocolo congelado `issue20-v1.0`, seis blocos balanceados e 18 slots. Todos os 18 foram adjudicados como válidos: native, interp e AOT tiveram 6/6 atualizações aceitas, completas e bem-sucedidas. A primeira resposta correta de v2 apareceu em até 60 s em todos os slots; os aceites ficaram abaixo de 300 ms e todas as janelas posteriores cumpriram o critério de estabilidade.

| Cenário | Slots válidos / completos | Disparo até v2: mínimo; mediana; máximo (s) | IQR (s) | RTT de aceite: mediana; faixa (ms) |
|---|---:|---:|---:|---:|
| Native | 6/6 | 12,975; 14,658; 16,870 | 14,324–15,456 | 5,789; 4,620–6,951 |
| Interp | 6/6 | 4,660; 6,782; 8,922 | 5,168–7,086 | 7,241; 4,819–10,875 |
| AOT | 6/6 | 4,676; 6,146; 7,391 | 5,589–6,736 | 10,849; 4,633–12,692 |

Todos os tempos até v2 ficaram abaixo do limite de 60 s e todos os RTTs de aceite abaixo de 300 ms. As contagens de timeouts/respostas tardias e os maiores intervalos observados foram:

| Cenário | Timeouts de controle | Respostas tardias | Maior lacuna de controle (s) | Maior lacuna de telemetria (s) |
|---|---:|---:|---:|---:|
| Native | 170 | 0 | 2,911 | 2,873 |
| Interp | 94 | 48 | 1,535 | 0,639 |
| AOT | 84 | 48 | 1,525 | 0,302 |

Timeouts e respostas tardias foram preservados nos denominadores e não invalidaram as capturas. A baseline integral de 16 MiB foi restaurada e lida de volta após cada slot. A campanha cumpre o mínimo de cinco atualizações completas por cenário e fecha o piloto; não é a campanha definitiva de 30 blocos/90 slots nem um estudo confirmatório de equivalência ou poder estatístico.

## Arquivos sanitizados

- [Resumo agregado por cenário](../../data/r8-piloto-issue20-summary.csv) — os valores publicados não incluem as observações individuais.
- [Agenda balanceada](schedule.json) — seis permutações, com a semente da campanha.
- [Manifesto e proveniência](manifest.json).
- [Figura de latência](../../analysis/figures/r8-piloto-18-slots.png) ([SVG](../../analysis/figures/r8-piloto-18-slots.svg)) e [script de geração](../../analysis/plot_r8_pilot.py).

## Integridade e limites

- Campanha: `5bb0678a-b17b-4f59-9155-c0885eaef22e`.
- Baseline restaurada: 16 MiB; SHA-256 `00aa22c35720354383c3d686a14612a7cb2fd99c57cb1ce214d07338c1c167a5`.
- SHA-256 da agenda: `52ccaddd2e801f30fa3ffbf5aa527b382bf84f14ce5dd0b406f6ef7e3a7a0d93`.
- SHA-256 da análise sanitizada: `00d84beed4476c6bccb9c9b365d9af43e90d3bc719c1f22d857cf7911c8b615b`.
- SHA-256 do relatório de adjudicação: `571c9cb08ab4eb3ad5bb481e81baf06633f2994c5ac23bb22634bfe793a430a8`.
- Integração pública do relatório e do orquestrador: repositório `wasmhome`, commit [`8677586`](https://github.com/haroldocurti/wasmhome/commit/8677586605eb800762f83addde4cc69f6f4f1539).

Os logs UART, observações UDP/HTTPS, dados por slot e imagens integrais de flash permanecem no armazenamento privado da bancada. O CSV é um resumo descritivo e não permite reconstruir distribuições por slot ou repetir a análise dos registros brutos. Não juntar a r8 aos perfis legados da r5 nem ao corte parcial da r7.
