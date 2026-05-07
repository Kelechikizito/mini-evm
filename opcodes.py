# STOP
STOP = 0x0


# The STOP opcode halts execution by setting the stop_flag to True
def stop(evm):
    evm.stop_flag = True


# MATH
ADD = 0x1
MUL = 0x2
SUB = 0x3
DIV = 0x4
SDIV = 0x5
MOD = 0x6
SMOD = 0x7
ADDMOD = 0x8
MULMOD = 0x9
EXP = 0xA
SIGNEXTEND = 0xB

# helper function to determine the sign of a NUMBER
pos_or_neg = lambda number: -1 if number < 0 else 1


# Helper fucntion to determine how many bytes does it take to store this number
def size_in_bytes(number):
    import math

    if number == 0:
        return 1
    bits_needed = math.ceil(math.log2(abs(number) + 1))
    return math.ceil(bits_needed / 8)


def add(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a + b)
    evm.pc += 1
    evm.gas_dec(3)


def mul(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a * b)
    evm.pc += 1
    evm.gas_dec(5)


def sub(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a - b)
    evm.pc += 1
    evm.gas_dec(3)


def div(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(0 if b == 0 else a // b)
    evm.pc += 1
    evm.gas_dec(5)


def sdiv(evm):

    a, b = evm.stack.pop(), evm.stack.pop()
    sign = pos_or_neg(a * b)
    evm.stack.push(0 if b == 0 else sign * (abs(a) // abs(b)))
    evm.pc += 1
    evm.gas_dec(5)


def mod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(0 if b == 0 else a % b)
    evm.pc += 1
    evm.gas_dec(5)


def smod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    sign = -1 if a < 0 else 1  # sign of dividend only
    evm.stack.push(0 if b == 0 else abs(a) % abs(b) * sign)
    evm.pc += 1
    evm.gas_dec(5)


def addmod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    N = evm.stack.pop()
    evm.stack.push((a + b) % N)
    evm.pc += 1
    evm.gas_dec(8)


def mulmod(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    N = evm.stack.pop()
    evm.stack.push((a * b) % N)
    evm.pc += 1
    evm.gas_dec(8)


def exp(evm):
    a, exponent = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a**exponent)
    evm.pc += 1
    evm.gas_dec(10 + (50 * size_in_bytes(exponent)))


def signextend(evm):
    b, x = evm.stack.pop(), evm.stack.pop()
    if b <= 31:
        testbit = b * 8 + 7
        sign_bit = 1 << testbit
        if x & sign_bit:
            result = x | (2**256 - sign_bit)
        else:
            result = x & (sign_bit - 1)
    else:
        result = x

    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(5)


# COMPARISONS
LT = 0x10
GT = 0x11
SLT = 0x12
SGT = 0x13
EQ = 0x14
ISZERO = 0x15



# LOGIC
AND = 0x16
OR = 0x17
XOR = 0x18
NOT = 0x19


# BIT OPERATIONS
BYTE = 0x1A
SHL = 0x1B
SHR = 0x1C
SAR = 0x1D


# MISCELLANEOUS
SHA3 = 0x20

# ETHEREUM STATE
ADDRESS = 0x30
BALANCE = 0x31
ORIGIN = 0x32
CALLER = 0x33
CALLVALUE = 0x34
CALLDATALOAD = 0x35
CALLDATASIZE = 0x36
CALLDATACOPY = 0x37
CODESIZE = 0x38
CODECOPY = 0x39
GASPRICE = 0x3A
EXTCODESIZE = 0x3B
EXTCODECOPY = 0x3C
RETURNDATASIZE = 0x3D
RETURNDATACOPY = 0x3E
EXTCODEHASH = 0x3F
BLOCKHASH = 0x40
COINBASE = 0x41
TIMESTAMP = 0x42
NUMBER = 0x43
PREVRANDAO = 0x44
GASLIMIT = 0x45
CHAINID = 0x46
SELFBALANCE = 0x47
BASEFEE = 0x48

# POP
POP = 0x50

# MEMORY
MLOAD = 0x51
MSTORE = 0x52
MSTORE8 = 0x53

# STORAGE
SLOAD = 0x54
SSTORE = 0x55

# JUMP
JUMP = 0x56
JUMPI = 0x57
PC = 0x58
JUMPDEST = 0x5B

# TRANSIENT STORAGE
TLOAD = 0x5C
TSTORE = 0x5D

# PUSH
PUSH1 = 0x60
PUSH2 = 0x61
PUSH3 = 0x62
PUSH4 = 0x63
PUSH5 = 0x64
PUSH6 = 0x65
PUSH7 = 0x66
PUSH8 = 0x67
PUSH9 = 0x68
PUSH10 = 0x69
PUSH11 = 0x6A
PUSH12 = 0x6B
PUSH13 = 0x6C
PUSH14 = 0x6D
PUSH15 = 0x6E
PUSH16 = 0x6F
PUSH17 = 0x70
PUSH18 = 0x71
PUSH19 = 0x72
PUSH20 = 0x73
PUSH21 = 0x74
PUSH22 = 0x75
PUSH23 = 0x76
PUSH24 = 0x77
PUSH25 = 0x78
PUSH26 = 0x79
PUSH27 = 0x7A
PUSH28 = 0x7B
PUSH29 = 0x7C
PUSH30 = 0x7D
PUSH31 = 0x7E
PUSH32 = 0x7F

# DUP
DUP1 = 0x80
DUP2 = 0x81
DUP3 = 0x82
DUP4 = 0x83
DUP5 = 0x84
DUP6 = 0x85
DUP7 = 0x86
DUP8 = 0x87
DUP9 = 0x88
DUP10 = 0x89
DUP11 = 0x8A
DUP12 = 0x8B
DUP13 = 0x8C
DUP14 = 0x8D
DUP15 = 0x8E
DUP16 = 0x8F

# SWAP
SWAP1 = 0x90
SWAP2 = 0x91
SWAP3 = 0x92
SWAP4 = 0x93
SWAP5 = 0x94
SWAP6 = 0x95
SWAP7 = 0x96
SWAP8 = 0x97
SWAP9 = 0x98
SWAP10 = 0x99
SWAP11 = 0x9A
SWAP12 = 0x9B
SWAP13 = 0x9C
SWAP14 = 0x9D
SWAP15 = 0x9E
SWAP16 = 0x9F

# LOG
LOG0 = 0xA0
LOG1 = 0xA1
LOG2 = 0xA2
LOG3 = 0xA3
LOG4 = 0xA4

# CONTRACT
CREATE = 0xF0
CALL = 0xF1
CALLCODE = 0xF2  # legacy NOT supported by us, fixed by DELEGATECALL
RETURN = 0xF3
DELEGATECALL = 0xF4
CREATE2 = 0xF5
STATICCALL = 0xFA
REVERT = 0xFD
INVALID = 0xFE
SELFDESTRUCT = 0xFF
