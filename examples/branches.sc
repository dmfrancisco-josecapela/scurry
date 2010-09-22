
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# ______________ Exemplos de utilizacao de instrucoes condicionais __________________

main:
    int A = 1;
    int B = 2;

    if A == 0 or B == 0:
        println("A == 0 ou B == 0");
    else if A == 1 and B == 1:
        println("A == 1 e B == 1");
    else if A == 1 and B == 2:
        println("A == 1 e B == 2");
    else:
        println("A maior que 2");
    end

    if A == B:
        println("A e B sao iguais");
    else:
        println("A e B sao diferentes");
    end

    # -- Instrucoes de seleccao alternativas ----------------------------------------

    bool admin = true;

    # Instrucao unless com apenas um statement
    println("Administrador") unless not admin;

    # Instrucao unless com um ou mais statements
    do:
        print("Admin");
        println("istrador");
    unless not admin;

    # Expressao condicional com instrucao unica em caso de verdade (semelhante ao IF)
    not admin? print("Not admin");

    # Expressao condicional com instrucao unica em caso de verdade e falsidade
    # Equivale a:
    #    if admin: println("Admin!"); else: println("Not admin!"); end
    #
    admin? println("Admin!") : println("Not admin!");
end
