# Exemplos de uso

Execute os comandos na pasta que contém `validador_formulario.py`.
Os exemplos seguem as [regras acadêmicas](REQUIREMENTS.md).

## Formulário aprovado

```powershell
python validador_formulario.py
```

Digite os quatro valores abaixo, pressionando Enter após cada um:

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

Esta transcrição inclui as entradas digitadas pelo usuário. Os dois cenários
desta página foram conferidos executando o programa em subprocessos com
entrada padrão automatizada; ambos terminaram com código de saída `0`.
O resultado acadêmico do formulário aparece na saída, não no código de saída.

## Formulário rejeitado

Digite `Matheus123`, `123456`, `email_invalido` e `12345` nessa ordem:

```text
=== Formulário ===
Nome: Matheus123
  Nome REJEITADO: use de 1 a 50 caracteres, somente letras de A a Z (sem acento) e espaços.
CPF: 123456
  CPF REJEITADO: use 11 algarismos ou o formato 000.000.000-00.
E-mail: email_invalido
  E-mail REJEITADO: use usuario@dominio.xxx (xxx: 3 letras minúsculas), com país opcional: .br, .ao, .pt, .es, .de ou .uk.
Telefone: 12345
  Telefone REJEITADO: use 11 algarismos ou o formato (00)00000-0000.

Resultado final: formulário REJEITADO.

=== E-mails válidos extraídos do texto ===
alice.souza@gmail.com
suporte_23@empresa-tech.com
joao99@dominio123.org
```

Um único campo inválido já rejeita o formulário. Por exemplo:

| Nome | CPF | E-mail | Telefone | Resultado |
|---|---|---|---|---|
| `Maria` | `12345678901` | `ab@cd.com.br` | `11987654321` | Aprovado |
| `João` | `12345678901` | `ab@cd.com.br` | `11987654321` | Rejeitado: nome com acento |
| `Maria` | `123.456.789.01` | `ab@cd.com.br` | `11987654321` | Rejeitado: máscara do CPF |
| `Maria` | `12345678901` | `ab@cd.com.fr` | `11987654321` | Rejeitado: país não permitido |
| `Maria` | `12345678901` | `ab@cd.com.br` | `(11) 98765-4321` | Rejeitado: espaço no telefone |

## Usar os validadores em Python

Importar o módulo não abre o formulário: o terminal só é iniciado pelo
bloco `if __name__ == "__main__"`.

```python
from validador_formulario import (
    validar_nome, validar_cpf, validar_email, validar_telefone,
)

assert validar_nome("Joao Silva")
assert not validar_nome("João Silva")
assert validar_cpf("123.456.789-01")
assert not validar_cpf("123456789-01")
assert validar_email("ab@cd.com.br")
assert not validar_email("ab@cd.com.xyz")
assert validar_telefone("(11)98765-4321")
assert not validar_telefone("(11) 98765-4321")
```

## Extrair os três e-mails do enunciado

```python
from validador_formulario import TEXTO_ENUNCIADO, extrair_emails

print(extrair_emails(TEXTO_ENUNCIADO))
```

Resultado:

```python
['alice.souza@gmail.com', 'suporte_23@empresa-tech.com', 'joao99@dominio123.org']
```

O quarto candidato, `erro.email@gmail..com`, contém pontos consecutivos e
é ignorado. O texto original permanece em `TEXTO_ENUNCIADO`.

## Pontuação, repetições e tokens inválidos

```python
from validador_formulario import extrair_emails

assert extrair_emails("Contato: (ab@cd.com...), xy@empresa.org!") == [
    "ab@cd.com", "xy@empresa.org",
]
assert extrair_emails("ab@cd.com; ab@cd.com") == ["ab@cd.com", "ab@cd.com"]
assert extrair_emails("ab@cd.com.xyz erro.email@gmail..com") == []
assert extrair_emails("Nenhum contato disponível.") == []
```

Essas regras de contexto são explicadas em
[REGEX_EXPLAINED.md](REGEX_EXPLAINED.md) e verificadas pela
[suíte de testes](TESTING.md).
