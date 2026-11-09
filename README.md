<h1 align="center">LFA Form Validator</h1>

<p align="center">
  Validação de formulários e extração de e-mails utilizando expressões regulares em Python.
</p>

<p align="center">
  <a href="https://www.python.org/"><img alt="Python 3" src="https://img.shields.io/badge/Python-3-3776AB?logo=python&amp;logoColor=white"></a>
  <a href="https://github.com/vrascode/lfa-form-validator/actions/workflows/python-tests.yml"><img alt="Testes automatizados na branch main" src="https://github.com/vrascode/lfa-form-validator/actions/workflows/python-tests.yml/badge.svg?branch=main"></a>
  <a href=".github/workflows/python-tests.yml"><img alt="GitHub Actions CI" src="https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?logo=githubactions&amp;logoColor=white"></a>
  <a href="#informações-acadêmicas"><img alt="Disciplina LFA" src="https://img.shields.io/badge/Disciplina-LFA-596579"></a>
</p>

<p align="center">
  <a href="#instalação-e-execução">Executar</a> ·
  <a href="#regras-de-validação">Regras</a> ·
  <a href="#execução-dos-testes">Testes</a> ·
  <a href="docs/EXAMPLES.md">Exemplos completos</a> ·
  <a href="docs/REGEX_EXPLAINED.md">Guia das regex</a>
</p>

## Visão geral

Aplicação de terminal que valida **Nome, CPF, E-mail e Telefone** e extrai
endereços válidos de um texto. O programa informa o resultado de cada campo
e aprova o formulário quando todos atendem às regras.

O código e os testes usam exclusivamente a biblioteca padrão do Python.
As regras reproduzem a interpretação acadêmica descrita na documentação.

## Objetivo acadêmico

Aplicar expressões regulares ao reconhecimento de formatos de entrada no
contexto de **Linguagens Formais e Autômatos**. O trabalho exercita classes
de caracteres, quantificadores, alternância, grupos e verificações de contexto,
relacionando a definição dos padrões com exemplos e testes de regressão.

## Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python 3 | Programa de terminal; verificado com Python 3.12.10 |
| `re` | Padrões compilados, `fullmatch()` e `findall()` |
| `unittest` | Suíte de testes automatizados |
| `unittest.mock` | Simulação das entradas do formulário |
| GitHub Actions | Workflow configurado para Python 3.12 |

## Funcionalidades

- Validar os quatro campos com correspondência da entrada inteira.
- Exibir aprovação ou rejeição e uma orientação para cada campo inválido.
- Rejeitar o formulário quando ao menos um campo for inválido.
- Extrair os e-mails válidos do texto do enunciado, mesmo após uma rejeição.
- Preservar a ordem e as repetições dos endereços extraídos.
- Impedir a extração de fragmentos de endereços inválidos.

## Regras de validação

| Campo | Regra | Exemplo aceito |
|---|---|---|
| Nome | De 1 a 50 letras ASCII ou espaços simples | `Joao Silva` |
| CPF | 11 algarismos ASCII ou máscara completa | `123.456.789-01` |
| E-mail | Usuário e domínio com pelo menos 2 caracteres; registro com 3 letras minúsculas | `ab@cd.com` |
| Telefone | 11 algarismos ASCII ou máscara completa | `(11)98765-4321` |

No e-mail, usuário e domínio aceitam alfanuméricos Unicode, ponto, underline
e hífen. Pontos consecutivos são rejeitados. O país é opcional e limitado a
**`br`, `ao`, `pt`, `es`, `de` e `uk`**.

Algumas escolhas fazem parte das regras do trabalho:

- Nome pode conter somente espaços; acentos e tabs são rejeitados.
- CPF valida o formato, sem calcular dígitos verificadores.
- Telefone não verifica DDD, existência do número ou código internacional.
- As entradas são preservadas, sem remoção automática de espaços.
- O primeiro segmento após ponto com três letras minúsculas é o registro
  do e-mail. Assim, `ab@cd.com.br` é aceito e `ab@cd.com.xyz` é rejeitado.

Os [cinco requisitos documentados](docs/REQUIREMENTS.md) detalham os formatos
e as decisões de interpretação.

## Exemplos de entradas válidas e inválidas

| Campo | Válida | Inválida | Motivo da rejeição |
|---|---|---|---|
| Nome | `Maria Silva` | `Maria123` | Algarismos não permitidos |
| Nome | `Joao` | `João` | Acento não permitido |
| CPF | `12345678901` | `123456789-01` | Máscara parcial |
| E-mail | `ab@cd.com.br` | `ab@cd.com.fr` | País fora da lista |
| E-mail | `ab@cd.xyz` | `erro.email@gmail..com` | Pontos consecutivos |
| Telefone | `11987654321` | `(11) 98765-4321` | Espaço adicional |

