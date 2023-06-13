import sys
import json
import time
import requests
import json_builder
import error_pop_up
from configparser import ConfigParser


# Diretorios
mainDir = "C:\\TinyAPI\\"
dirToken = f"{mainDir}" + "token.cfg"
dirPedido = f"{mainDir}" + "pedido.json"
dirResposta = f"{mainDir}" + "resposta.json"
dirResposta2 = f"{mainDir}" + "resposta2.json"

# Variavel para numerar requests
c = 0

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

time.sleep(0.3)

# Lê o json que contem o pedido
read_json(dirPedido)

# Informações para o envio das requests
url_incluir_pedido = 'https://api.tiny.com.br/api2/pedido.incluir.php'
url_gerar_NFCe = "https://api.tiny.com.br/api2/gerar.nota.fiscal.pedido.php"

data = f"token={token}&pedido={json.dumps(dados)}&formato=JSON"

# Função para mandar a request
def enviarREST(url, data):
    global c
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(url, data=data, headers=headers)
    
    if '"status":"OK"' in response.text:
        if c == 0:
            error_pop_up.log_info(response.text)
            c = 1
        else:
            error_pop_up.pop_up_check("O Cupom Fiscal foi enviado ao TinyERP com sucesso.")
            error_pop_up.log_info(response.text)
        return response.text
    else:
        # Transforma a resposta em um objeto JSON formatavel
        erro = json.loads(response.text)
        erro_json_str = json.dumps(erro, indent=4)
        erro_json = json.loads(erro_json_str)
        erro = erro_json["retorno"]["registros"]["registro"]["erros"][0]

        if c == 0:
            error_pop_up.pop_up_erro(f"1ª Request: Houve um erro ao incluir o pedido: {erro}")
            error_pop_up.log_erro(response.text)
        else:
            error_pop_up.pop_up_erro(f"2ª Request: Houve um erro ao enviar o Cupom Fiscal: {erro}")
            error_pop_up.log_erro(response.text)
        sys.exit()

# Chama a função para enviar a request
response = enviarREST(url_incluir_pedido, data)

# Cria um arquivo com a resposta do servidor
response_file(dirResposta)

time.sleep(0.3)

# Pega o id do pedido recem criado
read_json(dirResposta)
id = dados["retorno"]["registros"]["registro"]["id"]

# Manda a request para gerar a NFCe
data = f"token={token}&id={id}&modelo=NFCe&formato=JSON"
response = enviarREST(url_gerar_NFCe, data)

# Cria um arquivo com a resposta do servidor
response_file(dirResposta2)