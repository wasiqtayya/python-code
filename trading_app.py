import streamlit as st
import ccxt
import pandas as pd
import time
from playsound import playsound

api_key = 'iL7fqOxeyiTLe702Pvy3r7cgF7z0ARr2BQ6ADWxyRIndSU4F01STn5dMZ37TXRDm'
api_secret = 'LaveVwhd4QafzNiaik95dOrZKAF4YNADslEJOIU3aOUs9iLtyi78IX3yxpkG3SzG'

binance = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret
})

trading_pairs = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CHF", 
    "NZD/USD", "USD/CAD", "EUR/GBP", "EUR/JPY", "GBP/JPY", 
    "XRP/USDT", "SOL/USDT", "MATIC/USDT", "LTC/USDT", 
    "DOGE/USDT", "BNB/USDT", "XLM/USDT", "TRX/USDT", "EOS/USDT"
]

def fetch_data(pair):
    try:
        ticker = binance.fetch_ticker(pair)
        return ticker['last']
    except Exception as e:
        st.error(f"Error fetching data for {pair}: {str(e)}")
        return None

def trading_signal(pair_data):
    if pair_data is None:
        return "No data"
    price_change_percentage = (pair_data['last'] - pair_data['open']) / pair_data['open'] * 100
    if price_change_percentage > 1:
        return "Buy"
    elif price_change_percentage < -1:
        return "Sell"
    else:
        return "Hold"

def play_alert_sound(signal):
    if signal == "Buy":
        playsound('buy_alert.mp3')
    elif signal == "Sell":
        playsound('sell_alert.mp3')

st.title("Cryptocurrency and Forex Trading Strategy")
st.sidebar.header("Trading Strategy Parameters")

pair = st.sidebar.selectbox("Select Trading Pair", trading_pairs)

st.text("Fetching data every minute...")

while True:
    price = fetch_data(pair)
    st.write(f"**{pair}** Price: {price}")

    if price:
        signal = trading_signal(price)
        st.write(f"Trading Signal: {signal}")

        if signal == "Buy" or signal == "Sell":
            play_alert_sound(signal)

    st.sidebar.header("Historical Data")
    history_button = st.sidebar.button("Fetch Historical Data")

    if history_button:
        ohlcv = binance.fetch_ohlcv(pair, '1h')
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        st.write(df)

    if signal == "Buy":
        st.write("💰 **Buy Now!**")
    elif signal == "Sell":
        st.write("💸 **Sell Now!**")
    else:
        st.write("🔄 **Hold Position!**")

    time.sleep(60)