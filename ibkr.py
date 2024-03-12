import pandas as pd
from countries_list import countries_data, currencies_data, countries_full

#####
CAP_TOP_ROWS_TO_DROP = 313
CAP_BOTTOM_ROWS_TO_DROP = 406
ROWS_TO_DROP_3YEARS = [13,19,20]
DIVI_TOP_ROWS_TO_DROP = 540
DIVI_BOTTOM_ROWS_TO_DROP = 632
TAX_TOP_ROWS_TO_DROP = 631
TAX_BOTTOM_ROWS_TO_DROP = 701
csv_export = "U6484043_2023_2023.csv"
#####


final_df = pd.read_csv("final_taxes.csv", index_col=0)
tax_df = pd.read_csv("taxes_paid.csv", index_col=0)
capital_gains_df = pd.read_csv("capital_gains.csv", index_col=0)

def process_file(file, first_row, last_row):
    rows_to_skip = list(range(first_row)) + list(range(last_row,50000))
    df = pd.read_csv(file, skiprows=rows_to_skip)
    df.columns = df.iloc[0] # Assigning the first row values as column names
    return df

def get_isin(original_string):
    start_index = original_string.find("(")
    end_index = original_string.find(")")
    result = original_string[start_index + 1:end_index]
    return result

# Clean capital gains csv
df_cap = process_file(csv_export, first_row=CAP_TOP_ROWS_TO_DROP, last_row=CAP_BOTTOM_ROWS_TO_DROP)
df_cap = df_cap.reset_index()
df_cap = df_cap.dropna() # Drop rows with NaN values
df_cap.columns = df_cap.iloc[0] # Assigning the first row values as column names
df_cap = df_cap.drop(df_cap.index[0]) # Dropping the first row as it's now column names
df_cap = df_cap.drop(columns='Code')
# Converting datatype of last 8 columns to float
df_cap[df_cap.columns[-8:]] = df_cap[df_cap.columns[-8:]].astype(float)

# New DataFrame where Quantity is less than or equal to 0
df_sells = df_cap[df_cap["Quantity"] <= 0]

# Manually remove papers held for over 3 years
# 108x IUSN - purchased 03.06.2020
# 40x SEAC - purchased 07.07.2020
# 42x SEAC - purchased 07.09.2020

df_sells_3years = df_sells.drop(ROWS_TO_DROP_3YEARS)

def profit(currency):
    #Filter the dataframe to only include rows with the currency name and the "Market sell" action
    sells_data = df_sells_3years.loc[(df_sells_3years["Currency"] == currency)]
    sells = sells_data["Realized P/L"]
    return sells.sum()

def income(currency):
    income_data = df_sells_3years.loc[(df_sells_3years["Currency"] == currency)]
    income = income_data["Basis"] * (-1)
    return (income).sum()

def paragraph10():
    total_income = 0
    total_profit = 0

    for (index,row) in currencies_data.iterrows():
        one_income = income(row['name']) * row['value']
        one_profit = profit(row['name']) * row['value']
        total_income += one_income
        total_profit += one_profit
    total_expenses = total_income - total_profit
    print(f"Celkové zdanitelné příjmy z prodeje cenných papírů: {total_income:.0f} CZK, Příloha 2, tabulka 2, sloupec 2 Příjmy, řádek 207")
    capital_gains_df.loc["Příjmy", 'IBKR'] = round(total_income, 1)
    print(f"Celkem výdaje spojené s pořízením cenných papírů: {total_expenses:.0f} CZK, Příloha 2, tabulka 2, sloupec 3 Výdaje, řádek 208")
    capital_gains_df.loc["Výdaje", 'IBKR'] = round(total_expenses, 1)
    print(f"Dílčí základ daně dle §10: {total_profit:.0f} CZK, Příloha 2, tabulka 2 Úhrn, řádek 209")
    capital_gains_df.loc["Základ daně", 'IBKR'] = round(total_profit, 1)

# Clean dividends csv
df_divi = process_file(csv_export, first_row=DIVI_TOP_ROWS_TO_DROP, last_row=DIVI_BOTTOM_ROWS_TO_DROP)
df_divi = df_divi.dropna() # Drop rows with NaN values
df_divi = df_divi.drop(df_divi.index[0])
df_divi['ISIN'] = df_divi['Description'].apply(get_isin) # Get isin
df_divi['Amount'] = df_divi['Amount'].astype(float) # Convert Amount to float number

# Clean withholding tax CSV
df_tax = process_file(csv_export, first_row=TAX_TOP_ROWS_TO_DROP, last_row=TAX_BOTTOM_ROWS_TO_DROP)
df_tax = df_tax.reset_index() # Reset index and enumerate it
df_tax = df_tax.drop(columns='Code')
df_tax = df_tax.dropna()
df_tax = df_tax.drop(columns='index') # Drop added 'index' column
df_tax['ISIN'] = df_tax['Description'].apply(get_isin) # Get isin
df_tax = df_tax.drop(df_tax.index[0])
df_tax['Amount'] = df_tax['Amount'].astype(float) # Convert Amount to float number

def dividend_income(currency, ISIN):
    dividend_data = df_divi.loc[(df_divi["Currency"] == currency) & (df_divi["ISIN"].str[:2] == ISIN)]
    dividend_gross = dividend_data["Amount"]
    return dividend_gross.sum()


def withholding_tax(currency, ISIN):
    tax_data = df_tax.loc[(df_tax["Currency"] == currency) & (df_tax["ISIN"].str[:2] == ISIN)]
    withholding_tax = tax_data["Amount"] * (-1)
    return withholding_tax.sum()

def paragraph8():
    divi_all = 0
    for country in countries_data["shortcuts"]:
        divi_one_country = 0
        tax_one_country = 0

        for (index, row) in currencies_data.iterrows():
            divi_one_country_one_currency = dividend_income(row['name'], country) * row['value']
            divi_one_country += divi_one_country_one_currency
            tax_country_one_currency = withholding_tax(row['name'], country) * row['value']
            tax_one_country += tax_country_one_currency
        divi_all += divi_one_country
        if divi_one_country > 0:
            country_df = countries_data[countries_data['shortcuts'] == country]
            full_country_name = country_df.iloc[0]['full names']
            print(f"Hrubá hodnota připsaných dividend ze státu {full_country_name} je {divi_one_country.round(1)} CZK")
            final_df.loc[full_country_name, 'IBKR'] = round(divi_one_country,1)
            print(f"Již zaplacená daň ze státu {full_country_name} je {tax_one_country.round(1)} CZK")
            tax_df.loc[full_country_name, 'IBKR Tax Paid'] = round(tax_one_country, 1)
    print(f"Celková hrubá hodnota připsaných dividend je {divi_all.round(1)} CZK")

# 1. Zákon o daních z příjmu §10
print("\n1. Zákon o daních z příjmu §10.\n")
paragraph10()

# 2. Příjmy podle §8 ze zdrojů v zahraničí
print("\n1. Příjmy podle §8 ze zdrojů v zahraničí.\n")
paragraph8()

final_df.to_csv('final_taxes.csv', index=True)
tax_df.to_csv('taxes_paid.csv', index=True)
capital_gains_df.to_csv('capital_gains.csv', index=True)