Veja os [formulários completos e exemplos em Python](docs/EXAMPLES.md).

## Demonstração do terminal

Transcrição do cenário aprovado, incluindo as entradas digitadas:

```text
=== Formulário ===
Nome: Matheus Sulino
  Nome APROVADO.
CPF: 123.456.789-01
  CPF APROVADO.
E-mail: alice.souza@gmail.com
  E-mail APROVADO.
Telefone: (11)98765-4321
  Telefone APROVADO.

Resultado final: formulário APROVADO.

=== E-mails válidos extraídos do texto ===
alice.souza@gmail.com
suporte_23@empresa-tech.com
joao99@dominio123.org
```

Uma entrada inválida gera uma mensagem com o formato esperado e faz o
resultado final ser `formulário REJEITADO.`. Os demais campos continuam
sendo solicitados.

## Extração de e-mails

A função `extrair_emails(texto)` usa o mesmo objeto `REGEX_EMAIL` da validação.
Com `findall()`, retorna os endereços inteiros, em ordem, sem remover repetições.

```python
from validador_formulario import TEXTO_ENUNCIADO, extrair_emails

emails = extrair_emails(TEXTO_ENUNCIADO)
print(emails)
# ['alice.souza@gmail.com', 'suporte_23@empresa-tech.com', 'joao99@dominio123.org']
```

`erro.email@gmail..com` é ignorado. Pontuação de frase fica fora do resultado,
e tokens como `ab@cd.com.xyz` não produzem uma correspondência parcial.

## Instalação e execução

É necessário **Python 3**. A versão de referência dos testes é **3.12**.
Não há pacotes a instalar com `pip`.

Para obter o projeto pelo GitHub:

```powershell
git clone https://github.com/vrascode/lfa-form-validator.git
Set-Location lfa-form-validator
```

Se já tiver os arquivos, abra o terminal na pasta que contém
`validador_formulario.py`. Em seguida:

```powershell
python validador_formulario.py
```

Informe Nome, CPF, E-mail e Telefone, nessa ordem, pressionando Enter após
cada valor. No Windows, se `python` não estiver disponível, use
`py -3.12 validador_formulario.py`.

## Execução dos testes

Na raiz do projeto:

```powershell
python -m py_compile validador_formulario.py
python -m unittest discover -v
```

Verificação local: **83 testes aprovados**, sem falhas ou erros, com
**Python 3.12.10**. A contagem corresponde aos métodos de teste;
há casos adicionais parametrizados com `subTest()`.

O [workflow](.github/workflows/python-tests.yml) executa os mesmos comandos
em pushes e pull requests para `main`, com Python 3.12. O badge do cabeçalho
consulta o resultado real do GitHub; antes da primeira execução, pode aparecer
sem resultado. Consulte a [estratégia de testes](docs/TESTING.md).

## Estrutura do projeto

```text
lfa-form-validator/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── docs/
│   ├── REQUIREMENTS.md
│   ├── REGEX_EXPLAINED.md
│   ├── TESTING.md
│   └── EXAMPLES.md
├── .gitignore
├── README.md
├── validador_formulario.py
└── test_validador_formulario.py
```

## Explicação das expressões regulares

Os padrões são compilados com `re.compile()` e reutilizados pelas funções.
`fullmatch()` exige que o campo inteiro siga a regra; `findall()` procura
os endereços válidos dentro do texto.

```python
# Nome: de 1 a 50 letras ASCII ou espaços.
r"[a-zA-Z ]{1,50}"

# CPF: alternativa sem pontuação ou com máscara completa.
r"[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"

# Telefone: alternativa sem pontuação ou com máscara completa.
r"[0-9]{11}|\([0-9]{2}\)[0-9]{5}-[0-9]{4}"
```

O e-mail usa `re.VERBOSE`, grupos não capturantes e lookarounds para impedir
pontos consecutivos e correspondências parciais. O
[guia técnico das regex](docs/REGEX_EXPLAINED.md) reproduz o padrão completo
e explica classes, quantificadores, alternância, domínios e códigos de país.

## Informações acadêmicas

| Informação | Detalhe |
|---|---|
| Instituição | Universidade Federal do Tocantins (UFT) |
| Curso | Ciência da Computação |
| Disciplina | Linguagens Formais e Autômatos |
| Tema | Validação de formulários e extração de e-mails com expressões regulares |

## Autor

[vrascode](https://github.com/vrascode)

Nenhuma licença foi escolhida para este projeto.
