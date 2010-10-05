
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# ________________ Utilizacao de dados do tipo char (caracteres) ____________________

global char b;

main:
    char a = 'a';
    b = 'b';

    println(a);
    println(b);
    println('c');
    println('0' + '1'); # ascii['0'] = 48, ascii['1'] = 49, ascii['a'] = 97
end
