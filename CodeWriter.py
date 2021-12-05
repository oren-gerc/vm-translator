"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import utils


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_file = None
        self.file_name = ""
        self._comparison_command_index = 0
        self.call_counter = 0
        # self.is_init = False

    def set_output_file(self, output_stream: typing.TextIO):
        self.output_file = output_stream

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file has
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        self.file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given 
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        if command in utils.comparison_commands:
            assembly = ""
            if command == 'eq':
                assembly = utils.comparison_asm.format(utils.comparison_commands[command],
                                                       self._comparison_command_index)
            elif command == 'lt':
                assembly = utils.lt_asm.format(self._comparison_command_index)
            elif command == 'gt':
                assembly = utils.gt_asm.format(self._comparison_command_index)
            self._comparison_command_index += 1
        else:
            assembly = utils.ARITHMETIC_TO_ASM[command]
        self.output_file.write(assembly)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        to_write = ""
        if command == "C_PUSH":
            if segment == utils.STATIC:
                to_write = utils.static_push_asm.format(self.file_name, index)
            elif segment == utils.TEMP:
                to_write = utils.address_push_asm.format(utils.ADDRESSES["TEMP"] + index)
            elif segment == utils.CONST:
                to_write = utils.const_push_asm.format(index)
            elif segment == utils.POINTER:
                if index == 0:
                    to_write = utils.address_push_asm.format(utils.ADDRESSES["THIS"])
                elif index == 1:
                    to_write = utils.address_push_asm.format(utils.ADDRESSES["THAT"])
            else:  # segments: local, this, that, argument
                to_write = utils.generic_push_asm.format(index, utils.MEMORY_SEGMENT_TO_ASM[segment])
        else:
            if segment == utils.STATIC:
                to_write = utils.static_pop_asm.format(self.file_name, index)
            elif segment == utils.TEMP:
                to_write = utils.address_pop_asm.format(utils.ADDRESSES["TEMP"] + index)
            elif segment == utils.POINTER:
                if index == 0:
                    to_write = utils.address_pop_asm.format(utils.ADDRESSES["THIS"])
                elif index == 1:
                    to_write = utils.address_pop_asm.format(utils.ADDRESSES["THAT"])
            else:  # segments: local, this, that, argument
                to_write = utils.generic_pop_asm.format(index, utils.MEMORY_SEGMENT_TO_ASM[segment])

        self.output_file.write(to_write)

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()

    def write_init(self) -> None:
        """
        Writes the assembly code that effects the VM initialization (also called bootstrap code).
        This code should be placed in the ROM beginning in address 0x0000.
        :return:
        """
        self.output_file.write(utils.bootstrap_asm)
        self.write_call("Sys.init", 0)

    def write_label(self, label: str) -> None:
        """
        Writes the assembly code that is the translation of the given label command
        :return:
        """
        to_write = utils.label_asm.format(label)
        self.output_file.write(to_write)

    def write_goto(self, label: str) -> None:
        """
        Writes the assembly code that is the translation of the given goto command.
        :param label:
        :return:
        """
        to_write = utils.goto_asm.format(label)
        self.output_file.write(to_write)

    def write_if(self, label: str) -> None:
        """
        Writes the assembly code that is the translation of the given if-goto command.
        :param label:
        :return:
        """
        to_write = utils.if_goto_asm.format(label)
        self.output_file.write(to_write)

    def write_call(self, functionName: str, numArgs: int) -> None:
        """
        Writes the assembly code that is the translation of the given Call command.
        :param functionName:
        :param numArgs:
        :return:
        """
        # save return address
        return_address = utils.return_address_label.format(functionName, self.call_counter)
        self.call_counter += 1
        self.output_file.write(utils.const_push_asm.format(return_address))

        # save LCL,ARG,THIS,THAT
        for seg in ["LCL", "ARG", "THIS", "THAT"]:
            self.output_file.write(utils.address_push_asm.format(seg))

        # update position of LCL
        self.output_file.write(utils.save_func_local)

        # update position of ARG
        self.output_file.write(utils.save_func_arg.format(numArgs))

        # goto function (using goto)
        self.write_goto(functionName)

        # write label of return
        self.write_label(return_address)

    def write_return(self) -> None:
        """
        Writes the assembly code that is the translation of the given Return command.
        :return:
        """
        self.output_file.write(utils.return_asm)

    def write_function(self, functionName: str, numLocals: int) -> None:
        """
        Writes the assembly code that is the trans. of the given Function command.
        :param functionName:
        :param numLocals:
        :return:
        """
        self.write_label(functionName)
        # init all LCL to 0
        for i in range(numLocals):
            self.output_file.write(utils.const_push_asm.format(0))

        # for i in range(numLocals):
        #     if i == 0:
        #         self.output_file.write(utils.const_push_asm.format(0))
        #     else:
        #         # 0 is already in D, so no need to write assembly for
        #         # inserting it to D again.
        #         self.output_file.write(utils.generic_push_asm)
