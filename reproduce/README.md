# Reprodução das análises e da coleta

Há três tarefas distintas: regenerar as figuras publicadas, recalcular as estatísticas da r8 a partir das 18 observações sanitizadas e executar uma nova coleta na bancada. As duas primeiras usam arquivos deste repositório. A coleta completa exige código, firmware e entradas privadas que ainda não foram distribuídos; nenhuma repetição externa integral está documentada aqui.

## Conferir a análise pública

Execute os comandos abaixo na raiz de uma cópia deste repositório. Os scripts de análise usam a biblioteca padrão do Python; a geração de PNG também usa `rsvg-convert`. O ambiente conferido para esta versão tinha Python 3.14.7 e `rsvg-convert` 2.62.3. A [documentação de análise](../analysis/README.md) detalha os arquivos gerados e os critérios de cálculo.

Para **recalcular o resumo r8** a partir dos slots sanitizados e comparar com o CSV publicado, sem modificá-lo:

```sh
python3 analysis/summarize_r8_pilot.py \
  --csv data/r8-piloto-issue20-slots.csv \
  --check data/r8-piloto-issue20-summary.csv
```

Para gravar uma nova cópia do resumo em outro caminho:

```sh
python3 analysis/summarize_r8_pilot.py \
  --csv data/r8-piloto-issue20-slots.csv \
  --output /tmp/r8-summary-recalculado.csv
```

Para **regenerar a figura r8** a partir do resumo publicado:

```sh
python3 analysis/plot_r8_pilot.py \
  --csv data/r8-piloto-issue20-summary.csv \
  --svg analysis/figures/r8-piloto-18-slots.svg \
  --png analysis/figures/r8-piloto-18-slots.png
```

Esses comandos conferem a tabela sanitizada e suas figuras. A origem dos campos por slot continua nos registros brutos privados; os comandos não auditam essa extração nem repetem a coleta. A [r5 diagnóstica](../campaigns/r5-diagnostica-perfis-legados/README.md) e o [corte r7](../campaigns/r7-piloto-schema2/README.md) têm dados e figuras próprios e não entram no resumo da r8.

## Repetir a coleta física

O fluxo abaixo documenta como a campanha deve ser preparada e executada quando os componentes de execução estiverem disponíveis na revisão efetivamente usada.

### Materiais necessários

- Placa ESP32-S3 e a bancada descrita no protocolo, com observador externo e servidor de artefatos.
- Revisão identificada do código e do orquestrador HIL; registrar o commit e as versões das ferramentas.
- Builds dos três perfis, com bootloader, tabela, aplicação e configurações efetivas correspondentes.
- Imagem-base integral aprovada e perfis com hashes verificados. Esses arquivos são privados e não são distribuídos aqui.
- Ambiente Python/ESP-IDF e ferramenta de gravação nas versões fixadas pela revisão usada.
- Agenda balanceada e protocolo congelados antes de observar resultados.

### Fluxo de execução

1. **Obtenha uma revisão identificada do código.** Não execute uma branch que mudou durante a coleta. Guarde o identificador da revisão e versões de toolchain no manifesto privado da campanha.
2. **Monte e confira a bancada.** Use o [esquemático e a legenda das ligações](../hardware/README.md). Confirme placa, alimentação, sensor, loopback, serial, rede e observador. Nunca copie para um relatório público endereços da rede local ou nomes de credenciais.
3. **Prepare perfis schema 2.** Para `native`, `interp` e `aot`, fixe os artefatos de inicialização e as configurações do mesmo build; valide cada hash. Não reutilize o perfil legado da r5 para alegar qualificação final.
4. **Gere e congele a agenda antes dos ensaios.** Use o utilitário de campanha disponível na revisão escolhida. Preserve a semente, a ordem dos cenários e os IDs de bloco e slot.
5. **Faça o preflight.** Leia a identidade da placa e a flash integral, confirme a imagem-base aprovada e valide comunicação serial, observador, servidor, telemetria e controle. Qualquer divergência fecha a execução antes de gravar.
6. **Execute primeiro um slot.** O orquestrador restaura e verifica a baseline, instala o perfil selecionado, acompanha o serviço e tenta restaurar a baseline ao final. Revise a captura e a restauração antes de avançar.
7. **Continue na ordem congelada.** Use o mesmo manifesto e a mesma agenda; não reordene nem escolha tentativas de reposição pelo resultado. Se a execução for interrompida, use o procedimento de recuperação da mesma revisão; recuperação apenas restaura e não repete automaticamente um ensaio.
8. **Adjudique os registros.** Compare o diário do orquestrador, serial, observador e servidor. Classifique cada slot como válido, inválido ou inconclusivo segundo o protocolo; preserve falhas e resultados tardios.
9. **Analise por rodada e cenário.** Gere taxas com denominadores explícitos, tempos apenas para os eventos observados, lacunas e perdas, e distribuições exploratórias. Não misture r5, o corte parcial r7 e o piloto r8.
10. **Prepare a publicação.** Inclua tabelas sanitizadas, manifesto de proveniência, script de análise e gráficos. Mantenha capturas brutas, dumps de flash, chaves, credenciais e identificadores de rede em armazenamento privado.

### Comando do orquestrador

Na revisão que implementa o fluxo, a execução é feita pelo `issue20_hil_orchestrator.py`, com ação `run`, entradas privadas de campanha, perfis, baseline, identidade da placa, conexão serial, host observador e servidor. O comando real deve ser copiado do guia dessa mesma revisão (`docs/orquestrador-hil-issue20.md`, no repositório de implementação) e preenchido localmente. O [manifesto público da r8](../campaigns/r8-piloto-issue20/manifest.json) informa a revisão do runner registrada no plano e no diário concluído (`315e10feb2ad9d0d0fbca3ef8e42652433a349fb`); os arquivos capturados do observador remoto correspondem byte a byte à mesma revisão. O snapshot de origem dos insumos é `2ee11b678fa4d94f63dba61f25dae3dc764f97b1`, enquanto `8677586605eb800762f83addde4cc69f6f4f1539` integrou o relatório. Confirme os hashes dos perfis e artefatos antes de outra coleta. Não publique um comando com MAC, IP, porta serial, caminho de chave, hash da baseline ou caminhos pessoais reais.

Comece com um slot (`--max-slots 1`) e inspecione a captura/restauração antes de autorizar a continuação. Em uma interrupção, a ação `recover` serve para restaurar a baseline; ela não reexecuta o slot. Não rode o orquestrador sobre uma placa diferente da identificada no preflight.

### O que falta para uma reprodução pública completa

- Publicar ou espelhar, com licença aprovada, o orquestrador e as ferramentas necessárias.
- Fixar uma release/commit público e um manifesto de dependências que possa ser instalado por outra pessoa.
- Fornecer uma alternativa segura para a imagem-base e os perfis privados, ou explicar o procedimento para gerar substitutos compatíveis sem expor dados locais.
- Validar este roteiro com uma execução feita por alguém fora da bancada original.

## Referência do piloto r8

O piloto r8 foi executado com o protocolo `issue20-v1.0`, em seis blocos balanceados e 18 slots. A agenda sanitizada, as [observações por slot](../data/r8-piloto-issue20-slots.csv) e os resultados agregados estão vinculados à [ficha da r8](../campaigns/r8-piloto-issue20/README.md). O repositório não contém a imagem-base privada, firmware, capturas brutas ou os detalhes locais necessários para repetir aquela coleta; esta referência documenta a proveniência e os limites do resultado.
