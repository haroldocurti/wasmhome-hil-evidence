# Issue #22 — pré-teste físico encerrado sem célula experimental

Em 18/10/2026, a campanha preliminar `issue22-preliminary-20261018-r1` foi encerrada após uma tentativa de preparação. O preflight remoto validou o staging e a leitura integral inicial da baseline aprovada. Uma linha `ENV-SIG` do perfil nativo foi reservada, mas o coletor tentou vincular a porta UDP ao endereço do CT, que não está atribuído à máquina observadora local.

A falha ocorreu antes de abrir as capturas UDP e serial. Não foram observados `fault_request`, `fault_accepted` nem pedido HTTPS para a fixture. Nenhuma outra linha foi iniciada ou repetida. O resultado é **inconclusivo para a injeção de falhas**: não conta como rejeição, trap, recuperação, timeout do dispositivo nem tentativa instrumentada da matriz.

Os artefatos temporários de perfil foram gravados para preparar a linha. Depois da falha, a flash integral de 16 MiB foi restaurada e lida de volta; o SHA-256 coincidiu com a baseline aprovada (`00aa22c35720354383c3d686a14612a7cb2fd99c57cb1ce214d07338c1c167a5`). Não houve escrita ou limpeza direcionada de NVS. Capturas e dumps integrais permanecem no armazenamento privado.

O próximo ensaio exige uma campanha nova, depois de corrigir e verificar a rota do observador para UDP. Esta execução encerrada não deve ser retomada nem repetida. A issue #22 segue aberta; os critérios físicos de recusa, trap, recuperação e continuidade continuam pendentes.

Fonte sanitizada: [relato da tentativa na branch `codex/issue-22-resilience`](https://github.com/haroldocurti/wasmhome/blob/codex/issue-22-resilience/docs/evidence/issue22-hil-2026-10-18-preflight.md). A PR #39 permanece em draft.
