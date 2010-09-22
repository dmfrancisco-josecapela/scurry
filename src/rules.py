# coding: latin-1

################################# Análise sintática #################################

from codegen.ast import Node
from lib.ply import yacc
import sys

#//////////////////////////////////// DEFINIÇÕES ////////////////////////////////////

# Estabelecimento de precedências - associatividade preferencial à esquerda
precedence = (
    # Prioridades ao ní­vel das operações matemáticas
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVISION', 'MOD'),
    # Operações lógicas
    ('left', 'EQ', 'NEQ', 'LTE','LT','GT','GTE'),
    ('left', 'OR', 'AND'),
)

# //////////////////////////////////// REGRAS ///////////////////////////////////////
# Permite descrever os padrões, bem como definir acções associadas a cada padrão

# A regra de início da gramática é a primeira regra especificada. Para alterar:
# start = 'nome_da_regra'

def p_program(p):
    'program : proc_func_and_var MAIN COLON statement_sequence END'
    p[0] = Node('program',ln(p),p[1],p[4])


#-- Declaração e atribuição de variáveis globais ------------------------------------

def p_proc_func_and_var(p):
    """ proc_func_and_var : globalvar_declaration proc_func_and_var
                          | procedure_declaration proc_func_and_var
                          | function_declaration  proc_func_and_var
                          |
    """
    if len(p) > 1:
        p[0] = Node('proc_func_and_var_list',ln(p),p[1],p[2])

def p_globalvar_declaration(p):
    """ globalvar_declaration : GLOBAL type identifier SEMICOLON """
    p[0] = Node('global_var',ln(p),p[2],p[3])

#-- Declaração e atribuição de variáveis --------------------------------------------

def p_variable_declaration(p):
    """ variable_declaration : type identifier """
    p[0] = Node('var',ln(p),p[1],p[2])

def p_assignment_statement(p):
    """ assignment_statement : identifier ASSIGNMENT expression """
    p[0] = Node('assign',ln(p),p[1],p[3])

def p_declaration_and_assignment(p):
    ''' declaration_and_assignment : type identifier ASSIGNMENT expression '''
    p[0] = Node('var_assign',ln(p),p[1],p[2],p[4])


#-- Nomes de variáveis e tipos ------------------------------------------------------

def p_identifier(p):
    """ identifier : IDENTIFIER """
    p[0] = Node('identifier',ln(p),str(p[1]))

def p_type(p):
    """ type : TREAL
             | TINT
             | TCHAR
             | TBOOL
             | TSTRING
    """
    p[0] = Node('type',ln(p),p[1])

def p_real(p):
    """ real : REAL
             | MINUS REAL
    """
    if len(p) == 2:
        p[0] = Node('real',ln(p),p[1])
    else:
        p[2] = str(0-float(p[2])) # Valor negativo
        p[0] = Node('real',ln(p),p[2])

def p_int(p):
    """ int : INT
            | MINUS INT
    """
    if len(p) == 2:
        p[0] = Node('int',ln(p),p[1])
    else:
        p[2] = str(0-int(p[2])) # Valor negativo
        p[0] = Node('int',ln(p),p[2])

def p_string(p):
    """ string : STRING """
    p[0] = Node('string',ln(p),p[1])

def p_char(p):
    """ char : CHAR """
    p[0] = Node('char',ln(p),p[1])

def p_bool(p):
    """ bool : TRUE
             | FALSE
    """
    p[0] = Node('bool',ln(p),p[1])


#-- Funções com e sem valor de retorno ----------------------------------------------

def p_procedure_declaration(p):
    """ procedure_declaration : procedure_heading COLON statement_sequence END """
    p[0] = Node("procedure",ln(p),p[1],p[3])

def p_procedure_heading(p):
    """ procedure_heading : VOID identifier
                          | VOID identifier LPAREN parameter_list RPAREN
    """
    if len(p) == 3:
        p[0] = Node("procedure_head",ln(p),p[2])
    else:
        p[0] = Node("procedure_head",ln(p),p[2],p[4])

def p_function_declaration(p):
    """ function_declaration : function_heading COLON statement_sequence END """
    p[0] = Node('function',ln(p),p[1],p[3])

def p_function_heading(p):
    """ function_heading : type identifier
                         | type identifier LPAREN parameter_list RPAREN
    """
    if len(p) == 3: # O primeiro parâmetro é o nome da função
        p[0] = Node("function_head",ln(p),p[2],p[1])
    else:
        p[0] = Node("function_head",ln(p),p[2],p[4],p[1])


#-- Listas de parâmetros ------------------------------------------------------------

def p_parameter_list(p):
    """ parameter_list : parameter COMMA parameter_list
                       | parameter
    """
    if len(p) == 4:
        p[0] = Node("parameter_list", ln(p), p[1], p[3])
    else:
        p[0] = p[1]

def p_parameter(p):
    """ parameter : type identifier """
    p[0] = Node("parameter", ln(p), p[2], p[1])


#-- Chamada de funções e passagem de parâmetros -------------------------------------

def p_procedure_or_function_call(p):
    """ procedure_or_function_call : identifier LPAREN param_list RPAREN
                                   | identifier
    """
    if len(p) == 2:
        p[0] = Node("function_call",ln(p),p[1])
    else:
        p[0] = Node("function_call",ln(p),p[1],p[3])

def p_function_call_inline(p):
    """ function_call_inline : identifier LPAREN param_list RPAREN """
    p[0] = Node('function_call_inline',ln(p),p[1],p[3])

