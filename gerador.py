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

    # No resto do código, a cor de pele é definida como:
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

# Carregando listas de nomes e sobrenomes
nomes = carregar_lista_de_arquivo('nomes.csv')
sobrenomes = carregar_lista_de_arquivo('sobrenomes.csv')
cores_pele = ['Clara', 'Escura']  # Apenas duas opções de cor de pele
cidades = ["Abílio Pedro", "Âmago", "Anhanguera", "Caieiras", "Colinas do Engenho", "Odécio Degan", "Equidistante", "Esmeralda", "Geada", "Glória", "Graminha", "Nossa Sra. das Dores", "Nova Liméria", "Planalto", "Roseira", "Santa Adélia", "Vista Alegre"]
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

def gerar_altura(posicao_jogador):
    if posicao_jogador == "DC":
        return round(random.uniform(175, 200))  # Defesa Central deve ter entre 175cm e 200cm
    elif posicao_jogador == "G":
        return round(random.uniform(185, 205))  # Goleiro deve ter entre 185cm e 205cm
    else:
        return round(random.uniform(160, 190))  # Outras posições entre 160cm e 190cm

def gerar_cor_pele():
    return 'Clara' if random.random() < 0.75 else 'Escura'  # 75% clara, 25% escura

def gerar_pessoa():
    nome = random.choice(nomes)
    sobrenome = random.choice(sobrenomes)
    cor_pele = gerar_cor_pele()  # Usa a nova função para gerar a cor da pele
    cidade = random.choice(cidades)
    posicao_jogador = random.choice(posicoes_jogador)
    atributo_essencial = random.choice(configuracao_posicoes['posicoes'][posicao_jogador]['atributos_essenciais'])
    data_nascimento = gerar_data_nascimento()
    capacidade_atual = random.randint(120, 155)
    capacidade_possivel = random.choice(capacidade_potencial)
    posicoes_adicionais = gerar_posicoes_adicionais(posicao_jogador, atributo_essencial)
    pe = gerar_pe()
    altura = gerar_altura(posicao_jogador)  # Gerar altura com base na posição
    return Pessoa(nome, sobrenome, cor_pele, cidade, posicao_jogador, atributo_essencial, data_nascimento, capacidade_atual, capacidade_possivel, posicoes_adicionais, pe, altura)

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
        </style>
    </head>
    <body>
        <h1>Pessoas Geradas</h1>
        <img src="{{ grafico_base64 }}" alt="Gráfico de Posições">
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
    rendered_html = template.render(pessoas=pessoas, grafico_base64=grafico_base64)

    # Gera o caminho do arquivo HTML na pasta especificada
    nome_arquivo = os.path.join(pasta, 'pessoas_geradas.html')
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    # Abre o arquivo HTML no navegador
    webbrowser.open('file://' + nome_arquivo)

def main():
    n = 18  # Quantidade de pessoas a gerar
    pessoas = gerar_pessoas_com_probabilidades(n)
    pasta = os.getcwd()  # Usa o diretório atual
    gerar_tabela_html(pessoas, pasta)

if __name__ == "__main__":
    main()
