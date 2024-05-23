# RSI Alert Bot Discord - Binance

Este é um bot do Discord que envia alertas sobre o índice de força relativa (RSI) de uma criptomoeda específica. O bot obtém dados de preço e RSI da API da Binance e envia alertas no canal do Discord quando o RSI ultrapassa 70 ou cai abaixo de 30.

## Configuração

1. Crie um bot no Discord e obtenha o token. Veja [aqui](https://discord.com/developers/applications) para mais detalhes.
2. Copie o token do bot e substitua o valor de `TOKEN` no script pelo seu token do bot.
3. Obtenha o ID do canal onde os alertas serão enviados e substitua `CHANNEL_ID` pelo ID do canal desejado.

## Uso

### Comandos Disponíveis

- `!define <symbol>`: Define o símbolo da criptomoeda para monitorar (por exemplo, `BTCUSDT`).
- `!pause_alerts`: Pausa ou retoma o envio de alertas.

