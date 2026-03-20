import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# PKI's
# - Pasajeros transportados (Miles de  pasajeros) [5]
# - Ingresos por pasaje (Miles de pesos) [6]

def main():
    df_raw = pd.read_csv('GDL_T1.csv' , header=None)
    
    # (swap rows and columns)
    # Transpose the DataFrame to have dates as columns and variables as rows
    df = df_raw.transpose()
    
    # Define headers
    df.columns = df.iloc[0]  # Set the first row as header
    df = df.drop(df.index[0])  # Drop the first row which is now the header
    
    # Reset index to have a clean DataFrame
    df = df.reset_index(drop=True)
    
    columns = df.columns.tolist()
    numeric_columns = columns[2:]  # Assuming the first two columns are 'Año' and 'Mes'
    
    
    # Get list of df[columns]
    # df_columns = df.columns.tolist()
    # print(f"Columnas en el dataset: {df_columns}")
    
    
    # Convert the numeric columns to numeric type, handling errors with 'coerce' to convert non-numeric values to NaN
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # print(f"Convirtiendo columna '{col}' a numérica...")

    
    # Convert 'Mes' column to numeric using the mapping
    meses_map = {
        'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6,
        'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
    }
    df['Mes'] = df['Mes'].map(meses_map)

    # Variable de clase: 1 si el ingreso por pasaje está por encima de la media global.
    media_ingresos = df['Ingresos por pasaje (Miles de pesos)'].mean()
    df['arriba_ganancia_media'] = np.where(
        df['Ingresos por pasaje (Miles de pesos)'] > media_ingresos,
        1,
        0,
    )
    
    print(df[['Año', 'Mes', 'Ingresos por pasaje (Miles de pesos)', 'arriba_ganancia_media']].head(n=13))
    print(f"Media de ingresos por pasaje: {media_ingresos:.2f}")
    
    # MARK: graficas
    # Dispersion map for 'Pasajeros transportados (Miles de  pasajeros)' vs 'Ingresos por pasaje (Miles de pesos)'
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(
        df['Pasajeros transportados (Miles de  pasajeros)'],
        df['Ingresos por pasaje (Miles de pesos)'],
        c=df['arriba_ganancia_media'],
        cmap='coolwarm',
        alpha=0.8,
        edgecolors='k',
        linewidths=0.3,
    )
    plt.xlabel('Pasajeros transportados (Miles de  pasajeros)')
    plt.ylabel('Ingresos por pasaje (Miles de pesos)')
    plt.title('Dispersion Map por clase (arriba_ganancia_media)')
    handles, _ = scatter.legend_elements()
    plt.legend(handles, ['Debajo o igual a media (0)', 'Arriba de media (1)'], title='Clase')
    plt.show()

if __name__ == "__main__":
    main()
