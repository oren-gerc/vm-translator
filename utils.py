enum_command_type = {1: "C_ARITHMETIC", 2: "C_PUSH", 3: "C_POP"}

command_type_dict = {"add": 1, "sub": 1, "neg": 1, "eq": 1, "gt": 1, "lt": 1, "and": 1, "or": 1, "not": 1,
                     "push": 2, "pop": 3}

getAsmArithmetic = {
    "add": "M=M+1",
    "sub": 6
}

c_pop = "@{0} //index\n\
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
c_push = "@{0} //index\n\
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

ASM_commands = {"C_POP": c_pop, "C_PUSH": c_push}
