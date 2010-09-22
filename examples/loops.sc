
# SCURRY v2.01 - Dep. de Engenharia Informatica da Faculd. Ciencia e Tecnologia da UC
# -----------------------------------------------------------------------------------
# David Marques Francisco       n 2007183509    <dmfranc@student.dei.uc.pt>
# Jose Antonio Capela Dias      n 2007183794    <jacdias@student.dei.uc.pt>

# _____________________________ Instrucoes de ciclo _________________________________

main:
	int a;

	# Ciclo for decrescente
	for a = 5 downto 1:
		println(a);
	end

	println('');

	# Outra forma de codificar um ciclo decrescente
	for a = 5 to 1, -1:
		println(a);
	end

	println('');

	# Ciclo for com variavel de incremento
	for a = 1 to 10, 2:
		println(a);
	end

	println('');

	# Ciclo while
	while a >= 5:
		println(a);
		a = a - 2;
	end

	println('');

	# Ciclo do-until
	do:
		println(a);
		a = a * 2;
	until a > 100;
end