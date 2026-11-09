# Expressões regulares explicadas

Os padrões abaixo correspondem aos objetos `REGEX_*` de
[validador_formulario.py](../validador_formulario.py). São regras do trabalho
acadêmico; os detalhes de aceitação estão em [REQUIREMENTS.md](REQUIREMENTS.md).

## Compilação e aplicação

`re.compile()` transforma um padrão em um objeto reutilizável. As constantes
são compiladas na importação do módulo, e os validadores reutilizam esses objetos.
As strings `r"..."` preservam barras invertidas para interpretação por `re`.

```python
import re

padrao = re.compile(r"[a-zA-Z ]{1,50}")
assert padrao.fullmatch("Maria Silva") is not None
assert padrao.fullmatch("Maria\n") is None
```

`fullmatch()` exige correspondência da string inteira, retornando `Match` ou
`None`. O código converte isso para `bool` com `is not None`. Não são necessárias
âncoras `^` e `$`; `$` isoladamente poderia corresponder antes de uma quebra de
linha final. `findall()` percorre o texto e devolve todas as correspondências.

## Notação usada

| Construção | Significado no projeto |
|---|---|
| `[a-zA-Z ]` | Uma letra ASCII ou um espaço literal |
| `[0-9]` | Um algarismo ASCII; `\d` também aceitaria outros sistemas de escrita |
| `[\w._-]` | Um alfanumérico Unicode, underline, ponto ou hífen |
| `[^...]` | Classe negada: um caractere fora do conjunto |
| `\.` / `\(` / `\)` | Ponto ou parênteses literais |
| `{1,50}` | De 1 a 50 ocorrências |
| `{11}`, `{3}`, `{2}` | Quantidade exata de ocorrências |
| `{2,}` | Pelo menos 2 ocorrências |
| `?` | Zero ou uma ocorrência do grupo anterior |
| `+` | Uma ou mais ocorrências |
| `A\|B` | Alternância: aceita A ou B |
| `(?:...)` | Grupo não capturante |
| `(?!...)` | Lookahead negativo: a sequência seguinte não pode corresponder |
| `(?=...)` | Lookahead positivo: verifica o contexto seguinte sem consumi-lo |
| `(?<!...)` | Lookbehind negativo: verifica o contexto anterior sem consumi-lo |
| `\s` | Espaços em branco, incluindo tabs e quebras de linha |
| `\Z` | Fim absoluto da string no Python 3.12 |

Em `[\w._-]`, o ponto é literal por estar na classe e o hífen é literal por
estar no fim. O underline já pertence a `\w`, mas aparece explicitamente no
padrão para tornar a regra visível.

## Nome

```python
REGEX_NOME = re.compile(r"[a-zA-Z ]{1,50}")
```

Um único conjunto repetido de 1 a 50 vezes. A classe contém espaço simples,
portanto não exige que haja letras: `" "` é válido. Acentos, tabs e hífens
ficam fora da classe.

## CPF

```python
REGEX_CPF = re.compile(r"[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}")
```

A alternância separa os formatos sem pontuação e com pontuação completa.
`fullmatch()` se aplica ao padrão inteiro, incluindo ambas as alternativas.
Os grupos de 3, 3, 3 e 2 algarismos totalizam 11. Não há cálculo de dígitos.

## Telefone

```python
REGEX_TELEFONE = re.compile(r"[0-9]{11}|\([0-9]{2}\)[0-9]{5}-[0-9]{4}")
```

A segunda alternativa exige parênteses literais, 2 algarismos de DDD,
5 algarismos, hífen e 4 algarismos. Não aceita espaço, código internacional
ou ramal; tampouco verifica se o número existe.

## E-mail: padrão completo

