import csv
import random
import os
import webbrowser
import yaml
from datetime import datetime, timedelta
from jinja2 import Template

class Pessoa:
    def __init__(self, nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_potencial, posicoes_adicionais, pe, altura):
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
        self.altura = altura  # Altura em metros

    @property
    def nome_completo(self):
        return f"{self.nome}{self.sobrenome}"  # Concatenando nome e sobrenome sem espaço

    cores_pele = ['Clara', 'Escura']  # Apenas duas opções de cor de pele

    def __repr__(self):
        return (f"Pessoa(nome={self.nome}, sobrenome={self.sobrenome}, cor_pele={self.cor_pele}, "
                f"cidade={self.cidade}, posicao_jogador={self.posicao_jogador}, "
                f"atributo_essencial={self.atributo_essencial}, data_nascimento={self.data_nascimento}, "
                f"capacidade_atual={self.capacidade_atual}, capacidade_potencial={self.capacidade_potencial}, "
                f"posicoes_adicionais={self.posicoes_adicionais}, pe={self.pe}, altura={self.altura})")

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

# Definindo as posições do jogador
posicoes_jogador = ["G", "DD", "DC", "DE", "DAD", "MDC", "DAE", "MD", "MC", "ME", "MOD", "MOC", "MOE", "PL"]

# Carregando listas de nomes e sobrenomes
nomes = carregar_lista_de_arquivo('nomes.csv')
sobrenomes = carregar_lista_de_arquivo('sobrenomes.csv')
cidades = ["Abílio Pedro", "Âmago", "Anhanguera", "Caieiras", "Colinas do Engenho", "Odécio Degan", "Equidistante", "Esmeralda", "Geada", "Glória", "Graminha", "Nossa Sra. das Dores", "Nova Liméria", "Planalto", "Roseira", "Santa Adélia", "Vista Alegre"]
capacidade_potencial = [-8, -85, -9, -95]

# Carregando configurações
configuracao_posicoes = carregar_configuracao_posicoes('posicoes.yaml')
probabilidades = carregar_probabilidades('probabilidades.yaml')

def gerar_data_nascimento():
    start_date = datetime(1990, 1, 1)
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

def gerar_altura(posicao_jogador):
    if posicao_jogador == "DC":
        return round(random.uniform(175, 200))  # Defesa Central deve ter entre 175cm e 200cm
    elif posicao_jogador == "G":
        return round(random.uniform(185, 205))  # Goleiro deve ter entre 185cm e 205cm
    elif posicao_jogador == "PL":
        return round(random.uniform(175, 205))  # Ponta de lança deve ter entre 175cm e 205cm
    else:
        return round(random.uniform(160, 190))  # Outras posições entre 160cm e 190cm

def gerar_cor_pele():
    return 'Clara' if random.random() < 0.75 else 'Escura'  # 75% clara, 25% escura

# Definindo limites de jogadores por posição
limites_posicoes = {
    "G": 2,
    "DD": 2,
    "DC": 3,
    "DE": 2,
    "DAD": 0,
    "MDC": 2,
    "DAE": 0,
    "MD": 0,
    "MC": 3,
    "ME": 0,
    "MOD": 2,
    "MOC": 2,
    "MOE": 2,
    "PL": 3
}

# Gera o nome, com a probabilidade de nome composto
def gerar_nome_completo(probabilidade_nome_composto=0.4):
    
    # Gera um nome completo com a possibilidade de ser composto.
    # A probabilidade de ser composto é definida por probabilidade_nome_composto.

    nome = random.choice(nomes)
    
    # Se o nome for composto (de acordo com a probabilidade definida)
    if random.random() < probabilidade_nome_composto:
        segundo_nome = random.choice(nomes)
        nome_completo = f"{nome} {segundo_nome}"
    else:
        nome_completo = nome

    sobrenome = random.choice(sobrenomes)
    return nome_completo, sobrenome


# Gera o jogador
def gerar_pessoa(posicao_jogador, probabilidade_nome_composto=0.4):
    nome, sobrenome = gerar_nome_completo(probabilidade_nome_composto)
    cor_pele = gerar_cor_pele()
    cidade = random.choice(cidades)

    # Obter os atributos essenciais da posição escolhida
    atributos_essenciais = configuracao_posicoes['posicoes'][posicao_jogador]['atributos_essenciais']
    atributo_essencial = random.choice(atributos_essenciais)  # Escolher um atributo essencial a partir da posição

    data_nascimento = gerar_data_nascimento()
    capacidade_atual = random.randint(140, 155)
    capacidade_possivel = random.choice(capacidade_potencial)
    posicoes_adicionais = gerar_posicoes_adicionais(posicao_jogador, atributo_essencial)
    pe = gerar_pe()
    altura = gerar_altura(posicao_jogador)

    return Pessoa(nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_possivel, posicoes_adicionais, pe, altura)


