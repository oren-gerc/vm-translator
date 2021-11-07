enum_command_type = {1: "C_ARITHMETIC", 2: "C_PUSH", 3: "C_POP"}

command_type_dict = {"add": 1, "sub": 1, "neg": 1, "eq": 1, "gt": 1, "lt": 1, "and": 1, "or": 1, "not": 1,
                     "push": 2, "pop": 3}

# memory segments
CONST = "constant"
STATIC = "static"
LOCAL = "local"
ARGUMENT = "argument"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"

# arithmetic commands
add = "add"
subtract = "sub"
negate = "neg"
less_than = "lt"
greater_than = "gt"
equals = "eq"
logical_and = "and"
logical_or = "or"
logical_not = "not"

# assembly push/pop commands:
generic_pop_asm = "@{0} //index\n\
                    D=A\n\
                    @{1} //segment\n\
                    D=D+M\n\
                    @addr\n\
                    M=D\n\
                    \n\
                    @SP \n\
                    M=M-1 \n\
                    \n\
                    A=M \n\
                    D=M\n\
                    \n\
                    @addr\n\
                    A=M\n\
                    M=D"
const_pop_asm = "{}"
temp_pop_asm = "{}"
pointer_pop_asm = "{}"
static_pop_asm = "{}"
generic_push_asm = "@{0} //index\n\
                    D=A\n\
                    @{1} //segment\n\
                    D=D+M\n\
                    @addr\n\
                    M=D\n\
                    \n\
                    A=M \n\
                    D=M\n\
                    \n\
                    @addr\n\
                    A=M\n\
                    M=D\n\
                    \n\
                    @SP \n\
                    M=M-1 \n"
const_push_asm = "{}"
temp_push_asm = "{}"
pointer_push_asm = "{}"
static_push_asm = "{}"

PUSH_TO_ASM = {CONST: const_push_asm, STATIC: static_push_asm, TEMP: temp_push_asm,
               POINTER: pointer_push_asm, ARGUMENT: generic_push_asm, LOCAL: generic_push_asm,
               THIS: generic_push_asm, THAT: generic_push_asm}
POP_TO_ASM = {CONST: const_pop_asm, STATIC: static_pop_asm, TEMP: temp_pop_asm,
              POINTER: pointer_pop_asm, ARGUMENT: generic_pop_asm, LOCAL: generic_pop_asm,
              THIS: generic_pop_asm, THAT: generic_pop_asm}

# assembly arithmetic commands:
add_asm = "@SP\n\
            A=M-1\n\
            D=M\n\
            A=A-1\n\
            D=D+M\n\
            M=D\n\
            A=A+1"
sub_asm = "@SP\n\
            A=M-1\n\
            D=M\n\
            A=A-1\n\
            D=D-M\n\
            M=D\n\
            A=A+1"
neg_asm = ""
eq_asm = ""
gt_asm = ""
lt_asm = ""
and_asm = ""
or_asm = ""
not_asm = ""
ARITHMETIC_TO_ASM = {add: add_asm,
                     subtract: sub_asm,
                     negate: neg_asm,
                     equals: eq_asm,
                     greater_than: gt_asm,
                     less_than: lt_asm,
                     logical_and: and_asm,
                     logical_or: or_asm,
                     logical_not: not_asm}
