
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>
# ___________________________________________________________________________________

global int x;

# A passagem de parametros e feita por valor
void myfunc(int param):
    x = 2;
    println(param); # Imprime 1
    println(x); # Imprime 2
end

main:
    x = 1;
    myfunc(x);
end
