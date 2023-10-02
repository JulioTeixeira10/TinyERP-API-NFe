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
pagamento = config['DEFAULT']['forma_de_pagamento']
meio_pag = config['DEFAULT']['meio_pag']

itens = json.loads(itens_str)


# Função para construir o arquivo JSON do pedido
def build_json():

    dirPedido = "C:\\TinyAPI\\pedido.json"

    # Constroi a estrutura do JSON com as informações do pedido
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
            "valor_desconto": desconto,
            "forma_pagamento": pagamento,
            "meio_pagamento": meio_pag,
            "parcelas": [
                {
                    "parcela": {
                    "forma_pagamento": pagamento,
                    "meio_pagamento": meio_pag
                }
                }
            ],
            "obs_internas": "CFe"
        }
    }

    # Converte os dados para uma string JSON
    json_data = json.dumps(data, indent=3)

    with open(dirPedido, "w+") as file:
        file.write(json_data)
        file.close()