# Como reproduzir uma campanha

Este roteiro descreve o fluxo. **Esta cópia inicial não contém o código de execução nem imagens de firmware**, portanto ainda não permite que uma pessoa externa rode a bancada só a partir deste repositório. A reprodução completa exige acesso à revisão exata do código do WasmHome ou a uma versão pública equivalente do orquestrador e de suas ferramentas.

## Materiais necessários

- Placa ESP32-S3 e a bancada descrita no protocolo, com observador externo e servidor de artefatos.
- Revisão identificada do código e do orquestrador HIL; registrar o commit e as versões das ferramentas.
- Builds dos três perfis, com bootloader, tabela, aplicação e configurações efetivas correspondentes.
- Imagem-base integral aprovada e perfis com hashes verificados. Esses arquivos são privados e não são distribuídos aqui.
- Ambiente Python/ESP-IDF e ferramenta de gravação nas versões fixadas pela revisão usada.
- Agenda balanceada e protocolo congelados antes de observar resultados.

## Fluxo de execução

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

## Forma do comando

Na revisão que implementa o fluxo, a execução é feita pelo `issue20_hil_orchestrator.py`, com ação `run`, entradas privadas de campanha, perfis, baseline, identidade da placa, conexão serial, host observador e servidor. O comando real deve ser copiado do guia dessa mesma revisão (`docs/orquestrador-hil-issue20.md`) e preenchido localmente. Não publique um comando com MAC, IP, porta serial, caminho de chave, hash da baseline ou caminhos pessoais reais.

Comece com um slot (`--max-slots 1`) e inspecione a captura/restauração antes de autorizar a continuação. Em uma interrupção, a ação `recover` serve para restaurar a baseline; ela não reexecuta o slot. Não rode o orquestrador sobre uma placa diferente da identificada no preflight.

## O que falta para uma reprodução pública completa

- Publicar ou espelhar, com licença aprovada, o orquestrador e as ferramentas necessárias.
- Fixar uma release/commit público e um manifesto de dependências que possa ser instalado por outra pessoa.
- Fornecer uma alternativa segura para a imagem-base e os perfis privados, ou explicar o procedimento para gerar substitutos compatíveis sem expor dados locais.
- Validar este roteiro com uma execução feita por alguém fora da bancada original.

## Referência do piloto r8

O piloto r8 foi executado com o protocolo `issue20-v1.0`, em seis blocos balanceados e 18 slots. A agenda sanitizada e os resultados agregados estão na [ficha da r8](../campaigns/r8-piloto-issue20/README.md). O repositório não contém a imagem-base privada, firmware, capturas brutas ou os detalhes locais necessários para repetir aquela coleta; portanto, esta referência documenta a proveniência e os limites do resultado, não uma execução externa já reproduzida.
