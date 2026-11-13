# Entrega --- Consolidador de reservas de hotel

## 1. Resumo

Projeto de correção do CLI de consolidação de reservas de hotel. O
programa lê os CSVs de reservas e taxas de câmbio e gera um relatório
JSON conforme o contrato definido no README do desafio.

## 2. Defeitos corrigidos

---

Defeito Causa-raiz

---

Cálculo incorreto de noites, O cálculo original não utilizava
inclusive em estadias que corretamente a diferença entre as
atravessam meses e anos. datas civis de check-in e check-out
multiplicada pela quantidade de
quartos.

Conversão incorreta de valores para A conversão não aplicava
BRL. corretamente a taxa `rate_to_brl`
correspondente à moeda da reserva.

Reservas não faturáveis incluídas A regra de faturamento não
nos valores agregados. restringia as agregações
exclusivamente ao status
`CONFIRMED`.

Ordenação incorreta do ranking de A ordenação não priorizava o maior
hotéis. faturamento e/ou não aplicava
corretamente o desempate por
`hotel_id` crescente.

Precisão monetária e arredondamento Os cálculos precisavam preservar a
fora da regra especificada. precisão decimal e aplicar
`ROUND_HALF_UP` somente na
serialização dos valores.

Leitura interrompida após 200 O repositório de reservas continha
reservas. um limite artificial que
interrompia a leitura antes do fim
do CSV.

Aceitação de taxas especiais ou A validação da taxa não verificava
inválidas. explicitamente se o valor Decimal
era finito e positivo.

Arquivos CSV com codificação `UnicodeError` não estava incluído
inválida não classificados como no tratamento de falhas de leitura
erro de entrada. dos repositórios.

---

## 3. Investigação e abordagem

```{=html}
<!-- PREENCHER PELO CANDIDATO.
Descreva aqui, com suas próprias palavras:
- como executou os testes inicialmente e identificou os resultados incorretos;
- como comparou a saída com as regras e a amostra de validação;
- como isolou as causas nos componentes responsáveis;
- quais alterações decidiu implementar e por quê;
- como verificou que as correções não alteraram o contrato do CLI ou o schema do JSON.
-->
```

## 4. Como validar

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

## 5. Compatibilidade com o contrato

A entrega deve preservar:

- o comando e os argumentos originais do CLI;
- os códigos de saída: `0` para sucesso, `2` para entrada/argumento
  inválido e `1` para erro inesperado;
- o schema, os nomes, os tipos e a semântica dos campos do JSON;
- os arquivos originais `data/reservas_hoteis.csv` e
  `data/taxas_cambio.csv`.

## 6. Checklist final

- [ ] CLI executado com Python 3.11.
- [ ] Relatório completo gerado com sucesso.
- [ ] Amostra de validação conferida com os valores do README
      original.
- [ ] Todos os testes fornecidos passam sem alteração.
- [ ] Todos os testes adicionais passam.
- [ ] Seção de investigação preenchida.
- [ ] Resultado final do `pytest` registrado.
- [ ] Sessão e declaração de uso de IA incluídas em
      `entrega/uso-de-ia/`.
- [ ] Projeto publicado em repositório público no GitHub.
- [ ] Link do repositório enviado pelo formulário indicado pela Onfly.
