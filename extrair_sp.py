import pandas as pd
import os

def extrair_sp_completo(arquivo_entrada, arquivo_saida):
    chunks = []
    print(f"Lendo {arquivo_entrada}...")
    
    # Lendo o arquivo completo em pedaços (sem filtrar colunas por enquanto)
    reader = pd.read_csv(
        arquivo_entrada, 
        sep=';', 
        encoding='latin-1', 
        chunksize=100000, 
        low_memory=False
    )
    
    for chunk in reader:
        # Filtra apenas linhas de SP
        chunk_sp = chunk[chunk['SG_UF_ESC'] == 'SP'].copy()
        chunks.append(chunk_sp)

    # Une todos os pedaços de SP
    print("Consolidando dados de SP...")
    df_sp = pd.concat(chunks)
    
    df_agrupado = df_sp.groupby('CO_MUNICIPIO_ESC').mean(numeric_only=True).reset_index()
    
    # Salva o arquivo final
    os.makedirs(os.path.dirname(arquivo_saida), exist_ok=True)
    df_agrupado.to_csv(arquivo_saida, index=False)
    print(f"Sucesso! Arquivo gerado: {arquivo_saida}")

if __name__ == "__main__":
    ENTRADA = 'data/raw/RESULTADOS_2024.csv' 
    SAIDA = 'data/processed/enem_sp_completo_agrupado.csv'
    extrair_sp_completo(ENTRADA, SAIDA)