"""Testes dos formatos acadêmicos, da extração e do formulário interativo."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import validador_formulario as validador


EMAILS_ESPERADOS = [
    "alice.souza@gmail.com",
    "suporte_23@empresa-tech.com",
    "joao99@dominio123.org",
]

TEXTO_ORIGINAL = """Prezado usuário,

Aqui estão os contatos do nosso time de suporte:

- alice.souza@gmail.com
- suporte_23@empresa-tech.com
- joao99@dominio123.org
- erro.email@gmail..com

Por favor, envie suas dúvidas para qualquer um dos e-mails válidos acima.

Atenciosamente,

Equipe de Atendimento"""


class TestNome(unittest.TestCase):
    def test_todas_as_letras_ascii(self):
        for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            with self.subTest(letra=letra):
                self.assertTrue(validador.validar_nome(letra))

    def test_caracteres_de_controle_em_qualquer_posicao(self):
        for controle in ("\0", "\r", "\n", "\t", "\v", "\f"):
            for nome in (controle + "Ana", "An" + controle + "a", "Ana" + controle):
                with self.subTest(nome=nome):
                    self.assertFalse(validador.validar_nome(nome))

    def test_espacos_unicode_nao_substituem_espaco_ascii(self):
        for espaco in ("\u2002", "\u2003", "\u2009", "\u202f", "\u3000", "\u200b"):
            with self.subTest(espaco=repr(espaco)):
                self.assertFalse(validador.validar_nome("Ana" + espaco + "Silva"))

    def test_nomes_do_enunciado(self):
        for nome in ("Matheus Sulino", "Joao Silva", "Maria"):
            with self.subTest(nome=nome):
                self.assertTrue(validador.validar_nome(nome))

    def test_limite_um_caractere(self):
        self.assertTrue(validador.validar_nome("A"))

    def test_limite_cinquenta_caracteres(self):
        self.assertTrue(validador.validar_nome("A" * 49 + " "))

    def test_cinquenta_e_um_caracteres(self):
        self.assertFalse(validador.validar_nome("A" * 51))

    def test_vazio(self):
        self.assertFalse(validador.validar_nome(""))

    def test_acentos_e_unicode(self):
        for nome in ("João Silva", "José", "Ana界", "Аna"):
            with self.subTest(nome=nome):
                self.assertFalse(validador.validar_nome(nome))

    def test_numeros_e_caracteres_especiais(self):
        for nome in ("Maria123", "Ana@Silva", "Ana-Silva", "Ana_Silva"):
            with self.subTest(nome=nome):
                self.assertFalse(validador.validar_nome(nome))

    def test_espacos_permitidos_sem_exigir_letras(self):
        for nome in (" ", " " * 50, " Maria ", "Joao  Silva"):
            with self.subTest(nome=nome):
                self.assertTrue(validador.validar_nome(nome))

    def test_tab_e_quebra_de_linha(self):
        for nome in ("Maria\n", "Maria\r\n", "Maria\tSilva", "Ana\u00a0Silva"):
            with self.subTest(nome=nome):
                self.assertFalse(validador.validar_nome(nome))


class TestCPF(unittest.TestCase):
    def test_zeros_iniciais_nos_dois_formatos(self):
        for cpf in ("00123456789", "001.234.567-89"):
            with self.subTest(cpf=cpf):
                self.assertTrue(validador.validar_cpf(cpf))

    def test_cada_separador_da_mascara_e_obrigatorio(self):
        original = "123.456.789-01"
        for indice in (3, 7, 11):
            for separador in ("", " ", "/", "\u2010", "\uff0e"):
                cpf = original[:indice] + separador + original[indice + 1:]
                with self.subTest(cpf=cpf):
                    self.assertFalse(validador.validar_cpf(cpf))

    def test_nao_aceita_digito_unicode_misturado_com_ascii(self):
        for original in ("12345678901", "123.456.789-01"):
            for indice, caractere in enumerate(original):
                if caractere.isascii() and caractere.isdigit():
                    cpf = original[:indice] + "\u0661" + original[indice + 1:]
                    with self.subTest(cpf=cpf):
                        self.assertFalse(validador.validar_cpf(cpf))

    def test_sem_pontuacao(self):
        self.assertTrue(validador.validar_cpf("12345678901"))

    def test_com_pontuacao(self):
        self.assertTrue(validador.validar_cpf("123.456.789-01"))

    def test_nao_exige_calculo_dos_digitos(self):
        for cpf in ("00000000000", "000.000.000-00", "11111111111"):
            with self.subTest(cpf=cpf):
                self.assertTrue(validador.validar_cpf(cpf))

    def test_comprimentos_incorretos(self):
        for cpf in ("1234567890", "123456789012"):
            with self.subTest(cpf=cpf):
                self.assertFalse(validador.validar_cpf(cpf))

    def test_pontuacao_incorreta_ou_incompleta(self):
        for cpf in ("123.456.789.01", "123-456-789-01", "123.456789-01", "123456789-01"):
            with self.subTest(cpf=cpf):
                self.assertFalse(validador.validar_cpf(cpf))

    def test_letras(self):
        self.assertFalse(validador.validar_cpf("abcdefghijk"))

    def test_vazio(self):
        self.assertFalse(validador.validar_cpf(""))

    def test_espacos_e_quebras_de_linha(self):
        for cpf in (" 12345678901", "12345678901 ", "123 45678901", "12345678901\n"):
            with self.subTest(cpf=cpf):
                self.assertFalse(validador.validar_cpf(cpf))

    def test_algarismos_unicode(self):
        for cpf in ("１２３４５６７８９０１", "١٢٣٤٥٦٧٨٩٠١"):
            with self.subTest(cpf=cpf):
                self.assertFalse(validador.validar_cpf(cpf))


class TestEmail(unittest.TestCase):
    def test_validos_sem_pais(self):
        for email in (*EMAILS_ESPERADOS, "ab@cd.com"):
            with self.subTest(email=email):
                self.assertTrue(validador.validar_email(email))

    def test_todos_os_paises_permitidos(self):
        for pais in ("br", "ao", "pt", "es", "de", "uk"):
            with self.subTest(pais=pais):
                self.assertTrue(validador.validar_email(f"ab@cd.com.{pais}"))

    def test_paises_nao_permitidos(self):
        for pais in ("fr", "us", "ar", "BR", "xyz", "brx"):
            with self.subTest(pais=pais):
                self.assertFalse(validador.validar_email(f"ab@cd.com.{pais}"))

    def test_usuario_curto(self):
        for email in ("a@cd.com", "@cd.com"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_dominio_curto(self):
        for email in ("ab@c.com", "ab@.com"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_tipo_de_registro_tres_minusculas(self):
        for email in ("ab@cd.co", "ab@cd.COM", "ab@cd.comm", "ab@cd.c0m", "ab@cd.cóm"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))
        self.assertTrue(validador.validar_email("ab@cd.xyz"))

    def test_pontos_consecutivos(self):
        for email in ("erro.email@gmail..com", "a..b@cd.com", "ab@cd..empresa.com", "ab@cd.com..br"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_arroba_obrigatoria_e_unica(self):
        for email in ("ab@@cd.com", "abcd.com", "ab@cd@ef.com"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_sufixos_adicionais(self):
        for email in ("ab@cd.com.br.extra", "ab@cd.com.br.org", "ab@cd.org.com"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_caracteres_permitidos_no_usuario_e_dominio(self):
        self.assertTrue(validador.validar_email("A9._-@D9._-tech.com"))

    def test_pontos_internos_no_dominio(self):
        for email in ("ab@subdominio.empresa.com", "ab@cd.ef.com.br", "ab@cd.uk.empresa.org"):
            with self.subTest(email=email):
                self.assertTrue(validador.validar_email(email))

    def test_segmento_ambiguo_e_interpretado_como_registro(self):
        self.assertFalse(validador.validar_email("ab@cd.abc.empresa.com"))
        self.assertTrue(validador.validar_email("ab@cd.abc.br"))

    def test_ponto_isolado_permitido_pela_classe(self):
        for email in (".ab@cd.com", "ab.@cd.com", "ab@.cd.com"):
            with self.subTest(email=email):
                self.assertTrue(validador.validar_email(email))

    def test_vazio(self):
        self.assertFalse(validador.validar_email(""))

    def test_espacos_e_quebras_de_linha(self):
        for email in (" ab@cd.com", "ab@cd.com ", "ab @cd.com", "ab@c d.com", "ab@cd.com\n"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_unicode_alfanumerico_no_usuario_e_dominio(self):
        # Somente o campo Nome exige letras ASCII no enunciado.
        for email in ("josé@dominio.com", "ab@domínio.com", "用户@dominio.com", "１２@cd.com"):
            with self.subTest(email=email):
                self.assertTrue(validador.validar_email(email))

    def test_unicode_invalido_no_registro_e_simbolos(self):
        for email in ("ab@cd.cöm", "ab@cd.com.bŕ", "ab😀@cd.com", "ab\u0301@cd.com"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))

    def test_caracteres_nao_permitidos(self):
        for email in ("ab+tag@cd.com", "ab@cd/ef.com", "ab%cd@ef.com"):
            with self.subTest(email=email):
                self.assertFalse(validador.validar_email(email))


class TestTelefone(unittest.TestCase):
    def test_sem_pontuacao(self):
        self.assertTrue(validador.validar_telefone("11987654321"))

    def test_com_pontuacao(self):
        self.assertTrue(validador.validar_telefone("(11)98765-4321"))

    def test_nao_verifica_ddd_ou_existencia(self):
        for telefone in ("00000000000", "(00)00000-0000"):
            with self.subTest(telefone=telefone):
                self.assertTrue(validador.validar_telefone(telefone))

    def test_comprimentos_incorretos(self):
        for telefone in ("1198765432", "119876543210"):
            with self.subTest(telefone=telefone):
                self.assertFalse(validador.validar_telefone(telefone))

    def test_pontuacao_incorreta(self):
        for telefone in ("(11)9876-54321", "11 98765-4321", "11-98765-4321", "(11)987654321"):
            with self.subTest(telefone=telefone):
                self.assertFalse(validador.validar_telefone(telefone))

    def test_espacos_e_quebras_de_linha(self):
        for telefone in ("(11) 98765-4321", " 11987654321", "11987654321 ", "11987654321\n"):
            with self.subTest(telefone=telefone):
                self.assertFalse(validador.validar_telefone(telefone))

    def test_vazio_letras_e_unicode(self):
        for telefone in ("", "abcdefghijk", "１１９８７６５４３２１", "(١١)98765-4321"):
            with self.subTest(telefone=telefone):
                self.assertFalse(validador.validar_telefone(telefone))


class TestExtracao(unittest.TestCase):
    def test_texto_original_exato(self):
        self.assertEqual(validador.TEXTO_ENUNCIADO, TEXTO_ORIGINAL)

    def test_resultado_do_texto_original(self):
        self.assertEqual(validador.extrair_emails(TEXTO_ORIGINAL), EMAILS_ESPERADOS)

    def test_parenteses_colchetes_chaves_e_aspas(self):
        for abertura, fechamento in (("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"), ('"', '"'), ("'", "'")):
            with self.subTest(abertura=abertura):
                self.assertEqual(validador.extrair_emails(f"{abertura}ab@cd.com{fechamento}"), ["ab@cd.com"])

    def test_pontuacao_de_frase(self):
        for pontuacao in (".", ",", ";", ":", "!", "?", "...", ".)"):
            with self.subTest(pontuacao=pontuacao):
                self.assertEqual(validador.extrair_emails(f"Contato: ab@cd.com{pontuacao}"), ["ab@cd.com"])

    def test_quebras_de_linha_e_tabs(self):
        self.assertEqual(validador.extrair_emails("ab@cd.com\r\nxy@empresa.org\tzz@dominio.com.br"),
                         ["ab@cd.com", "xy@empresa.org", "zz@dominio.com.br"])

    def test_preserva_ordem_e_repeticoes(self):
        self.assertEqual(validador.extrair_emails("xy@ef.org ab@cd.com xy@ef.org"),
                         ["xy@ef.org", "ab@cd.com", "xy@ef.org"])

    def test_paises_validos(self):
        emails = [f"ab@cd.com.{pais}" for pais in ("br", "ao", "pt", "es", "de", "uk")]
        self.assertEqual(validador.extrair_emails("; ".join(emails)), emails)

    def test_rejeita_sufixos_invalidos_sem_extrair_prefixo(self):
        for email in ("ab@cd.com.fr", "ab@cd.com.xyz", "ab@cd.com.brx", "ab@cd.com.br.extra", "ab@cd.com.br.org", "ab@cd.comm"):
            with self.subTest(email=email):
                self.assertEqual(validador.extrair_emails(f"({email}),"), [])

    def test_rejeita_pontos_consecutivos_sem_extrair_sufixo(self):
        for email in ("erro.email@gmail..com", "erro..email@gmail.com", "ab@cd.com..br", "ab@cd.com..xyz"):
            with self.subTest(email=email):
                self.assertEqual(validador.extrair_emails(email), [])

    def test_rejeita_prefixos_invalidos_sem_extrair_sufixo(self):
        for email in ("ab@@cd.com", "xy@ab@cd.com", "foo+ab@cd.com", "/ab@cd.com", "😀ab@cd.com", "a\u0301ab@cd.com"):
            with self.subTest(email=email):
                self.assertEqual(validador.extrair_emails(email), [])

    def test_unicode_permitido_e_extraido_integralmente(self):
        emails = ["josé@dominio.com", "ab@domínio.com", "用户@dominio.com"]
        self.assertEqual(validador.extrair_emails(", ".join(emails)), emails)

    def test_rejeita_terminacoes_invalidas_sem_extrair_prefixo(self):
        for email in ("ab@cd.comé", "ab@cd.com/extra", "ab@cd.com+extra", "ab@cd.com@xy.org", "ab@cd.com_", "ab@cd.com-", "ab@cd.com.xyz."):
            with self.subTest(email=email):
                self.assertEqual(validador.extrair_emails(email), [])

    def test_rejeita_campos_curtos(self):
        self.assertEqual(validador.extrair_emails("a@cd.com ab@c.com ab@cd.co"), [])

    def test_texto_vazio_ou_sem_emails(self):
        for texto in ("", " \n\t", "Nenhum contato disponível."):
            with self.subTest(texto=texto):
                self.assertEqual(validador.extrair_emails(texto), [])

    def test_invalidos_nao_escondem_validos_vizinhos(self):
        self.assertEqual(validador.extrair_emails("erro.email@gmail..com, ab@cd.com; ab@cd.com.xyz\nxy@empresa.org."),
                         ["ab@cd.com", "xy@empresa.org"])

    def test_validacao_e_extracao_reutilizam_objeto_compilado(self):
        with patch.object(validador, "REGEX_EMAIL") as regex:
            regex.fullmatch.return_value = None
            regex.findall.return_value = []
            self.assertFalse(validador.validar_email("inválido"))
            self.assertEqual(validador.extrair_emails("texto"), [])
            regex.fullmatch.assert_called_once_with("inválido")
            regex.findall.assert_called_once_with("texto")


class TestFormulario(unittest.TestCase):
    ENTRADAS_VALIDAS = ["Matheus Sulino", "123.456.789-01", "alice.souza@gmail.com", "(11)98765-4321"]
    ENTRADAS_INVALIDAS = ["Matheus123", "123456", "email_invalido", "12345"]

    def executar(self, entradas, funcao=validador.processar_formulario):
        saida = io.StringIO()
        with patch("builtins.input", side_effect=entradas) as entrada, redirect_stdout(saida):
            funcao()
        self.assertEqual(entrada.call_args_list, [unittest.mock.call(f"{campo}: ") for campo in ("Nome", "CPF", "E-mail", "Telefone")])
        return saida.getvalue()

    def test_formulario_aprovado(self):
        saida = self.executar(self.ENTRADAS_VALIDAS)
        for campo in ("Nome", "CPF", "E-mail", "Telefone"):
            self.assertIn(f"{campo} APROVADO.", saida)
        self.assertIn("Resultado final: formulário APROVADO.", saida)

    def test_formulario_rejeitado(self):
        saida = self.executar(self.ENTRADAS_INVALIDAS)
        for campo in ("Nome", "CPF", "E-mail", "Telefone"):
            self.assertIn(f"{campo} REJEITADO:", saida)
        self.assertIn("Resultado final: formulário REJEITADO.", saida)

    def test_qualquer_campo_invalido_rejeita_formulario(self):
        for indice, campo in enumerate(("Nome", "CPF", "E-mail", "Telefone")):
            with self.subTest(campo=campo):
                entradas = self.ENTRADAS_VALIDAS.copy()
                entradas[indice] = self.ENTRADAS_INVALIDAS[indice]
                self.assertIn("Resultado final: formulário REJEITADO.", self.executar(entradas))

    def test_campos_vazios(self):
        saida = self.executar(["", "", "", ""])
        self.assertEqual(saida.count("REJEITADO:"), 4)
        self.assertIn("Resultado final: formulário REJEITADO.", saida)

    def test_entrada_nao_remove_espacos_proibidos(self):
        for indice in (1, 2, 3):
            with self.subTest(indice=indice):
                entradas = self.ENTRADAS_VALIDAS.copy()
                entradas[indice] += " "
                self.assertIn("Resultado final: formulário REJEITADO.", self.executar(entradas))

    def test_main_cenario_a_e_extracao(self):
        saida = self.executar(self.ENTRADAS_VALIDAS, validador.main)
        self.assertIn("Resultado final: formulário APROVADO.", saida)
        extraidos = saida.split("=== E-mails válidos extraídos do texto ===\n")[1].splitlines()
        self.assertEqual(extraidos, EMAILS_ESPERADOS)

    def test_main_cenario_b_e_extracao(self):
        saida = self.executar(self.ENTRADAS_INVALIDAS, validador.main)
        self.assertIn("Resultado final: formulário REJEITADO.", saida)
        extraidos = saida.split("=== E-mails válidos extraídos do texto ===\n")[1].splitlines()
        self.assertEqual(extraidos, EMAILS_ESPERADOS)


if __name__ == "__main__":
    unittest.main()
