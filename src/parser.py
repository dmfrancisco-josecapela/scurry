# coding: latin-1

import sys, os
import logging
from subprocess import Popen, PIPE

from lib.ply import yacc, lex

from tokens import *
from rules import *
from semantic import *
from codegen.builder import *


def get_input(file=False):
    ''' Obtenção dos dados do ficheiro de input ou da linha de comandos '''
    if file: # Se foi indicado o ficheiro de input
        f = open(file,"r")
        data = f.read()
        f.close()
    else: # Se não foi indicado ficheiro de input, ler da consola
        data = ""
        while True:
            try:
                data += raw_input() + "\n"
            except:
                break
    return data

def main(options={}, filename=False):
    ''' Rotina principal do scurry '''

    # Objecto de logging
    logging.basicConfig(
        level = logging.DEBUG,
        filename = "log/parselog.txt",
        filemode = "w",
        format = "%(lineno)4d: %(message)s"
    )
    log = logging.getLogger()
    yacc.yacc(debuglog=log, debug=True, outputdir="log")

    # Obter dados do ficheiro de input
    try:
        data = get_input(filename)
    except Exception, e:
        print "Error: %s" % e
        sys.exit()

    # Análise lexical e sintática
    lexer = lex.lex(nowarn=1)
    ast =  yacc.parse(data, tracking = True) # Para guardar números de linhas
    # O parâmetro "lexer" identifica o nosso tokenizer (sem este parâmetro procura
    # pelo ficheiro lex.py)

    # Análise semântica
    try:
        check(ast)
    except Exception, e:
        print e
        sys.exit()

    # Geração de Código
    try:
        o = Writer()(ast)
    except Exception, e:
        print e
        sys.exit()

    if not hasattr(o,"ptr"):
        print "Error compiling"
        sys.exit()

    if options.verbose:
        print o
        if options.run:
            print 20*"-" + " END " + 20*"-"

    if options.run: # Executar o programa resultante em vez de o gravar em ficheiro
        from llvm.core import _core
        bytecode = _core.LLVMGetBitcodeFromModule(o.ptr)

        p = Popen(['lli'],stdout=PIPE, stdin=PIPE)
        sys.stdout.write(p.communicate(bytecode)[0])

    elif options.cfile: # Gerar o ficheiro em código C reduzido
        o.to_bitcode(file("tmp/middle.bc", "w"))
        os.system("llc tmp/middle.bc -o %s -march c"  % options.cfile)

    else: # Gerar o ficheiro executável final
        o.to_bitcode(file("tmp/middle.bc", "w"))
        os.system("llc -f -o=tmp/middle.s tmp/middle.bc")
        os.system("gcc -o %s tmp/middle.s" % options.filename)


if __name__ == '__main__':
    main()
