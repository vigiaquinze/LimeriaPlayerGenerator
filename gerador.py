import csv
import random
import os
import webbrowser
import yaml
from datetime import datetime, timedelta
from jinja2 import Template
import matplotlib.pyplot as plt
import io
import base64

class Pessoa:
    def __init__(self, nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_potencial, posicoes_adicionais, pe):
        self.nome = nome
        self.sobrenome = sobrenome
        self.cor_pele = cor_pele
        self.cidade = cidade
        self.posicao_jogador = posicao_jogador
        self.atributo_essencial = atributo_essencial
        self.data_nascimento = data_nascimento
        self.capacidade_atual = capacidade_atual
        self.capacidade_potencial = capacidade_potencial
        self.posicoes_adicionais = posicoes_adicionais
        self.pe = pe  # Atributo do pé

    @property
    def nome_completo(self):
        return f"{self.nome}{self.sobrenome}"  # Concatenando nome e sobrenome sem espaço

    def __repr__(self):
        return (f"Pessoa(nome={self.nome}, sobrenome={self.sobrenome}, cor_pele={self.cor_pele}, "
                f"cidade={self.cidade}, posicao_jogador={self.posicao_jogador}, "
                f"atributo_essencial={self.atributo_essencial}, data_nascimento={self.data_nascimento}, "
                f"capacidade_atual={self.capacidade_atual}, capacidade_potencial={self.capacidade_potencial}, "
                f"posicoes_adicionais={self.posicoes_adicionais}, pe={self.pe})")

def carregar_lista_de_arquivo(nome_arquivo):
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

