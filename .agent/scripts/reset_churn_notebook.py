import json
import os

# Define the relative path to the notebook
file_path = "01_专项专栏/02_机器学习/09_Week2_用户流失预测实战_Pro.ipynb"

# Ensure we are in the root directory
if not os.path.exists(file_path):
    print(f"Error: File not found at {file_path}")
    # Try absolute path just in case
    file_path = "./01_专项专栏/02_机器学习/09_Week2_用户流失预测实战_Pro.ipynb"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified_count = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            
            # Reset Task 1 Part 1: Numeric Conversion
            if "pd.to_numeric(df_clean['TotalCharges']" in source:
                 cell['source'] = [
                    "df_clean = df.copy()\n",
                    "\n",
                    "# TODO: 将 'TotalCharges' 转换为数字 (提示: pd.to_numeric, errors='coerce')\n",
                    "# df_clean['TotalCharges'] = ...\n",
                    "# df_clean['MonthlyCharges'] = ...\n"
                 ]
                 cell['execution_count'] = None
                 cell['outputs'] = []
                 modified_count += 1
            
            # Reset Task 1 Part 2: Target Conversion
            elif "df_clean = df_clean.replace(replace_dict)" in source:
                 cell['source'] = [
                    "# TODO: 将 'Churn' (Yes/No) 转换为 1/0\n",
                    "# replace_dict = { ... }\n",
                    "# df_clean = ..."
                 ]
                 cell['execution_count'] = None
                 cell['outputs'] = []
                 modified_count += 1
            
            # Reset Reference Solution
            elif "# --- 完整参考代码 ---" in source:
                 cell['source'] = [
                    "# 参考答案已隐藏，请先尝试自己完成！\n",
                    "# (如果实在卡住，可以申请查看 task.md 中的提示)"
                 ]
                 cell['execution_count'] = None
                 cell['outputs'] = []
                 modified_count += 1

            # Clear Optuna and SHAP if they have code (optional, but good for 0-1)
            # The previous view showed they were mostly TODOs, but let's be safe
            
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        
    print(f"Successfully reset {modified_count} cells in {file_path}")

except Exception as e:
    print(f"Failed to reset notebook: {e}")
