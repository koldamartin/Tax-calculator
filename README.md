# Tax calculator - Interactive Brokers, Patria, Etoro, Trading212
Daňové přiznání v ČR se značně liší od podkladů zahraničních brokerů. Tento program umí po načtení csv souborů za daný rok spočítat daně z kapitálových příjmů §10 a ze zahraničních dividend §8. Zahraniční daně jsou počítány pro každou zemi zvlášť, aby se mohl provést daňový odpočet z již zaplacené daně.


## Před použitím
do countries_list.py vypsat jednodné měnové kurzy za daný rok
Do složky kde jsou *py skripty stáhnout csv/excely od brokerů a spárovat název souboru s textem v programu
Pro IBKR a Patrii dopsat hodnoty pro proměnné psané velkým písmem. Jde o řádky které je třeba ručně odstranit.

## a) Jednotlivé výpisy
Pro výpis z vybraného brokera použít notebooky *.ipynb, kde budou výsledné hodnoty vytištěné.

## b) Hromadný výpis pro více brokerů
Pustit skript main.py, a výsledky se vypíšou do tří nově vytvořených csv tabulek.

### Poznámky
Pro Trading212 nefunguje 3letý časový test. (z jednoho csv to nejde poznat)

Pro IBKR se papíry držené víc jak tři roky musí ručně odstranit. (vyplnit proměnnou ROWS_TO_DROP_3YEARS)
