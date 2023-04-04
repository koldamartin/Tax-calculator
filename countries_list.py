import pandas

countries_shortcuts = ["US", "IE", "FR", "GB", "CH", "NL", "JP", "CA", "LU", "DE", "JE", "ES", "BE", "AT", "PT"]
countries_full = ["USA", "Irsko", "Francie", "Velká Británie", "Švýcarsko", "Nizozemsko", "Japonsko", "Kanada",\
                  "Lucembursko", "Německo", "Jersey", "Španělsko", "Belgie", "Rakousko", "Portugalsko"]
countries_data = pandas.DataFrame({'shortcuts': countries_shortcuts, 'full names': countries_full})

USD_UFX = 23.41
GBX_UFX = 0.2872
GBP_UFX = GBX_UFX * 100
EUR_UFX = 24.54
CHF_UFX = 24.51

currencies_list = ["USD", "GBX", "GBP", "EUR", "CHF"]
unified_forex = [USD_UFX, GBX_UFX, GBP_UFX, EUR_UFX, CHF_UFX ]
currencies_data = pandas.DataFrame({'name': currencies_list, 'value': unified_forex})


# def get_countries_list():
#     ISIN_data = df.loc[~df["ISIN"].isnull()]
#     return ISIN_data["ISIN"].apply(lambda x: x[:2]).unique().tolist()



