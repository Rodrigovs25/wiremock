from ecommerce import inicializar_produto, calcular_subtotal, consultar_frete, realizar_pagamento

def test_frete_caderno_no_wiremock():
    caderno = inicializar_produto("1")
    subtotal = calcular_subtotal(caderno, quantidade=2)
    total = consultar_frete(caderno, subtotal)
    assert total == 66.80

def test_frete_geladeira_no_wiremock():
    geladeira = inicializar_produto("2")
    subtotal = calcular_subtotal(geladeira, quantidade=2)
    total = consultar_frete(geladeira, subtotal)
    assert total == 3699.98 # 3699.98

def test_pagamento_aprovado_no_wiremock():
    status = realizar_pagamento(total=66.80, cartao="1111")
    assert status == "APROVADO"

def test_pagamento_recusado_no_wiremock():
    status = realizar_pagamento(total=66.80, cartao="9999")
    assert status == "Cartão recusado por falta de limite" # NEGADO