import pandas
from countries_list import countries_data, currencies_data

df = pandas.read_csv("2022_trading212_tax_report.csv")

def profit(currency):
    sells_data = df.loc[(df["Currency (Price / share)"] == currency) & (~df["Result (CZK)"].isnull())]
    sells = sells_data["Result (CZK)"]
    exchange_rate = pandas.to_numeric(sells_data["Exchange rate"])
    return (sells * exchange_rate).sum()

def income(currency):
    income_data = df.loc[(df["Currency (Price / share)"] == currency) & (~df["Result (CZK)"].isnull())]
    income = income_data["Total (CZK)"]
    exchange_rate = pandas.to_numeric(income_data["Exchange rate"])
    return (income * exchange_rate).sum()

def paragraph10():
    total_income = 0
    total_profit = 0
    # for loop v dataframe lze napsat dvema zpusoby
    # for name, value in zip(currencies_data["name"], currencies_data["value"]):
    #     one_income = income(name) * value
    #     one_profit = profit(name) * value
    for (index,row) in currencies_data.iterrows():
        one_income = income(row['name']) * row['value']
        one_profit = profit(row['name']) * row['value']
        total_income += one_income
        total_profit += one_profit
    total_expenses = total_income - total_profit
    print(f"Celkové zdanitelné příjmy z prodeje cenných papírů: {total_income:.0f} CZK, Příloha 2, tabulka 2, sloupec 2 Příjmy, řádek 207")
    print(f"Celkem výdaje spojené s pořízením cenných papírů: {total_expenses:.0f} CZK, Příloha 2, tabulka 2, sloupec 3 Výdaje, řádek 208")
    print(f"Dílčí základ daně dle §10: {total_profit:.0f} CZK, Příloha 2, tabulka 2 Úhrn, řádek 209")

def dividend_income(currency, ISIN):
    dividend_data = df.loc[(df["Action"] == "Dividend (Ordinary)") & (df["Currency (Price / share)"] == currency) & (df["ISIN"].str[:2] == ISIN)]
    shares_no = dividend_data["No. of shares"]
    dividend_per_share_net = dividend_data["Price / share"]
    withholding_tax = dividend_data["Withholding tax"]
    dividend_gross = shares_no * dividend_per_share_net + withholding_tax
    return dividend_gross.sum().round(1)

def withholding_tax(currency, ISIN):
    tax_data = df.loc[(df["Withholding tax"] > 0) & (df["Currency (Price / share)"] == currency) & (df["ISIN"].str[:2] == ISIN)]
    withholding_tax = tax_data["Withholding tax"]
    return withholding_tax.sum().round(1)

def paragraph8():
    divi_all = 0
    for country in countries_data["shortcuts"]:
        divi_one_country = 0
        tax_one_country = 0
        # for loop v dataframe lze napsat dvema zpusoby
        # for name, value in zip(currencies_data["name"], currencies_data["value"]):
        #     divi_one_country_one_currency = dividend_income(name, country) * value
        #     divi_one_country += divi_one_country_one_currency
        #     tax_country_one_currency = withholding_tax(name, country) * value
        #     tax_one_country += tax_country_one_currency
        for (index,row) in currencies_data.iterrows():
            divi_one_country_one_currency = dividend_income(row['name'], country) * row['value']
            divi_one_country += divi_one_country_one_currency
            tax_country_one_currency = withholding_tax(row['name'], country) * row['value']
            tax_one_country += tax_country_one_currency
        divi_all += divi_one_country
        if divi_one_country > 0:
            country_df = countries_data[countries_data['shortcuts'] == country]
            full_country_name = country_df.iloc[0]['full names']
            print(f"Hrubá hodnota připsaných dividend ze státu {full_country_name} je {divi_one_country.round(1)} CZK")
            print(f"Již zaplacená daň ze státu {full_country_name} je {tax_one_country.round(1)} CZK")
    print(f"Celková hrubá hodnota připsaných dividend je {divi_all.round(1)} CZK")

# 1. Zákon o daních z příjmu §10
print("\n1. Zákon o daních z příjmu §10.\n")
paragraph10()

# 2. Příjmy podle §8 ze zdrojů v zahraničí
print("\n1. Příjmy podle §8 ze zdrojů v zahraničí.\n")
paragraph8()











