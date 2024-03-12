import pandas as pd
from countries_list import countries_data, currencies_data, USD_UFX

#####
df = pd.read_excel("etoro-account-statement-1-1-2023-12-31-2023.xlsx", sheet_name='Closed Positions')
df_divi = pd.read_excel("etoro-account-statement-1-1-2023-12-31-2023.xlsx", sheet_name='Dividends')
#####

final_df = pd.read_csv("final_taxes.csv", index_col=0)
tax_df = pd.read_csv("taxes_paid.csv", index_col=0)
capital_gains_df = pd.read_csv("capital_gains.csv", index_col=0)



def paragraph10():
    # calculate the difference in years and check if it's more than 3
    df['Open Date'] = pd.to_datetime(df['Open Date'])
    df['Close Date'] = pd.to_datetime(df['Close Date'])
    df['Over_A_Year'] = df.apply(lambda row: (row['Close Date'] - row['Open Date']) / pd.Timedelta(days=365) > 3, axis=1)

    # Drop all rows where 'Over_A_Year is True
    dropped_rows = df[df['Over_A_Year']==True]

    # Drop these row indices from the DataFrame
    df.drop(dropped_rows.index, inplace=True)

    total_profit = df['Profit(USD)'].sum() * USD_UFX # Total profit in CZK
    total_expenses = df['Amount'].sum() * USD_UFX # Total expenses in CZK
    total_income = (total_profit + total_expenses) # Total income in CZK

    print(f"Celkové zdanitelné příjmy z prodeje cenných papírů: {round(total_income, 1)} "
          f"CZK, Příloha 2, tabulka 2, sloupec 2 Příjmy, řádek 207")
    capital_gains_df.loc["Příjmy", 'Etoro'] = round(total_income, 1)
    print(f"Celkem výdaje spojené s pořízením cenných papírů: {round(total_expenses, 1)} "
          f"CZK, Příloha 2, tabulka 2, sloupec 3 Výdaje, řádek 208")
    capital_gains_df.loc["Výdaje", 'Etoro'] = round(total_expenses, 1)
    print(f"Dílčí základ daně dle §10: {round(total_profit, 1)} CZK, Příloha 2, tabulka 2 Úhrn, řádek 209")
    capital_gains_df.loc["Základ daně", 'Etoro'] = round(total_profit, 1)

def dividend_income(isin):
    dividend_data = df_divi.loc[(df_divi["ISIN"].str[:2] == isin)]
    dividend_net = dividend_data["Net Dividend Received (USD)"]
    withholding_tax = dividend_data["Withholding Tax Amount (USD)"]
    dividend_gross = dividend_net + withholding_tax
    return dividend_gross.sum()

def withholding_tax(isin):
    tax_data = df_divi.loc[(df_divi["ISIN"].str[:2] == isin)]
    withholding_tax = tax_data["Withholding Tax Amount (USD)"]
    return withholding_tax.sum()

def paragraph8():

    divi_all = 0

    for country in countries_data["shortcuts"]:

        divi_one_country = dividend_income(country) * USD_UFX
        tax_one_country = withholding_tax(country) * USD_UFX
        divi_all += divi_one_country

        if divi_one_country > 0:
            country_df = countries_data[countries_data['shortcuts'] == country]
            full_country_name = country_df.iloc[0]['full names']
            print(f"Hrubá hodnota připsaných dividend ze státu {full_country_name} je {divi_one_country.round(1)} CZK")
            final_df.loc[full_country_name, 'Etoro'] = round(divi_one_country, 1)
            print(f"Již zaplacená daň ze státu {full_country_name} je {tax_one_country.round(1)} CZK")
            tax_df.loc[full_country_name, 'Etoro Tax Paid'] = round(tax_one_country, 1)
    print(f"Celková hrubá hodnota připsaných dividend je {divi_all.round(1)} CZK")

print("\n1. Zákon o daních z příjmu §10.\n")
paragraph10()

print("\n1. Příjmy podle §8 ze zdrojů v zahraničí.\n")
paragraph8()

final_df.to_csv('final_taxes.csv', index=True)
tax_df.to_csv('taxes_paid.csv', index=True)
capital_gains_df.to_csv('capital_gains.csv', index=True)