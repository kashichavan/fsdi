import pandas as pd

# Create a DataFrame with 'name' and 'ph_no' columns
data = {
    'name': ['Ravi', 'Raju'],
    'ph_no': ['9420420420', '9421421421']
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
excel_file = 'students.xlsx'
df.to_excel(excel_file, index=False, engine='openpyxl')

print(f"Excel file '{excel_file}' created successfully.")