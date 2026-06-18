from enum import IntEnum

COMMAND_MEMORY_SIZE = 1 << 16
DATA_MEMORY_SIZE = 1 << 16

WORD_BITS = 32
WORD_BYTES = WORD_BITS // 8
WORD_MASK = (1 << WORD_BITS) - 1

FORMAT_OP = "op"
FORMAT_U16 = "u16"
FORMAT_I16 = "i16"
FORMAT_I32 = "i32"
FORMAT_PUSHN = "pushn"


class Opcode(IntEnum):
    HALT = 0x00
    ADD = 0x01
    SUB = 0x02
    MUL = 0x03
    DIV = 0x04
    MOD = 0x05
    EQ = 0x06
    LT = 0x07
    GT = 0x08
    MOV_TOS_NOS = 0x09
    MOV_NOS_TOS = 0x0A
    MOV_TOS_TMP = 0x0B
    MOV_TMP_TOS = 0x0C
    MOV_TMP_NOS = 0x0D
    MOV_NOS_TMP = 0x0E
    MOV_TOS_MDR = 0x0F
    MOV_NOS_MDR = 0x10
    SP_INC = 0x11
    SP_DEC = 0x12
    RP_INC = 0x13
    RP_DEC = 0x14
    LOAD = 0x15
    LOAD_SP = 0x16
    LOAD_SP_M1 = 0x17
    LOAD_RP = 0x18
    STORE = 0x19
    STORE_SP_TOS = 0x1A
    STORE_SP_M1_TOS = 0x1B
    STORE_SP_M1_NOS = 0x1C
    STORE_RP_TOS = 0x1D
    EI = 0x1E
    DI = 0x1F
    IRET = 0x20
    GET_CARRY = 0x21
    CALLXT = 0x22
    RET = 0x23
    LOADA = 0x24
    STOREA = 0x25
    ADDM = 0x26
    JMP = 0x27
    JZ = 0x28
    CALL = 0x29
    LDI = 0x2A
    PUSHN = 0x2B

    @property
    def mnemonic(self):
        return self.name

    @classmethod
    def from_mnemonic(cls, mnemonic):
        normalized = mnemonic.replace("-", "_").upper()
        try:
            return cls[normalized]
        except KeyError as exc:
            raise ValueError(f"unknown opcode mnemonic: {mnemonic}") from exc


opcode_to_format = {
    Opcode.HALT: FORMAT_OP,
    Opcode.ADD: FORMAT_OP,
    Opcode.SUB: FORMAT_OP,
    Opcode.MUL: FORMAT_OP,
    Opcode.DIV: FORMAT_OP,
    Opcode.MOD: FORMAT_OP,
    Opcode.EQ: FORMAT_OP,
    Opcode.LT: FORMAT_OP,
    Opcode.GT: FORMAT_OP,
    Opcode.MOV_TOS_NOS: FORMAT_OP,
    Opcode.MOV_NOS_TOS: FORMAT_OP,
    Opcode.MOV_TOS_TMP: FORMAT_OP,
    Opcode.MOV_TMP_TOS: FORMAT_OP,
    Opcode.MOV_TMP_NOS: FORMAT_OP,
    Opcode.MOV_NOS_TMP: FORMAT_OP,
    Opcode.MOV_TOS_MDR: FORMAT_OP,
    Opcode.MOV_NOS_MDR: FORMAT_OP,
    Opcode.SP_INC: FORMAT_OP,
    Opcode.SP_DEC: FORMAT_OP,
    Opcode.RP_INC: FORMAT_OP,
    Opcode.RP_DEC: FORMAT_OP,
    Opcode.LOAD: FORMAT_OP,
    Opcode.LOAD_SP: FORMAT_OP,
    Opcode.LOAD_SP_M1: FORMAT_OP,
    Opcode.LOAD_RP: FORMAT_OP,
    Opcode.STORE: FORMAT_OP,
    Opcode.STORE_SP_TOS: FORMAT_OP,
    Opcode.STORE_SP_M1_TOS: FORMAT_OP,
    Opcode.STORE_SP_M1_NOS: FORMAT_OP,
    Opcode.STORE_RP_TOS: FORMAT_OP,
    Opcode.EI: FORMAT_OP,
    Opcode.DI: FORMAT_OP,
    Opcode.IRET: FORMAT_OP,
    Opcode.GET_CARRY: FORMAT_OP,
    Opcode.CALLXT: FORMAT_OP,
    Opcode.RET: FORMAT_OP,
    Opcode.LOADA: FORMAT_U16,
    Opcode.STOREA: FORMAT_U16,
    Opcode.ADDM: FORMAT_U16,
    Opcode.JMP: FORMAT_I16,
    Opcode.JZ: FORMAT_I16,
    Opcode.CALL: FORMAT_I16,
    Opcode.LDI: FORMAT_I32,
    Opcode.PUSHN: FORMAT_PUSHN,
}

