import pandas

countries_shortcuts = ["US", "IE", "FR", "GB", "CH", "NL", "JP", "CA", "LU", "DE", "JE", "ES", "BE", "AT", "PT"]
countries_full = ["USA", "Irsko", "Francie", "Velká Británie", "Švýcarsko", "Nizozemsko", "Japonsko", "Kanada",\
                  "Lucembursko", "Německo", "Jersey", "Španělsko", "Belgie", "Rakousko", "Portugalsko"]
countries_data = pandas.DataFrame({'shortcuts': countries_shortcuts, 'full names': countries_full})

currencies_list = ["USD", "GBX", "GBP", "EUR", "CHF"]

# def get_countries_list():
#     ISIN_data = df.loc[~df["ISIN"].isnull()]
#     return ISIN_data["ISIN"].apply(lambda x: x[:2]).unique().tolist()



