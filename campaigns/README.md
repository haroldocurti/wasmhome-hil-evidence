# Campanhas

| Rodada | Perfil | Estado de coleta | Como interpretar |
|---|---|---|---|
| [r5 - diagnóstico com perfis legados](r5-diagnostica-perfis-legados/README.md) | Legado | 18/18 slots concluídos | Diagnóstico; não qualifica o caminho nativo sob schema 2. |
| [r6 - preparação interrompida](r6-preparo-interrompido/README.md) | Schema 2 | Parou antes do primeiro slot válido | Falha de preparação; excluída do denominador experimental. |
| [r7 - piloto schema 2](r7-piloto-schema2/README.md) | Schema 2 | 8/18 com resumo completo; adjudicação pendente | Corte parcial. Ativação v2 observada em 8/8; não é resultado final da campanha. |
| [r8 - piloto concluído da issue #20](r8-piloto-issue20/README.md) | Schema 2; `issue20-v1.0` | 18/18 slots válidos; 6/6 atualizações completas por cenário | Piloto concluído; não substitui a campanha normal de 30 blocos/90 slots. |
| [#22 - pré-teste de resiliência](issue22-preflight-2026-10-18/README.md) | Preparação `ENV-SIG` | Encerrado antes das capturas; sem célula experimental | Inconclusivo para injeção; baseline integral restaurada e verificada. |

## Regras para comparar rodadas

- Não juntar r5, r7 e r8: os perfis e/ou os cortes são diferentes. A r8 é o piloto schema 2 concluído sob o protocolo congelado.
- Uma falha anterior ao envio de uma atualização não é uma tentativa aceita; ainda assim, o resultado operacional do slot deve ser relatado conforme o protocolo.
- Um timeout, uma falha de ativação ou uma resposta funcional perdida não transforma automaticamente o ensaio em falha do instrumento.
- A campanha planejada de 30 blocos/90 slots permanece não executada. Esse número é um plano descritivo registrado, não um tamanho amostral demonstrado como ideal por cálculo de poder.
- A adjudicação precisa apontar quais registros são válidos, inválidos ou inconclusivos e por quê. Não eliminar resultados desfavoráveis.
- Resumo completo do observador não equivale a slot adjudicado. Em r7, a classificação final permanece pendente; na r8, o relatório final classifica as 18 capturas como válidas.
- A tentativa da #22 falhou antes das capturas UDP/serial e antes do pedido de falha. Não contabilizar como rejeição, trap, recuperação ou timeout do dispositivo.