opcode_to_binary = {opcode: int(opcode) for opcode in Opcode}
binary_to_opcode = {int(opcode): opcode for opcode in Opcode}


def _normalize_opcode(opcode):
    if isinstance(opcode, Opcode):
        return opcode
    if isinstance(opcode, str):
        return Opcode.from_mnemonic(opcode)
    return Opcode(opcode)


def instruction_format(opcode):
    return opcode_to_format[_normalize_opcode(opcode)]


def op(opcode):
    return _instruction(opcode)


def u16(opcode, arg):
    return _instruction(opcode, arg=arg)


def i16(opcode, arg):
    return _instruction(opcode, arg=arg)


def i32(opcode, arg):
    return _instruction(opcode, arg=arg)


def pushn(values):
    return _instruction(Opcode.PUSHN, values=tuple(values))


def _instruction(opcode, arg=None, values=()):
    instruction = {"opcode": _normalize_opcode(opcode)}
    if arg is not None:
        instruction["arg"] = arg
    if values:
        instruction["values"] = tuple(values)
    return instruction


def instruction_size(instruction):
    fmt = instruction_format(instruction["opcode"])
    if fmt == FORMAT_OP:
        return 1
    if fmt in (FORMAT_U16, FORMAT_I16):
        return 3
    if fmt == FORMAT_I32:
        return 5
    if fmt == FORMAT_PUSHN:
        return 2 + WORD_BYTES * len(instruction.get("values", ()))
    raise ValueError(f"unsupported instruction format: {fmt}")


def word_to_unsigned(value):
    return value & WORD_MASK


def word_to_signed(value):
    unsigned = value & WORD_MASK
    if unsigned > WORD_MASK >> 1:
        return unsigned - (1 << WORD_BITS)
    return unsigned


def encode_u16(value):
    return (value & 0xFFFF).to_bytes(2, byteorder="big", signed=False)


def decode_u16(payload):
    if len(payload) != 2:
        raise ValueError(f"uint16 payload must contain 2 bytes, got {len(payload)}")
    return int.from_bytes(payload, byteorder="big", signed=False)


def encode_i16(value):
    return (value & 0xFFFF).to_bytes(2, byteorder="big", signed=False)


def decode_i16(payload):
    if len(payload) != 2:
        raise ValueError(f"int16 payload must contain 2 bytes, got {len(payload)}")
    return int.from_bytes(payload, byteorder="big", signed=True)


def encode_i32(value):
    return word_to_unsigned(value).to_bytes(WORD_BYTES, byteorder="big", signed=False)


def decode_i32(payload):
    if len(payload) != WORD_BYTES:
        raise ValueError(f"int32 payload must contain {WORD_BYTES} bytes, got {len(payload)}")
    return word_to_signed(int.from_bytes(payload, byteorder="big", signed=False))


def encode_word(value):
    return encode_i32(value)


def decode_word(payload):
    return decode_i32(payload)


def encode_instruction(instruction):
    opcode = _normalize_opcode(instruction["opcode"])
    fmt = instruction_format(opcode)
    encoded = bytearray([opcode_to_binary[opcode]])

    if fmt == FORMAT_OP:
        return bytes(encoded)
    if fmt == FORMAT_U16:
        encoded.extend(encode_u16(instruction["arg"]))
        return bytes(encoded)
    if fmt == FORMAT_I16:
        encoded.extend(encode_i16(instruction["arg"]))
        return bytes(encoded)
    if fmt == FORMAT_I32:
        encoded.extend(encode_i32(instruction["arg"]))
        return bytes(encoded)
    if fmt == FORMAT_PUSHN:
        values = instruction.get("values", ())
        encoded.append(len(values))
        for value in values:
            encoded.extend(encode_i32(value))
        return bytes(encoded)
    raise ValueError(f"unsupported instruction format: {fmt}")


