
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# _________________ Operacoes matematicas com inteiros e reais ______________________

int add_ints(int num0, int num1):
    result = num0 + num1;
end

# Devolve o valor correspondente a base ^ exp
int pow(int base, int exp):
    result = 1;
    for a = 1 to exp:
        result = result * base;
    end
end

main:
    int j = 1;
    int res = add_ints(j, 2);

    if res == j + 2:
        print('j + 2 = ');
        println(res);
        print('\n');
    end

    print('4.0 / 3.0 \t = ');       println(4.0 / 3.0);
    print('4 / 3     \t = ');       println(4 / 3);
    print('5 mod 3   \t = ');       println(5 mod 3);
    print('2 * 6 / 2 \t = ');       println(2 * 6 / 2);
    println('');

    print('5 + 10 / 2   \t = ');    println(5+10/2);
    print('(5 * 10) % 3 \t = ');    println((5*10)%3); # % equivale a mod
    print('2 ^ 4        \t = ');    println(pow(2,4));
end