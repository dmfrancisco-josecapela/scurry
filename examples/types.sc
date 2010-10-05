
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# _______________________________ Tipos de dados ____________________________________

# Por default, os valores boolean sao impressos como 0 ou 1
# Esta funcao permite imprimir 'true' or 'false' conforme o valor do parametro
void println_bool(bool b):
    b? println('true') : println('false');
end

main:
    real f = 3.2;
    f = 1.0 + f;

    print("Numeros reais: \t");    println(f);
    print("               \t");    println(3.14159265);

    int i = (20 * 3) / 4;

    print("Inteiros: \t");         println(i);
    print("          \t");         println(48121623);

    char a = 'a';

    print("Caracteres: \t");       println(a);
    print("            \t");       println('b');

    bool b = false;

    print("Booleans: \t");         println_bool(not b);
    print("          \t");         println_bool(1 > 2);
    print("          \t");         println('1' > '2');
end
