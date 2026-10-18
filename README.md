# WasmHome - dados e evidências experimentais

Este repositório organiza os dados, protocolos, análises e instruções para reproduzir as campanhas do WasmHome em uma bancada com ESP32-S3.

> **Estado dos resultados (18/10/2026):** o piloto r8, sob o protocolo `issue20-v1.0`, concluiu 18/18 slots válidos em seis blocos balanceados, com 6/6 atualizações completas em cada cenário. A v2 foi observada até 60 s em todos. A campanha definitiva de 30 blocos/90 slots continua pendente; esse tamanho é uma decisão de viabilidade descritiva, sem alegação de poder confirmatório.

## Por onde começar

- [Campanhas e estado dos resultados](campaigns/README.md)
- [Piloto r8 concluído](campaigns/r8-piloto-issue20/README.md)
- [Pré-teste físico da resiliência #22](campaigns/issue22-preflight-2026-10-18/README.md)
- [Esquemático e ligações da bancada](hardware/README.md)
- [Resumo público do protocolo issue20-v1.0](protocols/issue20-v1.0-resumo-publico.md)
- [Como preparar e executar uma campanha](reproduce/README.md)
- [Organização dos dados e critérios de publicação](data/README.md)
- [Dicionário de dados](data/dicionario.md)
- [Plano de análise e figura parcial da r7](analysis/README.md)

## O que os resultados permitem dizer até agora

A rodada **r5** completou 18 slots com perfis legados e permanece diagnóstica: interpretado e AOT ativaram a versão 2 em 6/6 tentativas cada; o caminho nativo, em 0/6 dentro do limite de 60 segundos. Isso não qualifica a configuração nativa final.

A rodada **r7** é um corte parcial separado, com perfis schema 2: oito resumos completos de 18 slots no corte de 17/10/2026, v2 observada em 8/8 e adjudicação pendente. Cinco registros têm erro em um desafio UART auxiliar. Não agrupar r7 com r5 ou r8.

A rodada **r8** é o piloto fechado pela issue #20: 18/18 slots válidos, 6/6 atualizações completas em cada cenário, aceites abaixo de 300 ms e primeira v2 correta abaixo de 60 s. Os timeouts e as respostas tardias de controle foram mantidos e relatados; não invalidaram as capturas. A baseline integral foi restaurada e lida de volta após cada slot. Consulte o [resumo por cenário e agenda balanceada](campaigns/r8-piloto-issue20/README.md).

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

Os detalhes necessários para executar a bancada dependem de uma revisão identificada do código do WasmHome, do orquestrador HIL, dos artefatos de firmware e de entradas privadas da bancada. Este repositório ainda não contém esses executáveis nem imagens de firmware. O guia de reprodução documenta os passos e deixa explícito o que precisa ser disponibilizado para que uma pessoa externa consiga repetir o ensaio.

Os registros brutos, imagens integrais da flash, credenciais, chaves, endereços locais, identificadores de sessão e perfis privados não devem ser publicados aqui. A publicação usa resumos sanitizados com proveniência suficiente para interpretar cada resultado.

## Rastreamento

As campanhas se relacionam às issues [#20 - piloto e protocolo](https://github.com/haroldocurti/wasmhome/issues/20), [#21 - campanha normal](https://github.com/haroldocurti/wasmhome/issues/21) e [#24 - análise e publicação](https://github.com/haroldocurti/wasmhome/issues/24) do repositório de implementação.

A licença dos dados e dos materiais deste repositório ainda precisa ser definida pelos autores antes de autorizar reutilização formal. O pacote contém resumos sanitizados, agenda e documentação; registros brutos, dumps de flash e credenciais não estão incluídos.
