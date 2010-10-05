
void inutil0:
end

int inutil1:
    result = 0;
end

void print_hello:
    int C;
    C = 1;
    println('hello');
end

global real xglobal;
global char cglobal;

void print_global_var:
    xglobal = 2.0;
    println(xglobal);
    println(cglobal);
end

int add_ints(int num0, int num1):
    result = num0 + num1;
    print_hello;
end

real add_reals(real num0, real num1):
    result = num0 + num1;
end

void test_booleans:
    bool boolvar;
    boolvar = false;
end

main:
    int A = add_ints(4, 3); # A fica igual a 3
    real B = add_reals(-1.0, 2.0);

    if A == 1 or A == 2:
        println('Valor de A igual a 1 ou 2');
    else if A == 3 or A == 4:
        println('Valor de A igual a 3 ou 4');
    else if A == 5 or A == 6:
        println('Valor de A igual a 5 ou 6');
    else:
        print('Valor de A: ');
        println(A);
        print('Valor de B: ');
        println(B);
    end

    println(3.1 + 3.0);

    ##########################################

    char mychar;
    mychar = 'c';
    println('');
    println('Imprimir o caracter c: ');
    println('c');
    println('Imprimir o caracter guardado na variavel mychar: ');
    println(mychar);
    println('');

    print('Imprimir a variavel global: ');
    print_global_var;
    println('');

    test_booleans;

    bool myvar = true;

    ##########################################

    int a;
    int b = 4 / 3;
    real c = 4.0/3.0;

    print('int b = 4/3 = ');
    println(b);
    print('real c = 4.0/3.0 = ');
    println(c);
    print('15 mod 2 = ');
    println(15 mod 2);
    print('15 % 2 = ');
    println(15 % 2);

    ##########################################

    println('1' < '2');
    println('1' > '2');

    ##########################################

    a = 1;
    if a == 1 and a == 2 and a == 3:
        println(a);
    else:
        println(2);
    end
    println(3);

    println("----");
    for a = 20 downto 10:
        println(a);
    end
    println("----");

    while a >= 2:
        println(a);
        a = a - 1;
    end
    println("----");

    do:
        println(a);
        a = a * 2;
    until a > 100;
end
