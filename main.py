import pandas
from countries_list import countries_data

#jednotné kurzy jsou zde https://www.mfcr.cz/assets/cs/media/2023-01-05_Financni-zpravodaj-cislo-1-2023_v02.pdf
USD_UFX = 23.41
GBX_UFX = 0.2872
EUR_UFX = 24.54
CHF_UFX = 24.51

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
    total_income = income("USD")*USD_UFX + income("GBX")*GBX_UFX + income("EUR")*EUR_UFX + income("CHF")*CHF_UFX + income("GBP")*GBX_UFX*100
    total_proft = profit("USD")*USD_UFX + profit("GBX")*GBX_UFX + profit("EUR")*EUR_UFX + profit("CHF")*CHF_UFX + income("GBP")*GBX_UFX*100
    total_expenses = total_income - total_proft
    print(f"Celkové zdanitelné příjmy z prodeje cenných papírů: {total_income:.0f} CZK, Příloha 2, tabulka 2, sloupec 2 Příjmy, řádek 207")
    print(f"Celkem výdaje spojené s pořízením cenných papírů: {total_expenses:.0f} CZK, Příloha 2, tabulka 2, sloupec 3 Výdaje, řádek 208")
    print(f"Dílčí základ daně dle §10: {total_proft:.0f} CZK, Příloha 2, tabulka 2 Úhrn, řádek 209")

def dividend_income(currency, ISIN):
    dividend_data = df.loc[(df["Action"] == "Dividend (Ordinary)") & (df["Currency (Price / share)"] == currency) & (df["ISIN"].str[:2] == ISIN)]
    shares_no = dividend_data["No. of shares"]
    dividend_per_share_net = dividend_data["Price / share"]
    withholding_tax = dividend_data["Withholding tax"]
    dividend_gross = shares_no * dividend_per_share_net + withholding_tax
    return dividend_gross.sum().round(1)

def withholding_tax(currency):
    tax_data = df.loc[(df["Withholding tax"] > 0) & (df["Currency (Price / share)"] == currency)]
    withholding_tax = tax_data["Withholding tax"]
    return withholding_tax.sum().round(1)


def paragraph8():
    dividend_amount = 0
    for country in countries_data["shortcuts"]:
        divi_usd_czk = dividend_income('USD', country) * USD_UFX
        divi_gbx_czk = dividend_income('GBX', country) * GBX_UFX
        divi_gbp_czk = dividend_income('GBP', country) * GBX_UFX * 100
        divi_eur_czk = dividend_income('EUR', country) * EUR_UFX
        divi_chf_czk = dividend_income('CHF', country) * CHF_UFX
        total_dividend = divi_usd_czk + divi_gbx_czk + divi_gbp_czk + divi_eur_czk + divi_chf_czk
        dividend_amount += total_dividend
        if total_dividend != 0:
            country_df = countries_data[countries_data['shortcuts'] == country]
            full_country_name = country_df.iloc[0]['full names']
            print(f"Hrubá hodnota připsaných dividend ze státu {full_country_name} je {total_dividend.round(1)} CZK")
    print(f"Celková hrubá hodnota připsaných dividend je {dividend_amount.round(1)} CZK")

# 1. Zákon o daních z příjmu §10
print("\n1. Zákon o daních z příjmu §10.\n")
paragraph10()

# 2. Příjmy podle §8 ze zdrojů v zahraničí
print("\n1. Příjmy podle §8 ze zdrojů v zahraničí.\n")
paragraph8()











