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

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_file = output_stream
        self.file_name = ""

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
            if segment in [utils.CONST, utils.TEMP, utils.POINTER, utils.STATIC]:
                to_write = utils.PUSH_TO_ASM[segment].format(index)
            else:  # segments: local, this, that, argument
                to_write = utils.generic_push_asm.format(index, segment)
        elif command == "C_POP":
            if segment in [utils.CONST, utils.TEMP, utils.POINTER, utils.STATIC]:
                to_write = utils.POP_TO_ASM[segment].format(index)
            else:  # segments: local, this, that, argument
                to_write = utils.generic_pop_asm.format(index, segment)
        self.output_file.write(to_write)

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()
