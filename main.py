import requests
from configparser import ConfigParser
import json
import time
import json_builder

# Diretorios
mainDir = "C:\\TinyAPI\\"
dirToken = f"{mainDir}" + "token.cfg"
dirPedido = f"{mainDir}" + "pedido.json"
dirResposta = f"{mainDir}" + "resposta.json"
dirResposta2 = f"{mainDir}" + "resposta2.json"

# Função para ler arquivos json
def read_json(diretorio):
    with open(diretorio) as file:
        global dados
        dados = json.load(file)

# Função para criar arquivos com a resposta do server
def response_file(diretorio):
    with open(diretorio, "w+") as f:
        f.write(response)
        f.close()

# Importação do token
config_object = ConfigParser()
config_object.read(dirToken)
KEY = config_object["KEY"]
token = KEY["token"]

# Chama a função que constroi o JSON a partir dos dados recebidos
json_builder.build_json()

time.sleep(1)

# Lê o json que contem o pedido
read_json(dirPedido)

# Informações para o envio das requests
url_incluir_pedido = 'https://api.tiny.com.br/api2/pedido.incluir.php'
url_gerar_NFCe = "https://api.tiny.com.br/api2/gerar.nota.fiscal.pedido.php"

data = f"token={token}&pedido={json.dumps(dados)}&formato=JSON"

# Função para mandar a request
def enviarREST(url, data):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(url, data=data, headers=headers)
    
    if response.ok:
        return response.text
    else:
        raise Exception(f"Problema com {url}, {response.status_code}, {response.text}")

# Chama a função
response = enviarREST(url_incluir_pedido, data)

# Cria um arquivo com a resposta do servidor
response_file(dirResposta)

time.sleep(1)

# Pega o id do pedido recem criado
read_json(dirResposta)
id = dados["retorno"]["registros"]["registro"]["id"]

# Manda a request para gerar a NFCe
data = f"token={token}&id={id}&modelo=NFCe&formato=JSON"
response = enviarREST(url_gerar_NFCe, data)

# Cria um arquivo com a resposta do servidor
response_file(dirResposta2)