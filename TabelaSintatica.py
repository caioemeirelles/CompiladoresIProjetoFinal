#
# Universidade Federal de Mato Grosso
# Instituto de Computação
# Compiladores I
# Aluno: Caio Meirelles
# RGA: 201611310015
#

tabela_de_simbolos = {}
lista_de_tokens = []
tipo_esperado = ""

reservadas = ('var', 'integer', 'real', 'if', 'then')
terminais = (' ', '\t', '\n', ',', ':', ':=', '+', ',', ';', '=')
delimitador = (',', ':', ';')
operador = ('+', '-', ':=', '=')


def erro1(message):
    print("Erro: " + message)
    exit(66)


def erro2(token, esperado):
    print("Erro de sintaxe: na linha {} o esperado era {}, mas a entrada foi {}"
          "".format(token.index, esperado, token.value))
    exit(2)


def imprime_tabela():
    print('\nTabela de Simbolos:\n')
    for x in tabela_de_simbolos:
        print('Nome:', x)
        for y in tabela_de_simbolos[x]:
            print(y, ':', tabela_de_simbolos[x][y])
        print()


def pega_tabela(token):
    global tabela_de_simbolos
    aux = tabela_de_simbolos.get(token.value)
    return aux


def inserir_tabela_simbolos(token):
    global tabela_de_simbolos
    insert_ts = {token.value: {"Index": token.index}}
    busca_ts = pega_tabela(token)
    if busca_ts == None:
        tabela_de_simbolos.update(insert_ts)
    else:
        erro1("Variavel declarada anteriormente:" + token.value)


def verifica_fim_bizarro(tokens):
    if not tokens:
        erro1("Cadeia incompleta")


def Z(tokens):
    I(tokens)
    S(tokens)
    imprime_tabela()


def I(tokens):
    verifica_fim_bizarro(tokens)
    token = tokens.pop(0)
    if token.value != "var":
        erro2(token, "var")
    D(tokens)


def D(tokens):
    verifica_fim_bizarro(tokens)
    L(tokens)
    token = tokens.pop(0)
    if token.value != ":":
        erro2(token, "delimitador")
        erro1("Delimitador nao encontrado")
    K(tokens)
    O(tokens)


def K(tokens):
    verifica_fim_bizarro(tokens)
    token = tokens.pop(0)
    if token.value not in ("real", "integer"):
        erro2(token, 'Palavra Reservada')

    for aux in lista_de_tokens:
        busca_TS = pega_tabela(aux)
        busca_TS.update({"Tipo": token.value})
    lista_de_tokens.clear()


def O(tokens):
    verifica_fim_bizarro(tokens)
    if not tokens:
        erro1("Cadeia incompleta")
    tk = tokens[0]
    print("TESTE")
    print(tk)
    if tk.value != ";":
        return
    tokens.pop(0)
    D(tokens)


def L(tokens):
    verifica_fim_bizarro(tokens)
    token = tokens.pop(0)
    if token.type != "identificador":
        erro2(token, 'identificador')
    inserir_tabela_simbolos(token)
    lista_de_tokens.append(token)
    X(tokens)


def X(tokens):
    verifica_fim_bizarro(tokens)
    tk = tokens[0]
    if tk.value != ",":
        return
    tokens.pop(0)
    L(tokens)


def S(tokens):
    if not tokens:
        erro1("Esperava-se 'id' ou 'if'")

    tk = tokens.pop(0)
    if tk.type != 'identificador' and tk.value != 'if':
        erro2(tk, 'idenficador')

    if tk.type == 'identificador':
        busca = pega_tabela(tk)


        if busca == None:
            erro1("Variavel nao declarada")

        tipo_esperado = busca.get("Tipo")
        tk = tokens.pop(0)

        if tk.value != ':=':
            erro2(tk, ':=')

        E(tokens)
    elif tk.value == 'if':
        E(tokens)

        if not tokens:
            erro1("de sintaxe: linha {} | Esperado: then | Entrada: {}".format(tk.index, ''))
        tk = tokens.pop(0)

        if tk.value != 'then':
            erro2(tk, 'Palavra reservada')

        tipo_esperado = ""
        S(tokens)


def E(tokens):
    verifica_fim_bizarro(tokens)
    T(tokens)
    R(tokens)


def T(tokens):
    global tipo_esperado
    verifica_fim_bizarro(tokens)
    token = tokens.pop(0)
    if token.type != 'identificador':
        erro2(token, 'idenficador')
    busca = pega_tabela(token)

    if busca == None:
        erro1("Variavel nao declarada")

    if tipo_esperado == "":
        tipo_esperado = busca.get("Tipo")
    else:
        tipo_atual = busca.get("Tipo")
        if (not tipo_esperado == tipo_atual):
            erro1("Tipo incompativel: esperava-se tipo: %s, linha: %s, variavel: %s" % (tipo_esperado, busca.get("Index"), token.value))


def R(tokens):
    if not tokens:
        return

    tk = tokens[0]

    if tk.value == '+':
        tk = tokens.pop(0)
        T(tokens)
        R(tokens)
