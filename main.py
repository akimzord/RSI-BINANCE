import requests
import discord
from discord.ext import commands
import asyncio

# Endpoint da API da Binance para obter dados do ticker
ticker_url = 'https://api.binance.com/api/v3/ticker/price'
# Endpoint da API da Binance para obter dados do RSI
rsi_url = 'https://api.binance.com/api/v3/klines'

# Variável para controlar o tempo de espera entre os envios dos alertas (em segundos)
ALERT_INTERVAL = 10  # 60 segundos = 1 minuto

# Definição do token do bot e do ID do canal
TOKEN = '#'
CHANNEL_ID = '#'

# Variável para controlar o estado do envio de alertas
alert_paused = False

# Função para obter o preço atual da criptomoeda
def get_price(symbol):
    params = {'symbol': symbol}
    response = requests.get(ticker_url, params=params)
    data = response.json()
    return float(data['price'])

# Função para calcular o RSI
def calculate_RSI(symbol, interval, RSI_period):
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': RSI_period + 1
    }
    response = requests.get(rsi_url, params=params)
    data = response.json()

    closes = [float(entry[4]) for entry in data]
    changes = [closes[i] - closes[i-1] for i in range(1, len(closes))]
    gains = [change if change > 0 else 0 for change in changes]
    losses = [-change if change < 0 else 0 for change in changes]

    avg_gain = sum(gains) / RSI_period
    avg_loss = sum(losses) / RSI_period

    RS = avg_gain / avg_loss
    RSI = 100 - (100 / (1 + RS))
    return RSI

# Função para enviar alerta por Discord
async def send_discord_alert(ctx, symbol, price, rsi, condition):
    channel = ctx.bot.get_channel(int(CHANNEL_ID))
    await channel.send(f':warning:ALERTA: O RSI de {symbol} {condition}! Preço: ${price}, RSI: {rsi}')

# Função para o loop principal do programa
async def main_loop(ctx, symbol):
    try:
        print('Iniciando loop principal...')
        while True:
            print('Obtendo preço e RSI...')
            price = get_price(symbol)
            rsi = calculate_RSI(symbol, '15m', 6)

            print(f'Preço atual de {symbol}: ${price}')
            print(f'RSI de 6 períodos (intervalo de 15 minutos): {rsi}')

            # Verificar se o envio de alertas está pausado
            if alert_paused:
                await asyncio.sleep(ALERT_INTERVAL)
                continue

            # Verificar se o RSI ultrapassou 70 e enviar alerta por Discord
            if rsi > 70:
                print('RSI ultrapassou 70. Enviando alerta...')
                await send_discord_alert(ctx, symbol, price, rsi, 'ultrapassou 70')

            # Verificar se o RSI caiu abaixo de 30 e enviar alerta por Discord
            if rsi < 30:
                print('RSI caiu abaixo de 30. Enviando alerta...')
                await send_discord_alert(ctx, symbol, price, rsi, 'caiu abaixo de 30')

            # Espera o intervalo definido antes da próxima verificação
            await asyncio.sleep(ALERT_INTERVAL)

    except Exception as e:
        print("Ocorreu um erro ao processar a solicitação:", e)

# Configuração do bot com intents
intents = discord.Intents.all()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot está online.')

@bot.command()
async def define(ctx, symbol):
    print(f'Símbolo da criptomoeda definido como {symbol}. Iniciando loop principal...')
    await main_loop(ctx, symbol)

@bot.command()
async def pause_alerts(ctx):
    global alert_paused
    alert_paused = not alert_paused
    if alert_paused:
        await ctx.send("Os alertas foram pausados.")
    else:
        await ctx.send("Os alertas foram retomados.")

bot.run(TOKEN)
