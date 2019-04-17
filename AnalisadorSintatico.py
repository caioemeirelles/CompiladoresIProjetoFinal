from TabelaSintatica import *
import nltk

#
# Universidade Federal de Mato Grosso
# Instituto de Computação
# Compiladores I
# Aluno: Caio Meirelles
# RGA: 201611310015
#


# aqui a gente pega qual arquivo o ser humano quer testar
path = input("Digite o nome do arquivo a ser verificado:\n")
print("\n")


# palavras reservadas, delimitadores, operadores e terminais
reservadas = ('var', 'integer', 'real', 'if', 'then')
terminais = (' ', '\t', '\n', ',', ':', ':=', '+', ',', ';', '=')
delimitador = (',', ':', ';')
operador = ('+', '-', ':=', '=')


class Token:
    def __init__(self, _value, _type, _index):
        self.type = _type
        self.value = _value
        self.index = _index

    def __str__(self):
        return "'{}' {} linha {}".format(self.value, self.type, self.index)

    __repr__ = __str__


def tokenizer(l, i):
    aux = ''
    tokens = []
    for a in l:
        if a in terminais:
            if aux:
                if aux == ':=':
                    tokens.append(Token(aux, "operador", i))
                    aux = ''
                    continue
                if aux in reservadas:
                   tokens.append(Token(aux, "reservada", i))
                elif aux in delimitador:
                    tokens.append(Token(aux, "delimitador", i))
                elif aux in operador:
                    tokens.append(Token(aux, "operador", i))
                elif aux.isalpha():
                    tokens.append(Token(aux, 'identificador', i))
                else:
                    tokens.append(Token(aux, 'invalido', i))

                aux = ''
            if a == ':' and l[l.index(a)+1] == '=':
                aux = ':='
            elif a in delimitador:
                tokens.append(Token(a, 'delimitador', i))
            elif a in operador:
                tokens.append(Token(a, 'operador', i))
        else:
            aux+= a
    else:
        if aux in reservadas:
            tokens.append(Token(aux, "reservada", i))
        elif aux in delimitador:
            tokens.append(Token(aux, "delimitador", i))
        elif aux in operador:
            tokens.append(Token(aux, "operador", i))
        elif aux.isalpha():
            tokens.append(Token(aux, 'identificador', i))
        elif aux:
            tokens.append(Token(aux, 'invalido', i))

        aux = ''
    return tokens


if __name__ == '__main__':
    with open(path, 'r') as arq:
        tokens = []
        for i, l in enumerate(arq):
            tokens.append(tokenizer(l, i))
        for x in range(len(tokens)):
            print (tokens[x])
        aux = []
        for linha in tokens:
            aux += linha
        Z(aux)
        print('\nCadeia aceita')
