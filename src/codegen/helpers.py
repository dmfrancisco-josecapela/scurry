# coding: latin-1

from llvm.core import *
import ptypes as types


def compare(sign,v1,v2,builder):
    """ [">",">=","==","<=","<","<>"] """

    if sign == ">":
        i_cod = IPRED_UGT
        f_cod = RPRED_OGT
    elif sign == ">=":
        i_cod = IPRED_UGE
        f_cod = RPRED_OGE
    elif sign == "==":
        i_cod = IPRED_EQ
        f_cod = RPRED_OEQ
    elif sign == "<=":
        i_cod = IPRED_ULE
        f_cod = RPRED_OLE
    elif sign == "<":
        i_cod = IPRED_ULT
        f_cod = RPRED_OLT
    elif sign == "<>":
        i_cod = IPRED_NE
        f_cod = RPRED_ONE
    else:
        return c_bool(False)

    if v1.type == types.int:
        return builder.icmp(i_cod, v1, v2)
    elif v1.type == types.bool:
        return builder.icmp(i_cod, v1, v2)
    elif v1.type == types.char:
        return builder.icmp(i_cod, v1, v2)
    elif v1.type == types.real:
        return builder.fcmp(f_cod, v1, v2)
    else:
        return c_bool(False)

#------------------------------------------------------------------------------------

def c_int(val):
    return Constant.int(types.int,val)

def c_real(val):
    return Constant.real(types.real, val)

def c_char(val):
    return Constant.int(types.char,ord(val)) # ord('a') devolve 97 (codigo ascii)

def c_bool(val):
    if val:
        return c_int(1).icmp(IPRED_UGT,c_int(0))
    else:
        return c_int(0).icmp(IPRED_UGT,c_int(1))

def c_string(context,val,name=""):
    """ Creates a string for LLVM """
    str = context.add_global_variable(Type.array(types.int8, len(val) + 1), name)
    str.initializer = Constant.stringz(val)
    return str

def pointer(block,val):
    """ Returns the pointer for a value """
    return block.gep(val,(  c_int(0), c_int(0) ))

def eval_type(module, type_name, v):
    if type_name == 'int':
        return c_int(v)
    if type_name == 'real':
        return c_real(v)
    if type_name == 'string':
        return c_string(module, v)
    if type_name == 'char':
        return c_char(v)
    if type_name == 'bool':
        return c_bool(v)
    else:
        return types.void

def var_init(module, builder, name, type_name, value=False):
    if not value:
        v = eval_type(module, type_name, types.defaults[type_name])
    else:
        v = eval_type(module, type_name, value)

    t = types.translation[type_name]
    if type_name == 'string':
        try: t = t(len(value))
        except: t = t(10) # Tamanho por default

    ref = builder.alloca(t)
    builder.store(v,ref)
    return ref

#-- Escrita na consola - Standard output --------------------------------------------

def add_stdio(mod):
    """ Adds stdio functions to a module """
    return {
        "printf": mod.add_function(types.function(types.void, (Type.pointer(types.int8, 0),), 1), "printf"),
        "println": create_print(mod,ln=True),
        "print": create_print(mod),
        "printint": create_print_alt('int',mod),
        "printreal": create_print_alt('real',mod),
        "printchar": create_print_alt('char',mod),
        "printbool": create_print_alt('bool',mod),
        "printlnint": create_print_alt('int',mod,ln=True),
        "printlnreal": create_print_alt('real',mod,ln=True),
        "printlnchar": create_print_alt('char',mod,ln=True),
        "printlnbool": create_print_alt('bool',mod,ln=True)
    }

def create_print(mod,ln=False):
    """ Creates a stub of println """

    if ln:
        fname = "println"
    else:
        fname = "print"
    printf = mod.get_function_named("printf")

    string_pointer = Type.pointer(types.int8, 0)

    f = mod.add_function(
        types.function(types.void, (string_pointer,) )
    , fname)
    bb = f.append_basic_block("entry")
    builder = Builder.new(bb)
    builder.call(printf,   (
        f.args[0],
    ))

    if ln:
        builder.call(printf,   (
            pointer(builder, c_string(mod,"\n")),
        ))
    builder.ret_void()
    return f

def create_print_alt(type_,mod,ln=False):
    if type_ == 'int':
        fname = 'printint'
        code = '%d'
        argtype = types.int
    elif type_ == 'real':
        fname = 'printreal'
        code = '%f'
        argtype = types.real
    elif type_ == 'char':
        fname = 'printchar'
        code = '%c'
        argtype = types.char
    elif type_ == 'bool':
        fname = 'printbool'
        code = '%d'
        argtype = types.bool

    if ln:
        fname = fname.replace("print","println")
        code += "\n"

    printf = mod.get_function_named("printf")

    funcType = Type.function(Type.void(), [argtype])
    print_alt = mod.add_function(funcType, fname)

    bb = print_alt.append_basic_block('bb')
    b = Builder.new(bb)

    stringConst = c_string(mod,code)
    stringConst = pointer(b,stringConst)

    b.call(printf,[stringConst,print_alt.args[0]])
    b.ret_void()
    return print_alt;

#-- Variáveis globais ---------------------------------------------------------------

def global_var_init(context,type,name):
    val = types.defaults[type] # Valor default para o tipo
    if type == 'int':
        return c_int_global(context,val,name)
    if type == 'real':
        return c_real_global(context,val,name)
    if type == 'char':
        return c_char_global(context,val,name)
    if type == 'bool':
        return c_bool_global(context,val,name)
    else:
        return types.void

def c_int_global(context,val,name):
    var = context.add_global_variable(types.int, name)
    var.initializer = Constant.int(types.int,val) # que é igual a c_int(val)
    return var

def c_real_global(context,val,name):
    var = context.add_global_variable(types.real, name)
    var.initializer = Constant.real(types.real,val)
    return var

def c_char_global(context,val,name):
    var = context.add_global_variable(types.char, name)
    var.initializer = c_char(val)
    return var

def c_bool_global(context,val,name):
    var = context.add_global_variable(types.bool, name)
    var.initializer = c_bool(val)
    return var

#####################################################################################

def create_main(mod):
    """ Returns a main function """
    tpointer = Type.pointer(Type.pointer(types.int8, 0), 0)
    ft = Type.function(types.int,[types.int, tpointer])
    return mod.add_function(ft, "main")

class Block(object):
    def __init__(self, builder, where, label):
        self.emit = builder
        self.block = where.append_basic_block(label)
        self.post_block = fun.append_basic_block("__break__" + label)

    def __enter__(self):
        self.emit.branch(self.block)
        self.emit.position_at_end(self.block)
        return self.block, self.post_block

    def __exit__(self, *arg):
        self.emit.branch(self.post_block)
        self.emit.position_at_end(self.post_block)

class IfBlock(Block):
    count = 0
    def __init__(self, emit, fun, cond):
        Block.__init__(self, emit, fun, "if_%d" % self.__class__.count)
        self.__class__.count += 1
        emit.cbranch(cond, self.block, self.post_block)
