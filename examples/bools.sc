
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# _________________ Utilizacao de dados do tipo bool (booleanos) ____________________

bool are_equal(bool param0, bool param1):
    result = param0 == param1;
end

global bool b0;

main:
    b0 = true;
    bool b1 = !b0;

    if not are_equal(b0, b1): # Operador '!' igual a 'not'
        println('Diferentes!');
    else:
        println('Iguais!');
    end
end