def carregar_configuracao_posicoes(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def carregar_probabilidades(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)['probabilidades']

# Carregando listas de nomes e sobrenomes
nomes = carregar_lista_de_arquivo('nomes.csv')
sobrenomes = carregar_lista_de_arquivo('sobrenomes.csv')
cores_pele = ['Clara', 'Escura']  # Apenas duas opções de cor de pele
cidades = ["Abílio Pedro", "Âmago", "Anhanguera", "Caieiras", "Colinas do Engenho", "Crisque", "Odécio Degan", "Equidistante", "Esmeralda", "Geada", "Glória", "Graminha", "Nossa Sra. das Dores", "Nova Liméria", "Planalto", "Roseira", "Santa Adélia", "Vista Alegre"]
posicoes_jogador = ["G", "DD", "DAD", "DE", "DAE", "DC", "MDC", "MC", "MD", "ME", "MOC", "MOE", "MOD", "PL"]
capacidade_potencial = [-8, -85, -9, -95]

# Carregando configurações
configuracao_posicoes = carregar_configuracao_posicoes('posicoes.yaml')
probabilidades = carregar_probabilidades('probabilidades.yaml')

def gerar_data_nascimento():
    start_date = datetime(1994, 1, 1)
    end_date = datetime(2006, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%d/%m/%Y")

def gerar_posicoes_adicionais(posicao_primaria, atributo_essencial):
    atributos_essenciais = configuracao_posicoes['posicoes'][posicao_primaria]['atributos_essenciais']
    posicoes_adicionais = []
    
    if atributo_essencial in atributos_essenciais:
        for posicao, dados in configuracao_posicoes['posicoes'].items():
            if posicao != posicao_primaria:
                if atributo_essencial in dados['atributos_essenciais']:
                    posicoes_adicionais.append(posicao)

    return posicoes_adicionais

def gerar_pe():
    return 'Destro' if random.random() < 0.75 else 'Canhoto'  # 75% destro, 25% canhoto

def gerar_pessoa():
    nome = random.choice(nomes)
    sobrenome = random.choice(sobrenomes)
    cor_pele = random.choice(cores_pele)
    cidade = random.choice(cidades)
    posicao_jogador = random.choice(posicoes_jogador)
    atributo_essencial = random.choice(configuracao_posicoes['posicoes'][posicao_jogador]['atributos_essenciais'])
    data_nascimento = gerar_data_nascimento()
    capacidade_atual = random.randint(120, 155)
    capacidade_possivel = random.choice(capacidade_potencial)
    posicoes_adicionais = gerar_posicoes_adicionais(posicao_jogador, atributo_essencial)
    pe = gerar_pe()
    return Pessoa(nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_possivel, posicoes_adicionais, pe)

def gerar_pessoas_com_probabilidades(n):
    contagem_posicoes = {pos: 0 for pos in probabilidades.keys()}
    pessoas = []

    while len(pessoas) < n:
        pessoa = gerar_pessoa()
        posicao = pessoa.posicao_jogador
        
        # Verifica se a posição já atingiu o mínimo necessário
        if contagem_posicoes[posicao] < probabilidades[posicao]:
            pessoas.append(pessoa)
            contagem_posicoes[posicao] += 1
        else:
            # Se a posição já atingiu o mínimo, tenta outra geração
            continue

    return pessoas

def gerar_grafico_posicoes(contagem_posicoes):
    posicoes = list(contagem_posicoes.keys())
    quantidades = list(contagem_posicoes.values())

    plt.figure(figsize=(10, 6))
    plt.bar(posicoes, quantidades, color='blue')
    plt.xlabel('Posições')
    plt.ylabel('Quantidade')
    plt.title('Quantidade de Posições Geradas')
    plt.xticks(rotation=45)
    
    # Salva a imagem em um objeto de bytes
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    # Codifica a imagem em base64
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()  # Fecha a figura atual
    return f"data:image/png;base64,{img_str}"

def gerar_tabela_html(pessoas, pasta):
    contagem_posicoes = {p.posicao_jogador: 0 for p in pessoas}
    for p in pessoas:
        contagem_posicoes[p.posicao_jogador] += 1

    grafico_base64 = gerar_grafico_posicoes(contagem_posicoes)

    template_html = """
    <html>
    <head>
        <title>Pessoas Geradas</title>
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 8px; text-align: left; }
            tr.G { background-color: lightblue; }
            tr.DD { background-color: lightgreen; }
            tr.DAD { background-color: lightcoral; }
            tr.DE { background-color: lightgoldenrodyellow; }
            tr.DAE { background-color: lightpink; }
            tr.DC { background-color: lightgray; }
            tr.MDC { background-color: lightcyan; }
            tr.MC { background-color: lightseagreen; }
            tr.MD { background-color: lightsalmon; }
            tr.ME { background-color: lightslategray; }
            tr.MOC { background-color: lightsteelblue; }
            tr.MOE { background-color: lightyellow; }
            tr.MOD { background-color: lightgreen; }
            tr.PL { background-color: lightblue; }
        </style>
    </head>
    <body>
        <h1>Lista de Pessoas Geradas</h1>
        <table>
            <tr>
                <th>Nome Completo</th>
                <th>Cor de Pele</th>
                <th>Cidade</th>
                <th>Posição Jogador</th>
                <th>Posições Adicionais</th>
                <th>Atributo Essencial</th>
                <th>Data de Nascimento</th>
                <th>Capacidade Atual</th>
                <th>Capacidade Potencial</th>
                <th>Pé</th>
            </tr>
            {% for pessoa in pessoas %}
            <tr class="{{ pessoa.posicao_jogador }}">
                <td>{{ pessoa.nome_completo }}</td>
                <td>{{ pessoa.cor_pele }}</td>
                <td>{{ pessoa.cidade }}</td>
                <td>{{ pessoa.posicao_jogador }}</td>
                <td>{{ pessoa.posicoes_adicionais | join(', ') }}</td>
                <td>{{ pessoa.atributo_essencial }}</td>
                <td>{{ pessoa.data_nascimento }}</td>
                <td>{{ pessoa.capacidade_atual }}</td>
                <td>{{ pessoa.capacidade_potencial }}</td>
                <td>{{ pessoa.pe }}</td>
            </tr>
            {% endfor %}
        </table>
        <h2>Gráfico de Posições Geradas</h2>
        <img src="{{ grafico_base64 }}" alt="Gráfico de Posições">
    </body>
    </html>
    """

    # Renderizando o template
    template = Template(template_html)
    html_content = template.render(pessoas=pessoas, grafico_base64=grafico_base64)

    # Salvando o HTML em um arquivo
    with open(os.path.join(pasta, 'pessoas_geradas.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Abrindo o arquivo HTML no navegador
    webbrowser.open('file://' + os.path.abspath(os.path.join(pasta, 'pessoas_geradas.html')))

# Gera 50 pessoas e salva na pasta desejada
pessoas_geradas = gerar_pessoas_com_probabilidades(23)
gerar_tabela_html(pessoas_geradas, '.')
