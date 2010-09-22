# coding: latin-1

import sys

from llvm import *
from llvm.core import *

import ptypes as types
from helpers import *
from ast import Node

#------------------------------------------------------------------------------------

class Context(object):
    def __init__(self,current,builder = False):
        self.current = current
        if not builder:
            self.builder = Builder.new(self.current)
        else:
            self.builder = builder

        self.vars = {}
        self.params = {}

    def has_var(self,name):
        return name in self.vars or name in self.params

    def set_var(self,name,value):
        self.vars[name] = value

    def set_param(self,name,value):
        self.params[name] = value

    def get_var(self,name):
        if name in self.params:
            return self.params[name]
        if name in self.vars:
            return self.vars[name]
        raise_exception("Variable %s doesn't exist" % name)

    def get_builder(self):
        return self.builder

class ContextStack(object):
    def __init__(self):
        self.contexts = []

    def pop(self):
        self.contexts.pop()

    def push(self, obj):
        self.contexts.append(obj)

    def top(self):
        return self.contexts[-1]

    def __iter__(self):
        return iter(self.contexts[::-1])

#------------------------------------------------------------------------------------

class Writer(object):

    def __init__(self):
        self.functions={}
        self.context_stack = ContextStack()
        self.counter = 0

    def get_var(self,name):
        # Obter variável local (se existir)
        for c in self.context_stack:
            if c.has_var(name):
                return (c.get_var(name), False)
        try: # Obter variável global
            return (self.module.get_global_variable_named(name), True)
        except: # A variável não existe
            raise_exception("Variable %s doesn't exist" % name)

    def set_var(self,name,value):
        self.context_stack.top().set_var(name,value)

    def set_param(self,name,value):
        self.context_stack.top().set_param(name,value)

    def get_builder(self):
        return self.context_stack.top().get_builder()

    def get_current(self):
        return self.context_stack.top().current

    def get_function(self):
        for c in self.context_stack:
            if c.current.__class__ == Function:
                return c.current

    def descend(self,node):
        return self(node)

    def __call__(self, ast):
        if ast.__class__ != Node:
           return ast

        # PROGRAM
        if ast.type == "program": # Ínicio do programa
            self.module = Module.new("scurry") # Criar o módulo (string é um ID)
            # Os módulos LLVM são contentores. É preciso criá-lo antes de se poderem
            # adicionar variáveis globais, funções, etc.
            # Ver: http://mdevan.nfshost.com/llvm-py/userguide.html

            stdio = add_stdio(self.module)
            for f in stdio:
                self.functions[f] = stdio[f]

            main = create_main(self.module)

            block = Builder.new(main.append_basic_block("entry"))

            self.context_stack.push(Context(main,block))
            self.descend(ast.args[0]) # Variáveis globais, funções e procedimentos
            self.descend(ast.args[1]) # Main

            self.get_builder().ret(c_int(0))
            return self.module

        # PROC-FUNC-AND-VAR-LIST, STATEMENT-LIST
        elif ast.type in ["proc_func_and_var_list","statement_list"]:
            for son in ast.args:
                self.descend(son)

        # VAR
        elif ast.type == "var": # Declaração de variáveis
            var_type_name = self.descend(ast.args[0])
            var_name = self.descend(ast.args[1])
            builder = self.get_builder()
            v = var_init(self.module, builder, var_name, var_type_name)
            self.set_var(var_name,v)

        # GLOBAL-VAR
        elif ast.type == "global_var": # Declaração de variáveis globais
            var_type_name = self.descend(ast.args[0])
            var_name = self.descend(ast.args[1])
            builder = self.get_builder()
            v = global_var_init(self.module, var_type_name, var_name)

        # TYPE
        elif ast.type == "type":
            return str(ast.args[0])

        # IDENTIFIER
        elif ast.type == "identifier":
            return str(ast.args[0])

        # FUNCTION-CALL, FUNCTION-CALL-INLINE
        elif ast.type in ["function_call","function_call_inline"]:
            builder = self.get_builder()
            function_name = self.descend(ast.args[0])

            arguments = []
            if len(ast.args) > 1:
                if ast.args[1]:
                    arguments = self.descend(ast.args[1])

            if function_name in ['print','println']:
                if str(arguments[0].type) == 'double':
                    function_name += "real"
                elif str(arguments[0].type) == 'i32':
                    function_name += "int"
                elif str(arguments[0].type) == 'i8':
                    function_name += "char"
                elif str(arguments[0].type) == 'i1':
                    function_name += "bool"

            function = self.module.get_function_named(function_name)
            return builder.call(function,arguments)

        # PARAMETER-LIST
        elif ast.type == "parameter_list":
            l = []
            l.extend(self.descend(ast.args[0]))
            l.extend(self.descend(ast.args[1]))
            return l

        # PARAMETER
        elif ast.type == "parameter":
            c = ast.args[0]
            if c.type == "identifier":
                label = self.descend(ast.args[0])
                c = self.get_var(label)
            else:
                c = self.descend(ast.args[0])
            return [c]

        # ASSIGN
        elif ast.type == "assign":
            builder = self.get_builder()
            varName = self.descend(ast.args[0])
            value = self.descend(ast.args[1])

            (ref, isGlobal) = self.get_var(varName)
            if not isGlobal: # Variáveis locais
                # self.set_var(value, ref)
                builder.store(value, ref)
            else: # Variáveis globais
                ref.initializer = value
            return varName

        # VAR-ASSIGN
        elif ast.type == "var_assign":
            var_type_name = self.descend(ast.args[0])
            var_name = self.descend(ast.args[1])
            value = self.descend(ast.args[2])

            builder = self.get_builder()
            v = var_init(self.module, builder, var_name, var_type_name)
            self.set_var(var_name,v)
            if var_type_name != 'string':
                builder.store(value, v)

        # PROCEDURE, FUNCTION
        elif ast.type in ['procedure','function']:

            def get_params(node):
                """ Return a list of tuples of params """
                if node.type == 'parameter':
                    return [(self.descend(node.args[0]), types.translation[self.descend(node.args[1])])]
                else:
                    l = []
                    for p in node.args:
                        l.extend(get_params(p))
                    return l

            head = ast.args[0]
            if head.type == 'procedure_head':
                return_type = types.void
            else:
                return_type = types.translation[self.descend(head.args[-1])]

            name = self.descend(head.args[0])

            if ast.type == 'procedure' and len(head.args) == 1: # Apenas o nome
                params = [] # Nos procedimentos sem parâms é só nome que é posto na AST
            elif ast.type == 'function' and len(head.args) == 2: # Nome e tipo
                params = [] # Nas funções sem parâmetros, é só nome e tipo de retorno
            else:
                params = get_params(head.args[1])
            code = ast.args[1]

            ftype = types.function(return_type, [ i[1] for i in params ])
            f = Function.new(self.module, ftype, name)
            fb = Builder.new(f.append_basic_block("entry"))

            self.context_stack.push(Context(f, fb))
            b = self.get_builder()
            for i,p in enumerate(params):
                x = f.args[i]; x.name = p[0]
                type_name = types.reverse_translation[x.type]
                v = var_init(self.module, b, x.name, type_name)
                self.set_param(p[0],v)
                b.store(x, v)

            if ast.type == 'function': # Criar uma variável para guardar o retorno
                type_name = types.reverse_translation[return_type]
                v = var_init(self.module, b, 'result', type_name)
                self.set_var('result',v)
            self.descend(code)
            b = self.get_builder()
            if ast.type == 'procedure':
                b.ret_void()
            else:
                (ref, isGlobal) = self.get_var('result')
                b.ret(b.load(ref))
            self.context_stack.pop()

        # WHILE
        elif ast.type == "while":
            self.counter += 1
            now = self.get_function()
            builder = self.get_builder()

            loop = now.append_basic_block("loop_%d" % self.counter)
            body = now.append_basic_block("body_%d" % self.counter)
            tail = now.append_basic_block("tail_%d" % self.counter)

            # do while code
            self.context_stack.push(Context(loop))
            b = self.get_builder()
            cond = self.descend(ast.args[0])
            b.cbranch(cond,body,tail)
            self.context_stack.pop()

            self.context_stack.push(Context(body))
            b = self.get_builder()
            self.descend(ast.args[1])
            # repeat
            b.branch(loop)
            self.context_stack.pop()

            # start loop
            builder.branch(loop)
            self.context_stack.top().builder = Builder.new(tail)

        # DO
        elif ast.type == "do":
            cond = Node('not',ast.lineno,ast.args[1])
            body = ast.args[0]

            while_b = Node('while',ast.lineno,cond,body)
            final = Node('statement_list',ast.lineno,body,while_b)
            return self.descend(final)

        # FOR
        elif ast.type == "for":
            direction = self.descend(ast.args[1]) # Se é TO ou DOWNTO
            limit = ast.args[2] # O extremo direito a atingir

            if len(ast.args) == 5: # Se consiste em for com incremento diferente de 1
                inc = int(ast.args[4].args[0].args[0]) # Valor de incremento
            else: inc = 1

            builder = self.get_builder()

            # Declaração da variável contador
            varname = self.descend(ast.args[0].args[0])
            vartype = "int"
            v = var_init(self.module, builder, varname, vartype)
            self.set_var(varname,v)

            # var init
            variable = self.descend(ast.args[0])

            # cond
            var1 = Node('element',ast.lineno,Node('identifier',ast.lineno,varname))
            var1_name = Node('identifier',ast.lineno,varname)

            # body
            if (direction == "to" and inc > 0) or (direction == "downto" and inc < 0):
                sign_term = '<='
                op_term   = '+'
            elif (direction == "to" and inc < 0) or (direction == "downto" and inc > 0):
                sign_term = '>='
                op_term   = '-'
            else: raise_exception("Invalid increment value on 'for' statement")

            sign = Node('sign',ast.lineno,sign_term)
            op = Node('sign',ast.lineno,op_term)
            comp = Node('op',ast.lineno,sign,var1,limit)

            varvalue = Node('op',ast.lineno,op,var1,Node('element',ast.lineno,Node('int',ast.lineno,abs(inc))))
            increment = Node('assign',ast.lineno,var1_name,varvalue)
            body = Node('statement_list',ast.lineno,ast.args[3],increment)

            # do while
            while_block = Node('while',ast.lineno,comp,body)

            self.descend(while_block)

        # IF
        elif ast.type == "if":
            now = self.get_function()
            builder = self.get_builder()

            #if
            cond = self.descend(ast.args[0])

            # the rest
            self.counter += 1
            tail = now.append_basic_block("tail_%d" % self.counter)

            # then
            then_block = now.append_basic_block("if_%d" % self.counter)
            self.context_stack.push( Context(then_block)  )
            self.descend(ast.args[1])
            b = self.get_builder()
            b.branch(tail)
            b.position_at_end(tail)
            self.context_stack.pop()

            # else
            else_block = now.append_basic_block("else_%d" % self.counter)
            self.context_stack.push( Context(else_block)  )
            if len(ast.args) > 2:
                self.descend(ast.args[2])
            b = self.get_builder()
            b.branch(tail)
            b.position_at_end(tail)
            self.context_stack.pop()

            builder.cbranch(cond,then_block,else_block)
            self.context_stack.top().builder = Builder.new(tail)

        # UNLESS
        elif ast.type == "unless":
            # Transformar a condição 'unless' num 'if'
            cond = self.descend(ast.args[1])
            neg_cond = Node('not',ast.lineno,cond)
            node = Node('if',ast.lineno,neg_cond,ast.args[0])
            self.descend(node)

        # SIGN, AND-OR
        elif ast.type in ["sign","and_or"]:
            return ast.args[0]

        # OP
        elif ast.type == "op":
            sign = self.descend(ast.args[0])
            v1 = self.descend(ast.args[1])
            v2 = self.descend(ast.args[2])

            builder = self.get_builder()

            if sign == "+":
                return builder.add(v1, v2)
            elif sign == "-":
                return builder.sub(v1, v2)
            elif sign == "*":
                return builder.mul(v1, v2)
            # elif sign == "**":
            #     print "v1", v1
            #     print "v2", v2
            #     base = ast.args[1].args[0].args[0] # Base
            #     exp  = ast.args[2].args[0].args[0] # Expoente
            #     print "base", base
            #     print "exp", exp
            #     if ast.args[1].args[0].type == 'int':
            #         return c_int(int(base) ** int(exp))
            #     else: # Ambos base e expoente são float
            #         return c_real(float(base) ** float(exp))
            elif sign == "/" and str(v1.type) == 'i32' and str(v2.type) == 'i32':
                return builder.sdiv(v1, v2) # Divisão de inteiros
            elif sign == "/": # Divisão de floats
                return builder.fdiv(v1, v2)
            elif sign in ["mod", "%"]:
                return builder.urem(v1, v2)
            elif sign in [">",">=","==","<=","<","<>"]:
                return compare(sign,v1,v2,builder)
            elif sign == "and":
                return builder.and_(v1,v2)
            elif sign == "or":
                return builder.or_(v1,v2)
            else:
                raise_exception("undefined operator %s" % sign)

        # ELEMENT
        elif ast.type == "element":
            builder = self.get_builder()

            e = ast.args[0]
            if e.type == "identifier":
                var_name = ast.args[0].args[0] # Nome da variável
                (ref, isGlobal) = self.get_var(self.descend(e))
                if isGlobal:
                    return ref.initializer
                elif ref.__class__ == Argument:
                    return ref
                return builder.load(ref)
            else:
                return self.descend(ast.args[0])

        # NOT
        elif ast.type == 'not':
            # O nó é do tipo Node('not',ln(p),p[2]) logo p[2] == ast.args[0]
            v = self.descend(ast.args[0]) # A expressão a ser negada
            return self.get_builder().not_(v) # Negação da expressão v

        # STRING
        elif ast.type == "string":
            b = self.get_builder()
            s = c_string(self.module, ast.args[0])
            return pointer(b,s)

        # INT
        elif ast.type == "int":
            return c_int(int(ast.args[0]))

        # REAL
        elif ast.type == "real":
            return c_real(float(ast.args[0]))

        # CHAR
        elif ast.type == "char":
            char = ast.args[0][1] # Preciso [1] prq vem 'a' e queremos a (sem plicas)
            return c_char(char)

        # BOOL
        elif ast.type == "bool":
            if ast.args[0] == "false":
                return c_bool(False)
            else:
                return c_bool(True)

        else: # Se for encontrado um outro tipo de nó inesperado (só acontece se o
            # rules.py foi modificado)
            raise_exception("unknown: %s" % ast.type)

#- Standard Error -------------------------------------------------------------------

def raise_exception(message):
    raise Exception, "Code generation error: %s " % message
