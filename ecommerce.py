import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

API_URL = "http://localhost:8080"

class Produto:
    def __init__(self, id, nome, preco):
        self.id = id
        self.nome = nome
        self.preco = preco

def inicializar_produto(escolha="1"):
    produtos = {
        "1": Produto(id=1, nome="Caderno", preco=25.90),
        "2": Produto(id=2, nome="Geladeira", preco=1799.99),
    }
    return produtos[escolha]

def calcular_subtotal(produto, quantidade=2):
    subtotal = round(produto.preco * quantidade, 2)
    print(f"Produto: {produto.nome} (id: {produto.id})")
    print(f"Preço unitário: R$ {produto.preco:.2f}")
    print(f"Quantidade: {quantidade}")
    print(f"Subtotal: R$ {subtotal:.2f}")
    return subtotal

def consultar_frete(produto, subtotal):
    url = f"{API_URL}/frete?produto_id={produto.id}&cep=01001000"
    print(f"  GET {url}")
    
    with urlopen(url) as resposta:
        frete = json.load(resposta)

    total = round(subtotal + frete["valor"], 2)
    print(f"Frete: R$ {frete['valor']:.2f}")
    print(f"Prazo: {frete['prazo_dias']} dias úteis")
    print(f"Total com frete: R$ {total:.2f}")
    return total

def realizar_pagamento(total, cartao="1111"):
    dados = json.dumps({"total": total, "cartao_final": cartao}).encode("utf-8")
    
    requisicao = Request(
        API_URL + "/pagamentos",
        data=dados,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print(f"  POST {requisicao.full_url}")
    
    try:
        with urlopen(requisicao) as resposta:
            pagamento = json.load(resposta)
        print(f"Pagamento: {pagamento['status']}")
        print(f"Compra finalizada. Total: R$ {total:.2f}")
        return pagamento["status"]
    except HTTPError as erro:
        mensagem = json.load(erro)["mensagem"] if erro.code == 402 else "Erro na requisição."
        print(f"Compra não concluída: HTTP {erro.code} — {mensagem}")
        return mensagem

if __name__ == "__main__":
    print("Loja\n1. Caderno — R$ 25.90\n2. Geladeira — R$ 1799.99")
    escolha = input("Escolha o produto: ").strip() or "1"
    produto = inicializar_produto(escolha)

    quantidade = int(input("Quantidade [2]: ").strip() or "2")
    subtotal = calcular_subtotal(produto, quantidade)

    input("\nPressione Enter para consultar o frete do CEP 01001000...")
    total = consultar_frete(produto, subtotal)

    cartao = input("\nFinal do cartão: 1111 aprova / 9999 recusa [1111]: ").strip() or "1111"
    status = realizar_pagamento(total, cartao)
    if status != "APROVADO":
        exit(1)