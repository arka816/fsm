from treelib import Tree

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
        # 1. concat : concatenation operator
        # 2. union  : union operator
        # 3. star   : kleine star operator
        # 4. literal: literal

        self.type = type
        self.val = val
        if (self.type == 'literal' or self.type == 'nest') and self.val == None:
            raise Exception(f'need literal value for {self}')
        self.children = []
        print(f'node of type {self.type} created')

    def add_children(self, children) ->None:
        if type(children) == list:
            self.children += children
        else:
            self.children.append(children)


class RegExp:
    def __init__(self, exp) -> None:
        self.exp = exp

    def parse(self, subexps):
        # Step 2.a : first layer based on union of sub-regexes
        # Step 2.b : second layer based on concatenation of sub-regexes
        # Step 2.c : third layer based on kleine star

        # check if corner case:
        if len(subexps) == 1:
            exp = subexps[0]
            if exp[1] == 'literal':
                return ASTNode('literal', exp[0]) 
            elif exp[1] == 'nest':
                return self.parse(exp[0])

        # check if union operator is present
        if (UNION_OP, 'union') in subexps:
            node = ASTNode('union')
            union_indices = [index for index in range(len(subexps)) if subexps[index][1] == 'union'] 
            
            children = [self.parse(subexps[: union_indices[0]])]
            children += [self.parse(subexps[union_indices[i] + 1 : union_indices[i+1]]) for i in range(len(union_indices)-1)]
            children += [self.parse(subexps[union_indices[-1] + 1 :])]
            node.add_children(children)
            return node

        # count sub-regexes to be concatenated
        count = 0
        for subexp in subexps:
            if subexp[1] == 'literal' or subexp[1] == 'nest':
                count += 1

        # check for kleine star
        star_indices = [index for index in range(len(subexps)) if subexps[index][1] == 'star']  

        if count > 1:
            children = []
            i = 0 
            while i < len(subexps):
                if i+1 in star_indices:
                    node = ASTNode('star')
                    node.add_children(self.parse([subexps[i]]))
                    children.append(node)
                    i += 1
                else:
                    children.append(self.parse([subexps[i]]))
                i += 1
            node = ASTNode('concat')
            node.add_children(children)
            return node
            
        elif count == 1:
            if len(star_indices) == 1:
                if star_indices[0] == 1:
                    node = ASTNode('star')
                    node.add_children(self.parse([subexps[0]]))
                    return node
                else:
                    raise Exception('stray kleine star found')
            elif len(star_indices) == 0:
                if len(subexps) == 1:
                    return self.parse([subexps[0]])
            else:
                raise Exception('stray kleine star found')

    def compile(self):
        # Step 1: split into subexpressions recursively
        self.subexps = self.__compile_rec(self.exp)

        # Step 2: bundle subexpressions into an AST
        self.root = self.parse(self.subexps)

        return self.subexps, self.root

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
                    subexps.append((subexp, 'star'))
                    subexp = ""
            else:
                if group_mode:
                    subexp += c
                else:
                    subexps.append((c, 'literal'))

            i += 1

        return subexps

    def visualize(self):
        tree = Tree()
        # depth first traversal
        stack = [(self.root, None)]

        symbols = {
            'concat': '.',
            'union' : '+',
            'star'  : '*'
        }

        while len(stack) != 0:
            curr = stack.pop()
            obj, parent = curr
            if parent == None:
                if obj.type == 'literal':
                    tree.create_node(obj.val, id(obj))
                else:
                    tree.create_node(symbols[obj.type], id(obj))
            else:
                if obj.type == 'literal':
                    tree.create_node(obj.val, id(obj), parent = id(parent))
                else:
                    tree.create_node(symbols[obj.type], id(obj), parent = id(parent))
            
            for child in obj.children:
                stack.append((child, obj))

        tree.show()



regex = "10*+01(01+1)*1(0(0+1)1)*+(0*1)*"
compiler = RegExp(regex)
subexps, root = compiler.compile()
compiler.visualize()
