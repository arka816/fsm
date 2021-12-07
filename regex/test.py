from regex import RegExp

regex1 = "10*+01(01+1)*1(0(0+1)1)*+(0*1)*"
regex2 = "1+0*"
compiler = RegExp(regex1)
subexps, root, nfa = compiler.compile()
compiler.visualize()