# Gera a lista de jogadores
def gerar_pessoas(n):
    pessoas = []
    contagem_posicoes = {pos: 0 for pos in limites_posicoes.keys()}  # Inicializa contadores de posição

    while len(pessoas) < n:
        # Cria uma lista de posições disponíveis com base nos limites
        posicoes_disponiveis = [pos for pos in posicoes_jogador if contagem_posicoes[pos] < limites_posicoes[pos]]

        if not posicoes_disponiveis:  # Se não há posições disponíveis, saia do loop
            break

        posicao_jogador = random.choices(posicoes_disponiveis, weights=[probabilidades[pos] for pos in posicoes_disponiveis])[0]

        nova_pessoa = gerar_pessoa(posicao_jogador)  # Passa a posição gerada para a função
        pessoas.append(nova_pessoa)
        contagem_posicoes[posicao_jogador] += 1  # Incrementa contador para a posição

    return pessoas

# Cria um dicionário que relaciona cada posição a um índice
indices_posicoes = {pos: i for i, pos in enumerate(posicoes_jogador)}

def ordenar_pessoas_por_posicao(pessoas):
    return sorted(pessoas, key=lambda p: indices_posicoes[p.posicao_jogador])

# Exemplo de uso
def gerar_tabela_html(pessoas, pasta):
    pessoas = ordenar_pessoas_por_posicao(pessoas)

    template_html = """
    <html>
    <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Funnel+Display:wght@300..800&display=swap" rel="stylesheet">
        <title>Pessoas Geradas</title>
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ffffff1c; padding: 8px; text-align: center; font-family: "Funnel Display", monospace;}
            th { font-weight: 900 }
            td { font-weight: 100 }
            thead { background-color: #191220; color: #fff; }
            tr.G { background-color: #38154d; color: #fff; }
            tr.DD { background-color: #1b294b; color: #fff; }
            tr.DAD { background-color: #1c436d; color: #fff; }
            tr.DE { background-color: #1b294b; color: #fff; }
            tr.DAE { background-color: #1c436d; color: #fff; }
            tr.DC { background-color: #1b294b; color: #fff; }
            tr.MDC { background-color: #1c436d; color: #fff; }
            tr.MC { background-color: #2b7a31; color: #fff; }
            tr.MD { background-color: #2b7a31; color: #fff; }
            tr.ME { background-color: #2b7a31; color: #fff; }
            tr.MOC { background-color: #b56503; color: #fff; }
            tr.MOE { background-color: #b56503; color: #fff; }
            tr.MOD { background-color: #b56503; color: #fff; }
            tr.PL { background-color: #771515; color: #fff; }
            tr:hover { background-color: #4b4b4b; }
        </style>
    </head>
    <body>
        <h1>Pessoas Geradas</h1>
        <table>
            <thead>
                <tr>
                    <th>Nome Completo</th>
                    <th>Cor da Pele</th>
                    <th>Altura</th>
                    <th>Data de nascimento</th>
                    <th>Cidade</th>
                    <th>CA</th>
                    <th>CP</th>
                    <th>Melhor pé</th>
                    <th>Posição natural</th>
                    <th>Posições adicionais</th>
                    <th>Atributo especial</th>
                </tr>
            </thead>
            <tbody>
                {% for pessoa in pessoas %}
                    <tr class="{{ pessoa.posicao_jogador }}">
                        <td>{{ pessoa.nome_completo }}</td>
                        <td>{{ pessoa.cor_pele }}</td>
                        <td>{{ pessoa.altura }}</td>
                        <td>{{ pessoa.data_nascimento }}</td>
                        <td>{{ pessoa.cidade }}</td>
                        <td>{{ pessoa.capacidade_atual }}</td>
                        <td>{{ pessoa.capacidade_potencial }}</td>
                        <td>{{ pessoa.pe }}</td>
                        <td>{{ pessoa.posicao_jogador }}</td>
                        <td>{{ pessoa.posicoes_adicionais | join(', ') }}</td>
                        <td>{{ pessoa.atributo_essencial }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    
    template = Template(template_html)
    html = template.render(pessoas=pessoas)

    with open(os.path.join(pasta, 'tabela_jogadores.html'), 'w', encoding='utf-8') as file:
        file.write(html)

# Gerar os jogadores e salvar em HTML
num_jogadores = 18  # Número de jogadores a serem gerados
jogadores_gerados = gerar_pessoas(num_jogadores)

# Cria a pasta caso não exista
pasta_saida = 'output'
os.makedirs(pasta_saida, exist_ok=True)

# Gera o arquivo HTML
gerar_tabela_html(jogadores_gerados, pasta_saida)

# Abrir o arquivo HTML no navegador
webbrowser.open(f'file://{os.path.abspath(os.path.join(pasta_saida, "tabela_jogadores.html"))}')