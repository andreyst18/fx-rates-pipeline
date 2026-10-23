import requests
from datetime import date, timedelta


def get_fx_rates(base="USD", quote="EUR", days_back=30):
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)

    url = "https://api.frankfurter.dev/v2/rates"
    params = {
        "from": start_date.isoformat(),
        "to": end_date.isoformat(),
        "base": base,
        "quotes": quote
    }

    print(f'Запрос курсов {base}/{quote} с {start_date} по {end_date}')
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    rates = []
    for item in data:
        rates.append(
            {
                "date": item['date'],
                "base": item['base'],
                "quote": item['quote'],
                "rate": item['rate'],
            }
        )

    print(f'Получено записей: {len(rates)}')
    return rates

if __name__ == '__main__':
    rates = get_fx_rates(base='USD', quote='EUR', days_back=30)
    