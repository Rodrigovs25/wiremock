import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "http://localhost:8080"

class Produto:
    def __init__(self, id, nome, preco):
        self.id = id
        self.nome = nome
        self.preco = preco

def dinheiro(valor):
    return f"R$ {valor:.2f}".replace(".", ",")

def inicializar_produto():
    produtos = {
        "1": Produto(id=1, nome="Caderno", preco=25.90),
        "2": Produto(id=2, nome="Mochila", preco=89.90),
    }
    print("\n=== Minha Loja ===")
    for produto in produtos.values():
        print(f"{produto.id}. {produto.nome} — {dinheiro(produto.preco)}")

    escolha = input("Escolha o produto [1]: ").strip() or "1"
    if escolha not in produtos:
        raise SystemExit("Escolha 1 para Caderno ou 2 para Mochila.")
    return produtos[escolha]

def calcular_subtotal(produto):
    quantidade = int(input("Quantidade [2]: ").strip() or "2")
    if quantidade <= 0:
        raise ValueError

    subtotal = round(produto.preco * quantidade, 2)
    print(f"Produto: {produto.nome} (id: {produto.id})")
    print(f"Preço unitário: {dinheiro(produto.preco)}")
    print(f"Quantidade: {quantidade}")
    print(f"Subtotal: {dinheiro(subtotal)}")
    return subtotal

# WireMock informa o frete do produto escolhido.
def consultar_frete(produto, subtotal):
    input("\nPressione Enter para consultar o frete do CEP 01001000...")
    url = f"{API_URL}/frete?produto_id={produto.id}&cep=01001000"
    print(f"  GET {url}")
    with urlopen(url, timeout=5) as resposta:
        frete = json.load(resposta)

    total = round(subtotal + frete["valor"], 2)
    print(f"Frete: {dinheiro(frete['valor'])}")
    print(f"Prazo: {frete['prazo_dias']} dias úteis")
    print(f"Total com frete: {dinheiro(total)}")
    return total

# WireMock aprova ou recusa o pagamento.
def realizar_pagamento(total):
    cartao = input("\nFinal do cartão: 1111 aprova / 9999 recusa [1111]: ").strip() or "1111"
    if cartao not in ("1111", "9999"):
        raise SystemExit("Use 1111 ou 9999 para selecionar o cenário da aula.")

    dados = json.dumps({"total": total, "cartao_final": cartao}).encode("utf-8")
    requisicao = Request(
        API_URL + "/pagamentos",
        data=dados,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print(f"  POST {requisicao.full_url}")
    with urlopen(requisicao, timeout=5) as resposta:
        pagamento = json.load(resposta)

    print(f"Pagamento: {pagamento['status']}")
    print(f"Compra finalizada. Total: {dinheiro(total)}")

def main():
    produto = inicializar_produto()
    subtotal = calcular_subtotal(produto)
    total = consultar_frete(produto, subtotal)
    realizar_pagamento(total)


if __name__ == "__main__":
    try:
        main()
    except HTTPError as erro:
        mensagem = "Confira as regras configuradas no WireMock."
        if erro.code == 402:
            with erro:
                mensagem = json.load(erro)["mensagem"]
        raise SystemExit(f"Compra não concluída: HTTP {erro.code} — {mensagem}")
    except (URLError, TimeoutError):
        raise SystemExit("API indisponível. Confira o WireMock: docker compose up -d")
    except ValueError:
        raise SystemExit("Informe uma quantidade inteira maior que zero.")
