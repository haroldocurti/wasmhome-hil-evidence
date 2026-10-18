# Bancada experimental

Para identificar os componentes e repetir as ligações da bancada, consulte em sequência a topologia experimental, o **esquemático original** e a fotografia da montagem real. A topologia situa os equipamentos; o esquema fixa os pinos; a foto documenta a realização física.

## Topologia do ambiente experimental

![Diagrama de blocos da bancada, PC observador e CT107 no Proxmox](topologia-experimental.png)

O diagrama separa a placa ESP32-S3, o PC que executou o observador externo e o CT107 hospedado pelo Proxmox. A comunicação UDP/3333 entre a placa e o observador foi verificada nas sessões físicas documentadas; o CT107 é o servidor LXC de artefatos. A placa usou USB para alimentação e serial. O teste ESP32→CT107 registrado em 09/10/2026 usou um endpoint temporário TCP/HTTP; é evidência separada do fluxo UDP e não comprova HTTPS/COSE. Endereços e identificadores de rede foram omitidos.

## Esquemático original e pinagem

![Esquemático original da bancada ESP32-S3 e DS18B20](esquematico-da-bancada.png)

Na ESP32-S3-DevKitC-1, os contatos J1-1 e J1-2 são 3V3; J1-4 é GPIO4, J1-5 é GPIO5, J1-6 é GPIO6 e J1-22 é GND. As ligações indicadas no esquemático original são:

- **DS18B20 VDD (pino 3)** → **J1-1 (3V3)**.
- **DS18B20 DQ (pino 2)** → **J1-4 (GPIO4)**.
- **Resistor de 4,7 kΩ** entre DQ e **J1-2 (3V3)**, como pull-up.
- **DS18B20 GND (pino 1)** → **J1-22 (GND)**.
- **Loopback de controle:** ligação direta entre **J1-5 (GPIO5)** e **J1-6 (GPIO6)**.

A numeração J1 e as funções dos pinos seguem o [guia oficial da ESP32-S3-DevKitC-1 v1.0](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html). No DS18B20 mostrado de frente, com os terminais para baixo, a ordem é pino 1 GND, pino 2 DQ e pino 3 VDD. Confira a revisão da placa e a orientação do sensor antes de reproduzir a montagem.

O DS18B20 fornece a telemetria de temperatura; o loopback GPIO5↔GPIO6 verifica o caminho de controle.

## Foto da montagem real

![Foto da bancada real com ESP32-S3-DevKitC-1 e sensor DS18B20](foto-bancada-real.jpg)

A foto registra a placa ESP32-S3 montada na protoboard, com o cabo USB à direita. Os fios e o resistor aparecem como foram montados. Alguns contatos ficam parcialmente encobertos; por isso, o esquemático original é a referência para conferir as conexões.

## Limites da evidência

A foto documenta a montagem física; o esquema e a topologia explicam pinagem e papéis dos equipamentos. Nenhuma figura, isoladamente, demonstra a validade dos slots. Consulte os [resultados por campanha](../campaigns/README.md), os [dados sanitizados](../data/README.md) e o [guia de reprodução](../reproduce/README.md). O esquemático original fornecido pelo autor está publicado como PNG; registros brutos, firmware e imagem-base permanecem privados.
