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

# Calcular limites para outliers
def calcular_outliers(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    outliers = series[(series < limite_inferior) | (series > limite_superior)]
    return len(outliers)

# Exibir algumas métricas estatísticas antes e depois do tratamento
analise_original = {
    'Quantidade Média': dados['Quantidade'].mean(),
    'Quantidade Mediana': dados['Quantidade'].median(),
    'Quantidade Moda': dados['Quantidade'].mode()[0] if not dados['Quantidade'].mode().empty else None,
    'Desvio Padrão Quantidade': dados['Quantidade'].std(),
    'Amplitude Quantidade': amplitude(dados['Quantidade']),
    'Assimetria Quantidade': dados['Quantidade'].skew(),
    'Curtose Quantidade': dados['Quantidade'].kurtosis(),
    'Outliers Quantidade': calcular_outliers(dados['Quantidade']),
    'Valor Médio': dados['Valor'].mean(),
    'Valor Mediano': dados['Valor'].median(),
    'Valor Moda': dados['Valor'].mode()[0] if not dados['Valor'].mode().empty else None,
    'Desvio Padrão Valor': dados['Valor'].std(),
    'Amplitude Valor': amplitude(dados['Valor']),
    'Assimetria Valor': dados['Valor'].skew(),
    'Curtose Valor': dados['Valor'].kurtosis(),
    'Outliers Valor': calcular_outliers(dados['Valor']),
    'Total de Registros': len(dados),
    'Registros com Quantidade Negativa': (dados['Quantidade'] < 0).sum(),
    'Registros com ID Cliente ausente': dados['ID Cliente'].isna().sum(),
    'Percentual de Valores Nulos': (dados.isna().sum() / len(dados)) * 100
}

analise_tratada = {
    'Quantidade Média': dados_tratados['Quantidade'].mean(),
    'Quantidade Mediana': dados_tratados['Quantidade'].median(),
    'Quantidade Moda': dados_tratados['Quantidade'].mode()[0] if not dados_tratados['Quantidade'].mode().empty else None,
    'Desvio Padrão Quantidade': dados_tratados['Quantidade'].std(),
    'Amplitude Quantidade': amplitude(dados_tratados['Quantidade']),
    'Assimetria Quantidade': dados_tratados['Quantidade'].skew(),
    'Curtose Quantidade': dados_tratados['Quantidade'].kurtosis(),
    'Outliers Quantidade': calcular_outliers(dados_tratados['Quantidade']),
    'Valor Médio': dados_tratados['Valor'].mean(),
    'Valor Mediano': dados_tratados['Valor'].median(),
    'Valor Moda': dados_tratados['Valor'].mode()[0] if not dados_tratados['Valor'].mode().empty else None,
    'Desvio Padrão Valor': dados_tratados['Valor'].std(),
    'Amplitude Valor': amplitude(dados_tratados['Valor']),
    'Assimetria Valor': dados_tratados['Valor'].skew(),
    'Curtose Valor': dados_tratados['Valor'].kurtosis(),
    'Outliers Valor': calcular_outliers(dados_tratados['Valor']),
    'Total de Registros': len(dados_tratados),
    'Registros com Quantidade Negativa': (dados_tratados['Quantidade'] < 0).sum(),
    'Registros com ID Cliente ausente': dados_tratados['ID Cliente'].isna().sum(),
    'Percentual de Valores Nulos': (dados_tratados.isna().sum() / len(dados_tratados)) * 100
}

# Calcular correlação entre Quantidade e Valor
correlacao_original = dados[['Quantidade', 'Valor']].corr().iloc[0, 1]
correlacao_tratada = dados_tratados[['Quantidade', 'Valor']].corr().iloc[0, 1]

print("Análise Original:", analise_original)
print("Correlação Original entre Quantidade e Valor:", correlacao_original)
print("\nAnálise Tratada:", analise_tratada)
print("Correlação Tratada entre Quantidade e Valor:", correlacao_tratada)

# Salvar o dataset tratado em um novo arquivo CSV
dados_tratados.to_csv('vendas-tratadas.csv', index=False)
