# Dados

Os dados publicados devem ser tabulares, sanitizados e vinculados a uma campanha identificada. Cada linha representa um slot ou uma tentativa claramente definida pelo protocolo. Manter cada rodada em seu próprio diretório; não concatenar perfis legados e schema 2 como se fossem a mesma condição.

## Resumo por cenário da r8

`r8-piloto-issue20-summary.csv` contém estatísticas agregadas do piloto concluído em 18/10/2026, a partir do relatório sanitizado e da nota de adjudicação registrados no repositório de implementação. Cada linha representa um **cenário**, não um slot individual. Há seis slots válidos e seis atualizações completas por cenário; os tempos são resumidos por mínimo, mediana, IQR e máximo. O CSV não substitui os registros por slot, que permanecem privados.

Todos os 18 slots foram classificados como válidos, a v2 correta foi observada até 60 s em todos e a janela posterior foi estável. Timeouts e respostas tardias de controle permanecem nos denominadores e são informados no resumo. A agenda balanceada sanitizada e o manifesto de proveniência acompanham a [ficha da r8](../campaigns/r8-piloto-issue20/README.md). Não juntar estes dados à r5 ou ao corte parcial r7.

## Conjunto r7 no corte parcial

`r7-piloto-schema2-8-slots.csv` contém oito resumos do observador da r7, de 18 slots planejados. Os oito registram pré-janela aprovada, atualização aceita e v2 observada até 60 s. A classificação de validade dos slots está pendente; cinco registros têm um erro em um desafio UART auxiliar. A figura correspondente e o script de geração ficam em `analysis/`.

O corte é descritivo e não substitui a adjudicação nem o relatório final. O CSV exclui dados pessoais e detalhes de rede, IDs internos, caminhos, binários e registros brutos. Não juntar esse arquivo à r5.

## Conjunto mínimo por rodada

- Resumo por slot com cenário, bloco, resultado de preparo, aceite, ativação no prazo, tempo observado, estado do instrumento e adjudicação.
- Manifesto de campanha com versão do protocolo, revisão de código, versões de ferramentas, perfil, agenda, unidade experimental e corte dos dados.
- Nota de adjudicação com causa e evidência para cada exclusão ou incerteza.
- Script de análise e versão do gráfico/tabela derivados desses dados.

## O que fica fora

Não versionar logs UART/JSONL brutos, journal operacional completo, dump de flash, firmware binário, baseline, dados de Wi-Fi, MAC, IP privado, portas locais, nomes de host, caminhos pessoais, chaves ou credenciais. Conservar os originais em armazenamento controlado e publicar somente resumos com os campos necessários à análise.
