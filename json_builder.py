import json
import configparser


# Configura o configparser
config = configparser.ConfigParser()
config.read('C:\\TinyAPI\\dados.cfg')

# Transfere as variaveis do arquivo .cfg
nome = config['DEFAULT']['nome']
cpf_cnpj = config['DEFAULT']['cpf_cnpj']
desconto = config['DEFAULT']['desconto']
itens_str = config['DEFAULT']['itens']

itens = json.loads(itens_str)


# Função para construir o arquivo JSON do pedido
def build_json():

    dirPedido = "C:\\TinyAPI\\pedido.json"

    # Constroi a estrutura do JSON com as informções do pedido
    data = {
        "pedido": {
            "cliente": {
                "nome": nome,
                "cpf_cnpj": cpf_cnpj
            },
            "itens": [
                {
                    "item": item
                }
                for item in itens
            ],
            "valor_desconto": desconto
        }
    }

    # Converte os dados para uma string JSON
    json_data = json.dumps(data, indent=3)

    with open(dirPedido, "w+") as file:
        file.write(json_data)
        file.close()