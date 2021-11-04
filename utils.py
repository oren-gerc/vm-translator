enum_command_type = {1: "C_ARITHMETIC", 2: "C_PUSH", 3: "C_POP"}

command_type_dict = {"add": 1, "sub": 1, "neg": 1, "eq": 1, "gt": 1, "lt": 1, "and": 1, "or": 1, "not": 1,
                     "push": 2, "pop": 3}

# assembly commands:
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
const_push_asm = ""
temp_push_asm = ""
pointer_push_asm = ""
static_push_asm = ""

# memory segments
CONST = "constant"
STATIC = "static"
LOCAL = "local"
ARGUMENT = "argument"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"

ASM_PUSH_1_PARAM = {CONST: const_push_asm, STATIC: static_push_asm, TEMP: temp_push_asm,
                    POINTER: pointer_push_asm}
ASM_PUSH_2_PARAM = {ARGUMENT: generic_push_asm, LOCAL: generic_push_asm, THIS: generic_push_asm,
                    THAT: generic_push_asm}
