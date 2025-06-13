import os
import pandas as pd

# Define la ruta donde vas a guardar el archivo Excel
FILES_PATH = os.path.join(os.getcwd(),r'Files')

def save_info(new_df):
    file_path = os.path.join(FILES_PATH, 'original_info.xlsx')
    
    # Intentar leer archivo existente
    if os.path.exists(file_path):
        try:
            original_df = pd.read_excel(file_path, engine='openpyxl')
            print(f"Archivo {file_path} leído correctamente.")
        except Exception as e:
            print(f"No se pudo leer '{file_path}': {e}")
            original_df = pd.DataFrame()
    else:
        print(f"No se encontró '{file_path}', se creará uno nuevo.")
        original_df = pd.DataFrame()
    
    # Si querés combinar datos (por ejemplo, concatenar y eliminar duplicados)
    combined_df = pd.concat([original_df, new_df], ignore_index=True)
    
    # Opcional: eliminar filas duplicadas según una columna clave, por ejemplo 'ID'
    if 'ID' in combined_df.columns:
        combined_df.drop_duplicates(subset='ID', inplace=True)
    
    # Guardar el dataframe combinado en Excel
    combined_df.to_excel(file_path, index=False, engine='openpyxl')
    print(f"Datos guardados en '{file_path}' exitosamente.")
