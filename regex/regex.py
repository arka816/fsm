# regex compiler
# follows the original regular expression syntax
# does not support character escaping

# operators:
# 1. concatenation:             .
# 2. union:                     +
# 3. star or kleine closure:    *
# 4. parentheses:               ()

UNION_OP                = '+'
STAR_OP                 = '*'
PARENTHESES_OPENING_OP  = '('
PARENTHESES_CLOSING_OP  = ')'

class ASTNode:
    def __init__(self, type, val=None) -> None:
        # type can be 1 of 5 values
        # 1. concatenation operator
        # 2. union operator
        # 3. kleine star operator
        # 4. literal
        self.type = type
        if self.type == 'literal' and self.val == None:
            raise Exception(f'need literal value for {self}')
        self.val = val
        self.children = []

    def add_child(self, child) ->None:
        self.children.append(child)


class RegExp:
    def __init__(self, exp) -> None:
        self.exp = exp

    def parse(self, subexps):
        # Step 2.a : first layer based on union of sub-regexes
        # Step 2.b : second layer based on concatenation of sub-regexes
        # Step 2.c : third layer based on kleine star

        if (UNION_OP, 'union') in subexps:
            node = ASTNode('union')
            
        pass
            
    def compile(self):
        # Step 1: split into subexpressions recursively
        subexps = self.__compile_rec(self.exp)
        # Step 2: bundle subexpressions into an AST
        return subexps

    def __compile_rec(self, exp):
        i, length = 0, len(exp)
        group_mode = False

        subexps = []
        subexp = ''

        while i < length:
            c = exp[i]

            if c == PARENTHESES_OPENING_OP:
                subexp += c
                if group_mode:
                    group_stack.append(PARENTHESES_OPENING_OP)
                else:
                    group_mode = True
                    group_stack = []
                    group_stack.append(PARENTHESES_OPENING_OP)
            elif c == PARENTHESES_CLOSING_OP:
                subexp += c
                if group_mode:
                    # pop parentheses to maintain balanced parsed expression
                    group_stack.pop()
                    if len(group_stack) == 0:
                        # end of group
                        group_mode = False
                        subexp = subexp[1:len(subexp)-1]
                        subexps.append((self.__compile_rec(subexp), 'nest'))
                        subexp = ""
                else:
                    raise Exception(f'stray closing parentheses {PARENTHESES_CLOSING_OP} spotted')
            elif c == UNION_OP:
                if group_mode:
                    subexp += c
                else:
                    subexp = c
                    subexps.append((subexp, 'union'))
                    subexp = ""
            elif c == STAR_OP:
                if group_mode:
                    subexp += c
                else:
                    subexp = c
                    subexps.append((subexp, 'kleine star'))
                    subexp = ""
            else:
                if group_mode:
                    subexp += c
                else:
                    subexps.append((c, 'literal'))

            i += 1

        return subexps


regex = "10*+01(01+1)*1(0(0+1)1)*+(0*1)*"
compiler = RegExp(regex)
subexps = compiler.compile()
