# Resumo público do protocolo issue20-v1.0

Este arquivo é um resumo de leitura do protocolo congelado antes do piloto. Ele não substitui a especificação completa nem os artefatos de execução mantidos junto ao código do WasmHome. Revisar com o documento normativo da revisão de código antes de iniciar uma nova coleta.

## Pergunta experimental

Na mesma bancada física, como o tempo e a continuidade do serviço se comportam ao atualizar o controle por três caminhos: firmware nativo, módulo WebAssembly interpretado e módulo WebAssembly compilado para execução AOT?

## O que é comparado

Um único ESP32-S3 executa os cenários `native`, `interp` e `aot`, com o mesmo estímulo de controle, telemetria e observador externo. A ordem dos três cenários é balanceada entre blocos. Cada tentativa começa após restaurar e verificar a mesma imagem-base integral.

## Limites registrados

| Item | Valor | Interpretação |
|---|---:|---|
| Período de controle/observação | 100 ms | Cadência comum aos três cenários. |
| Leitura do sensor | 500 ms | Período de aquisição configurado. |
| Janela estável anterior | 60 s | Exige controles e telemetria válidos antes do disparo. |
| Resposta funcional | 300 ms | Prazo comum para cada resposta correlacionada ao controle. |
| Prazo para observar a versão 2 | 60 s | Conta do disparo até a primeira resposta correta da versão 2. |
| Janela posterior | 30 s | Observação após sucesso ou após o prazo terminal, para registrar recuperação tardia. |
| Piloto inicial | 6 blocos, 18 slots | Uma ocorrência de cada ordem dos três cenários. |
| Mínimo do piloto | 5 atualizações aceitas e terminais por cenário | Aceites recusados ou ausentes não atendem a esse mínimo. |
| Campanha normal planejada | 30 blocos, 90 slots | Plano registrado; não executado até o momento deste resumo. |

O plano de 30 blocos não foi obtido por cálculo de poder estatístico e não deve ser chamado de tamanho “ideal”. A campanha só pode sustentar as conclusões correspondentes aos dados efetivamente coletados e adjudicados.

## O que conta como resultado

O desfecho operacional principal é o sucesso do slot planejado. Também se relata separadamente a taxa de ativação entre atualizações aceitas e com instrumentação válida. Timeout, recusa, atualização aceita sem ativação, resposta tardia, lacuna de sequência e falha do dispositivo são preservados como resultados; nenhum deles é apagado por ser inconveniente.

Um slot só é marcado inválido quando existe evidência de falha do instrumento de medição prevista no protocolo, como interrupção comprovada da captura ou corrupção dos registros. Quando não é possível decidir, usar estado inconclusivo e preservar a evidência.

## Segurança e integridade da bancada

Antes de escrever na placa, confirmar sua identidade, o tamanho da flash e a imagem-base aprovada. Restaurar a imagem-base integral e verificar sua leitura após cada slot. Se identidade, hash ou restauração não puderem ser comprovados, interromper a campanha e registrar a ocorrência. Chaves, credenciais, endereços locais e imagens integrais da flash nunca entram na publicação.
