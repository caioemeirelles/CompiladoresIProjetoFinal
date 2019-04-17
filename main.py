#
# Universidade Federal de Mato Grosso
# Instituto de Computação
# Compiladores I
# Aluno: Caio Meirelles
# RGA: 201611310015
#

path = input("Digite o nome do arquivo a ser verificado")
tabela_de_simbolos = {}
lista_token = []
tipo_esperado = ""


# palavras reservadas, delimitadores, operadores e terminais
reservadas = ('var', 'integer', 'real', 'if', 'then')
delimitador = (',', ':', ';')
operador = ('+', '-', ':=', '=')
terminais = (' ', '\t', '\n', ',', ':', ':=', '+', ',', ';', '=')


class Token:
    def __init__(self, _value, _type, _index):
        self.type = _type
        self.value = _value
        self.index = _index

    def __str__(self):
        return "'{}' {} linha {}".format(self.value, self.type, self.index)

    __repr__ = __str__


# olha o primeiro elemento de uma pilha
def peek(l, ch):
    if len(l) - 1 > l.index(ch):
        return l[l.index(ch)+1]
    return ch


def inserir_TS(token):
    global tabela_de_simbolos
    insert_ts = {token.value: {"Token": token.type}}
    busca_ts = get_ts(token)
    if busca_ts == None:
        tabela_TS.update(insert_ts)
    else:
        print("Variavel ja declarada:", (token.value))
        exit()

def get_ts(token):
    global tabela_de_simbolos
    get_dict = tabela_TS.get(token.value)
    return get_dict


def check(token):
    if not token:
        print("Cadeia incompleta")
        exit()


def Z(token):
    I(token)
    S(token)
    print('\nTabela de Simbolos:')
    for x in tabela_de_simbolos:
        print('Nome:',x)
        for y in tabela_de_simbolos[x]:
            print(y,':', tabela_de_simbolos[x][y])


def erro(token, esperado):
    print("Erro de sintaxe: Linha {} | Esperado: {} | Entrada: {}"
          "".format(token.index,esperado, token.value))
    exit()


def I(tokens):
    check(tokens)
    token = tokens.pop(0)
    if token.value != "var":
        erro(token, "var")
    D(tokens)


def D(tokens):
    check(tokens)
    L(tokens)
    token = tokens.pop(0)
    if token.value != ":":
        erro(token, "delimitador")
        exit()
    K(tokens)
    O(tokens)


def K(tokens):
    check(tokens)
    token = tokens.pop(0)
    #print(token)
    if token.value not in ("real", "integer"):
        erro(token, 'Palavra Reservada')
    for elemento in lista_token:
        busca_TS = get_ts(elemento)
        busca_TS.update({"Tipo": token.value})
    lista_token.clear()


def O(tokens):
    check(tokens)
    if not tokens:
        print("Erro: cadeia incompleta")
        exit()
    token = tokens[0]
    #print(token)
    if token.value != ";":
        return
    tokens.pop(0)
    D(tokens)


def L(tokens):
    check(tokens)
    token = tokens.pop(0)
    if token.type != "identificador":
        erro(token, 'identificador')
    inserir_TS(token)
    lista_token.append(token)
    X(tokens)


def X(tokens):
    check(tokens)
    token = tokens[0]
    if token.value != ",":
        return
    tokens.pop(0)
    L(tokens)


def S(tokens):
    if not tokens:
        print("Erro: 'id' ou 'if' esperado")
        exit()
    token = tokens.pop(0)
    if token.type != 'identificador' and token.value != 'if':
        erro(token, 'erro de idenficador')
    if token.type == 'identificador':

        busca=get_ts(token)
        tipo_esperado = busca.get("Tipo")
        token = tokens.pop(0)
        if busca == None:
            print("Erro: variável não declarada")
            exit()
        if token.value != ':=':
            erro(token, ':=')
        E(tokens)
    elif token.value == 'if':
        E(tokens)

        if not tokens:
            print("Erro de sintaxe: linha {} | Esperado: then | Entrada: {}".format(token.index, ''))
            exit()
        token = tokens.pop(0)
        if token.value != 'then':
            erro(token, 'Palavra reservada')
        tipo_esperado = ""
        S(tokens)


def E(tokens):
    check(tokens)
    T(tokens)
    R(tokens)


def T(tokens):
    global tipo_esperado
    check(tokens)
    token = tokens.pop(0)
    if token.type != 'identificador':
        erro(token, 'idenficador')
    busca = get_ts(token)

    if busca == None:
        print("Erro:variável não declarada")
        exit()
    if (tipo_esperado == ""):
        tipo_esperado = busca.get("Tipo")
    else:
        tipo_atual = busca.get("Tipo")
        if (not tipo_esperado == tipo_atual):
            print("Tipo de varíavel incompatível, esperava-se tipo: %s, variavel: %s" \
                            % (tipo_esperado,token.value))
            exit()


def R(tokens):
    if not tokens:
        return
    token = tokens[0]

    if token.value != '+':
        return

    token = tokens.pop(0)
    T(tokens)
    R(tokens)


def tokenizer(l, i):
    aux = ''
    tkns = []
    for ch in l:
        if ch in terminais:
            if aux:
                if aux == ':=':
                    tkns.append(Token(aux, "operador", i))
                    aux = ''
                    continue
                if aux in reservadas:
                   tkns.append(Token(aux, "reservada" , i))
                elif aux in delimitador:
                    tkns.append(Token(aux, "delimitador", i))
                elif aux in operador:
                    tkns.append(Token(aux, "operador", i))
                elif aux.isalpha():
                    tkns.append(Token(aux, 'identificador', i))
                else:
                    tkns.append(Token(aux, 'invalido', i))

                aux = ''
            if ch == ':' and peek(l, ch) == '=':
                aux = ':='
            elif ch in delimitador:
                tkns.append(Token(ch, 'delimitador', i))
            elif ch in operador:
                tkns.append(Token(ch, 'operador', i))
        else:
            aux+= ch
    else:
        if aux in reservadas:
            tkns.append(Token(aux, "reservada", i))
        elif aux in delimitador:
            tkns.append(Token(aux, "delimitador", i))
        elif aux in operador:
            tkns.append(Token(aux, "operador", i))
        elif aux.isalpha():
            tkns.append(Token(aux, 'identificador', i))
        elif aux:
            tkns.append(Token(aux, 'invalido', i))

        aux = ''
    return tkns


if __name__ == '__main__':
    with open(path, 'r') as inputfile:
        tokens = []
        for i, l in enumerate(inputfile):
            tokens.append(tokenizer(l, i))
        for x in range(len(tokens)):
            print(tokens[x])
        juntalinha = []
        for linha in tokens:
            juntalinha += linha
        Z(juntalinha)
        print(' \n Cadeia aceita')
