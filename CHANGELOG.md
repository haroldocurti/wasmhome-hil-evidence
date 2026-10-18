# Histórico do pacote de evidências

## v0.1.0 — 18 de outubro de 2026

Primeira versão marcada do pacote público. O piloto continua com 18 execuções válidas, seis atualizações completas por cenário. A publicação acrescenta meios de conferir os resultados existentes; não representa uma nova coleta.

- Tabela individual sanitizada do piloto r8 e cálculo reproduzível dos agregados por cenário.
- Dados e figura da fase diagnóstica r5, apresentados separadamente do piloto e do corte intermediário r7.
- Documentação de proveniência, citação, navegação e correspondência entre resultados e arquivos.
- Orientações distintas para regenerar gráficos, recalcular estatísticas e preparar uma nova coleta.
- Esquemático original e fotografia como referências da montagem, com a topologia dos computadores e da rede.

### Correção de um extremo do tempo de ativação

Na revisão anterior, `bb517d9`, o maior tempo do cenário interpretado no piloto foi publicado como **8,922 s**. O registro individual de `B0001-interp` contém **8.921.206.852 ns**, equivalentes a **8,921206852 s**. O valor apresentado com três casas decimais foi corrigido para **8,921 s** no resumo, na documentação associada e no gráfico.

Os dados individuais de origem foram preservados. A correção não modifica as medianas, os quartis, os denominadores ou as contagens de ativação observada. Ela decorre da conferência do agregado contra as observações individuais.

### Limites desta publicação

O pacote não distribui registros brutos completos, firmware, imagens de flash ou configurações privadas da bancada. A reprodução integral da coleta continua dependente dos componentes descritos no guia. A situação dos direitos de reutilização está documentada em `LICENSING.md`; a marcação de versão e os metadados de citação não concedem uma licença.
