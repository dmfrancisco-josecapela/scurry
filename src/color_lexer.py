# coding: latin-1

# Este ficheiro não faz parte do compilador da linguagem.
# Serve apenas para permitir a coloração do código (syntax highlighting) através do
# programa 'scurry-sh.py'

import re

from pygments.lexer import Lexer, RegexLexer, ExtendedRegexLexer, \
     LexerContext, include, combined, do_insertions, bygroups, using
from pygments.token import Error, Text, \
     Comment, Operator, Keyword, Name, String, Number, Generic, Punctuation
from pygments.util import get_bool_opt, get_list_opt, shebang_matches
from pygments import unistring as uni


class ScurryLexer(RegexLexer):
    name = 'Scurry'
    aliases = ['scurry', 'sc']
    filenames = ['*.sc']
    mimetypes = ['text/x-scurry', 'application/x-scurry']

    tokens = {
        'root': [
            (r'\n', Text),
            (r'[^\S\n]+', Text),
            (r'#.*$', Comment),
            (r'[]:(),;[]', Punctuation),
            # (r'\\\n', Text),
            # (r'\\', Text),
            (r'(and|or|not)\b', Operator.Word),
            (r'!=|==|<<|>>|[-~+/*%=<>?!&^|.]', Operator),
            include('keywords'),
            include('builtins'),
            ('(?:[rR]|[uU][rR]|[rR][uU])"', String, 'dqs'),
            ("(?:[rR]|[uU][rR]|[rR][uU])'", String, 'sqs'),
            ('[uU]?"', String, combined('stringescape', 'dqs')),
            ("[uU]?'", String, combined('stringescape', 'sqs')),
            include('name'),
            include('numbers'),
        ],
        'keywords': [
            (r'(main|end|if|else|unless|for|while|do|to|downto|'
             r'until|global|void|real|int|string|char|'
             r'bool|mod|result)\b', Keyword),
        ],
        'builtins': [
            (r'(?<!\.)(print|println)\b', Name.Builtin),
            (r'(?<!\.)(true|false)\b', Name.Builtin.Pseudo),
        ],
        'numbers': [
            (r'-?[0-9]+\.[0-9]+', Number.Float),
            (r'-?[0-9]+', Number.Integer)
        ],
        'name': [
            ('[A-z][A-z0-9_]*', Name),
        ],
        'stringescape': [
            (r'\\([\\abfnrtv"\']|\n|N{.*?}|u[a-fA-F0-9]{4}|'
             r'U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', String.Escape)
        ],
        'strings': [
            (r'%(\([a-zA-Z0-9]+\))?[-#0 +]*([0-9]+|[*])?(\.([0-9]+|[*]))?'
             '[hlL]?[diouxXeEfFgGcrs%]', String.Interpol),
            (r'[^\\\'"%\n]+', String),
            # quotes, percents and backslashes must be parsed one at a time
            (r'[\'"\\]', String),
            # unhandled string formatting sign
            (r'%', String)
            # newlines are an error (use "nl" state)
        ],
        'nl': [
            (r'\n', String)
        ],
        'dqs': [
            (r'"', String, '#pop'),
            (r'\\\\|\\"|\\\n', String.Escape), # included here again for raw strings
            include('strings')
        ],
        'sqs': [
            (r"'", String, '#pop'),
            (r"\\\\|\\'|\\\n", String.Escape), # included here again for raw strings
            include('strings')
        ],
    }
