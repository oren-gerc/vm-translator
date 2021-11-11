command_type_dict = {"add": "C_ARITHMETIC", "sub": "C_ARITHMETIC", "neg": "C_ARITHMETIC", "eq": "C_ARITHMETIC",
                     "gt": "C_ARITHMETIC", "lt": "C_ARITHMETIC", "and": "C_ARITHMETIC", "or": "C_ARITHMETIC",
                     "not": "C_ARITHMETIC",
                     "push": "C_PUSH", "pop": "C_POP"}

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
temp_pop_asm = "{}"
pointer_pop_asm = "{}"
static_pop_asm = "{}"

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
general_segment_push_asm = """
@{0}
D=A
@{1}
A=A+D
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
temp_push_asm = """

"""
address_push_asm = """
@{}
D=M
""" + push_asm

PUSH_TO_ASM = {CONST: const_push_asm, STATIC: static_push_asm, TEMP: temp_push_asm,
               POINTER: address_push_asm, ARGUMENT: general_segment_push_asm, LOCAL: general_segment_push_asm,
               THIS: general_segment_push_asm, THAT: general_segment_push_asm}
POP_TO_ASM = {STATIC: static_pop_asm, TEMP: temp_pop_asm, POINTER: pointer_pop_asm, ARGUMENT: generic_pop_asm,
              LOCAL: generic_pop_asm, THIS: generic_pop_asm, THAT: generic_pop_asm}

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
neg_asm = "@SP\n\
            A=M-1\n\
            M=-M"
comparison_asm = """
    @SP
	A = M - 1 //A -> y
	D = M
	A = A - 1 // A -> x
	D = D - M // D = y - x
	@SP
	M = M - 1  // SP--
	A = M - 1
	@TRUE
	D; {}
	M = 0 // false
	(END)
	@END
	0; JMP // infinite loop
	(TRUE)
	M = -1 // true
	0; JMP // infinite loop
"""
eq_asm = comparison_asm.format("JEQ")
gt_asm = comparison_asm.format("JGT")
lt_asm = comparison_asm.format("JLT")
and_or_asm = """
@SP
A=M-1
D=M
A=A-1
M=D{}M
@SP
M=M-1
and
"""
and_asm = and_or_asm.format("&")
or_asm = and_or_asm.format("|")
not_asm = """
    @SP
    A=M-1
    M= !M
"""
ARITHMETIC_TO_ASM = {add: add_asm,
                     subtract: sub_asm,
                     negate: neg_asm,
                     equals: eq_asm,
                     greater_than: gt_asm,
                     less_than: lt_asm,
                     logical_and: and_asm,
                     logical_or: or_asm,
                     logical_not: not_asm}
