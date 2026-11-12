"""Loja com produto local; frete e pagamento simulados pelo WireMock."""

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


# GET para consultar o frete; POST para enviar o pagamento.
def chamar_api(caminho, dados=None):
    corpo = None if dados is None else json.dumps(dados).encode("utf-8")
    requisicao = Request(
        API_URL + caminho,
        data=corpo,
        headers={"Content-Type": "application/json"},
    )
    print(f"  {requisicao.get_method()} {requisicao.full_url}")
    with urlopen(requisicao, timeout=5) as resposta:
        return json.load(resposta)


# 1. O produto já está implementado na loja.
def inicializar_produto():
    return Produto(id=1, nome="Caderno", preco=25.90)


# 2. O carrinho calcula o subtotal localmente.
def calcular_subtotal(produto):
    quantidade = int(input("Quantidade de cadernos [2]: ").strip() or "2")
    if quantidade <= 0:
        raise ValueError

    subtotal = round(produto.preco * quantidade, 2)
    print(f"Produto: {produto.nome} (id: {produto.id})")
    print(f"Preço unitário: {dinheiro(produto.preco)}")
    print(f"Quantidade: {quantidade}")
    print(f"Subtotal: {dinheiro(subtotal)}")
    return subtotal


# 3. O WireMock simula o serviço de frete que ainda não existe.
def consultar_frete(subtotal):
    input("\nPressione Enter para consultar o frete do CEP 01001000...")
    frete = chamar_api("/frete?cep=01001000")
    total = round(subtotal + frete["valor"], 2)
    print(f"Frete: {dinheiro(frete['valor'])}")
    print(f"Prazo: {frete['prazo_dias']} dias úteis")
    print(f"Total com frete: {dinheiro(total)}")
    return total


# 4. O WireMock simula aprovação ou recusa do pagamento.
def realizar_pagamento(total):
    cartao = input("\nFinal do cartão: 1111 aprova / 9999 recusa [1111]: ").strip() or "1111"
    if cartao not in ("1111", "9999"):
        raise SystemExit("Use 1111 ou 9999 para selecionar o cenário da aula.")

    pagamento = chamar_api("/pagamentos", {"total": total, "cartao_final": cartao})
    print(f"Pagamento: {pagamento['status']}")
    print(f"Compra finalizada. Total: {dinheiro(total)}")


# A main mostra apenas a sequência da compra.
def main():
    print("\n=== Minha Loja ===")
    produto = inicializar_produto()
    subtotal = calcular_subtotal(produto)
    total = consultar_frete(subtotal)
    realizar_pagamento(total)


if __name__ == "__main__":
    try:
        main()
    except HTTPError as erro:
        with erro:
            try:
                mensagem = json.load(erro)["mensagem"]
            except (ValueError, KeyError, TypeError):
                mensagem = "Confira as regras configuradas no WireMock."
        raise SystemExit(f"Compra não concluída: HTTP {erro.code} — {mensagem}")
    except (URLError, TimeoutError):
        raise SystemExit("API indisponível. Confira o WireMock: docker compose up -d")
    except ValueError:
        raise SystemExit("Informe uma quantidade inteira maior que zero.")
