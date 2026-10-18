# Dicionário de dados

O arquivo `r8-piloto-issue20-slots.csv` contém os 18 slots adjudicados do piloto, em seis blocos pareados. Identificadores de bloco são públicos; identificadores internos, caminhos e registros brutos foram omitidos. As medidas temporais individuais retêm a precisão de nanossegundos da fonte, expressa em segundos com nove casas decimais, ou de nanossegundos expressa em milissegundos com seis casas decimais para o RTT. O valor vazio indica medida ausente, nunca zero.

| Campo individual da r8 | Significado |
|---|---|
| `block_id`, `scenario`, `order_in_block` | Bloco público (`B0001` a `B0006`), cenário e posição na agenda pareada. |
| `pre_window_passed` | Critério da janela antes do disparo satisfeito no resumo do observador. |
| `update_request_accepted`, `accepted_attempt_status`, `slot_success` | Aceite do despacho, resultado da tentativa aceita e resultado terminal do slot registrados na adjudicação. |
| `instrument_status`, `adjudication` | Estado instrumental decidido pelo operador; `adjudication=valid` representa o estado `instrument_status=valid` no registro de adjudicação, independentemente da observação de v2. |
| `v2_observed_within_60s`, `activation_time_s` | Sucesso no prazo e tempo entre envio do disparo e primeira resposta funcional v2 correta, em segundos. |
| `accept_rtt_ms` | RTT da resposta de aceite, em milissegundos. |
| `control_timeout_count`, `late_response_count` | Contagens de timeouts e respostas de controle tardias do slot; as tardias não anulam a ativação observada. |
| `max_control_gap_s`, `max_telemetry_gap_s` | Maiores intervalos observados entre controles e mensagens de telemetria, em segundos. |
| `post_window_status`, `baseline_restored` | Estado da janela posterior e confirmação de readback da baseline aprovada após o slot. |

O arquivo `r8-piloto-issue20-summary.csv` é agregado por cenário a partir da tabela individual; seus campos descrevem seis slots válidos em cada grupo. `activation_q1_s` e `activation_q3_s` são os limites do intervalo interquartil, calculados por interpolação linear inclusiva. `max_control_gap_s` e `max_telemetry_gap_s` são os maiores intervalos entre os seis slots do cenário. Os campos de timeout e resposta tardia são contagens do conjunto por cenário. O script aplica arredondamento decimal a três casas somente ao gerar este agregado.

| Campo da r8 | Significado |
|---|---|
| `scenario` / `scenario_label` | Código e rótulo do cenário (`native`, `interp` ou `aot`). |
| `planned_slots` | Oportunidades agendadas para o cenário. |
| `valid_slots` | Slots classificados como válidos após adjudicação. |
| `complete_successful_updates` | Atualizações aceitas, completas e bem-sucedidas. |
| `v2_within_60s` | Slots em que a primeira resposta v2 correta foi observada no prazo. |
| `activation_min_s`, `activation_median_s`, `activation_q1_s`, `activation_q3_s`, `activation_max_s` | Estatísticas publicadas do tempo entre disparo e primeira v2 correta, em segundos. |
| `accept_rtt_median_ms`, `accept_rtt_min_ms`, `accept_rtt_max_ms` | RTT da resposta de aceite, em milissegundos. |
| `control_timeouts`, `late_responses` | Contagens de timeouts de controle e respostas tardias preservadas no relatório. |
| `max_control_gap_s`, `max_telemetry_gap_s` | Maiores lacunas de controle e telemetria, em segundos. |
| `stable_post_windows`, `baseline_restored_slots` | Quantidade de janelas pós-atualização estáveis e de slots com baseline restaurada/verificada. |

O arquivo `r8-piloto-issue20-transfer.csv` é agregado por cenário e resume seis atualizações completas por linha. Os campos `artifact_bytes` e `manifest_bytes` descrevem o tamanho do artefato e do manifesto servidos; `http_body_bytes_per_update` é a soma dos dois; `http_body_bytes_total` soma os corpos HTTP das seis atualizações, com duas respostas por atualização (12 por cenário). Os valores derivam de registros do servidor com respostas completas `200`. Não representam bytes de rede no fio e não incluem cabeçalhos, TLS/TCP/IP ou retransmissões.