```python
REGEX_EMAIL = re.compile(
    r"""
    (?<![^\s(\[<{"':;,!?])
    (?:(?!\.\.)[\w._-]){2,}
    @
    (?:(?!\.\.|\.[a-z]{3}\.)[\w._-]){2,}
    \.[a-z]{3}
    (?:\.(?:br|ao|pt|es|de|uk))?
    (?=\Z|[\s)\]}>"':;,!?]|\.+(?=\Z|[\s)\]}>"':;,!?]))
    """,
    re.VERBOSE,
)
```

`re.VERBOSE` permite espaços, quebras de linha e comentários no padrão,
sem que eles precisem aparecer na entrada. Espaços dentro de classes de
caracteres continuam literais. Nenhuma flag ignora diferenças de maiúsculas.

### Usuário e domínio

`(?:(?!\.\.)[\w._-]){2,}` verifica, antes de cada caractere, que não começam
dois pontos consecutivos. Em seguida consome um caractere permitido.
O grupo é repetido pelo menos duas vezes.

No domínio, o lookahead `(?!\.\.|\.[a-z]{3}\.)` também impede consumir um
ponto seguido por três letras minúsculas e outro ponto. Isso reserva o
primeiro segmento desse tipo para o registro, em vez de absorvê-lo no domínio.

`\w` aceita alfanuméricos Unicode e underline: `josé@domínio.com` é válido.
Símbolos como `+` e marcas combinantes isoladas não pertencem à classe.
Não foram acrescentadas restrições de provedores para pontos isolados nas
extremidades, nem limites máximos de tamanho.

### Registro e código de país

`\.[a-z]{3}` exige um ponto e exatamente três letras ASCII minúsculas.
`xyz` é um registro aceito; não há consulta a registros reais de domínio.

`(?:\.(?:br|ao|pt|es|de|uk))?` representa o país opcional. A alternância
restringe as seis possibilidades; `?` se aplica ao conjunto ponto + país.
Esses códigos pertencem ao endereço de e-mail e não representam prefixos
telefônicos.

| Entrada | Interpretação | Resultado |
|---|---|---|
| `ab@cd.com.br` | Domínio `cd`, registro `com`, país `br` | Aceito |
| `ab@cd.ef.com` | Domínio `cd.ef`, registro `com` | Aceito |
| `ab@cd.com.xyz` | Registro `com`, país `xyz` | Rejeitado |
| `ab@cd.abc.empresa.com` | Registro `abc`, continuação não permitida | Rejeitado |

### Bordas da extração

O lookbehind `(?<![^\s(\[<{"':;,!?])` falha quando o caractere anterior está
fora do conjunto de separadores permitido. No início do texto, não há
caractere anterior e ele passa. É uma verificação de largura fixa de um
caractere. O endereço pode começar após espaço, `(`, `[`, `<`, `{`, aspas,
apóstrofo, `:`, `;`, `,`, `!` ou `?`.

O lookahead final permite fim do texto (`\Z`), espaço, um dos separadores
de fechamento ou um ou mais pontos seguidos de fim/separador. Assim,
`(ab@cd.com...)` retorna somente `ab@cd.com`. Uma continuação `.xyz` ou
`/extra` invalida o token, sem retornar um prefixo aparentemente válido.
Os separadores não fazem parte da correspondência.

Em `fullmatch()`, as bordas externas já são início/fim da string. Pontuação
externa continua sendo rejeitada, pois não é consumida pelo padrão.

## Por que `findall()` retorna endereços inteiros

Todos os grupos do padrão são não capturantes ou verificações de contexto.
Sem grupos de captura, `findall()` retorna cada correspondência completa,
preservando ordem e repetições:

```python
from validador_formulario import extrair_emails, validar_email

assert validar_email("ab@cd.com")
assert not validar_email("(ab@cd.com)")
assert extrair_emails("(ab@cd.com), ab@cd.com.") == ["ab@cd.com", "ab@cd.com"]
assert extrair_emails("ab@cd.com.xyz") == []
```

Consulte [TESTING.md](TESTING.md) para executar os testes dessas decisões.
