#!/usr/bin/env python
# coding: latin-1

# Pré-requisitos
# -----------------------------------------------------------------------------------
# - PLY (Python Lex-Yacc) 3.3                              http://www.dabeaz.com/ply
#     O código relativo a esta versão encontra-se incorporado no projecto (na pasta
#     lib) por isso não é necessário instalá-lo.
# - PY-LLVM                                         http://code.google.com/p/llvm-py
# - LLVM Compiler Infrastructure 2.4                                 http://llvm.org

# Utilização da aplicação
# -----------------------------------------------------------------------------------
#  $ python scurry.py <options>
#  Exemplo: python scurry.py input.sc -o output.out
#
#  Options:
#    -h, --help                            show this help message and exit
#    -c <filename>, --ansic=<filename>     generate reduced C code to <filename>
#    -o <filename>, --out=<filename>       write output to <filename>
#    -e, --emit                            prints the bytecode to the screen
#    -i, --instant                         runs the result instead of saving

# ___________________________________________________________________________________


# optparse é um módulo que permite fazer o parsing das opções de linha de comandos
# de uma forma simples (ver doc: http://docs.python.org/library/optparse.html)
from optparse import OptionParser
from src.parser import main

# Configuração do parser das opções de linha de comandos
parser = OptionParser(usage   = "Usage:   %prog [options] \n" \
                                "Example: %prog input_file.sc -o output_file.out",
                      version = "%prog 2.0")

parser.add_option("-c", "--ansic",
                  default = False,
                  dest    = "cfile",
                  metavar = "<filename>",
                  help    = "generate reduced C code to <filename>")
parser.add_option("-o", "--out",
                  default = False,
                  dest    = "filename",
                  metavar = "<filename>",
                  help    = "write output to <filename>")
parser.add_option("-e", "--emit",
                  default = False,
                  dest    = "verbose",
                  action  = "store_true",
                  help    = "prints the bytecode to the screen")
parser.add_option("-i", "--instant",
                  default = False,
                  dest    = "run",
                  action  = "store_true",
                  help    = "runs the result instead of saving")

# Parsing das opções de linha de comandos
(options, args) = parser.parse_args()

# Se não foi indicado o ficheiro de output
if not options.filename:
	if len(args) > 0:
		options.filename = args[0].replace(".sc",".out")
	else:
		options.filename = "a.out"

# Se foram passados parâmetros, o primeiro corresponde ao nome do ficheiro de input
if len(args) > 0:
    main(options, args[0])
else:
    main(options)
