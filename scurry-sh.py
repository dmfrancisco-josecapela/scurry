#!/usr/bin/env python
# coding: latin-1

# Pré-requisitos
# -----------------------------------------------------------------------------------
# - Pygments 1.3.1 (opcional para syntax highlighting)          http://pygments.org/

# Utilização da aplicação
# -----------------------------------------------------------------------------------
#  $ scurry-sh.py <options>
#  Exemplo: scurry-sh.py source_code.sc --html output.html
#
#  Options:
#    --version                       show program's version number and exit
#    -h, --help                      show this help message and exit
#    -c, --cmd                       print source code with syntax coloring to stdout
#    -w <filename>, --www=<filename> print code with syntax coloring to an html file
#    -r <filename>, --rtf=<filename> print code with syntax coloring to a rtf file

# ___________________________________________________________________________________


# optparse é um módulo que permite fazer o parsing das opções de linha de comandos
# de uma forma simples (ver doc: http://docs.python.org/library/optparse.html)
from optparse import OptionParser
from pygments import highlight
from pygments.formatters import *
from src.color_lexer import *
import sys, codecs

# Configurão do parser das opções de linha de comandos
parser = OptionParser(usage   = "Usage:   %prog [options] \n" \
                                "Example: %prog source_code.sc --html output.html",
                      version = "%prog 0.1")

parser.add_option("-c", "--cmd",
                  default = False,
                  dest    = "commandline",
                  action  = "store_true",
                  help    = "print source code with syntax coloring to stdout")
parser.add_option("-w", "--www",
                  default = False,
                  dest    = "html",
                  metavar = "<filename>",
                  help    = "print source code with syntax coloring to an html file")
parser.add_option("-r", "--rtf",
                  default = False,
                  dest    = "rtf",
                  metavar = "<filename>",
                  help    = "print source code with syntax coloring to a rtf file")


# Parsing das opções de linha de comandos
(options, args) = parser.parse_args()

# Se foram passados parâmetros, o primeiro corresponde ao nome do ficheiro de input
if len(args) > 0:
    f = open(args[0],"r")
    data = f.read()
    f.close()
else:
    data = ""
    while 1:
        try: data += raw_input() + "\n"
        except: break

#####################################################################################

lexer = ScurryLexer()

# Imprimir código colorido num ficheiro html
if options.html:
    formatter = HtmlFormatter(title = 'Scurry source code', encoding='utf-8')

    output = """<?xml version="1.0" encoding="UTF-8"?> \n
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \n
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> \n
                <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head> \n
                <title>Scurry source code</title> \n
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> \n
                <style type="text/css"> \n
             """
    output += formatter.get_style_defs('.highlight')
    output += "\n </style> \n </head> \n <body> \n"
    output += highlight(data, lexer, formatter)
    output += "\n </body> \n </html>"

    f = open(options.html,"w")
    f.write(output) # output.encode("utf-8")
    f.close()

# Imprimir código colorido num ficheiro rtf
elif options.rtf:
    formatter = RtfFormatter()
    output = highlight(data, lexer, formatter)

    f = open(options.rtf,"w")
    f.write(output)
    f.close()

# Imprimir na consola (cores na consola apenas funcionam em linux e macosx)
elif options.commandline or len(args) == 1:
    formatter = TerminalFormatter()
    print highlight(data, lexer, formatter)

else:
    raise "Invalid command-line parameters"
