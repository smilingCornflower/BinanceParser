from binance import Client
from datetime import datetime, timedelta, timezone
import csv


client = Client('ApiKey', 'SecretKey')


while True:
    symbol = input("Enter a character (for example, BTCUSDT): ")

    exchange_info = client.get_exchange_info()
    symbols = [symbol_info['symbol'] for symbol_info in exchange_info['symbols']]

    if symbol in symbols:
        break
    else:
        print(f"The {symbol} symbol was not found on Binance. Please enter the correct character.")

PATTERN = '%d.%m.%Y'
PATTERN_FULL = '%d.%m.%Y %H:%M'

while True:
    try:
        print('Enter the start date in the format day.month.year: ', end='')
        start_dt = datetime.strptime(input(), PATTERN)
        print('Enter the end date in the format day.month.year: ', end='')
        end_dt = datetime.strptime(input(), PATTERN)
        break
    except ValueError:
        print("Error in the date format. Please enter the date in the correct format.")

with (open('data.csv', 'w', encoding='utf-8', newline='') as data_file):
    writer = csv.writer(data_file, delimiter=';')
    header = ['Time', 'Open Price', 'Close Price', 'Low Price', 'High Price', 'Volume']
    writer.writerow(header)
    interval = Client.KLINE_INTERVAL_1HOUR
    while end_dt >= start_dt:
        end_interval = start_dt + timedelta(days=1)
        klines = client.get_klines(symbol=symbol, interval=interval,
                                   startTime=int(start_dt.timestamp()) * 1000,
                                   endTime=int(end_interval.timestamp()) * 1000)


        if klines:
            for kline in klines:
                start_of_hour = datetime.fromtimestamp(kline[0] / 1000)
                open_price, high_price, low_price, close_price, volume = [round(float(kline[i]), 2) for i in
                                                                          range(1, 6)]
                data_line = [start_of_hour.strftime(PATTERN_FULL), open_price, close_price, low_price, high_price,
                             volume]

                writer.writerow(data_line)
            print(start_dt.strftime(PATTERN))
        else:
            print(f'Для {start_dt.strftime(PATTERN)} not data available. ')
        start_dt = start_dt + timedelta(days=1)


print('The program was completed successfully. ')
input()