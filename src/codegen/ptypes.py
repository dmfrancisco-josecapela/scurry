from llvm.core import *

# auxiliary
void = Type.void()
int8 = Type.int(8)

int  = Type.int()
real = Type.double()
char = Type.int(8)
bool = Type.int(1)
string = lambda x: Type.array(int, x)

function = Type.function

def procedure(*args):
	return Type.function(void, args)


translation = {
	"int":  int,
	"real": real,
	"char": char,
    "bool": bool,
    "string": string
}

class ReverseDict(object):
	def __init__(self,dic):
		self.dic = dic
	def __getitem__(self,p):
		for k in self.dic:
			if self.dic[k] == p:
				return k

reverse_translation = ReverseDict(translation)

defaults = {
	"int":    0,
	"real":   0.0,
	"char":   '_',
    "bool":   0,
    "string": " ",
}