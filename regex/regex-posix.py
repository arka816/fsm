# UNIX Syntax

# NO SUPPORT FOR:
# 1. character class subtraction
# 2. character class intersection
# 3. named capture in groups
# 4. lookahead
# 5. lookbehind

# SUPPORTS:
# 1. nested grouping
# 2. no-capture grouping using ?:

# most reserved (special) characters need to be escaped
# if they are meant as literal characters

anchors                     = ['^', '$']
quantifiers                 = ['*', '+', '?']           # quantifiers are all unary operators
char_classes                = ['\d', '\w', '\s', '\D', 'W', '\S', '.']
operators                   = ['|']                     # or operator is a binary operator
flags                       = ['g', 'm', 'i']
meta_inside_character_class = [']', '\\', '^', '-']     # character classes will be parsed separately

CHARACTER_CLASS_START   = "["
CHARACTER_CLASS_END     = "]"
GROUP_OP_START          = "("
GROUP_OP_END            = ")"                         
QUANTIFIER_START        = "{"
QUANTIFIER_END          = "}"
NOT_OP                  = "^"                           # not operator is an unary operator
OR_OP                   = "|"                           # or operator is also an unary operator

KEYWORD_ANCHOR          = "anchor"
KEYWORD_LITERAL         = "literal"
KEYWORD_CHARACTER_CLASS = "character_class"
KEYWORD_GROUP           = "group"
KEYWORD_OPERATOR        = "operator"
KEYWORD_ESCAPED_LITERAL = "escaped_literal"
KEYWORD_QUANTIFIER      = "quantifier"

def parse_group_postfix(group):
    return group

def parse(exp):
    # step 1: tokenize
    # step 2: atomised regexes
    # step 3: convert to reverse polish form (postfix)
    
    # step 1: tokenize
    character_class_start_index = -1
    group_op_start_index = -1
    limited_quantifier_state = False
    
    groupstack = []
    stack = []
    curr = ""
    i = -1

    while i+1 < len(exp):
        i += 1
        char = exp[i]
        
        if char == "\\":
            # eliminate escape sequences by forward lookup
            if i+1 == len(exp):
                raise Exception('rogue escape sequence found')
            else:
                if character_class_start_index != -1 or \
                    limited_quantifier_state or \
                    group_op_start_index != -1:
                    curr += char + exp[i+1]
                else:
                    literal = char+exp[i+1]
                    if literal in char_classes:
                        stack.append((literal, KEYWORD_CHARACTER_CLASS))
                    else:
                        stack.append((literal, KEYWORD_ESCAPED_LITERAL))
                i += 1
                continue
            
        # handle character class
        if character_class_start_index != -1:
            curr += char
            if char == CHARACTER_CLASS_END and exp[i-1] != "\\" \
                    and character_class_start_index != i-1 and \
                    not(i >= 2 and character_class_start_index == i-2 and exp[i-1] == NOT_OP):
                stack.append((curr, KEYWORD_CHARACTER_CLASS))
                curr = ""
                character_class_start_index = -1
            continue
        
        # handle limiting quantifier
        if limited_quantifier_state:
            curr += char
            if char == QUANTIFIER_END:
                stack.append((curr, KEYWORD_QUANTIFIER))
                curr = ""
                limited_quantifier_state = False
            continue
        
        # handle grouping
        if group_op_start_index != -1:
            curr += char
            if char == GROUP_OP_START and exp[i-1] != "\\":
                groupstack.append(char)
            elif char == GROUP_OP_END and exp[i-1] != "\\":
                groupstack.pop()
                if len(groupstack) == 0:
                    stack.append((curr, KEYWORD_GROUP))
                    curr = ""
                    group_op_start_index = -1
            continue
        

        if char == CHARACTER_CLASS_START:
            curr += char
            character_class_start_index = i
        elif char == QUANTIFIER_START:
            curr += char
            limited_quantifier_state = True
        elif char == GROUP_OP_START:
            group_op_start_index = i
            curr += char
            groupstack.append(char)
        else:
            if i == 0 and char == anchors[0]:
                type = KEYWORD_ANCHOR
            elif i == len(exp) - 1 and char == anchors[1]:
                type = KEYWORD_ANCHOR
            elif char in quantifiers:
                type = KEYWORD_QUANTIFIER
            elif char in char_classes:
                type = KEYWORD_CHARACTER_CLASS
            else:
                type = "literal"
            
            stack.append((char, type))
            
    if character_class_start_index != -1:
        raise Exception("non terminating character class initiation")
    if group_op_start_index != -1:
        raise Exception("non terminating grouping initiation")
    if limited_quantifier_state:
        raise Exception("non terminating limited quantifier")
    

    # step 2: atomised regexes and postfix conversion
    # no point in converting groups to postfix since that would 
    # lead to deletion of the no-capture property
    
    atoms = []
    i = len(stack)
    literal_list = []

    while i > 0:
        i -= 1
        sub, type = stack[i]

        if type == KEYWORD_QUANTIFIER:
            if len(literal_list) != 0:
                atoms += literal_list
                literal_list = []
            if i > 0:
                if stack[i-1][1] == KEYWORD_GROUP:
                    atoms.append(stack[i-1][0] + sub)
                elif stack[i-1][1] == KEYWORD_CHARACTER_CLASS:
                    atoms.append(stack[i-1][0] + sub)
                else:
                    # either a literal or an escaped literal
                    atoms.append(stack[i-1][0] + sub)
                i -= 1
        elif type == KEYWORD_CHARACTER_CLASS:
            if len(literal_list) != 0:
                atoms += literal_list
                literal_list = []
            atoms.append(sub)
        elif type == KEYWORD_GROUP:
            if len(literal_list) != 0:
                atoms += literal_list
                literal_list = []
            atoms.append(parse_group_postfix(sub))
        elif type == KEYWORD_ANCHOR:
            if len(literal_list) != 0:
                atoms.append("".join(literal_list[::-1])+sub)
                literal_list = []
            elif sub == anchors[1]:
                j = i-1
                curr = ""
                while j >= 0 and (stack[j][1] == KEYWORD_LITERAL or stack[j][1] == KEYWORD_ESCAPED_LITERAL):
                    curr = stack[j][0] + curr
                    j -= 1
                i = j+1
                atoms.append(curr + sub)
        elif type == KEYWORD_LITERAL or type == KEYWORD_ESCAPED_LITERAL:
            literal_list.append(sub)
        elif type == KEYWORD_OPERATOR:
            if len(literal_list) != 0:
                atoms += literal_list
                literal_list = []
            if sub == OR_OP:
                atoms.append(sub)

    return stack, atoms[::-1]


exp = "^the[^a-zA-Z1-9\[-\]]*\{c\((?:(a|b|(?:c|b))|\)|c){2,5}ab\?[^]]+\d*ac$"
stack, atoms = parse(exp)
