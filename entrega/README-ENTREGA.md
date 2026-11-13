# Entrega --- Consolidador de reservas de hotel

## 1. Resumo

Projeto de correção do CLI de consolidação de reservas de hotel. O
programa lê os CSVs de reservas e taxas de câmbio e gera um relatório
JSON conforme o contrato definido no README do desafio.

## 2. Defeitos corrigidos

| Defeito                                                                         | Causa-raiz                                                                                                                                      | Abordagem adotada |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | --- |
| Cálculo incorreto de noites, inclusive em estadias que atravessam meses e anos. | O cálculo original não utilizava corretamente a diferença entre as datas civis de check-in e check-out multiplicada pela quantidade de quartos. |                   |
| Conversão incorreta de valores para BRL.                                        | A conversão não aplicava corretamente a taxa `rate_to_brl` correspondente à moeda da reserva.                                                   |                   |
| Reservas não faturáveis incluídas nos valores agregados.                        | A regra de faturamento não restringia as agregações exclusivamente ao status `CONFIRMED`.                                                       |                   |
| Ordenação incorreta do ranking de hotéis.                                       | A ordenação não priorizava o maior faturamento e/ou não aplicava corretamente o desempate por `hotel_id` crescente.                             |                   |
| Leitura interrompida após 200 reservas.                                         | O repositório de reservas continha um limite artificial que interrompia a leitura antes do fim do CSV.                                          |                   |
| Aceitação de taxas especiais ou inválidas.                                      | A validação da taxa não verificava explicitamente se o valor `Decimal` era finito e positivo.                                                   |                   |
| Arquivos CSV com codificação inválida não classificados como erro de entrada.   | `UnicodeError` não estava incluído no tratamento de falhas de leitura dos repositórios.                                                         |                   |     |

## 3. Como validar

Requisitos: Python 3.11 ou superior e dependências de desenvolvimento
listadas em `requirements-dev.txt`.

### Criar e ativar o ambiente virtual

Linux/macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

### Executar o relatório completo

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json \
  --top 5
```

No Windows PowerShell, configure o caminho de importação antes de
executar:

```powershell
$env:PYTHONPATH = "src"
python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json --top 5
```

### Validar a amostra de referência

```bash
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json
```

A saída deve apresentar:

- 12 reservas no total;
- 9 confirmadas, 2 canceladas e 1 `NO_SHOW`;
- 28 noites faturáveis;
- total de `7566.00` BRL;
- média de `270.21` BRL por noite;
- agregações mensais e ranking conforme a tabela de amostra do README
  original.

### Executar todos os testes

```bash
python -m pytest -q
```

### Resultado dos testes

- Testes fornecidos: **5**
- Testes adicionais: **3**

Os testes fornecidos foram mantidos inalterados. Os testes adicionais
foram criados em arquivos separados.

## 4. Compatibilidade com o contrato

A entrega deve preservar:

- o comando e os argumentos originais do CLI;
- os códigos de saída: `0` para sucesso, `2` para entrada/argumento
  inválido e `1` para erro inesperado;
- o schema, os nomes, os tipos e a semântica dos campos do JSON;
- os arquivos originais `data/reservas_hoteis.csv` e
  `data/taxas_cambio.csv`.
