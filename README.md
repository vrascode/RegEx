# LFA Form Validator

Validação de formulários e extração de e-mails utilizando expressões regulares em Python.

## Visão geral

Aplicação de terminal que valida Nome, CPF, E-mail e Telefone e extrai os
endereços válidos de um texto. Cada campo recebe um resultado individual;
o formulário só é aprovado quando os quatro campos são aceitos.

## Objetivo acadêmico

Trabalho de Linguagens Formais e Autômatos do curso de Ciência da Computação
da Universidade Federal do Tocantins (UFT). O programa aplica classes de
caracteres, quantificadores, alternância e verificações de contexto na
definição de formatos por expressões regulares.

## Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3 | Aplicação de terminal |
| `re` | Compilação de padrões, validação e extração |
| `unittest` e `unittest.mock` | Testes automatizados e simulação das entradas |

Não há dependências externas para executar o programa ou os testes.

## Funcionalidades

- Validação integral dos quatro campos com `fullmatch()`.
- Mensagens de aprovação ou rejeição com orientação por campo.
- Extração com `findall()`, preservando ordem e repetições.
- Extração executada após o formulário, mesmo quando ele é rejeitado.
- Entradas preservadas, sem remoção automática de espaços.

## Regras de validação

| Campo | Formato aceito |
|---|---|
| Nome | De 1 a 50 letras ASCII ou espaços simples |
| CPF | `12345678901` ou `123.456.789-01` |
| E-mail | Usuário e domínio com no mínimo 2 caracteres; registro com 3 letras minúsculas; país opcional permitido |
| Telefone | `11987654321` ou `(11)98765-4321` |

As regras são acadêmicas: Nome admite apenas espaços; CPF verifica formato,
sem calcular dígitos; Telefone não consulta DDD ou existência do número.
E-mail permite alfanuméricos Unicode, `_`, `.` e `-`, sem pontos consecutivos.
O país, quando informado, deve ser `br`, `ao`, `pt`, `es`, `de` ou `uk`.
O primeiro segmento após ponto com três letras minúsculas é interpretado
como registro: `ab@cd.com.xyz` é rejeitado e `ab@cd.com.br` é aceito.

## Instalação e execução

Na pasta do projeto, com Python 3 instalado:

```powershell
python validador_formulario.py
```

Informe Nome, CPF, E-mail e Telefone, nessa ordem. O programa também exibe:

```text
=== E-mails válidos extraídos do texto ===
alice.souza@gmail.com
suporte_23@empresa-tech.com
joao99@dominio123.org
```

## Execução dos testes

```powershell
python -m py_compile validador_formulario.py
python -m unittest discover -v
```

## Informações acadêmicas

| Instituição | Curso | Disciplina |
|---|---|---|
| Universidade Federal do Tocantins (UFT) | Ciência da Computação | Linguagens Formais e Autômatos |

## Autor

[vrascode](https://github.com/vrascode)
