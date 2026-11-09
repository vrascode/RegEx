# Validador de formulário — Trabalho de LFA

Programa de terminal em Python 3 para validar Nome, CPF, E-mail e Telefone
com expressões regulares e extrair e-mails de um texto. Utiliza somente a
biblioteca padrão: `re` no programa e `unittest` nos testes.

## Requisitos e expressões regulares

Todos os campos são validados com `fullmatch()`: o valor inteiro precisa
corresponder à expressão. As entradas são preservadas, sem `strip()`, para
que espaços ou quebras de linha indevidos não sejam ocultados.

| Campo | Regra |
|---|---|
| Nome | `[a-zA-Z ]{1,50}`: de 1 a 50 letras ASCII ou espaços, sem acentos, números ou outros símbolos. |
| CPF | `[0-9]{11}` ou `[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}`. |
| E-mail | Usuário e domínio com pelo menos 2 caracteres alfanuméricos, ponto, underline ou hífen; registro com exatamente 3 letras minúsculas e país opcional permitido. |
| Telefone | `[0-9]{11}` ou `\([0-9]{2}\)[0-9]{5}-[0-9]{4}`. |

Nome não exige sobrenome nem quantidade mínima de letras: até uma entrada
composta somente por espaços é permitida pela expressão do professor.
CPF e Telefone validam exclusivamente o formato, sem calcular dígitos,
verificar DDD ou consultar a existência do número. `[0-9]` impede algarismos
de outros sistemas de escrita nesses dois campos.

## Interpretação da expressão de e-mail

A expressão está comentada em `REGEX_EMAIL`, com `re.VERBOSE`:

- `(?:(?!\.\.)[\w._-]){2,}` aceita o usuário com pelo menos dois caracteres
  e impede pontos consecutivos, conforme os exemplos inválidos.
- O domínio usa a mesma classe e quantidade mínima, acrescentando
  `(?!\.[a-z]{3}\.)` para resolver a ambiguidade dos pontos internos.
- `\.[a-z]{3}` representa o ponto e o tipo de registro.
- `(?:\.(?:br|ao|pt|es|de|uk))?` limita o país opcional à lista exigida.
- As verificações de contexto no início e no fim não consomem caracteres:
  separam o endereço do texto e impedem correspondências parciais.

Como o domínio pode conter pontos, `ab@cd.com.xyz` teria duas interpretações:
domínio `cd.com` com registro `xyz`, ou domínio `cd` com registro `com` e país
inválido `xyz`. Para atender à rejeição obrigatória desse exemplo, adotou-se
uma regra determinística: **o primeiro segmento após ponto com exatamente
três letras minúsculas encerra o domínio e é o registro; somente um país
permitido pode aparecer depois dele**.

Assim, `ab@subdominio.empresa.com` e `ab@cd.ef.com.br` são aceitos, enquanto
`ab@cd.com.xyz`, `ab@cd.com.brx` e `ab@cd.com.br.org` são rejeitados. Pela
mesma interpretação, `ab@cd.abc.empresa.com` é rejeitado: `abc` já é lido
como registro. Essa escolha resolve a ambiguidade do enunciado e é coberta
pelos testes, tanto na validação quanto na extração.

O enunciado restringe a letras ASCII somente o campo Nome. Para preservar
os alfanuméricos permitidos no E-mail, `\w` inclui letras e números Unicode
e o underline; por exemplo, `josé@dominio.com` é aceito. Registro e país
continuam restritos às letras ASCII especificadas. Não se acrescentam
regras de provedores reais, limite de tamanho do e-mail ou exigência de
letras: pontos isolados no início/fim do usuário também são permitidos.

## Execução

Abra o PowerShell na pasta que contém estes três arquivos. Se estiver na
pasta `Trabalho 1 LFA`, entre primeiro em `lfa1`:

```powershell
Set-Location .\lfa1
python validador_formulario.py
```

Exemplo de entradas e resultado:

```text
Nome: Matheus Sulino
CPF: 123.456.789-01
E-mail: alice.souza@gmail.com
Telefone: (11)98765-4321

Resultado final: formulário APROVADO.
```

O programa também informa a aprovação ou rejeição de cada campo. Se qualquer
campo for inválido, mostra `Resultado final: formulário REJEITADO.`.
Por exemplo, as entradas `Matheus123`, `123456`, `email_invalido` e `12345`,
nessa ordem, rejeitam os quatro campos e o formulário.

## Extração de e-mails

Após o formulário, inclusive se ele for rejeitado, o programa utiliza
`REGEX_EMAIL.findall(TEXTO_ENUNCIADO)`. É o mesmo objeto compilado usado
por `validar_email()` com `fullmatch()`. Os grupos são não capturantes,
portanto o retorno contém os endereços inteiros, na ordem de ocorrência,
preservando eventuais repetições.

O texto do enunciado é mantido integralmente. O resultado é:

```text
alice.souza@gmail.com
suporte_23@empresa-tech.com
joao99@dominio123.org
```

`erro.email@gmail..com` não é retornado. As bordas aceitam espaços, quebras
de linha, parênteses, colchetes, chaves, sinais `< >`, aspas e pontuação
de frase. Um ponto final ou reticências após o endereço ficam fora da
correspondência, desde que seguidos por fim do texto ou separador.
Uma continuação como `.xyz` não é pontuação de frase: invalida o endereço
inteiro, sem extrair o prefixo `ab@cd.com`. Símbolos como `+`, `/` e `@`
adjacentes também impedem a extração de fragmentos de um endereço inválido.

## Testes

Na pasta `lfa1`, execute:

```powershell
python -m py_compile validador_formulario.py
python -m unittest discover -v
```

Se `python` não estiver disponível, use `py` nos comandos acima.

A suíte contém 66 métodos de teste, com variações adicionais em `subTest`.
Ela cobre os exemplos obrigatórios, limites de tamanho, espaços e quebras
de linha, Unicode, países, pontos internos/consecutivos, extração com
pontuação, rejeição de fragmentos e integração com `unittest.mock.patch`
para simular as quatro entradas. Os dois cenários de `main()` verificam
também que a extração contém exatamente os três endereços esperados.

Verificação realizada com Python 3.12.10: compilação concluída e todos os
66 testes aprovados, sem falhas ou erros. Os cenários A (aprovado) e B
(rejeitado) também foram executados em processos reais do programa, com
entrada padrão automatizada e conferência da saída e do código de saída.