| Campo de transferência | Significado |
|---|---|
| `scenario` | Cenário da atualização (`native`, `interp` ou `aot`). |
| `successful_updates` | Número de atualizações completas incluídas no agregado. |
| `artifact` | Nome do arquivo de firmware ou módulo servido. |
| `artifact_bytes` | Tamanho do corpo do artefato, em bytes. |
| `manifest_bytes` | Tamanho do corpo do manifesto servido, em bytes. |
| `http_body_bytes_per_update` | Bytes do artefato mais manifesto em uma atualização. |
| `http_body_bytes_total` | Soma dos bytes de corpo de 12 respostas HTTP completas nas seis atualizações incluídas. |

O CSV `r5-diagnostica-perfis-legados.csv` registra 18 oportunidades da fase diagnóstica com perfis legados, seis por cenário. A adjudicação está pendente; os campos observados não devem ser interpretados como decisão final de validade. Os tempos ausentes ficam vazios, sem substituição por zero.

| Campo da r5 | Significado |
|---|---|
| `block` | Identificador público do bloco pareado (`B0001` a `B0006`). |
| `scenario` | Cenário `native`, `interp` ou `aot`. |
| `pre_window_passed` | Resultado da janela de preparo registrado pelo observador (`True` ou `False`). |
| `update_request_accepted` | Indica aceite da solicitação de atualização (`1` ou `0`). |
| `v2_observed_within_60s` | Indica observação funcional da v2 correta até 60 s (`1` ou `0`). |
| `activation_time_s` | Tempo observado até a primeira v2 correta, em segundos; vazio quando não houve ativação medida no prazo. |
| `instrument_aborted` | Indica aborto declarado pelo instrumento (`True` ou `False`); `False` não substitui a adjudicação. |
| `adjudication` | Estado da revisão humana (`pendente` nesta tabela). |

O CSV `r7-piloto-schema2-8-slots.csv` registra um corte parcial, não uma campanha encerrada. Campos de ativação descrevem o que o observador registrou; `instrument_status` e `adjudication` descrevem a revisão humana ainda pendente.

| Campo | Significado |
|---|---|
| `campaign_id` | Identificador público da rodada, sem UUID interno. |
| `protocol_version` | Revisão congelada do protocolo. |
| `profile_schema_version` | Versão do esquema dos perfis de firmware. |
| `source_revision` | Commit do código-fonte associado aos artefatos da rodada. |
| `block_id` | Bloco pareado que contém uma oportunidade por cenário. |
| `scenario` | `native`, `interp` ou `aot`. |
| `order_in_block` | Posição do cenário na ordem do bloco. |
| `slot_id` | Oportunidade planejada identificada por bloco e cenário. |
| `observer_state` | Estado final da execução do observador (`complete` neste corte). |
| `pre_window_passed` | Se a janela de preparo satisfez os critérios antes do disparo. |
| `update_request_accepted` | Se houve aceite correlacionado dentro do limite. |
| `v2_observed_within_60s` | Se a primeira resposta funcional correta da versão 2 foi observada até o prazo. |
| `activation_time_s` | Tempo do disparo até a primeira resposta funcional correta da versão 2, em segundos. |
| `control_timeout_count` | Número de respostas de controle que excederam o timeout no resumo observado. |
| `telemetry_unavailable_count` | Número de eventos registrados como telemetria indisponível. |
| `max_control_gap_s` | Maior intervalo observado entre respostas de controle, em segundos. |
| `max_telemetry_gap_s` | Maior intervalo observado entre mensagens de telemetria, em segundos. |
| `instrument_aborted` | Se o observador declarou aborto instrumental. `false` não substitui a adjudicação. |
| `instrument_status` | Estado da revisão da instrumentação; `pending_adjudication` enquanto não houver decisão. |
| `ancillary_uart_challenge` | Resultado registrado para um desafio auxiliar: `session_not_active`, `other_error` ou `none_recorded`. Ausência de erro registrado não prova aprovação do desafio. |
| `adjudication` | Estado da revisão do slot (`pending` neste corte). |

Os valores ausentes não significam zero. A ativação no prazo é uma observação funcional; ela não decide sozinha se todos os requisitos para classificar o slot como válido foram atendidos. A ausência de um slot no CSV significa que ele ainda não tinha resumo final no corte, não que falhou.
