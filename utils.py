command_type_dict = {"add": "C_ARITHMETIC", "sub": "C_ARITHMETIC", "neg": "C_ARITHMETIC", "eq": "C_ARITHMETIC",
                     "gt": "C_ARITHMETIC", "lt": "C_ARITHMETIC", "and": "C_ARITHMETIC", "or": "C_ARITHMETIC",
                     "not": "C_ARITHMETIC", "push": "C_PUSH", "pop": "C_POP",
                     "call": "C_CALL", "return": "C_RETURN", "function": "C_FUNCTION",
                     "if-goto": "C_IF", "goto": "C_GOTO", "label": "C_LABEL"}

# memory segments
CONST = "constant"
STATIC = "static"
LOCAL = "local"
ARGUMENT = "argument"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"

ADDRESSES = {"THIS": 3, "THAT": 4, "TEMP": 5}

MEMORY_SEGMENT_TO_ASM = {
    LOCAL: "LCL",
    ARGUMENT: "ARG",
    THIS: "THIS",
    THAT: "THAT",
}

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
pop_asm = """
// D register holds the address of where we want to pop to
@address
M=D

@SP
M=M-1

A=M 
D=M

@address
A=M
M=D
"""
generic_pop_asm = """
@{0}
D=A
@{1}
D=D+M
""" + pop_asm
static_pop_asm = """
@{0}.{1}
D=A
""" + pop_asm
address_pop_asm = """
@{}
D=A
""" + pop_asm

push_asm = """
//assumes D register is loaded with the value to push into stack
//*sp=D
@SP
A=M
M=D

//sp++
@SP
M=M+1
"""
generic_push_asm = """
@{0}
D=A
@{1}
A=M+D
D=M
""" + push_asm
const_push_asm = """
@{0}
D=A
""" + push_asm
static_push_asm = """
@{0}.{1}
D=M
""" + push_asm
address_push_asm = """
@{}
D=M
""" + push_asm

# assembly arithmetic commands:
add_subtract_asm = """
@SP
A=M-1
D=M
A=A-1
M=M{}D
@SP
M=M-1
"""
add_asm = add_subtract_asm.format("+")
sub_asm = add_subtract_asm.format("-")
neg_asm = """
@SP
A=M-1
M=-M
"""
comparison_asm = """
@SP
A = M - 1 //A -> y
D = M
A = A - 1 // A -> x
D = M - D // D = y - x
@SP
M = M - 1  // SP--
A = M - 1
@{1}.TRUE
D; {0}

//else, set to false
({1}.FALSE)
@SP
A = M - 1
M = 0
@{1}.END
0; JMP

({1}.TRUE)
@ SP
A = M - 1
M = -1 // true

({1}.END)
"""

lt_asm = """
//check lt 
@SP
A = M - 1
A = A - 1
D = M // D=x
@{0}.X_POS
D; JGT
@SP
A = M - 1
D = M // D=y
//check if y pos and x neg
@{0}.Y_POS
D; JGT
@{0}.REG_CHECK
0; JMP

({0}.REG_CHECK)
@SP
A = M - 1 //A -> y
D = M
A = A - 1 // A -> x
D = M - D // D = y - x
@SP
M = M - 1  // SP--
A = M - 1
@{0}.TRUE
D; JLT
//else, set to false
({0}.FALSE)
@SP
A = M - 1
M = 0
@{0}.END
0; JMP

({0}.TRUE)
@ SP
A = M - 1
M = -1 // true
@{0}.END
0; JMP

({0}.Y_POS)
@ SP
M = M - 1
A = M - 1
M = -1 // true
@{0}.END
0;JMP

({0}.X_POS)
@ SP
A = M - 1
D = M // D=y
@{0}.Y_NEG
D; JLT
@{0}.REG_CHECK
0; JMP

({0}.Y_NEG)
@SP
M = M - 1
A = M - 1
M = 0
@{0}.END
0; JMP

({0}.END)
"""

gt_asm = """
@SP
A = M - 1
A = A - 1
D = M // D=x
@{0}.X_POS
D; JGT
@SP
A = M - 1
D = M // D=y
//check if y pos and x neg
@{0}.Y_POS
D; JGT
@{0}.REG_CHECK
0; JMP

({0}.REG_CHECK)
@SP
A = M - 1 //A -> y
D = M
A = A - 1 // A -> x
D = M - D // D = y - x
@SP
M = M - 1  // SP--
A = M - 1
@{0}.TRUE
D; JGT
//else, set to false
({0}.FALSE)
@SP
A = M - 1
M = 0
@{0}.END
0; JMP

({0}.TRUE)
@ SP
A = M - 1
M = -1 // true
@{0}.END
0; JMP

({0}.Y_POS)
@ SP
M = M - 1
A = M - 1
M = 0 // false
@{0}.END
0;JMP

({0}.X_POS)
@ SP
A = M - 1
D = M // D=y
@{0}.Y_NEG
D; JLT
@{0}.REG_CHECK
0; JMP

({0}.Y_NEG)
@SP
M = M - 1
A = M - 1
M = -1 // true
@{0}.END
0; JMP

({0}.END)
"""
comparison_commands = {'eq': "JEQ", 'gt': "JGT", 'lt': "JLT"}
and_or_asm = """
@SP
A=M-1
D=M
A=A-1
M=D{}M
@SP
M=M-1
"""
and_asm = and_or_asm.format("&")
or_asm = and_or_asm.format("|")
not_asm = """
@SP
A=M-1
M= !M
"""

shift_left_asm = """
@SP
A=M-1
M= M<<
"""

shift_right_asm = """
@SP
A=M-1
M= M>>
"""

ARITHMETIC_TO_ASM = {add: add_asm,
                     subtract: sub_asm,
                     negate: neg_asm,
                     logical_and: and_asm,
                     logical_or: or_asm,
                     logical_not: not_asm,
                     "shiftleft": shift_left_asm,
                     "shiftright": shift_right_asm}

label_asm = """
({0})
"""

goto_asm = """
@{0}
0; JMP
"""

if_goto_asm = """
// if-goto command

@SP
AM=M-1 // sp--
D=M // pop
@{0} // load c
D; JNE // check last item is not 0
"""

return_address_label = """{0}$ret.{1}"""

save_func_arg = """
@{0}
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D
"""

save_func_local = """
@SP
D=M
@LCL
M=D
"""

save_end_frame = """
//frame=LCL
@LCL
D=M
@frame
M=D
"""
save_return_address = """
//retAddress=*(frame-5)
@5
D=A
@frame
A=M-D
D=M
@retAddress
M=D
"""
return_value_to_arg = """
//*ARG=POP()
@SP
A=M-1
D=M
@ARG
A=M
M=D
"""
sp_after_arg = """
//SP=ARG+1
@ARG
D=M+1
@SP
M=D
"""
restore_seg = """
//SEG=*(frame-SEG_INDEX)
@{1}
D=A
@frame
D=M-D
A=D
D=M
@{0}
M=D
"""
restore_segments = restore_seg.format("THAT", 1) + restore_seg.format("THIS", 2) + restore_seg.format("ARG", 3) + restore_seg.format("LCL", 4)
goto_return = """
//goto return address
@retAddress
0;JMP
"""

return_asm = save_end_frame + save_return_address + return_value_to_arg + sp_after_arg + restore_segments + goto_return

bootstrap_asm = """
@256
D=A
@SP
M=D
"""
