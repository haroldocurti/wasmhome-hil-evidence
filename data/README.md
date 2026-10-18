# Dados

Os dados publicados devem ser tabulares, sanitizados e vinculados a uma campanha identificada. Cada linha representa um slot ou uma tentativa claramente definida pelo protocolo. Manter cada rodada em seu próprio diretório; não concatenar perfis legados e schema 2 como se fossem a mesma condição.

## Slots e resumo por cenário da r8

`r8-piloto-issue20-slots.csv` publica 18 observações individuais sanitizadas, uma por slot, com bloco e ordem preservados para a comparação pareada. Foi extraído diretamente dos resumos do observador (`summary.json` e `slot.json`) e da nota de adjudicação (`operator-adjudication.json`) da campanha privada r8. O estado instrumental e o resultado terminal vêm da adjudicação; a restauração corresponde aos readbacks finais cujo digest coincide com a baseline aprovada. Somente os campos indicados no [dicionário](dicionario.md) foram publicados. Os registros brutos, identificadores internos e caminhos privados continuam fora deste repositório.

`r8-piloto-issue20-summary.csv` contém estatísticas agregadas calculadas dessa tabela pelo [script de resumo](../analysis/summarize_r8_pilot.py). Cada linha representa um **cenário** com seis slots válidos e seis atualizações completas. Os tempos são resumidos por mínimo, mediana, quartis e máximo, com três casas decimais no agregado. As medidas individuais retêm a precisão original dos inteiros em nanossegundos.

Todos os 18 slots foram classificados como válidos, a v2 correta foi observada até 60 s em todos e a janela posterior foi estável. Timeouts e respostas tardias de controle permanecem nos denominadores e são informados no resumo. A agenda balanceada sanitizada e o manifesto de proveniência acompanham a [ficha da r8](../campaigns/r8-piloto-issue20/README.md). Não juntar estes dados à r5 ou ao corte parcial r7.

## Volume de transferência HTTP no piloto

`r8-piloto-issue20-transfer.csv` resume, por cenário, os bytes dos artefatos e manifestos e os bytes dos corpos HTTP servidos em cada atualização concluída. O cálculo usa os registros `server.jsonl` dos 18 slots mantidos no armazenamento privado: cada cenário teve seis respostas completas `200` para o manifesto e seis para o artefato, totalizando 12 respostas. Os registros incluem tamanho, digest, estado HTTP e conclusão da resposta; a tabela pública omite endereços, caminhos locais e identificadores privados.

`http_body_bytes_per_update` soma o artefato e seu manifesto. `http_body_bytes_total` soma os corpos de 12 respostas HTTP daquele cenário, duas para cada uma das seis atualizações. São bytes de corpo HTTP registrados pelo servidor, não uma captura do tráfego total: cabeçalhos HTTP, handshake e overhead TLS/TCP/IP e retransmissões não entram nessa contagem. O caminho nativo transfere a imagem de firmware; os caminhos WebAssembly transferem somente o módulo de controle. Portanto, a tabela descreve o volume observado nesta configuração do piloto e não é uma comparação normalizada de código nem uma medida geral de eficiência de rede.

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
