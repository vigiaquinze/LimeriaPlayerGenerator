import csv
import random
import os
import webbrowser
import yaml
from datetime import datetime, timedelta
from jinja2 import Template

class Pessoa:
    def __init__(self, nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_potencial, posicoes_adicionais):
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

    @property
    def nome_completo(self):
        return f"{self.nome}{self.sobrenome}"  # Concatenando nome e sobrenome sem espaço

    def __repr__(self):
        return (f"Pessoa(nome={self.nome}, sobrenome={self.sobrenome}, cor_pele={self.cor_pele}, "
                f"cidade={self.cidade}, posicao_jogador={self.posicao_jogador}, "
                f"atributo_essencial={self.atributo_essencial}, data_nascimento={self.data_nascimento}, "
                f"capacidade_atual={self.capacidade_atual}, capacidade_potencial={self.capacidade_potencial}, "
                f"posicoes_adicionais={self.posicoes_adicionais})")

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

nomes = carregar_lista_de_arquivo('nomes.csv')
sobrenomes = carregar_lista_de_arquivo('sobrenomes.csv')
cores_pele = list(range(1, 21))
cidades = ["Lisboa", "Porto", "Coimbra", "Braga"]
posicoes_jogador = ["G", "DD", "DAD", "DE", "DAE", "DC", "MDC", "MC", "MD", "ME", "MOC", "MOE", "MOD", "PL"]
capacidade_potencial = [-8, -85, -9, -95]

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
    return Pessoa(nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_possivel, posicoes_adicionais)

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

def gerar_tabela_html(pessoas, pasta):
    template_html = """
    <html>
    <head><title>Pessoas Geradas</title></head>
    <body>
        <h1>Lista de Pessoas Geradas</h1>
        <table border="1">
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
            </tr>
            {% for pessoa in pessoas %}
            <tr>
                <td>{{ pessoa.nome_completo }}</td>
                <td>{{ pessoa.cor_pele }}</td>
                <td>{{ pessoa.cidade }}</td>
                <td>{{ pessoa.posicao_jogador }}</td>
                <td>{{ pessoa.posicoes_adicionais }}</td>
                <td>{{ pessoa.atributo_essencial }}</td>
                <td>{{ pessoa.data_nascimento }}</td>
                <td>{{ pessoa.capacidade_atual }}</td>
                <td>{{ pessoa.capacidade_potencial }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    
    template = Template(template_html)
    html_content = template.render(pessoas=pessoas)

    if not os.path.exists(pasta):
        os.makedirs(pasta)
    
    caminho_arquivo = os.path.join(pasta, 'pessoas_geradas.html')
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        file.write(html_content)

    webbrowser.open(f'file://{os.path.realpath(caminho_arquivo)}')

# Gerar 20 pessoas com as probabilidades configuradas
pessoas = gerar_pessoas_com_probabilidades(20)
gerar_tabela_html(pessoas, 'output')
