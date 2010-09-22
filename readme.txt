
 SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
 -----------------------------------------------------------------------------------
 David Marquês Francisco       nº2007183509    <dmfranc@student.dei.uc.pt>
 José António Capela Dias      nº2007183794    <jacdias@student.dei.uc.pt>



 Pré-requisitos
 -----------------------------------------------------------------------------------
 - PLY (Python Lex-Yacc) 3.3                              http://www.dabeaz.com/ply
     O código relativo a esta versão encontra-se incorporado no projecto (na pasta
     lib) por isso não é necessário instalá-lo.
 - PY-LLVM                                         http://code.google.com/p/llvm-py
 - LLVM Compiler Infrastructure 2.4                                 http://llvm.org
 - Pygments 1.3.1 (opcional para syntax highlighting)          http://pygments.org/



 Guia rápido de instalação das dependências
 -----------------------------------------------------------------------------------
 1. PLY
    Não é necessário instalar. Todavia pode ser obtido em:
        # http://www.dabeaz.com/ply/ply-3.3.tar.gz
    E instalado com o seguinte comando:
        $  sudo python setup.py install
    Uma alternativa para Ubuntu é instalar a partir do Synaptic o pacote:
        # python-llvm

 2. PY-LLVM
    a. Obtenha a versão 2.7 do LLVM e compile-a. Tenha em atenção que deve passar o
       parâmetro '--enable-pic' ao LLVM 'configure'.
    b. Instale o llvm-py:
        $ tar jxvf llvm-py-0.5.tar.bz2
        $ cd llvm-py-0.5
        # Locate llvm-config, usually under <llvm>/Release/bin
        $ sudo python setup.py install --llvm-config=/path/to/llvm-config

 3. LLVM
    A instalação em Ubuntu é fácil. A partir do Synaptic basta instalar os pacotes:
        # llvm
        # llvm-dev
        # libllvm2.7
        # llvm-gcc-4.2
    Para outros sistemas operativos, visite:
        # http://llvm.org/releases/

 4. Pygments
    O código fonte pode ser obtido em:
        # http://pypi.python.org/pypi/Pygments
    Basta executar o seguinte comando:
        $  sudo python setup.py install
    Uma alternativa para Ubuntu é instalar a partir do Synaptic o pacote:
        # python-pygments



 Utilização da aplicação
 -----------------------------------------------------------------------------------
  $ python scurry.py <options>
  Exemplo: python scurry.py input.sc -o output.out

  Options:
    -h, --help                            show this help message and exit
    -c <filename>, --ansic=<filename>     generate reduced C code to <filename>
    -o <filename>, --out=<filename>       write output to <filename>
    -e, --emit                            prints the bytecode to the screen
    -i, --instant                         runs the result instead of saving



 Agradecimentos
 -----------------------------------------------------------------------------------
  Scurry teve como base um projecto criado por Alcides Fonseca.
  O código está acessível em: http://github.com/alcides/pascal-in-python