def decode_instruction(code, address=0):
    if not 0 <= address < len(code):
        raise ValueError(f"instruction address is outside code: {address}")

    opcode_byte = code[address]
    try:
        opcode = binary_to_opcode[opcode_byte]
    except KeyError as exc:
        raise ValueError(f"unknown opcode 0x{opcode_byte:02X} at address {address}") from exc

    fmt = instruction_format(opcode)
    if fmt == FORMAT_OP:
        return op(opcode)
    if fmt == FORMAT_U16:
        end = address + 3
        _ensure_available(code, address, end)
        return u16(opcode, decode_u16(code[address + 1 : end]))
    if fmt == FORMAT_I16:
        end = address + 3
        _ensure_available(code, address, end)
        return i16(opcode, decode_i16(code[address + 1 : end]))
    if fmt == FORMAT_I32:
        end = address + 5
        _ensure_available(code, address, end)
        return i32(opcode, decode_i32(code[address + 1 : end]))
    if fmt == FORMAT_PUSHN:
        count_end = address + 2
        _ensure_available(code, address, count_end)
        count = code[address + 1]
        end = count_end + WORD_BYTES * count
        _ensure_available(code, address, end)
        values = tuple(decode_i32(code[offset : offset + WORD_BYTES]) for offset in range(count_end, end, WORD_BYTES))
        return pushn(values)
    raise ValueError(f"unsupported instruction format: {fmt}")


def _ensure_available(code, address, end):
    if len(code) < end:
        raise ValueError(
            f"truncated instruction at address {address}: need {end - address} bytes, have {len(code) - address}"
        )


def to_bytes(code):
    binary = bytearray()
    for instruction in code:
        binary.extend(encode_instruction(instruction))
    return bytes(binary)


def from_bytes(binary_code):
    code = []
    address = 0
    while address < len(binary_code):
        instruction = decode_instruction(binary_code, address)
        code.append(instruction)
        address += instruction_size(instruction)
    return code


def instruction_addresses(code, start=0):
    address = start
    addresses = []
    for instruction in code:
        addresses.append(address)
        address += instruction_size(instruction)
    return addresses


def code_size(code):
    return sum(instruction_size(instruction) for instruction in code)


def relative_offset(source_address, instruction_size, target_address):
    return target_address - (source_address + instruction_size)


def instruction_to_hex(instruction):
    return encode_instruction(instruction).hex().upper()


def instruction_to_mnemonic(instruction):
    opcode = _normalize_opcode(instruction["opcode"])
    fmt = instruction_format(opcode)

    if fmt == FORMAT_PUSHN:
        values = " ".join(str(value) for value in instruction.get("values", ()))
        return f"{opcode.mnemonic} {values}".rstrip()
    if "arg" not in instruction:
        return opcode.mnemonic
    if fmt == FORMAT_U16:
        return f"{opcode.mnemonic} 0x{instruction['arg']:04X}"
    return f"{opcode.mnemonic} {instruction['arg']}"


def to_hex(code):
    lines = []
    address = 0
    for instruction in code:
        lines.append(f"{address} - {instruction_to_hex(instruction)} - {instruction_to_mnemonic(instruction)}")
        address += instruction_size(instruction)
    return "\n".join(lines)


def data_to_bytes(words):
    binary = bytearray()
    for word in words:
        binary.extend(encode_word(word))
    return bytes(binary)


def data_from_bytes(payload):
    if len(payload) % WORD_BYTES != 0:
        raise ValueError(f"data memory payload size must be a multiple of {WORD_BYTES}, got {len(payload)}")
    return [decode_word(payload[offset : offset + WORD_BYTES]) for offset in range(0, len(payload), WORD_BYTES)]


def data_to_hex(words, start=0):
    lines = []
    for offset, word in enumerate(words):
        address = start + offset
        encoded = encode_word(word).hex().upper()
        lines.append(f"{address} - {encoded} - {word}")
    return "\n".join(lines)
