from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

# Caminho do arquivo CSV
file_path = "C:/Users/maren/Desktop/analise_covid/covid_19_clean_complete.csv"

# Verifica se o arquivo existe
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

try:
    data = pd.read_csv(file_path, encoding='utf-8') 
    data['Date'] = pd.to_datetime(data['Date'])
except Exception as e:
    raise ValueError(f"Erro ao carregar o arquivo CSV: {e}")

app = Flask(__name__)

@app.route('/')
def home():
    """Página inicial com informações do dataset"""
    dataset_info = {
        'columns': data.columns.tolist(),
        'rows': len(data),
        'source': 'Dataset disponível no Kaggle: <a href="https://www.kaggle.com/datasets/shriyasingh900/covid19-dataset/data" target="_blank">COVID-19 Dataset</a>'
    }
    return render_template('home.html', dataset_info=dataset_info) 

@app.route('/funcionalidade', methods=['GET', 'POST'])
def funcionalidade():
    """Página de funcionalidade com gráficos"""
    filtered_data = data.copy()
    region = request.form.get('region')

    # Filtra os dados pela região:;
    if region:
        filtered_data = filtered_data[filtered_data['Country/Region'] == region]

    # Gráfico de evolução de casos confirmados
    img_confirmed = BytesIO()
    plt.figure(figsize=(10, 6))
    filtered_data.groupby('Date')['Confirmed'].sum().plot(kind='line', title='Evolução dos Casos Confirmados')
    plt.xlabel('Data')
    plt.ylabel('Casos Confirmados')
    plt.grid()
    plt.tight_layout()
    plt.savefig(img_confirmed, format='png')
    img_confirmed.seek(0)
    graph_url_confirmed = base64.b64encode(img_confirmed.getvalue()).decode()
    plt.close()

    # Gráfico de evolução de mortes
    img_deaths = BytesIO()
    plt.figure(figsize=(10, 6))
    filtered_data.groupby('Date')['Deaths'].sum().plot(kind='line', color='red', title='Evolução das Mortes')
    plt.xlabel('Data')
    plt.ylabel('Mortes')
    plt.grid()
    plt.tight_layout()
    plt.savefig(img_deaths, format='png')
    img_deaths.seek(0)
    graph_url_deaths = base64.b64encode(img_deaths.getvalue()).decode()
    plt.close()

    # Renderiza a página funcionalidade
    return render_template(
        'funcionalidade.html', 
        graph_url_confirmed=graph_url_confirmed, 
        graph_url_deaths=graph_url_deaths,
        regions=data['Country/Region'].unique()
    )

@app.route('/apresentacao')
def apresentacao():
    """Página de apresentação dos membros"""
    membros = [
        {'nome': 'Gabriel Marengoni', 'contribuição': 'Códigos'},
        {'nome': 'Apolo', 'contribuição': 'Apresentação'},
        {'nome': 'Kaio', 'contribuição': 'Apresentação'},
    ]
    return render_template('apresentacao.html', membros=membros)

if __name__ == '__main__':
    app.run(debug=True)

