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
delimitador = (',', ':', ';')
operador = ('+', '-', ':=', '=')
terminais = (' ', '\t', '\n', ',', ':', ':=', '+', ',', ';', '=')


# classe pra ajudar a formatar os tokens e imprimir bonitinho
class Token:
    def __init__(self, _valor, _tipo, _index):
        self.tipo = _tipo
        self.valor = _valor
        self.index = _index

    def __str__(self):
        return "'{}' {} linha {}".format(self.valor, self.tipo, self.index)

    __repr__ = __str__


# metodo de erro pro caso de achar um caractere invalido
def caractere_invalido(aux):
    print("Caractere invalido: '" + aux + "'")
    exit(66)  # execute order 66


# a execucao actually comeca aqui
if __name__ == '__main__':
    with open(path, 'r') as input_file:
        tokens = []
        for i, l in enumerate(input_file):
            tokenizador = nltk.WordPunctTokenizer()
            lista_de_termos = tokenizador.tokenize(l)
            for j in lista_de_termos:
                if j in reservadas:
                    tokens.append(Token(j, "reservada", i))
                elif j in delimitador:
                    tokens.append(Token(j, "delimitador", i))
                elif j in operador:
                    tokens.append(Token(j, "operador", i))
                elif j.isalpha():
                    tokens.append(Token(j, "identificador", i))
                elif j:
                    caractere_invalido(j)
        for i in tokens:
            print('[', i, ']')
