# coding: latin-1

################################# Sintaxe abstracta #################################
# Ficheiro que representa os nós da árvore de sintaxe abstracta

class Node(object):

    def __init__(self, t, lineno, *args):
        self.type = t
        self.lineno = lineno
        self.args = args

    def __str__(self):
        ''' String que representa a informação do nó '''
        s = "type: " + str(self.type) + "\n"
        s += "".join(["i: " + str(i) + "\n" for i in self.args])
        return s

    @staticmethod
    def is_node(n):
        ''' Devolve se o parâmetro n é ou não um objecto Node '''
        return type(n) == type(Node("", 0))
