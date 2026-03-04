import nbformat
import os

nb_path = './01_专项专栏/02_机器学习/09_Project2B_Retail_Sales_Forecasting.ipynb'

if not os.path.exists(nb_path):
    print(f"Error: Notebook not found at {nb_path}")
    exit(1)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Find the cell with the XGBoost training code
target_cell_index = -1
for idx, cell in enumerate(nb.cells):
    if cell.cell_type == 'code' and 'model_xgb = xgb.XGBRegressor' in cell.source:
        target_cell_index = idx
        break

if target_cell_index != -1:
    # Get the source code
    source = nb.cells[target_cell_index].source
    
    # Check if we need to apply the fix
    if 'early_stopping_rounds=50' in source and 'model_xgb.fit(' in source:
        # Move early_stopping_rounds to constructor
        new_source = source.replace(
            "random_state=42\n)",
            "random_state=42,\n    early_stopping_rounds=50\n)"
        )
        
        # Remove from fit()
        new_source = new_source.replace(
            "early_stopping_rounds=50,\n    verbose=100",
            "verbose=100"
        )
        
        nb.cells[target_cell_index].source = new_source
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("Successfully fixed XGBoost early_stopping_rounds usage.")
    else:
        print("Code pattern not found or already fixed.")
else:
    print("XGBoost training cell not found.")
