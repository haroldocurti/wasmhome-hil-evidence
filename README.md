# WasmHome - dados e evidências experimentais

Este repositório reúne protocolo, bancada, dados sanitizados e análises de uma investigação no ESP32-S3: **a atualização modular com WebAssembly ativa a versão 2? Como o tempo até a primeira resposta correta se compara ao da atualização do firmware nativo?** Os arquivos permitem conferir os resultados publicados; a repetição da coleta física depende de componentes de execução ainda privados.

> **Resultado principal (18/10/2026):** no piloto r8, sob `issue20-v1.0` e perfis schema 2, os 18 slots foram adjudicados como válidos, seis por cenário. Native, interpretado e AOT concluíram 6/6 atualizações cada, com a primeira resposta correta v2 em até 60 s. As medianas observadas foram **14,658 s**, **6,782 s** e **6,146 s**, respectivamente. Os caminhos modulares tiveram menores medianas nesta bancada e neste piloto; a amostra não sustenta comparação confirmatória. A campanha planejada de 30 blocos/90 slots ainda não foi executada.

## Por onde começar

- [Tabela principal da r8: resumo por cenário](data/r8-piloto-issue20-summary.csv) e [18 observações por slot](data/r8-piloto-issue20-slots.csv)
- [Gráfico principal de latência r8](analysis/figures/r8-piloto-18-slots.png) ([SVG](analysis/figures/r8-piloto-18-slots.svg))
- [Índice entre tabelas e figuras do TCC, dados e scripts](EVIDENCE_INDEX.md)
- [Campanhas e estado dos resultados](campaigns/README.md)
- [Piloto r8 concluído](campaigns/r8-piloto-issue20/README.md)
- [Pré-teste físico da resiliência #22](campaigns/issue22-preflight-2026-10-18/README.md)
- [Esquemático e ligações da bancada](hardware/README.md)
- [Resumo público do protocolo issue20-v1.0](protocols/issue20-v1.0-resumo-publico.md)
- [Como preparar e executar uma campanha](reproduce/README.md)
- [Organização dos dados e critérios de publicação](data/README.md)
- [Dicionário de dados](data/dicionario.md)
- [Scripts, comandos e figuras de análise](analysis/README.md)

## Três níveis de reprodução

1. **Regenerar gráficos:** os scripts públicos desenham as figuras a partir dos CSVs publicados. Veja os [comandos e requisitos](analysis/README.md).
2. **Recalcular estatísticas da r8:** a [tabela sanitizada de 18 slots](data/r8-piloto-issue20-slots.csv) e o [script de resumo](analysis/summarize_r8_pilot.py) permitem reconstruir o agregado por cenário. Essa conferência parte das observações publicadas; os registros brutos de origem continuam privados.
3. **Repetir a coleta:** requer revisões identificadas do código do WasmHome, do orquestrador e do observador, além de perfis, firmware, imagem-base e entradas locais da bancada. O [guia](reproduce/README.md) descreve o fluxo e as lacunas de distribuição. Não há repetição externa completa documentada neste pacote.

## O que os resultados permitem dizer até agora

A rodada **r5** completou 18 slots com perfis legados e permanece diagnóstica: interpretado e AOT ativaram a versão 2 em 6/6 tentativas cada; o caminho nativo, em 0/6 dentro do limite de 60 segundos. Isso não qualifica a configuração nativa final.

Os dados sanitizados e o gráfico dessa rodada estão na [ficha r5](campaigns/r5-diagnostica-perfis-legados/README.md). O 0/6 nativo da r5 não caracteriza o nativo sob perfis schema 2.

A rodada **r7** é um corte parcial separado, com perfis schema 2: oito resumos completos de 18 slots no corte de 17/10/2026, v2 observada em 8/8 e adjudicação pendente. Cinco registros têm erro em um desafio UART auxiliar. Não agrupar r7 com r5 ou r8.

A rodada **r8** é o piloto fechado pela issue #20: 18/18 slots válidos, 6/6 atualizações completas em cada cenário, aceites abaixo de 300 ms e primeira v2 correta abaixo de 60 s. Os timeouts e as respostas tardias de controle foram mantidos e relatados; não invalidaram as capturas. A baseline integral foi restaurada e lida de volta após cada slot. Consulte o [resumo por cenário e agenda balanceada](campaigns/r8-piloto-issue20/README.md).

Os registros do servidor também permitem recuperar os tamanhos dos artefatos e dos corpos HTTP servidos em cada atualização. Esses bytes não incluem o overhead de rede; veja a [tabela sanitizada de transferência](data/r8-piloto-issue20-transfer.csv) e seus limites metodológicos.

A campanha planejada de 30 blocos/90 slots permanece não concluída. A r6 parou durante a preparação, antes de produzir um slot experimental válido. O pré-teste físico da resiliência #22 também parou antes de abrir as capturas e não produziu célula experimental; a baseline foi restaurada e verificada. Esse evento é documentado separadamente e não conta como rejeição, trap ou recuperação.

## Estrutura

```text
campaigns/    índice e fichas de cada rodada e pré-teste
protocols/    protocolo público e suas revisões
reproduce/    preparo da bancada e roteiro de execução
data/        dados tabulares sanitizados e dicionário
analysis/    método, tabelas, gráficos e scripts reproduzíveis
hardware/    esquemático, montagem e topologia experimental
```

## Limites de reprodução

Os detalhes necessários para executar a bancada dependem de revisões identificadas do código do WasmHome, do orquestrador HIL e do observador, dos artefatos de firmware e de entradas privadas da bancada. Este repositório ainda não contém esses executáveis nem imagens de firmware. O guia de reprodução documenta o fluxo e o que precisa ser disponibilizado para repetir a coleta.

Os registros brutos, imagens integrais da flash, credenciais, chaves, endereços locais, identificadores de sessão e perfis privados não devem ser publicados aqui. A publicação usa resumos sanitizados com proveniência suficiente para interpretar cada resultado.

## Rastreamento

As campanhas se relacionam às issues [#20 - piloto e protocolo](https://github.com/haroldocurti/wasmhome/issues/20), [#21 - campanha normal](https://github.com/haroldocurti/wasmhome/issues/21) e [#24 - análise e publicação](https://github.com/haroldocurti/wasmhome/issues/24) do repositório de implementação.

Consulte [CITATION.cff](CITATION.cff), [LICENSING.md](LICENSING.md) e [CHANGELOG.md](CHANGELOG.md) para identificar e citar esta versão e verificar as condições de reutilização, ainda pendentes de definição pelos autores.
