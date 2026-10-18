# Dicionário de dados

O arquivo `r8-piloto-issue20-summary.csv` é agregado por cenário; seus campos descrevem seis slots válidos em cada grupo, não linhas individuais. `latency_q1_s` e `latency_q3_s` são os limites do intervalo interquartil publicados no relatório sanitizado. `max_control_gap_s` e `max_telemetry_gap_s` são os maiores intervalos observados entre os seis slots daquele cenário. Os campos de timeout e resposta tardia são contagens do conjunto por cenário.

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

O arquivo `r8-piloto-issue20-transfer.csv` é agregado por cenário e resume seis atualizações completas por linha. Os campos `artifact_bytes` e `manifest_bytes` descrevem o tamanho do artefato e do manifesto servidos; `http_body_bytes_per_update` é a soma dos dois; `http_body_bytes_total` soma os seis corpos HTTP do cenário. Os valores derivam de registros do servidor com respostas completas `200`. Não representam bytes de rede no fio e não incluem cabeçalhos, TLS/TCP/IP ou retransmissões.

| Campo de transferência | Significado |
|---|---|
| `scenario` | Cenário da atualização (`native`, `interp` ou `aot`). |
| `successful_updates` | Número de atualizações completas incluídas no agregado. |
| `artifact` | Nome do arquivo de firmware ou módulo servido. |
| `artifact_bytes` | Tamanho do corpo do artefato, em bytes. |
| `manifest_bytes` | Tamanho do corpo do manifesto servido, em bytes. |
| `http_body_bytes_per_update` | Bytes do artefato mais manifesto em uma atualização. |
| `http_body_bytes_total` | Soma dos bytes de corpos HTTP nas atualizações incluídas. |

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
