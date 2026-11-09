
"""Validação de formulário e extração de e-mails com expressões regulares.

As validações usam fullmatch, que exige que a string inteira siga a regra.
Ao contrário de $, fullmatch não permite uma quebra de linha final excedente.
"""

import re

# Nome: de 1 a 50 caracteres, somente letras de A a Z e espaços.
REGEX_NOME = re.compile(r"[a-zA-Z ]{1,50}")

# CPF: 11 algarismos ou 000.000.000-00 (pontos nas posições 3 e 7, hífen na 11).
# Usa [0-9] porque \d também aceitaria algarismos de outros sistemas de escrita.
REGEX_CPF = re.compile(r"[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}")

# Telefone: 11 algarismos ou (00)00000-0000.
REGEX_TELEFONE = re.compile(r"[0-9]{11}|\([0-9]{2}\)[0-9]{5}-[0-9]{4}")

# E-mail: a mesma expressão valida o formulário (fullmatch) e varre o texto
# (findall). Os limites de início e fim só fazem diferença na varredura: exigem
# que o endereço esteja isolado, sem extrair partes de endereços inválidos.
# Como pontos internos são permitidos, existe ambiguidade em cd.com.xyz.
# Interpretação: o primeiro segmento após ponto com três letras minúsculas é
# o registro; depois dele, somente um país permitido pode aparecer. Assim,
# "com" não pode ser absorvido pelo domínio para aceitar "xyz" como registro.
# \w mantém os alfanuméricos Unicode e o underline: o enunciado restringe a
# letras ASCII somente o Nome. Ponto e hífen são permitidos explicitamente.
REGEX_EMAIL = re.compile(
    r"""
    (?<![^\s(\[<{"':;,!?])         # início: texto, espaço ou pontuação de abertura
    (?:(?!\.\.)[\w._-]){2,}        # usuário: 2 ou mais símbolos, sem ".."
    @
    (?:(?!\.\.|\.[a-z]{3}\.)[\w._-]){2,}  # domínio sem absorver um registro
    \.[a-z]{3}                     # tipo de registro: exatamente 3 minúsculas
    (?:\.(?:br|ao|pt|es|de|uk))?   # país: opcional, limitado à lista do enunciado
    (?=\Z|[\s)\]}>"':;,!?]|\.+(?=\Z|[\s)\]}>"':;,!?]))
                                   # fim: texto, separador ou pontos de frase
    """,
    re.VERBOSE,
)

TEXTO_ENUNCIADO = """Prezado usuário,

Aqui estão os contatos do nosso time de suporte:

- alice.souza@gmail.com
- suporte_23@empresa-tech.com
- joao99@dominio123.org
- erro.email@gmail..com

Por favor, envie suas dúvidas para qualquer um dos e-mails válidos acima.

Atenciosamente,

Equipe de Atendimento"""


def validar_nome(nome):
    """Retorna True se o nome atender às regras do campo Nome."""
    return REGEX_NOME.fullmatch(nome) is not None


def validar_cpf(cpf):
    """Retorna True se o CPF estiver em um dos dois formatos aceitos."""
    return REGEX_CPF.fullmatch(cpf) is not None


def validar_email(email):
    """Retorna True se a string inteira for um e-mail válido."""
    return REGEX_EMAIL.fullmatch(email) is not None


def validar_telefone(telefone):
    """Retorna True se o telefone estiver em um dos dois formatos aceitos."""
    return REGEX_TELEFONE.fullmatch(telefone) is not None


def extrair_emails(texto):
    """Retorna, na ordem em que aparecem, os e-mails válidos de um texto.

    O findall devolve o endereço inteiro porque REGEX_EMAIL só tem grupos não
    capturantes, escritos com (?:...).
    """
    return REGEX_EMAIL.findall(texto)


# Cada campo: rótulo, função de validação e orientação usada na rejeição.
CAMPOS = (
    ("Nome", validar_nome,
     "use de 1 a 50 caracteres, somente letras de A a Z (sem acento) e espaços."),
    ("CPF", validar_cpf,
     "use 11 algarismos ou o formato 000.000.000-00."),
    ("E-mail", validar_email,
     "use usuario@dominio.xxx (xxx: 3 letras minúsculas), com país opcional: "
     ".br, .ao, .pt, .es, .de ou .uk."),
    ("Telefone", validar_telefone,
     "use 11 algarismos ou o formato (00)00000-0000."),
)


def processar_formulario():
    """Solicita cada campo, informa o resultado dele e apresenta o resultado final."""
    print("=== Formulário ===")
    formulario_aprovado = True

    for rotulo, validar, orientacao in CAMPOS:
        valor = input(f"{rotulo}: ")
        if validar(valor):
            print(f"  {rotulo} APROVADO.")
        else:
            print(f"  {rotulo} REJEITADO: {orientacao}")
            formulario_aprovado = False

    resultado = "APROVADO" if formulario_aprovado else "REJEITADO"
    print(f"\nResultado final: formulário {resultado}.")


def main():
    """Executa o formulário e, em seguida, a extração de e-mails do texto."""
    processar_formulario()

    print("\n=== E-mails válidos extraídos do texto ===")
    for email in extrair_emails(TEXTO_ENUNCIADO):
        print(email)


if __name__ == "__main__":
    main()
