# r5 — diagnóstico com perfis legados

**Estado:** coleta concluída (18/18 slots); rodada diagnóstica, não qualificatória.

A r5 executou seis blocos balanceados, com seis oportunidades por cenário (`native`, `interp` e `aot`). Usou perfis anteriores à exigência schema 2 de fixar, para cada cenário, o bootloader, a tabela, o aplicativo e as configurações correspondentes do mesmo build. Por isso, a rodada não demonstra que o caminho nativo final esteja qualificado.

| Cenário | Versão 2 observada até 60 s | Mediana até ativação entre sucessos | Observação |
|---|---:|---:|---|
| Nativo | 0/6 | Não se aplica | As seis atualizações foram aceitas, mas a versão 2 não foi observada no prazo. |
| Interpretado | 6/6 | 6,533 s | Seis ativações observadas. |
| AOT | 6/6 | 7,401 s | Seis ativações observadas. |

Os 18 slots passaram pelas janelas de preparo registradas e não tiveram abort instrumental. Foram observadas três lacunas de sequência no cenário nativo; elas permanecem não resolvidas e não devem ser descritas como ausência de lacunas. Os registros de depuração também mostram `ESP_ERR_INVALID_STATE` após reinicializações no caminho nativo, sem causa-raiz confirmada. Esses fatos não provam, por si só, defeito do observador; o resultado funcional continua sendo 0/6 ativações nativas no prazo.

## Dados e figura

- [Tabela sanitizada por slot](../../data/r5-diagnostica-perfis-legados.csv): 18 observações do resumo local, com bloco e cenário para preservar o pareamento. Os identificadores de tentativa e campanha foram retirados. A coluna `adjudication` continua `pendente` na fonte; as conclusões acima são diagnósticas e não uma adjudicação final.
- [Figura diagnóstica](../../analysis/figures/r5-diagnostica.svg) ([PNG](../../analysis/figures/r5-diagnostica.png)) e [script de geração](../../analysis/plot_r5_diagnostic.py).

Na tabela, a ativação nativa ausente é representada por célula vazia após o prazo de 60 s, sem imputar tempo zero. O código publica os tempos individuais observados em segundos para `interp` e `aot`; a mediana é calculada somente entre ativações observadas. O commit `d09a37bd79b0eec7b370d09b430792a1c98a5de0` constava na fonte local como `source_commit`, mas o conjunto de perfis legados não tem manifesto público de hashes equivalente ao da r8. Os registros brutos permanecem privados.
