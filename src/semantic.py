# coding: latin-1

from codegen.ast import Node

types = ['int','real','char','string','bool','void']

class Any(object):
    def __eq__(self,o):
        return True
    def __ne__(self,o):
        return False

#-- Tabelas de símbolos -------------------------------------------------------------
# Ambientes que mapeiam identificadores com os seus tipos e localizações
# Atribuição dos valores associados às variáveis é feito no passo seguinte

class Context(object):
    def __init__(self,name=None):
        self.variables = {}
        self.var_count = {}
        self.name = name

    def has_var(self,name):
        return name in self.variables

    def get_var(self,name):
        return self.variables[name]

    def set_var(self,typ,name):
        self.variables[name] = typ
        self.var_count[name] = 0

class ContextStack(object):
    def __init__(self):
        self.contexts = []

    def pop(self):
        count = self.contexts[-1].var_count
        for v in count:
            if count[v] == 0:
                warning("variable %s was declared, but not used." % v)
        self.contexts.pop()

    def push(self, obj):
        self.contexts.append(obj)

    def top(self):
        return self.contexts[-1]

    def __iter__(self):
        return iter(self.contexts[::-1])

context_stack = ContextStack()

#------------------------------------------------------------------------------------

# Funções standard incorporadas na linguagem
functions = {
    'print':('void',[
            ("a",Any())
        ]),
    'println':('void',[
            ("a",Any())
        ])
}

def check_if_function(var):
    if var in functions and not is_function_name(var):
        raise_nolineno("A function called %s already exists" % var)

def is_function_name(var):
    for i in context_stack:
        if i.name == var:
            return True
    return False


def has_var(varn):
    var = varn
    check_if_function(var)
    for c in context_stack:
        if c.has_var(var):
            return True
    return False

def get_var(varn):
    var = varn
    for c in context_stack:
        if c.has_var(var):
            c.var_count[var] += 1
            return c.get_var(var)
    raise_nolineno("Variable %s is referenced before assignment" % var)

def set_var(typ,varn):
    var = varn
    check_if_function(var)
    now = context_stack.top()
    if now.has_var(var):
        raise_nolineno("Variable %s already defined" % var)
    else:
        now.set_var(typ,var)

def get_params(node):
    if node.type == "parameter":
        return [check(node.args[0])]
    else:
        l = []
        for i in node.args:
            l.extend(get_params(i))
        return l

def flatten(n):
    if not Node.is_node(n): return [n]
    if not n.type.endswith("_list"):
        return [n]
    else:
        l = []
        for i in n.args:
            l.extend(flatten(i))
        return l

current_node = None

