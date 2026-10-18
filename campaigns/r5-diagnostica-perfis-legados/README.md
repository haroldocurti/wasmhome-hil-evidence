# r5 — diagnóstico com perfis legados

**Estado:** coleta concluída (18/18 slots); rodada diagnóstica, não qualificatória.

A r5 executou seis blocos balanceados, com seis oportunidades por cenário (`native`, `interp` e `aot`). Usou perfis anteriores à exigência schema 2 de fixar, para cada cenário, o bootloader, a tabela, o aplicativo e as configurações correspondentes do mesmo build. Por isso, a rodada não demonstra que o caminho nativo final esteja qualificado.

| Cenário | Versão 2 observada até 60 s | Mediana até ativação entre sucessos | Observação |
|---|---:|---:|---|
| Nativo | 0/6 | Não se aplica | As seis atualizações foram aceitas, mas a versão 2 não foi observada no prazo. |
| Interpretado | 6/6 | 6,533 s | Seis ativações observadas. |
| AOT | 6/6 | 7,401 s | Seis ativações observadas. |

Os 18 slots passaram pelas janelas de preparo registradas e não tiveram abort instrumental. Foram observadas três lacunas de sequência no cenário nativo; elas permanecem não resolvidas e não devem ser descritas como ausência de lacunas. Os registros de depuração também mostram `ESP_ERR_INVALID_STATE` após reinicializações no caminho nativo, sem causa-raiz confirmada. Esses fatos não provam, por si só, defeito do observador; o resultado funcional continua sendo 0/6 ativações nativas no prazo.

**Material de dados:** tabela pública por slot, manifesto de proveniência e figuras ainda serão acrescentados após revisão de adjudicação e de privacidade. Os registros brutos permanecem privados.
