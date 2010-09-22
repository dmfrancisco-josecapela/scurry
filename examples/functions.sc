
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# ___________________________ Funcoes e procedimentos _______________________________

void inutil:
end

void inutil2:
	println('teste');
end

void inutil3(real r):
	r = 1.5;
	print('Valor de r igual a ');
	println(r);
end

# Calcula a funcao de fibonacci de um numero recebido por parametro
int fibonacci(int f):
	if f == 0:
		result = 0;
	else if f == 1:
		result = 1;
	else:
		result = fibonacci(f-2) + fibonacci(f-1);
	end
end

main:
	inutil;
	inutil2;

	real r = -1.0;
	inutil3(r);
	print('Valor de r igual a ');
	println(r);

	print('Fibonacci de 20 igual a ');
	println(fibonacci(20));
end