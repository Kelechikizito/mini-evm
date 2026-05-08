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


def lt(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(1 if a < b else 0)
    evm.pc += 1
    evm.gas_dec(3)


def slt(evm):  # signed less than
    a, b = evm.stack.pop(), evm.stack.pop()
    a = unsigned_to_signed(a)
    b = unsigned_to_signed(b)
    evm.stack.push(1 if a < b else 0)
    evm.pc += 1
    evm.gas_dec(3)


def gt(evm):  # greater than
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(1 if a > b else 0)
    evm.pc += 1
    evm.gas_dec(3)


def sgt(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    a = unsigned_to_signed(a)
    b = unsigned_to_signed(b)
    evm.stack.push(1 if a > b else 0)
    evm.pc += 1
    evm.gas_dec(3)


def eq(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(1 if a == b else 0)
    evm.pc += 1
    evm.gas_dec(3)


def iszero(evm):
    a = evm.stack.pop()
    evm.stack.push(1 if a == 0 else 0)
    evm.pc += 1
    evm.gas_dec(3)


# LOGIC
AND = 0x16
OR = 0x17
XOR = 0x18
NOT = 0x19


def _and(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a & b)
    evm.pc += 1
    evm.gas_dec(3)


def _or(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a | b)
    evm.pc += 1
    evm.gas_dec(3)


def _xor(evm):
    a, b = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(a ^ b)
    evm.pc += 1
    evm.gas_dec(3)


def _not(evm):
    a = evm.stack.pop()
    evm.stack.push(~a)
    evm.pc += 1
    evm.gas_dec(3)


# BIT OPERATIONS
BYTE = 0x1A
SHL = 0x1B
SHR = 0x1C
SAR = 0x1D

# Get one byte from a word (32 bytes)


def byte(evm):
    i, x = evm.stack.pop(), evm.stack.pop()
    if i >= 32:
        result = 0
    else:
        result = (x // pow(256, 31 - i)) % 256
    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)


def shl(evm):
    shift, value = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(value << shift)
    evm.pc += 1
    evm.gas_dec(3)


def shr(evm):
    shift, value = evm.stack.pop(), evm.stack.pop()
    evm.stack.push(value >> shift)
    evm.pc += 1
    evm.gas_dec(3)


def sar(evm):
    shift, value = evm.stack.pop(), evm.stack.pop()

    if shift >= 256:
        # If shifting all bits: result = 0 (for positive) or -1 (for negative)
        result = 0 if (value >> 255) == 0 else UINT_255_NEGATIVE_ONE
    else:
        # interpret as signed 256-bit integer
        if value & (1 << 255):
            signed_value = value - (1 << 256)
        else:
            signed_value = value

        shifted = signed_value >> shift
        result = shifted & UINT_256_MAX

    evm.stack.push(result)
    evm.pc += 1
    evm.gas_dec(3)


# MISCELLANEOUS
SHA3 = 0x20


def sha3(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    value = evm.memory.access(offset, size)
    evm.stack.push(hash(str(value)))

    evm.pc += 1

    # calculate gas
    minimum_word_size = (size + 31) / 32
    dynamic_gas = 6 * minimum_word_size  # TODO: + memory_expansion_cost
    evm.gas_dec(30 + dynamic_gas)


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


# Returns the address of the account currently executing this program
def address(evm):
    evm.stack.push(evm.sender)
    evm.pc += 1
    evm.gas_dec(2)


def balance(evm):
    address = evm.stack.pop()
    evm.stack.push(99999999999)

    evm.pc += 1
    evm.gas_dec(2600)  # 100 if warm


def origin(evm):
    evm.stack.push(evm.sender)
    evm.pc += 1
    evm.gas_dec(2)


def caller(evm):
    evm.stack.push("0x414b60745072088d013721b4a28a0559b1A9d213")
    evm.pc += 1
    evm.gas_dec(2)


def callvalue(evm):
    evm.stack.push(evm.value)
    evm.pc += 1
    evm.gas_dec(2)


def calldataload(evm):
    i = evm.stack.pop()

    delta = 0
    if i + 32 > len(evm.calldata):
        delta = i + 32 - len(evm.calldata)

    # always has to be 32 bytes
    # if its not we append 0x00 bytes until it is
    calldata = evm.calldata[i : i + 32 - delta]
    calldata += 0x00 * delta

    evm.stack.push(calldata)
    evm.pc += 1
    evm.gas_dec(3)


def calldatasize(evm):
    evm.stack.push(len(evm.calldata))
    evm.pc += 1
    evm.gas_dec(2)


def calldatacopy(evm):
    destOffset = evm.stack.pop()
    offset = evm.stack.pop()
    size = evm.stack.pop()

    calldata = evm.calldata[offset : offset + size]
    memory_expansion_cost = evm.memory.store(destOffset, calldata)

    static_gas = 3
    minimum_word_size = (size + 31) // 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost

    evm.gas_dec(static_gas + dynamic_gas)
    evm.pc += 1


def codesize(evm):
    evm.stack.push(len(evm.program))
    evm.pc += 1
    evm.gas_dec(2)


def codecopy(evm):
    destOffset = evm.stack.pop()
    offset = evm.stack.pop()
    size = evm.stack.pop()

    code = evm.program[offset : offset + size]
    memory_expansion_cost = evm.memory.store(destOffset, code)

    static_gas = 3
    minimum_word_size = (size + 31) / 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost

    evm.gas_dec(static_gas + dynamic_gas)
    evm.pc += 1


def gasprice(evm):
    evm.stack.push(0x00)
    evm.pc += 1
    evm.gas_dec(2)


def extcodesize(evm):
    address = evm.stack.pop()
    evm.stack.push(0x00)
    evm.gas_dec(2600)  # 100 if warm
    evm.pc += 1


def extcodecopy(evm):
    address = evm.stack.pop()
    destOffset = evm.stack.pop()
    offset = evm.stack.pop()
    size = evm.stack.pop()

    extcode = []  # no external code
    memory_expansion_cost = evm.memory.store(destOffset, extcode)

    # refactor this in seperate method
    minimum_word_size = (size + 31) / 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost
    address_access_cost = 100 if warm else 2600

    evm.gas_dec(dynamic_gas + address_access_cost)
    evm.pc += 1


def returndatasize(evm):
    evm.stack.push(0x00)  # no return data
    evm.pc += 1
    evm.gas_dec(2)


def returndatacopy(evm):
    destOffset = evm.stack.pop()
    offset = evm.stack.pop()
    size = evm.stack.pop()

    returndata = evm.program[offset : offset + size]
    memory_expansion_cost = evm.memory.store(destOffset, returndata)

    minimum_word_size = (size + 31) / 32
    dynamic_gas = 3 * minimum_word_size + memory_expansion_cost

    evm.gas_dec(3 + dynamic_gas)
    evm.pc += 1


def extcodehash(evm):
    address = evm.stack.pop()
    evm.stack.push(0x00)  # no code

    evm.gas_dec(2600)  # 100 if warm
    evm.pc += 1


def blockhash(evm):
    blockNumber = evm.stack.pop()
    if blockNumber > 256:
        raise Exception("Only last 256 blocks can be accessed")
    evm.stack.push(0x1CBCFA1FFB1CA1CA8397D4F490194DB5FC0543089B9DEE43F76CF3F962A185E8)
    evm.pc += 1
    evm.gas_dec(20)


def coinbase(evm):
    evm.stack.push("0x5B38Da6a701c568545dCfcB03FcB875f56beddC4")
    evm.pc += 1
    evm.gas_dec(2)


import time


def timestamp(evm):
    now = int(time.time())
    now -= now % 12
    evm.stack.push(now)
    evm.pc += 1
    evm.gas_dec(2)


import random


def prevrandao(evm):
    # Should be from the previous block's mixHash, such as:
    # prevMixHash = prevBlock.mixHash
    # prevMixHash = 0xaeaec252beafe3fd35a11bdc5e3c71925f2e9e01472b7a2a290dc4619f645206
    # here we use random int
    prevMixHash = random.randint(0, 2**256 - 1)
    return prevMixHash


# POP
POP = 0x50


# Pops the first element from the stack
def pop(evm):
    evm.pc += 1
    evm.gas_dec(2)
    evm.stack.pop(0)


# MEMORY
MLOAD = 0x51
MSTORE = 0x52
MSTORE8 = 0x53


# MLOAD lets us load one word (32 bytes) from memory specified by an offset. It puts that word on top of the stack.
def mload(evm):
    offset = evm.stack.pop()
    value = evm.memory.load(offset)
    evm.stack.push(value)
    evm.pc += 1


# MSTORE allows us to save one word to memory and MSTORE8 allows us to save one byte to memory.
def mstore(evm):
    offset = evm.stack.pop()
    value = evm.stack.pop()
    evm.memory.store(offset, value)
    evm.pc += 1


def mstore8(evm):
    offset = evm.stack.pop()
    value = evm.stack.pop()
    evm.memory.store(offset, value)
    evm.pc += 1


# STORAGE
SLOAD = 0x54
SSTORE = 0x55


def sload(evm):
    key = evm.stack.pop().value
    warm, value = evm.storage.load(key)
    evm.stack.push(value)

    evm.gas_dec(2100)  # 100 if warm
    evm.pc += 1


def sstore(evm):
    key, value = evm.stack.pop(), evm.stack.pop()
    warm, old_value = evm.storage.store(key, value)

    base_dynamic_gas = 0

    if value != old_value:
        if old_value == 0:
            base_dynamic_gas = 20000
        else:
            base_dynamic_gas = 2900

    access_cost = 100 if warm else 2100
    evm.gas_dec(base_dynamic_gas + access_cost)

    evm.pc += 1

    # TODO: do refunds


# JUMP
JUMP = 0x56
JUMPI = 0x57
PC = 0x58
JUMPDEST = 0x5B


def jump(evm):
    counter = evm.stack.pop()

    # make sure that we jump to an JUMPDEST opcode
    if not evm.program[counter] == JUMPDEST:
        raise Exception("Can only jump to JUMPDEST")

    evm.pc = counter
    evm.gas_dec(8)


def jumpi(evm):
    counter, b = evm.stack.pop(), evm.stack.pop()

    if b != 0:
        evm.pc = counter
    else:
        evm.pc += 1

    evm.gas_dec(10)


def pc(evm):
    evm.stack.push(evm.pc)
    evm.pc += 1
    evm.gas_dec(2)


def jumpdest(evm):
    evm.pc += 1
    evm.gas_dec(1)


# TRANSIENT STORAGE
TLOAD = 0x5C
TSTORE = 0x5D


# These opcodes behave almost identically to storage but changes are discarded after every transaction.
def tload(evm):
    key = evm.stack.pop().value
    warm, value = evm.storage.load(key)
    evm.stack.push(value)

    evm.gas_dec(100)
    evm.pc += 1


def tstore(evm):
    key, value = evm.stack.pop(), evm.stack.pop()
    evm.storage.store(key, value)
    evm.gas_dec(100)
    evm.pc += 1


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


def _push(evm, n):
    evm.pc += 1
    evm.gas_dec(3)

    value = []
    for _ in range(n):
        value.append(evm.peek())
        evm.pc += 1
    evm.stack.push(int("".join(map(str, value))))


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


# This duplicates a stack item by putting it on top of the stack
def _dup(evm, n):
    # make sure stack is big enough!
    value = evm.stack[n]
    evm.stack.push(value)

    evm.pc += 1
    evm.gas_dec(3)


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


def _swap(evm, n):
    value1, value2 = evm.stack.get(0), evm.stack.get(n + 1)
    evm.stack.set(0, value2)
    evm.stack.set(n + 1, value1)

    evm.pc += 1
    evm.gas_dec(3)


# LOG
LOG0 = 0xA0
LOG1 = 0xA1
LOG2 = 0xA2
LOG3 = 0xA3
LOG4 = 0xA4


class Log:
    def __init__(self, data, topic1=None, topic2=None, topic3=None, topic4=None):

        self.data = data
        self.topic1 = topic1
        self.topic2 = topic2
        self.topic3 = topic3
        self.topic4 = topic4

    def __str__(self):
        return f"Log: {self.data}"


def calc_gas(topic_count, size, memory_expansion_cost=0):
    # 375 := static_gas
    return 375 * topic_count + 8 * size + memory_expansion_cost


def log0(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()

    data = evm.memory.access(offset, size)
    log = Log(data)
    evm.append_log(log)

    evm.pc += 1
    evm.gas_dec(calc_gas(0, size))  # TODO: memory expansion cost


def log1(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    topic = evm.stack.pop().value

    data = evm.memory.access(offset, size)
    log = Log(data, topic)
    evm.append_log(log)

    evm.pc += 1
    evm.gas_dec(calc_gas(1, size))  # TODO: memory expansion cost


def log2(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    topic1, topic2 = evm.stack.pop(), evm.stack.pop()

    data = evm.memory.access(offset, size)
    log = Log(data, topic1, topic2)
    evm.append_log(log)

    evm.pc += 1
    evm.gas_dec(calc_gas(2, size))  # TODO: memory expansion cost


def log3(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    topic1 = evm.stack.pop()
    topic2 = evm.stack.pop()
    topic3 = evm.stack.pop()

    data = evm.memory.access(offset, size)
    log = Log(data, topic1, topic2, topic3)
    evm.append_log(log)

    evm.pc += 1
    evm.gas_dec(calc_gas(3, size))  # TODO: memory expansion cost


def log4(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    topic1 = evm.stack.pop()
    topic2 = evm.stack.pop()
    topic3 = evm.stack.pop()
    topic4 = evm.stack.pop()

    data = evm.memory.access(offset, size)
    log = Log(data, topic1, topic2, topic3, topic4)
    evm.append_log(log)

    evm.pc += 1
    evm.gas_dec(calc_gas(4, size))  # TODO: memory expansion cost


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


def revert(evm):
    offset, size = evm.stack.pop(), evm.stack.pop()
    evm.returndata = evm.memory.access(offset, size)

    evm.stop_flag = True
    evm.revert_flag = True
    evm.pc += 1
    evm.gas_dec(0)
