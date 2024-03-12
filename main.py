import os
import pandas as pd
from countries_list import countries_full

def run_script(script_name):
    try:
        # Check if the file exists
        if os.path.exists(script_name):
            # Execute the script
            os.system(f"python {script_name}")
            print(f"{script_name} executed successfully!")
        else:
            print(f"Error: File '{script_name}' not found.")
    except Exception as e:
        print(f"Error executing {script_name}: {e}")

if __name__ == "__main__":

    final_df = pd.DataFrame(index=countries_full)
    final_df.to_csv('final_taxes.csv', index=True)
    final_df.to_csv('taxes_paid.csv', index=True)
    capital_gains_df = pd.DataFrame(index=["Příjmy", "Výdaje", "Základ daně"])
    capital_gains_df.to_csv('capital_gains.csv', index=True)

    scripts = ["ibkr.py", "etoro.py", "patria.py", "trading.py"]

    for script in scripts:
        run_script(script)

    print("All scripts executed sequentially.")

    final_df = pd.read_csv('final_taxes.csv')
    tax_df = pd.read_csv('taxes_paid.csv')
    capital_gains_df = pd.read_csv('capital_gains.csv')
    # For each row in final_df make a sum of tha values in all columns
    final_df['Total gross dividend'] = round(final_df.sum(axis=1), 1)
    tax_df['Wihholding tax paid'] = round(tax_df.sum(axis=1), 1)
    capital_gains_df['Total'] = round(capital_gains_df.sum(axis=1), 1)
    # Drop all rows where the is value 0 in Total dividend column
    final_df = final_df[final_df['Total gross dividend'] != 0]
    tax_df = tax_df[tax_df['Wihholding tax paid'] != 0]
    final_df.to_csv('final_taxes.csv', index=True)
    tax_df.to_csv('taxes_paid.csv', index=True)
    capital_gains_df.to_csv('capital_gains.csv', index=True)






