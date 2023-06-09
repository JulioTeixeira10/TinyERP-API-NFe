import json
import dados_pedido

# Diretorio onde será armazenado o pedido
dirPedido = "C:\\Users\\Usefr\\Desktop\\TinyAPI\\pedido.json"

# Constroi a estrutura do JSON com as informções do pedido
data = {
    "pedido": {
        "cliente": {
            "nome": dados_pedido.nome,
            "cpf_cnpj": dados_pedido.cpf_cnpj
        },
        "itens": [
            {
                "item": item
            }
            for item in dados_pedido.itens
        ],
        "valor_desconto": dados_pedido.desconto
    }
}

# Converte os dados para uma string JSON
json_data = json.dumps(data, indent=3)

with open(dirPedido, "w+") as file:
    file.write(json_data)
    file.close()