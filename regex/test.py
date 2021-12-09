from regex import RegExp

regex1 = "10*+01(01+1)*1(0(0+1)1)*+(0*1)*"
string1 = "010111001011"
regex2 = "(1+0)*"
string2 = "100112"
compiler = RegExp(regex1)
subexps, root, nfa = compiler.compile()
compiler.visualize()
print(compiler.process(string1))
