# Requisitos de validação

Os cinco requisitos abaixo descrevem a interpretação implementada no trabalho
de Linguagens Formais e Autômatos. A referência disponível é o código e o
texto armazenado em `TEXTO_ENUNCIADO`; o documento original do professor não
está neste repositório.

As entradas são strings, preservadas sem `strip()`, normalização ou conversão
de maiúsculas. Os quatro validadores retornam `bool` e usam `fullmatch()`.

## 1. Nome

De **1 a 50 caracteres**, exclusivamente letras ASCII (`A-Z`, `a-z`) e
espaço simples (`U+0020`). Não é obrigatório informar sobrenome.

| Aceito | Rejeitado | Motivo da rejeição |
|---|---|---|
| `Maria` | `João` | Acento |
| `Joao Silva` | `Maria123` | Algarismos |
| ` Maria ` | `Ana-Silva` | Hífen |
| Um espaço simples | String vazia | Mínimo de 1 caractere |
| 50 letras `A` | 51 letras `A` | Máximo de 50 caracteres |

A expressão permite nomes compostos apenas por espaços e espaços repetidos.
Tabs, quebras de linha e espaços Unicode, como `U+00A0`, são rejeitados.

## 2. CPF

Exatamente **11 algarismos ASCII**, sem pontuação, ou a máscara completa
`000.000.000-00`. Pontos e hífen são literais e têm posições fixas.

| Aceito | Rejeitado | Motivo da rejeição |
|---|---|---|
| `12345678901` | `1234567890` | Quantidade de algarismos |
| `123.456.789-01` | `123.456.789.01` | Separador incorreto |
| `00000000000` | `123456789-01` | Máscara parcial |
| `000.000.000-00` | `１２３４５６７８９０１` | Algarismos Unicode |

A aprovação indica somente formato. Não há cálculo dos dígitos verificadores,
consulta cadastral ou rejeição de sequências repetidas.

## 3. E-mail

Estrutura: **`usuario@dominio.registro[.pais]`**, em que os colchetes indicam
opcionalidade e não fazem parte do endereço.

| Parte | Regra |
|---|---|
| Usuário | Pelo menos 2 caracteres de `\w`, ponto, underline ou hífen |
| Domínio | Pelo menos 2 caracteres da mesma classe |
| Registro | Exatamente 3 letras ASCII minúsculas |
| País | Opcional: `br`, `ao`, `pt`, `es`, `de` ou `uk` |
| Pontos | Dois pontos consecutivos são rejeitados |

`\w` inclui alfanuméricos Unicode e underline. Usuário e domínio podem conter
maiúsculas; registro e país são sensíveis a maiúsculas. Não há limite máximo
explícito de comprimento na expressão.

| Aceito | Rejeitado | Motivo da rejeição |
|---|---|---|
| `ab@cd.com` | `a@cd.com` | Usuário curto |
| `ab@cd.xyz` | `ab@c.com` | Domínio curto |
| `ab@cd.com.br` | `ab@cd.com.fr` | País fora da lista |
| `josé@domínio.com` | `ab@cd.COM` | Registro em maiúsculas |
| `ab@subdominio.empresa.com` | `erro.email@gmail..com` | Pontos consecutivos |
| `.ab@cd.com` | `ab+tag@cd.com` | `+` fora da classe permitida |

### Interpretação dos domínios e países

O domínio aceita pontos internos. Para resolver a ambiguidade com o registro,
o primeiro segmento após ponto com **três letras minúsculas** encerra o domínio
e é tratado como registro. Depois dele, somente um país permitido pode aparecer.

- `ab@cd.ef.com.br`: aceito; `cd.ef` é o domínio, `com` o registro e `br` o país.
- `ab@cd.com.xyz`: rejeitado; `com` já é registro e `xyz` não é país permitido.
- `ab@cd.abc.empresa.com`: rejeitado; `abc` já é registro.
- `ab@cd.uk.empresa.org`: aceito; `uk` tem duas letras e faz parte do domínio.

Não são aplicadas regras adicionais de provedores ou validação de DNS.
Pontos isolados nas extremidades de usuário ou domínio podem ser aceitos
pela classe de caracteres. A explicação completa está em
[REGEX_EXPLAINED.md](REGEX_EXPLAINED.md).

## 4. Telefone

Exatamente **11 algarismos ASCII**, ou a máscara completa `(00)00000-0000`.
Não pode haver espaço entre o DDD e o número.

| Aceito | Rejeitado | Motivo da rejeição |
|---|---|---|
| `11987654321` | `1198765432` | Quantidade de algarismos |
| `(11)98765-4321` | `(11) 98765-4321` | Espaço adicional |
| `(00)00000-0000` | `+5511987654321` | Código internacional não previsto |
| `00000000000` | `(11)9876-5432` | Número local com 8 algarismos |

Não se verifica DDD, operadora, existência do número ou prefixo de celular.
Os códigos de país da regra de **e-mail** não se aplicam ao telefone.

## 5. Extração de e-mails

`extrair_emails(texto)` usa o mesmo `REGEX_EMAIL` da validação, com `findall()`.
Retorna uma lista de endereços inteiros, em ordem, preservando repetições.

O endereço deve estar isolado por início/fim do texto, espaços ou pontuação
permitida. Pontos de frase e reticências ficam fora do resultado. Símbolos
adjacentes como `+`, `/` ou `@` impedem extrair fragmentos de tokens inválidos.

No texto do enunciado, os três resultados são:

```text
alice.souza@gmail.com
suporte_23@empresa-tech.com
joao99@dominio123.org
```

`erro.email@gmail..com` é ignorado. Em `ab@cd.com.xyz`, o prefixo `ab@cd.com`
também não é extraído.

## Resultado do formulário

Nome, CPF, E-mail e Telefone são solicitados uma vez, nessa ordem. Cada campo
recebe uma mensagem própria; qualquer rejeição torna o formulário rejeitado.
A extração do texto fixo ocorre em seguida, inclusive após rejeição.

Consulte os [exemplos executáveis](EXAMPLES.md) e a
[estratégia de testes](TESTING.md).

## Rastreabilidade entre requisitos, código e testes

| Requisito | Função pública | Classe de teste |
|---|---|---|
| Nome | `validar_nome(nome)` | `TestNome` |
| CPF | `validar_cpf(cpf)` | `TestCPF` |
| E-mail | `validar_email(email)` | `TestEmail` |
| Telefone | `validar_telefone(telefone)` | `TestTelefone` |
| Extração | `extrair_emails(texto)` | `TestExtracao` |
| Integração dos campos | `processar_formulario()` e `main()` | `TestFormulario` |

As funções de validação recebem strings e retornam `True` ou `False`.
`extrair_emails()` recebe uma string e retorna `list[str]`. O fluxo interativo
escreve as mensagens no terminal; não há persistência de formulários em disco.