def p_param_list(p):
    """ param_list : param_list COMMA param
                   | param
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node("parameter_list",ln(p),p[1],p[3])

def p_param(p):
    """ param : expression """
    p[0] = Node("parameter",ln(p),p[1])


#-- Sequências e instruções de repetição --------------------------------------------

def p_statement_sequence(p):
    """ statement_sequence : statement statement_sequence
                           |
    """
    if len(p) > 1:
        p[0] = Node('statement_list',ln(p),p[1],p[2])

def p_statement(p):
    """ statement : assignment_statement SEMICOLON
                  | if_statement
                  | conditional_expression SEMICOLON
                  | do_statement SEMICOLON
                  | while_statement
                  | for_statement
                  | procedure_or_function_call SEMICOLON
                  | variable_declaration SEMICOLON
                  | declaration_and_assignment SEMICOLON
                  | unless_statement SEMICOLON
    """
    p[0] = p[1]

def p_if_statement(p):
    """if_statement : IF expression COLON statement_sequence ELSE COLON statement_sequence END
                    | IF expression COLON statement_sequence END
                    | IF expression COLON statement_sequence ELSE if_statement
    """
    if len(p) == 9:
        p[0] = Node('if',ln(p),p[2],p[4],p[7])
    elif len(p) == 6:
        p[0] = Node('if',ln(p),p[2],p[4])
    else:
        p[0] = Node('if',ln(p),p[2],p[4],p[6])

def p_conditional_expression(p):
    """ conditional_expression : expression QMARK statement_no_semicolon
                               | expression QMARK statement_no_semicolon COLON statement_no_semicolon
    """
    if len(p) == 4:
        p[0] = Node('if',ln(p),p[1],p[3])
    else:
        p[0] = Node('if',ln(p),p[1],p[3],p[5])

def p_unless_statement(p):
    """ unless_statement : statement_no_semicolon UNLESS expression
                         | DO COLON statement_sequence UNLESS expression """
    if len(p) == 4:
        p[0] = Node('unless',ln(p),p[1],p[3])
    else:
        p[0] = Node('unless',ln(p),p[3],p[5])

def p_statement_no_semicolon(p):
    """ statement_no_semicolon : assignment_statement
                               | procedure_or_function_call
                               | variable_declaration
                               | declaration_and_assignment
    """
    p[0] = p[1]

def p_while_statement(p):
    """ while_statement : WHILE expression COLON statement_sequence END """
    p[0] = Node('while',ln(p),p[2],p[4])

def p_do_statement(p):
    """ do_statement : DO COLON statement_sequence UNTIL expression """
    p[0] = Node('do',ln(p),p[3],p[5])

def p_for_statement(p):
    """for_statement : FOR assignment_statement TO expression COLON statement_sequence END
                     | FOR assignment_statement TO expression COMMA expression COLON statement_sequence END
                     | FOR assignment_statement DOWNTO expression COLON statement_sequence END
                     | FOR assignment_statement DOWNTO expression COMMA expression COLON statement_sequence END
    """
    if len(p) == 10:
        p[0] = Node('for',ln(p),p[2],p[3],p[4],p[8],p[6])
    else:
        p[0] = Node('for',ln(p),p[2],p[3],p[4],p[6])


def p_expression(p):
    """ expression : expression and_or expression_m
                   | expression_m
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('op',ln(p),p[2],p[1],p[3])

def p_expression_m(p):
    """ expression_m : element
                     | element sign expression_m
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('op',ln(p),p[2],p[1],p[3])

def p_and_or(p):
    """ and_or : AND
               | OR
    """
    p[0] = Node('and_or',ln(p),p[1])

def p_sign(p):
    """ sign : PLUS
             | MINUS
             | DIVISION
             | TIMES
             | MOD
             | POW
             | EQ
             | NEQ
             | LT
             | LTE
             | GT
             | GTE
    """
    p[0] = Node('sign',ln(p),p[1])

def p_element(p):
    """element : identifier
               | real
               | int
               | string
               | char
               | bool
               | LPAREN expression RPAREN
               | NOT element
               | function_call_inline
    """
    if len(p) == 2:
        p[0] = Node("element",ln(p),p[1])
    elif len(p) == 3: # not e
        p[0] = Node('not',ln(p),p[2])
    else: # ( e )
        p[0] = Node('element',ln(p),p[2])


# /////////////////////////////////// SUBROTINAS ////////////////////////////////////

last_error_msg = None
default_msg = "Syntax error: Erroneous input" # Caso não se consiga apurar a linha

def p_error(p):
    ''' Regra para erros de sintaxe '''
    global last_error_msg

    try: error_msg = "Syntax error [line %d]: Input error at '%s'" %(p.lineno, p.value)
    except: error_msg = default_msg

    if error_msg == last_error_msg or (last_error_msg and error_msg == default_msg):
        sys.exit()
    print error_msg
    last_error_msg = error_msg # Guardar a última mensagem de erro. Isto é feito uma
    # vez que o comportamento de yacc.errok() nem sempre é o esperado, e pode entrar
    # em ciclo ilustrando sempre a mesma mensagem de erro

    # Dos slides:
    # É conveniente que o parser não interrompa a acção quando encontra um erro
    # Ele deve levar a análise até ao fim e reportar todos os erros encontrados

    yacc.errok() # Tenta continuar apesar do erro que ocorreu
    return yacc.token() # Devolve o próximo token da stream

def ln(p):
    ''' Devolve a linha em que se encontra '''
    return p.lineno(0) # Útil para termos esta informação na árvore de sintaxe
    # abstracta para as mensagens de erro da análise semântica e de geração de código


if __name__ == '__main__':
    # Build the parser
    parser = yacc.yacc()

    f = open(r'input')
    try:
       for line in f:
           result = parser.parse(line.strip())
    finally:
        f.close()
