1. Baixe a imagem antes da aula.

   ```bash
   docker compose pull
   ```

2. Inicie o WireMock.

   ```bash
   docker compose up -d
   ```

3. Mostre a regra do frete.

   ```bash
   cat simulacoes/01-frete.json
   ```

4. Aguarde a inicialização e consulte o frete simulado.

   ```bash
   curl -i 'http://localhost:8080/frete?cep=01001000'
   ```

5. Execute a loja e pressione Enter na quantidade, no frete e no cartão para aprovar a compra.

   ```bash
   python3 ecommerce.py
   ```

6. Execute novamente, pressione Enter na quantidade e no frete e digite 9999 no cartão para recusar a compra.

   ```bash
   python3 ecommerce.py
   ```
