import pandas as pd

countries_shortcuts = ["US", "IE", "FR", "GB", "CH", "NL", "JP", "CA", "LU", "DE", "JE", "ES", "BE", "AT", "PT", "DK"]
countries_full = ["USA", "Irsko", "Francie", "Velká Británie", "Švýcarsko", "Nizozemsko", "Japonsko", "Kanada",
                  "Lucembursko", "Německo", "Jersey", "Španělsko", "Belgie", "Rakousko", "Portugalsko", "Dánsko"]
countries_data = pd.DataFrame({'shortcuts': countries_shortcuts, 'full names': countries_full})

#jednotné kurzy za rok 2023 jsou níže
USD_UFX = 22.14
GBX_UFX = 0.2759
GBP_UFX = GBX_UFX * 100
EUR_UFX = 23.97
CHF_UFX = 24.69
CZK_UFX = 1

currencies_list = ["USD", "GBX", "GBP", "EUR", "CHF", "CZK"]
unified_forex = [USD_UFX, GBX_UFX, GBP_UFX, EUR_UFX, CHF_UFX, CZK_UFX]
currencies_data = pd.DataFrame({'name': currencies_list, 'value': unified_forex})




