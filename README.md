1. Baixe a imagem antes da aula.

   ```bash
   docker compose pull
   ```

2. Inicie o WireMock e recarregue as regras após atualizar os JSONs.

   ```bash
   docker compose up -d
   docker compose restart wiremock
   ```

3. Mostre as regras de frete de R$ 15,00 para Caderno e R$ 100,00 para Geladeira, e as regras de pagamento aprovado e recusado.

   ```bash
   cat mappings/01-frete-caderno.json
   cat mappings/02-frete-geladeira.json
   cat mappings/03-pagamento-aprovado.json
   cat mappings/04-pagamento-recusado.json
   ```

4. Consulte o frete do Caderno.

   ```bash
   curl -i 'http://localhost:8080/frete?produto_id=1&cep=01001000'
   ```

5. Consulte o frete da Geladeira.

   ```bash
   curl -i 'http://localhost:8080/frete?produto_id=2&cep=01001000'
   ```

6. Limpe o histórico para começar a demonstração manual de integração.

   ```bash
   curl -i -X DELETE http://localhost:8080/__admin/requests
   ```

7. Execute a loja e pressione Enter no produto, na quantidade, no frete e no cartão para comprar dois cadernos por R$ 66,80.

   ```bash
   python3 ecommerce.py
   ```

8. Execute novamente, escolha o produto 2 e pressione Enter na quantidade, no frete e no cartão para comprar duas geladeiras por R$ 3.699,98.

   ```bash
   python3 ecommerce.py
   ```

9. Execute novamente, pressione Enter no produto, na quantidade e no frete e digite 9999 no cartão para simular uma recusa de negócio.

   ```bash
   python3 ecommerce.py
   ```

10. Confira no histórico os produtos enviados na consulta do frete e os totais 66.8 e 3699.98 enviados ao pagamento.

    ```bash
    curl -s http://localhost:8080/__admin/requests | python3 -m json.tool
    ```
