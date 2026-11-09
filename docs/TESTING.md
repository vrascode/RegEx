# Testes automatizados

A suíte usa somente `unittest`, `unittest.mock`, `io` e `contextlib`, da
biblioteca padrão. Não consulta rede, serviços, dados pessoais reais ou
credenciais. Execute os comandos na pasta que contém o código principal.

## Compilação e suíte completa

```powershell
python -m py_compile validador_formulario.py
python -m unittest discover -v
```

Se `python` não estiver no PATH do Windows, substitua por `py -3.12`.
`py_compile` verifica a sintaxe e cria cache local; não substitui os testes.
`unittest discover` descobre os métodos `test_*` de `test_validador_formulario.py`.
Qualquer falha ou erro produz código de saída diferente de zero.

## Organização da suíte

| Classe | O que verifica |
|---|---|
| `TestNome` | Limites de comprimento, ASCII, espaços, acentos e símbolos |
| `TestCPF` | Máscaras, quantidade de algarismos, Unicode e validação somente de formato |
| `TestEmail` | Usuário, domínio, registro, países, pontos e Unicode |
| `TestTelefone` | Máscaras, comprimento, separadores e ausência de consulta de DDD |
| `TestExtracao` | Texto original, ordem, repetições, pontuação e rejeição de fragmentos |
| `TestFormulario` | Prompts, mensagens, resultado agregado e execução de `main()` |

`subTest()` identifica cada entrada dentro de um método parametrizado.
A contagem apresentada por `unittest` corresponde aos métodos executados,
não ao total de valores verificados nos laços.

## Executar um grupo ou caso específico

```powershell
python -m unittest test_validador_formulario.TestEmail -v
python -m unittest test_validador_formulario.TestExtracao.test_resultado_do_texto_original -v
```

## Integração do formulário

`patch("builtins.input", side_effect=...)` fornece as quatro entradas sem
interação manual. `redirect_stdout()` captura a saída para conferir mensagens
e resultado. Os testes garantem que um campo inválido basta para rejeitar o
formulário e que a extração ainda acontece após a rejeição.

O texto original é comparado integralmente, e a extração precisa retornar
exatamente os três endereços esperados, em ordem. Os testes de borda evitam
extrair partes de endereços inválidos como `ab@cd.com.xyz`.

## Resultado verificado na análise inicial

Ambiente local: **Python 3.12.10**, Windows. Resultado observado:

```text
python -m py_compile validador_formulario.py
# Código de saída: 0; sem mensagens de erro.

python -m unittest discover -v
Ran 66 tests
OK
```

O tempo de execução foi omitido por variar entre execuções. Os cenários
aprovado e rejeitado também foram executados em processos reais, com
conferência do código de saída e dos três e-mails extraídos. Veja as
[entradas e saídas](EXAMPLES.md).

## GitHub Actions

O workflow [python-tests.yml](../.github/workflows/python-tests.yml) executa
em pushes para `main` e pull requests cujo destino é `main`, em Ubuntu com
Python 3.12. Ele faz checkout, configura o interpretador, compila o arquivo
principal e executa a mesma suíte com `unittest discover -v`.

Não instala dependências do projeto, não usa secrets e não consulta serviços
externos durante os testes. A infraestrutura do próprio GitHub Actions
obtém as actions e configura o Python. As permissões do token são limitadas
à leitura do conteúdo; qualquer comando que termine com erro falha o job.

Os comandos assumem que os arquivos Python estão na **raiz do repositório**.
O badge do README consulta o estado real desse workflow na branch `main`;
antes da primeira publicação/execução ele pode aparecer sem resultado.
Para confirmar uma execução remota, abra a aba Actions e confira o commit
associado. A configuração local não comprova execução bem-sucedida no GitHub.
