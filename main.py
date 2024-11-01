import pandas as pd

# Carregar o arquivo original
file_path = 'vendas-por-fatura.csv'
dados = pd.read_csv(file_path)

# Converter a coluna "Valor" para float, substituindo a vírgula por ponto
dados['Valor'] = pd.to_numeric(dados['Valor'].str.replace(',', '.'), errors='coerce')

# Remover registros com valores negativos na coluna "Quantidade"
dados_tratados = dados[dados['Quantidade'] >= 0].copy()

# Preencher IDs de clientes ausentes com um valor padrão e converter para Int64
dados_tratados['ID Cliente'] = dados_tratados['ID Cliente'].fillna(-1).astype('Int64')

# Função para calcular amplitude
def amplitude(series):
    return series.max() - series.min()

# Exibir algumas métricas estatísticas antes e depois do tratamento
analise_original = {
    'Quantidade Média': dados['Quantidade'].mean(),
    'Quantidade Mediana': dados['Quantidade'].median(),
    'Quantidade Moda': dados['Quantidade'].mode()[0] if not dados['Quantidade'].mode().empty else None,
    'Desvio Padrão Quantidade': dados['Quantidade'].std(),
    'Amplitude Quantidade': amplitude(dados['Quantidade']),
    'Valor Médio': dados['Valor'].mean(),
    'Valor Mediano': dados['Valor'].median(),
    'Valor Moda': dados['Valor'].mode()[0] if not dados['Valor'].mode().empty else None,
    'Desvio Padrão Valor': dados['Valor'].std(),
    'Amplitude Valor': amplitude(dados['Valor']),
    'Total de Registros': len(dados),
    'Registros com Quantidade Negativa': (dados['Quantidade'] < 0).sum(),
    'Registros com ID Cliente ausente': dados['ID Cliente'].isna().sum()
}

analise_tratada = {
    'Quantidade Média': dados_tratados['Quantidade'].mean(),
    'Quantidade Mediana': dados_tratados['Quantidade'].median(),
    'Quantidade Moda': dados_tratados['Quantidade'].mode()[0] if not dados_tratados['Quantidade'].mode().empty else None,
    'Desvio Padrão Quantidade': dados_tratados['Quantidade'].std(),
    'Amplitude Quantidade': amplitude(dados_tratados['Quantidade']),
    'Valor Médio': dados_tratados['Valor'].mean(),
    'Valor Mediano': dados_tratados['Valor'].median(),
    'Valor Moda': dados_tratados['Valor'].mode()[0] if not dados_tratados['Valor'].mode().empty else None,
    'Desvio Padrão Valor': dados_tratados['Valor'].std(),
    'Amplitude Valor': amplitude(dados_tratados['Valor']),
    'Total de Registros': len(dados_tratados),
    'Registros com Quantidade Negativa': (dados_tratados['Quantidade'] < 0).sum(),
    'Registros com ID Cliente ausente': dados_tratados['ID Cliente'].isna().sum()
}

print("Análise Original:", analise_original)
print("Análise Tratada:", analise_tratada)

# Salvar o dataset tratado em um novo arquivo CSV
dados_tratados.to_csv('vendas-tratadas.csv', index=False)
