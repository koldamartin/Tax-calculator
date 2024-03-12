import pandas as pd
from countries_list import countries_data, currencies_data, USD_UFX

#####
# CAPITAL GAINS EXCEL
ROWS_TO_DROP_TOP_CAP = 6
ROWS_TO_DROP_BOTTOM_CAP = 9
# DIVIDEND EXCEL
ROWS_TO_DROP_TOP_DIV = 5
ROWS_TO_DROP_BOTTOM_DIV = 2
csv_export_divi = "11899766_2023_DIVIDENDY (1).XLSX"
csv_export_cap = "11899766_2023_KALKULACE 1.XLSX"
#####

final_df = pd.read_csv("final_taxes.csv", index_col=0)
tax_df = pd.read_csv("taxes_paid.csv", index_col=0)
capital_gains_df = pd.read_csv("capital_gains.csv", index_col=0)
df_divi = pd.read_excel(csv_export_divi, sheet_name="Dividendy", usecols="A:L")
df_cap = pd.read_excel(csv_export_cap, sheet_name="Souhrn", usecols="A:W")



def process_dividend_excel(excel_file, top, bottom):
    excel_file = excel_file.drop(range(0, top)) # Drop the first 5 rows (indexed from 0 to 4)
    num_rows = excel_file.shape[0] # Find the total number of rows
    new_num_rows = num_rows - bottom # Subtract 2 from total number of rows
    excel_file = excel_file[:new_num_rows] # Slice the dataframe to exclude the last 2 rows
    excel_file.columns = excel_file.iloc[0] # Assigning the first row values as column names
    excel_file = excel_file.drop(excel_file.index[0]) # Dropping the first row as it's now column names
    return excel_file

def profit(currency):
    #Filter the dataframe to only include rows with the currency name and the "Market sell" action
    sells_data = df_cap.loc[(df_cap["Měna"] == currency) & (~df_cap["Čistý zisk/ztráta"].isnull())]
    sells = sells_data["Čistý zisk/ztráta"]
    return sells.sum()

def income(currency):
    #Filter the dataframe to only include rows with the currency name and the "Market sell" action
    sells_data = df_cap.loc[(df_cap["Měna"] == currency) & (~df_cap["Příjmy v CZK"].isnull())]
    sells = sells_data["Příjmy"]
    return sells.sum()

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
    capital_gains_df.loc["Příjmy", 'Patria'] = round(total_income, 1)
    print(f"Celkem výdaje spojené s pořízením cenných papírů: {total_expenses:.0f} CZK, Příloha 2, tabulka 2, sloupec 3 Výdaje, řádek 208")
    capital_gains_df.loc["Výdaje", 'Patria'] = round(total_expenses, 1)
    print(f"Dílčí základ daně dle §10: {total_profit:.0f} CZK, Příloha 2, tabulka 2 Úhrn, řádek 209")
    capital_gains_df.loc["Základ daně", 'Patria'] = round(total_profit, 1)

def dividend_income(currency, ISIN):
    dividend_data = df_divi.loc[(df_divi["Měna"] == currency) & (df_divi["ISIN"].str[:2] == ISIN)]
    dividend_gross = dividend_data["Hrubá dividenda"]
    return dividend_gross.sum()

def withholding_tax(currency, ISIN):
    tax_data = df_divi.loc[(df_divi["Měna"] == currency) & (df_divi["ISIN"].str[:2] == ISIN)]
    withholding_tax = tax_data["Srážková daň"]
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
            print(f"Hrubá hodnota připsaných dividend ze státu {full_country_name} je {round(divi_one_country, 1)} CZK")
            final_df.loc[full_country_name, 'Patria'] = round(divi_one_country, 1)
            print(f"Již zaplacená daň ze státu {full_country_name} je {round(tax_one_country,1)} CZK")
            tax_df.loc[full_country_name, 'Patria Tax Paid'] = round(tax_one_country, 1)
    print(f"Celková hrubá hodnota připsaných dividend je {round(divi_all,1)} CZK")

# 1. Zákon o daních z příjmu §10
print("\n1. Zákon o daních z příjmu §10.\n")
df_cap = process_dividend_excel(df_cap, ROWS_TO_DROP_TOP_CAP, ROWS_TO_DROP_BOTTOM_CAP)
df_cap = pd.concat([df_cap.iloc[:,:6], df_cap.iloc[:,-9:]], axis=1)
paragraph10()


print("\n1. Příjmy podle §8 ze zdrojů v zahraničí.\n")
df_divi = process_dividend_excel(df_divi, ROWS_TO_DROP_TOP_DIV, ROWS_TO_DROP_BOTTOM_DIV)
paragraph8()

final_df.to_csv('final_taxes.csv', index=True)
tax_df.to_csv('taxes_paid.csv', index=True)
capital_gains_df.to_csv('capital_gains.csv', index=True)