def check(node):
    if not Node.is_node(node):
        # Se for uma lista de nós (é iterable mas não é string)
        if hasattr(node,"__iter__") and type(node) != type(""):
            for i in node:
                check(i)
        else:
            return node
    else:
        current_node = node

        # PROGRAM
        if node.type in ["program"]:
            context_stack.push(Context())
            check(node.args)
            context_stack.pop()

        # PROC-FUNC-AND-VAR-LIST, STATEMENT-LIST
        elif node.type in ['proc_func_and_var_list','statement_list']:
            return check(node.args)

        # IDENTIFIER
        elif node.type in ['identifier']:
            return node.args[0]

        # VAR, GLOBAL-VAR
        elif node.type in ['global_var', 'var']: # Criação de uma nova variável
            # A regra é: variable_declaration -> type identifier
            # Em vez de existir um elif para type, obtemos logo aqui o seu valor
            # Daí: node.args[0] é type; node.args[0].args[0] é símbolo terminal TYPE
            var_type = node.args[0].args[0]
            var_name = node.args[1].args[0] # O mesmo para o nome da variável
            set_var(var_type, var_name)

        # FUNCTION
        elif node.type in ['function','procedure']:
            # As regras da gramática:
            # function_declaration -> function_heading COLON statement_sequence END
            # function_heading : type identifier
            #                  | type identifier LPAREN parameter_list RPAREN
            #     Com p[0] = Node("function_head",ln(p),p[2],p[4],p[1])
            head = node.args[0]
            name = head.args[0].args[0] # Nome é o primeiro filho
            check_if_function(name)

            if node.type == 'procedure' and len(head.args) == 1: # Apenas o nome
                args = [] # Nos procedimentos sem parâms é só nome que é posto na AST
            elif node.type == 'function' and len(head.args) == 2: # Nome e tipo
                args = [] # Nas funções sem parâmetros, é só nome e tipo de retorno
            else:
                args = flatten(head.args[1])
                args = map(lambda x: (x.args[0].args[0],x.args[1].args[0]), args)

            if node.type == 'procedure':
                rettype = 'void'
            else:
                rettype = head.args[-1].args[0]

            functions[name] = (rettype,args)

            context_stack.push(Context(name))
            for i in args:
                set_var(i[1], i[0])
            set_var(rettype, 'result') # Variável que permite armazenar o retorno
            context_stack.top().var_count['result'] += 1 # Não mostrar warning
            check(node.args[1])
            context_stack.pop()

        # FUNCTION-CALL, FUNCTION-CALL-INLINE
        elif node.type in ["function_call","function_call_inline"]:
            fname = node.args[0].args[0]
            if fname not in functions:
                raise_exception(node, "Function %s is not defined" % fname)
            if len(node.args) > 1:
                args = get_params(node.args[1])
            else:
                args = []
            rettype,vargs = functions[fname]

            if len(args) != len(vargs):
                raise_exception(node, "Function %s is expecting %d parameters and " \
                    "got %d" % (fname, len(vargs), len(args)))
            else:
                for i in range(len(vargs)):
                    if vargs[i][1] != args[i]:
                        raise_exception(node, "Parameter #%d passed to function %s should " \
                            "be of type %s and not %s" % (i+1,fname,vargs[i][1],args[i]))
            return rettype

        # ASSIGN
        elif node.type == "assign": # Atribuição (ex: a = 1; )
            varn = check(node.args[0]) # Nome da variável

            # if is_function_name(varn): # Como no pascal
            #     vartype = functions[varn][0]
            if varn == 'result': # Se a variável corresponde ao valor de retorno
                # func_name = context_stack.top().name # Nome da função em que estamos

                # Isto não é suficiente porque podemos estar dentro de um ciclo FOR
                # por exemplo, e então temos de descer na pilha de contextos
                for c in context_stack:
                    if c.name is not None:
                        func_name = c.name # Nome da função em que estamos
                        break
                if func_name is None:
                    raise_exception(node, "Cannot use result value")
                vartype = functions[func_name][0] # Identificar o tipo de retorno
            else:
                if not has_var(varn):
                    raise_exception(node, "Variable %s not declared" % varn)
                vartype = get_var(varn)
            assgntype = check(node.args[1])

            if vartype != assgntype:
                raise_exception(node, "Variable %s is of type %s and does not " \
                    "support %s" % (varn, vartype, assgntype))

        # VAR-ASSIGN
        elif node.type == "var_assign": # Declaração e atribuição (ex: int a = 1; )
            var_type = node.args[0].args[0]
            var_name = node.args[1].args[0]
            set_var(var_type, var_name)
            assgntype = check(node.args[2])

            if var_type != assgntype:
                raise_exception(node, "Variable %s is of type %s and does not " \
                    "support %s" %(var_name, var_type, assgntype))

        # AND, OR
        elif node.type == 'and_or':
            op = node.args[0].args[0]
            for i in range(1,2):
                a = check(node.args[i])
                if a != "bool":
                    raise_exception(node, "%s requires a boolean. Got %s instead." % (op,a))

        # OP
        elif node.type == "op":
            op = node.args[0].args[0]
            vt1 = check(node.args[1])
            vt2 = check(node.args[2])

            if vt1 != vt2:
                raise_exception(node, "Arguments of operation '%s' must be of the " \
                    "same type. Got %s and %s." % (op,vt1,vt2))

            if op in ['mod', '%']:
                if vt1 != 'int':
                    raise_exception(node, "Operation %s requires integers." % op)

            if op == '/':
                if vt1 != 'real' and vt1 != 'int':
                    raise_exception(node, "Operation %s requires numbers." % op)

            if op in ['==','<=','>=','>','<','<>']:
                return 'bool'
            else:
                return vt1

        # IF, WHILE, DO, UNLESS
        elif node.type in ['if','while','do','unless']:
            # Análise da condição lógica
            if node.type in ['do','unless']: # Nos 'do' e 'unless' aparece no final
                t = check(node.args[1])
            else:
                t = check(node.args[0])
            # Se o resultado da análise da expressão não é booleano
            if t != 'bool':
                raise_exception(node, "%s condition requires a boolean. " \
                    "Got %s instead." % (node.type,t))
            # Análise do corpo
            if node.type in ['do','unless']:
                check(node.args[0])
            else:
                check(node.args[1])
            # Se tem mais que dois argumentos, terceiro é um else (ou else-if)
            if len(node.args) > 2:
                check(node.args[2])

        # FOR
        elif node.type == 'for':
            context_stack.push(Context())
            v = node.args[0].args[0].args[0] # Variável contador
            st = node.args[0].args[1].args[0].type # Atribuição inicial ao contador
            fv = node.args[2].args[0].type # Valor final para o contador

            if st != 'int':
                raise_exception(node, 'For requires an integer as a starting value')
            elif fv not in ['int', 'identifier']: # Valor final para o contador
                raise_exception(node, 'For requires an integer as a final value')
            elif fv == 'identifier' and check(node.args[2]) != 'int':
                # Valor final para o contador é uma variável inteira
                raise_exception(node, 'For requires an integer as a final value')
            else: # Cria a variável contador neste contexto
                set_var('int', v)
                context_stack.top().var_count[v] += 1 # Evitar warning de var não usada

            if len(node.args) == 5: # Existe uma variável de incremento
                iv = node.args[4].args[0].type
                if iv != 'int':
                    raise_exception(node, 'For requires an integer as an incremental value')

            check(node.args[3]) # Analisar o conteúdo do ciclo for
            context_stack.pop()

        # NOT
        elif node.type == 'not': # Negação de um 'element'. Ao nível da semântica
            # basta que verifiquemos se está tudo correcto com o 'element'. A negação
            # é feita no builder.py
            return check(node.args[0])

        # ELEMENT
        elif node.type == "element":
            if node.args[0].type == 'identifier':
                return get_var(node.args[0].args[0])
            elif node.args[0].type == 'function_call_inline':
                return check(node.args[0])
            else:
                if node.args[0].type in types: # Se é um tipo de dados
                    return node.args[0].type
                else:
                    return check(node.args[0])

        else: # Se for encontrado um outro tipo de nó inesperado (só acontece se o
            # rules.py foi modificado)
            print "semantic missing:", node.type

#- Standard Error -------------------------------------------------------------------

def raise_exception(node, message):
    raise Exception, "Semantic error [line %d]: %s" %(node.lineno, message)

def raise_nolineno(message):
    raise Exception, "Semantic error: %s" % message

def warning(message):
    print "Warning:", message
