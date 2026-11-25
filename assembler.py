#!/usr/bin/env python3
"""
Hack Assembler (Nand to Tetris, Capstone Part B)
Name : Madhur Mangla
Roll : 2501350087   ->   K = 87
Extra feature (K mod 3 = 0, since 87 mod 3 = 0): save all labels and variables with their
addresses in symbols.txt.

Usage:  python assembler.py Prog.asm
Output: Prog.hack  and  symbols.txt  (both in the same folder as Prog.asm)
"""
import os
import sys

# ---------- lookup tables ----------
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
    # same operations written in the other order
    "A+D": "0000010", "M+D": "1000010", "A&D": "0000000", "M&D": "1000000",
    "A|D": "0010101", "M|D": "1010101", "1+D": "0011111", "1+A": "0110111",
    "1+M": "1110111",
}
DEST_BIT = {"A": 4, "D": 2, "M": 1}          # d1 d2 d3 = A D M
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
for i in range(16):
    PREDEFINED["R%d" % i] = i


def fail(line_no, text):
    print("Line %d: invalid instruction '%s'" % (line_no, text))
    sys.exit(1)


def clean(line):
    """Remove comment and all spaces."""
    return "".join(line.split("//")[0].split())


# ---------- first reading ----------
def first_pass(lines):
    """Drop comments/blank lines; record each (LABEL) with the number of the
    next real instruction."""
    symbols = dict(PREDEFINED)
    labels = {}
    instructions = []                 # list of (source line number, text)
    for n, raw in enumerate(lines, 1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith("("):
            if not line.endswith(")") or len(line) < 3:
                fail(n, line)
            name = line[1:-1]
            symbols[name] = len(instructions)
            labels[name] = len(instructions)
        else:
            instructions.append((n, line))
    return symbols, labels, instructions


# ---------- second reading ----------
def c_instruction(line, n):
    dest, jump = "", ""
    rest = line
    if "=" in rest:
        dest, rest = rest.split("=", 1)
    if ";" in rest:
        rest, jump = rest.split(";", 1)
    comp = rest
    if comp not in COMP or jump not in JUMP:
        fail(n, line)
    d = 0
    for ch in dest:
        if ch not in DEST_BIT:
            fail(n, line)
        d |= DEST_BIT[ch]
    return "111" + COMP[comp] + format(d, "03b") + JUMP[jump]


def second_pass(instructions, symbols):
    """Turn every instruction into 16 bits. New variables get 16, 17, 18..."""
    variables = {}
    next_addr = 16
    out = []
    for n, line in instructions:
        if line.startswith("@"):
            sym = line[1:]
            if not sym:
                fail(n, line)
            if sym.isdigit():
                addr = int(sym)
            else:
                if sym not in symbols:
                    symbols[sym] = next_addr
                    variables[sym] = next_addr
                    next_addr += 1
                addr = symbols[sym]
            if addr > 32767:
                fail(n, line)
            out.append(format(addr, "016b"))
        else:
            out.append(c_instruction(line, n))
    return out, variables


# ---------- extra feature (K mod 3 = 0) ----------
def save_symbols(path, labels, variables):
    with open(path, "w") as f:
        f.write("# Labels (ROM address)\n")
        for name, addr in sorted(labels.items(), key=lambda x: x[1]):
            f.write("%s = %d\n" % (name, addr))
        f.write("\n# Variables (RAM address)\n")
        for name, addr in sorted(variables.items(), key=lambda x: x[1]):
            f.write("%s = %d\n" % (name, addr))


def main():
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".asm"):
        print("Usage: python assembler.py Prog.asm")
        sys.exit(1)
    src = sys.argv[1]
    with open(src) as f:
        lines = f.read().splitlines()

    symbols, labels, instructions = first_pass(lines)
    binary, variables = second_pass(instructions, symbols)

    folder = os.path.dirname(os.path.abspath(src))
    hack_path = os.path.splitext(os.path.abspath(src))[0] + ".hack"
    with open(hack_path, "w") as f:
        f.write("\n".join(binary) + "\n")
    save_symbols(os.path.join(folder, "symbols.txt"), labels, variables)
    print("Wrote %s (%d instructions) and symbols.txt" % (hack_path, len(binary)))


if __name__ == "__main__":
    main()
