import pandas as pd

# Carregar o arquivo original
file_path = 'vendas-por-fatura.csv'
dados = pd.read_csv(file_path)

# Converter a coluna "Valor" para float, substituindo a vírgula por ponto
dados['Valor'] = pd.to_numeric(dados['Valor'].str.replace(',', '.'), errors='coerce')

# Remover registros com valores negativos na coluna "Quantidade"
dados_tratados = dados[dados['Quantidade'] >= 0].copy()

# Preencher IDs de clientes ausentes com um valor padrão
dados_tratados['ID Cliente'].fillna(-1, inplace=True)

# Preencher IDs de clientes ausentes com um valor padrão e converter para Int64
dados_tratados['ID Cliente'] = dados_tratados['ID Cliente'].fillna(-1).astype('Int64')

# Exibir algumas métricas estatísticas antes e depois do tratamento
analise_original = {
    'Quantidade Média': dados['Quantidade'].mean(),
    'Quantidade Mediana': dados['Quantidade'].median(),
    'Desvio Padrão Quantidade': dados['Quantidade'].std(),
    'Valor Médio': dados['Valor'].mean(),
    'Valor Mediano': dados['Valor'].median(),
    'Desvio Padrão Valor': dados['Valor'].std(),
    'Total de Registros': len(dados),
    'Registros com Quantidade Negativa': (dados['Quantidade'] < 0).sum(),
    'Registros com ID Cliente ausente': dados['ID Cliente'].isna().sum()
}

analise_tratada = {
    'Quantidade Média': dados_tratados['Quantidade'].mean(),
    'Quantidade Mediana': dados_tratados['Quantidade'].median(),
    'Desvio Padrão Quantidade': dados_tratados['Quantidade'].std(),
    'Valor Médio': dados_tratados['Valor'].mean(),
    'Valor Mediano': dados_tratados['Valor'].median(),
    'Desvio Padrão Valor': dados_tratados['Valor'].std(),
    'Total de Registros': len(dados_tratados),
    'Registros com Quantidade Negativa': (dados_tratados['Quantidade'] < 0).sum(),
    'Registros com ID Cliente ausente': dados_tratados['ID Cliente'].isna().sum()
}

print("Análise Original:", analise_original)
print("Análise Tratada:", analise_tratada)

# Salvar o dataset tratado em um novo arquivo CSV
dados_tratados.to_csv(' vendas-tratadas.csv', index=False)
