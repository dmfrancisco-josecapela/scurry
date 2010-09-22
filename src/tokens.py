# coding: latin-1

################################## Análise lexical ##################################

from lib.ply import lex
from lib.ply.lex import TOKEN
import sys

#//////////////////////////////////// DEFINIÇÕES ////////////////////////////////////

# Lista de palavras reservadas
reserved = {
    'main':   'MAIN',
    'end':    'END',

  # Controlo de fluxo de execução
    'if':     'IF',
    'else':   'ELSE',
    'unless': 'UNLESS',
    'for':    'FOR',
    'while':  'WHILE',
    'do':     'DO',
    'to':     'TO',
    'downto': 'DOWNTO',
    'until':  'UNTIL',

  # Expressões lógicas
    'and':   'AND',
    'or':    'OR',
    'true':  'TRUE',
    'false': 'FALSE',

    'global': 'GLOBAL',

  # Funções
    'void': 'VOID',

  # Nomes dos tipos de dados
    'real':   'TREAL',
    'int':    'TINT',
    'string': 'TSTRING',
    'char':   'TCHAR',
    'bool':   'TBOOL'
}
dup_reserved = { # Palavras que são ao mesmo tempo reservadas e tokens
    'not': 'NOT', # Existe também a token ! que faz o mesmo que tem o mesmo nome
    'mod': 'MOD', # Existe também a token %
}

# Lista de tokens
tokens = [
  # Declarações
    'IDENTIFIER',
    'ASSIGNMENT',
    'SEMICOLON',
    'COLON',
    'COMMA',
    'QMARK',
  # Operadores matemáticos
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVISION',
    'MOD',
    'POW',
  # Comparadores lógicos
    'EQ',
    'NEQ',
    'LT',
    'GT',
    'LTE',
    'GTE',
    'NOT',
  # Funções e operações matemáticas
    'LPAREN',
    'RPAREN',
  # Tipos de dados
    'REAL',
    'INT',
    'STRING',
    'CHAR'
] + list(reserved.values())


# //////////////////////////////////// REGRAS ///////////////////////////////////////
# Descrição dos padrões e acções associadas a cada padrão

t_ASSIGNMENT = r"="
t_SEMICOLON  = r";"
t_COLON      = r":"
t_COMMA      = r","
t_QMARK      = r'\?'

t_PLUS       = r"\+"
t_MINUS      = r"\-"
t_TIMES      = r"\*"
t_DIVISION   = r"/"
t_MOD        = r"\%"
t_POW        = r"\*\*"

t_EQ         = r"\=\="
t_NEQ        = r"\<\>"
t_LT         = r"\<"
t_GT         = r"\>"
t_LTE        = r"\<\="
t_GTE        = r"\>\="
t_NOT        = r"\!"

t_LPAREN     = r"\("
t_RPAREN     = r"\)"

t_REAL       = r"[0-9]+\.[0-9]+"
t_INT        = r"[0-9]+"

# Uma variável é um conjunto de caracteres diferente de qualquer palavra reservada
def t_IDENTIFIER(t):
    r'[A-z][A-z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in dup_reserved:
        t.type = dup_reserved[t.value]
    return t

def t_CHAR(t):
    r"(\'([^\\\'])\')|(\"([^\\\"])\")"
    return t

def t_STRING(t):
    r"(\"([^\\\"]|(\\.))*\")|(\'([^\\\']|(\\.))*\')"
    escaped = 0
    str = t.value[1:-1]
    new_str = ""
    for i in range(0, len(str)):
        c = str[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = 0
        else:
            if c == "\\":
                escaped = 1
            else:
                new_str += c
    t.value = new_str
    return t

# Nontoken - Ignorar o conteúdo dos comentários
def t_COMMENT(t):
    r"[ ]*\043[^\n]*"  # \043 is '#'
    pass

# Nontoken - Regra para guardar o número da linha em que nos encontramos
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global lexpos
    lexpos = t.lexpos # Armazenar número de caracteres consumidos até ao momento

t_ignore = ' \t' # Nontokens - Caracteres a ignorar (espaços e tabs)


# /////////////////////////////////// SUBROTINAS ////////////////////////////////////

def t_error(t):
    ''' Regra para tratamento de erros '''
    print "Error [line %d column %d]: Illegal character '%s'" %(t.lineno,\
        find_column(t), t.value[0])
    t.lexer.skip(1)

lexpos = 0 # Para armazenar número de caracteres consumidos até ao momento

def find_column(t):
    ''' Identificar a coluna em que ocorreu o erro '''
    # token.lexpos devolve o número de caracteres desde o inicio
    # Nós queremos o número de caracteres desde o princípio desta linha
    return t.lexpos-lexpos


if __name__ == '__main__':
    # Build the lexer
    from ply import lex
    import sys

    lex.lex()

    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
    else:
        data = ""
        while 1:
            try:
                data += raw_input() + "\n"
            except:
                break

    lex.input(data)

    # Tokenize
    while 1:
        tok = lex.token()
        if not tok: break # No more input
        print tok
