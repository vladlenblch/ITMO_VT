import os
import sys

import isa
from isa import Opcode

DATA_STACK_BASE = 0xD000
DATA_STACK_LIMIT = 0xDFFF
RETURN_STACK_BASE = 0xE000
RETURN_STACK_LIMIT = 0xEFFF

INPUT_CHAR_ADDR = 0xFF00
OUTPUT_CHAR_ADDR = 0xFF02

FETCH_OPCODE = "FETCH_OPCODE"
FETCH_ARGUMENT = "FETCH_ARGUMENT"
EXECUTE = "EXECUTE"
MEM_READ = "MEM_READ"
WRITEBACK = "WRITEBACK"
MEMORY_ALU = "MEMORY_ALU"
CALL_ENTER = "CALL_ENTER"
CALLXT_LOAD_TOS = "CALLXT_LOAD_TOS"
CALLXT_LATCH_TOS = "CALLXT_LATCH_TOS"
CALLXT_LOAD_NOS = "CALLXT_LOAD_NOS"
CALLXT_LATCH_NOS = "CALLXT_LATCH_NOS"
INTERRUPT_ENTER = "INTERRUPT_ENTER"
FETCH_PUSHN_VALUE = "FETCH_PUSHN_VALUE"
PREPARE_PUSHN_NOS = "PREPARE_PUSHN_NOS"
PREPARE_PUSHN_SP = "PREPARE_PUSHN_SP"
WRITE_PUSHN_VALUE = "WRITE_PUSHN_VALUE"
INTERRUPT = "INTERRUPT"


class MachineError(Exception):
    pass


class DataPath:
    def __init__(self, data_words=None):
        self.data_memory = [0] * isa.DATA_MEMORY_SIZE
        if data_words is not None:
            for address, word in enumerate(data_words):
                if address >= len(self.data_memory):
                    raise MachineError("data memory image is too large")
                self.data_memory[address] = isa.word_to_signed(word)

        self.output_buffer = []
        self.input_char = 0
        self.input_ready = False

        self.tos = 0
        self.nos = 0
        self.sp = DATA_STACK_BASE - 1
        self.rp = RETURN_STACK_BASE - 1
        self.tmp = 0
        self.mdr = 0
        self.interrupt_safe = True

        self.flags = {"Z": 0, "N": 0, "C": 0, "V": 0, "IE": 0, "INT": 0}

    def signal_input_char(self, char):
        if isinstance(char, int):
            self.input_char = char & 0xFF
        else:
            self.input_char = ord(char[0]) if char else 0
        self.input_ready = True

    def signal_mem_read(self, address):
        address &= 0xFFFF
        if address == INPUT_CHAR_ADDR:
            value = self.input_char if self.input_ready else 0
            self.input_ready = False
        else:
            value = self.data_memory[address]
        self.signal_latch_special("mdr", value)

    def signal_mem_write(self, address, value):
        address &= 0xFFFF
        value = isa.word_to_signed(value)
        if address == OUTPUT_CHAR_ADDR:
            self.output_buffer.append(chr(value & 0xFF))
        else:
            self.data_memory[address] = value

    def signal_latch_special(self, register, value):
        setattr(self, register, isa.word_to_signed(value))
        self.interrupt_safe = False

    def signal_move(self, target, source):
        value = getattr(self, source)
        self.signal_latch_special(target, value)
        if target == "nos" and source == "mdr":
            self.interrupt_safe = True

    def signal_step(self, register, delta):
        value = getattr(self, register)
        if register == "sp":
            if delta > 0 and value >= DATA_STACK_LIMIT:
                raise MachineError("data stack overflow")
            if delta < 0 and value < DATA_STACK_BASE:
                raise MachineError("data stack underflow")
        if register == "rp":
            if delta > 0 and value >= RETURN_STACK_LIMIT:
                raise MachineError("return stack overflow")
            if delta < 0 and value < RETURN_STACK_BASE:
                raise MachineError("return stack underflow")
        alu_op = Opcode.ADD if delta > 0 else Opcode.SUB
        result, _, _ = self.signal_alu(alu_op, value, 1)
        self.signal_latch_special(register, result)

    def signal_store_sp(self, value):
        self.signal_mem_write(self.sp, value)
        self.interrupt_safe = True

    def signal_latch_flags(self, result=None, carry=0, overflow=0, flags_ctrl="ALU_FLAGS"):
        if flags_ctrl == "ALU_FLAGS":
            result = isa.word_to_signed(result)
            self.flags["Z"] = 1 if result == 0 else 0
            self.flags["N"] = 1 if result < 0 else 0
            self.flags["C"] = 1 if carry else 0
            self.flags["V"] = 1 if overflow else 0
            return
        if flags_ctrl == "SET_IE":
            self.flags["IE"] = 1
            return
        if flags_ctrl == "CLEAR_IE":
            self.flags["IE"] = 0
            return
        if flags_ctrl == "CLEAR_INT":
            self.flags["INT"] = 0
            return
        if flags_ctrl == "SET_INT":
            self.flags["INT"] = 1
            return
        raise MachineError(f"unsupported flags_ctrl: {flags_ctrl}")

    def signal_binary_alu(self, alu_op):
        result, carry, overflow = self.signal_alu(alu_op, self.nos, self.tos)
        self.signal_latch_special("tos", result)
        self.signal_latch_flags(result, carry, overflow)

    def signal_memory_alu(self, alu_op):
        result, carry, overflow = self.signal_alu(alu_op, self.tos, self.mdr)
        self.signal_latch_special("tos", result)
        self.signal_latch_flags(result, carry, overflow)

    def signal_alu(self, alu_op, a, b):
        carry = 0
        overflow = 0

        if alu_op is Opcode.ADD:
            unsigned = (a & isa.WORD_MASK) + (b & isa.WORD_MASK)
            result = isa.word_to_signed(unsigned)
            carry = unsigned > isa.WORD_MASK
            overflow = (a >= 0 and b >= 0 and result < 0) or (a < 0 and b < 0 and result >= 0)
        elif alu_op is Opcode.SUB:
            unsigned = (a & isa.WORD_MASK) - (b & isa.WORD_MASK)
            result = isa.word_to_signed(unsigned)
            carry = unsigned < 0
            overflow = (a >= 0 and b < 0 and result < 0) or (a < 0 and b >= 0 and result >= 0)
        elif alu_op is Opcode.MUL:
            result = isa.word_to_signed(a * b)
        elif alu_op is Opcode.DIV:
            result = self._truncate_division(a, b)
        elif alu_op is Opcode.MOD:
            quotient = self._truncate_division(a, b)
            result = a - quotient * b
        elif alu_op is Opcode.EQ:
            result = 1 if a == b else 0
        elif alu_op is Opcode.LT:
            result = 1 if a < b else 0
        elif alu_op is Opcode.GT:
            result = 1 if a > b else 0
        else:
            raise MachineError(f"unsupported ALU op: {alu_op.mnemonic}")

        return isa.word_to_signed(result), carry, overflow

    def _truncate_division(self, a, b):
        if b == 0:
            raise MachineError("division by zero")
        quotient = abs(a) // abs(b)
        return -quotient if (a < 0) != (b < 0) else quotient

    def data_stack(self):
        if self.sp < DATA_STACK_BASE:
            return []
        return list(self.data_memory[DATA_STACK_BASE : self.sp + 1])

    def return_stack(self):
        if self.rp < RETURN_STACK_BASE:
            return []
        return list(self.data_memory[RETURN_STACK_BASE : self.rp + 1])


class ControlUnit:
    def __init__(self, command_memory, data_path, interrupt_vector=None, input_schedule=None):
        self.command_memory = self._load_command_memory(command_memory)
        self.data_path = data_path
        self.interrupt_vector = interrupt_vector
        self.input_schedule = sorted(input_schedule or [], key=lambda item: item[0])

        self.pc = 0
        self.ir = None
        self.arg = 0
        self.current_instruction = None
        self.fetch_address = 0

        self.state = FETCH_OPCODE
        self._tick = 0
        self.halted = False
        self.log = []
        self.pushn_remaining = 0

    def _load_command_memory(self, command_memory):
        payload = bytes(command_memory)
        if len(payload) > isa.COMMAND_MEMORY_SIZE:
            raise MachineError("command memory image is too large")
        return payload + bytes(isa.COMMAND_MEMORY_SIZE - len(payload))

    def current_tick(self):
        return self._tick

    def tick(self, stage, detail=""):
        self._tick += 1
        self.log.append(self.format_state(stage, detail))

    def process_next_tick(self):
        if self.halted:
            raise StopIteration()

        self.deliver_input_tokens()

        if self.state == FETCH_OPCODE and self.interrupt_requested():
            self.data_path.signal_step("rp", 1)
            self.data_path.signal_latch_flags(flags_ctrl="SET_INT")
            self.state = INTERRUPT_ENTER
            self.tick("INTERRUPT_PREPARE", f"rp={self.data_path.rp:04X}")
            return

        if self.state == INTERRUPT_ENTER:
            if self.interrupt_vector is None:
                raise MachineError("input interrupt requested but no interrupt vector configured")
            self.data_path.signal_mem_write(self.data_path.rp, self.pc)
            self.signal_latch_pc(self.interrupt_vector)
            self.data_path.interrupt_safe = True
            self.state = FETCH_OPCODE
            self.tick(INTERRUPT, f"vector={self.interrupt_vector}")
            return

        if self.state == FETCH_OPCODE:
            self.fetch_address = self.pc
            self.signal_latch_ir()
            self.state = EXECUTE if isa.instruction_format(self.ir) == isa.FORMAT_OP else FETCH_ARGUMENT
            self.tick(FETCH_OPCODE, f"instr_addr={self.fetch_address}")
            return

        if self.state == FETCH_ARGUMENT:
            self.signal_latch_arg()
            self.state = EXECUTE
            self.tick(FETCH_ARGUMENT, self.current_instruction_mnemonic())
            return

        if self.state == MEM_READ:
            self.signal_mem_read_stage()
            return

        if self.state == WRITEBACK:
            self.signal_writeback_stage()
            return

        if self.state == MEMORY_ALU:
            self.data_path.signal_memory_alu(Opcode.ADD)
            self.signal_finish_execute()
            self.tick(EXECUTE, Opcode.ADDM.mnemonic)
            return

        if self.state == CALL_ENTER:
            self.signal_call_enter()
            return

        if self.state == CALLXT_LOAD_TOS:
            self.data_path.signal_mem_read(self.data_path.sp)
            self.state = CALLXT_LATCH_TOS
            self.tick(CALLXT_LOAD_TOS, f"addr={self.data_path.sp & 0xFFFF:04X}")
            return

        if self.state == CALLXT_LATCH_TOS:
            self.data_path.signal_move("tos", "mdr")
            self.state = CALLXT_LOAD_NOS
            self.tick(CALLXT_LATCH_TOS)
            return

        if self.state == CALLXT_LOAD_NOS:
            self.data_path.signal_mem_read(self.data_path.sp - 1)
            self.state = CALLXT_LATCH_NOS
            self.tick(CALLXT_LOAD_NOS, f"addr={(self.data_path.sp - 1) & 0xFFFF:04X}")
            return

        if self.state == CALLXT_LATCH_NOS:
            self.data_path.signal_move("nos", "mdr")
            self.signal_finish_execute()
            self.tick(CALLXT_LATCH_NOS)
            return

        if self.state == FETCH_PUSHN_VALUE:
            self.arg = isa.decode_i32(self.read_command_bytes(isa.WORD_BYTES))
            self.state = PREPARE_PUSHN_NOS
            self.tick(FETCH_PUSHN_VALUE, f"value={self.arg}")
            return

        if self.state == PREPARE_PUSHN_NOS:
            self.data_path.signal_move("nos", "tos")
            self.state = PREPARE_PUSHN_SP
            self.tick(PREPARE_PUSHN_NOS)
            return

        if self.state == PREPARE_PUSHN_SP:
            self.data_path.signal_step("sp", 1)
            self.state = WRITE_PUSHN_VALUE
            self.tick(PREPARE_PUSHN_SP, f"sp={self.data_path.sp:04X}")
            return

        if self.state == WRITE_PUSHN_VALUE:
            self.data_path.signal_latch_special("tos", self.arg)
            self.data_path.signal_store_sp(self.arg)
            self.pushn_remaining -= 1
            self.state = FETCH_OPCODE if self.pushn_remaining == 0 else FETCH_PUSHN_VALUE
            self.tick(WRITE_PUSHN_VALUE, f"value={self.data_path.tos}")
            return

        if self.state == EXECUTE:
            self.decode_and_execute()
            return

        raise MachineError(f"unknown control state: {self.state}")

    def deliver_input_tokens(self):
        next_tick = self._tick + 1
        while self.input_schedule and self.input_schedule[0][0] <= next_tick:
            _, char = self.input_schedule.pop(0)
            if self.data_path.input_ready:
                raise MachineError("input register overrun")
            self.data_path.signal_input_char(char)

    def interrupt_requested(self):
        flags = self.data_path.flags
        return flags["IE"] == 1 and flags["INT"] == 0 and self.data_path.input_ready and self.data_path.interrupt_safe

    def signal_latch_ir(self):
        opcode_byte = self.command_memory[self.pc]
        try:
            self.ir = isa.binary_to_opcode[opcode_byte]
        except KeyError as exc:
            raise MachineError(f"unknown opcode 0x{opcode_byte:02X} at address {self.pc}") from exc

        self.arg = 0
        self.current_instruction = isa.op(self.ir)
        self.signal_latch_pc(step=1)

    def signal_latch_arg(self):
        fmt = isa.instruction_format(self.ir)
        if fmt == isa.FORMAT_U16:
            self.arg = isa.decode_u16(self.read_command_bytes(2))
            self.current_instruction = isa.u16(self.ir, self.arg)
            return
        if fmt == isa.FORMAT_I16:
            self.arg = isa.decode_i16(self.read_command_bytes(2))
            self.current_instruction = isa.i16(self.ir, self.arg)
            return
        if fmt == isa.FORMAT_I32:
            self.arg = isa.decode_i32(self.read_command_bytes(4))
            self.current_instruction = isa.i32(self.ir, self.arg)
            return
        if fmt == isa.FORMAT_PUSHN:
            self.arg = self.read_command_bytes(1)[0]
            self.current_instruction = isa.pushn(())
            return
        raise MachineError(f"unsupported instruction format: {fmt}")

    def read_command_bytes(self, count):
        end = self.pc + count
        if end > len(self.command_memory):
            raise MachineError(f"truncated instruction at address {self.fetch_address}")
        payload = self.command_memory[self.pc : end]
        self.signal_latch_pc(step=count)
        return payload

    def signal_latch_pc(self, target=None, step=0):
        self.pc = self.pc + step if target is None else target

    def current_instruction_mnemonic(self):
        if self.ir is Opcode.PUSHN:
            return f"PUSHN count={self.arg}"
        return isa.instruction_to_mnemonic(self.current_instruction)

    def signal_finish_execute(self):
        self.state = FETCH_OPCODE

    def signal_mem_read_stage(self):
        opcode = self.ir
        addresses = {
            Opcode.LOAD: self.data_path.tos,
            Opcode.LOAD_SP: self.data_path.sp,
            Opcode.LOAD_SP_M1: self.data_path.sp - 1,
            Opcode.LOAD_RP: self.data_path.rp,
            Opcode.LOADA: self.arg,
            Opcode.ADDM: self.arg,
            Opcode.RET: self.data_path.rp,
            Opcode.IRET: self.data_path.rp,
        }
        if opcode not in addresses:
            raise MachineError(f"opcode does not use MEM_READ: {opcode.mnemonic}")

        address = addresses[opcode]
        self.data_path.signal_mem_read(address)
        if opcode is Opcode.ADDM:
            self.state = MEMORY_ALU
        elif opcode in {Opcode.RET, Opcode.IRET}:
            self.state = WRITEBACK
        else:
            self.signal_finish_execute()
        self.tick(MEM_READ, f"addr={address & 0xFFFF:04X}")

    def signal_writeback_stage(self):
        opcode = self.ir
        if opcode not in {Opcode.RET, Opcode.IRET}:
            raise MachineError(f"opcode does not use WRITEBACK: {opcode.mnemonic}")

        self.signal_latch_pc(self.data_path.mdr)
        self.data_path.signal_step("rp", -1)
        if opcode is Opcode.IRET:
            self.data_path.signal_latch_flags(flags_ctrl="CLEAR_INT")
        self.data_path.interrupt_safe = True
        self.signal_finish_execute()
        self.tick(EXECUTE, opcode.mnemonic)

    def signal_call_enter(self):
        self.data_path.signal_mem_write(self.data_path.rp, self.pc)
        if self.ir is Opcode.CALL:
            self.signal_latch_pc(self.pc + self.arg)
            self.data_path.interrupt_safe = True
            self.signal_finish_execute()
        elif self.ir is Opcode.CALLXT:
            self.signal_latch_pc(self.data_path.tos)
            self.data_path.signal_step("sp", -1)
            self.state = CALLXT_LOAD_TOS
        else:
            raise MachineError(f"opcode does not use CALL_ENTER: {self.ir.mnemonic}")
        self.tick(EXECUTE, self.ir.mnemonic)

    def decode_and_execute(self):
        opcode = self.ir
        detail = opcode.mnemonic
        dp = self.data_path

        if opcode is Opcode.HALT:
            self.halted = True
            self.tick(EXECUTE, detail)
            raise StopIteration()

        if opcode in {Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD, Opcode.EQ, Opcode.LT, Opcode.GT}:
            dp.signal_binary_alu(opcode)
        elif opcode is Opcode.MOV_TOS_NOS:
            dp.signal_move("tos", "nos")
        elif opcode is Opcode.MOV_NOS_TOS:
            dp.signal_move("nos", "tos")
        elif opcode is Opcode.MOV_TOS_TMP:
            dp.signal_move("tos", "tmp")
        elif opcode is Opcode.MOV_TMP_TOS:
            dp.signal_move("tmp", "tos")
        elif opcode is Opcode.MOV_TMP_NOS:
            dp.signal_move("tmp", "nos")
        elif opcode is Opcode.MOV_NOS_TMP:
            dp.signal_move("nos", "tmp")
        elif opcode is Opcode.MOV_TOS_MDR:
            dp.signal_move("tos", "mdr")
        elif opcode is Opcode.MOV_NOS_MDR:
            dp.signal_move("nos", "mdr")
        elif opcode is Opcode.SP_INC:
            dp.signal_step("sp", 1)
        elif opcode is Opcode.SP_DEC:
            dp.signal_step("sp", -1)
        elif opcode is Opcode.RP_INC:
            dp.signal_step("rp", 1)
        elif opcode is Opcode.RP_DEC:
            dp.signal_step("rp", -1)
        elif opcode in {
            Opcode.LOAD,
            Opcode.LOAD_SP,
            Opcode.LOAD_SP_M1,
            Opcode.LOAD_RP,
            Opcode.LOADA,
            Opcode.RET,
            Opcode.IRET,
        }:
            self.state = MEM_READ
            self.signal_mem_read_stage()
            return
        elif opcode is Opcode.STORE:
            dp.signal_mem_write(dp.tos, dp.nos)
        elif opcode is Opcode.STORE_SP_TOS:
            dp.signal_store_sp(dp.tos)
        elif opcode is Opcode.STORE_SP_M1_TOS:
            dp.signal_mem_write(dp.sp - 1, dp.tos)
        elif opcode is Opcode.STORE_SP_M1_NOS:
            dp.signal_mem_write(dp.sp - 1, dp.nos)
        elif opcode is Opcode.STORE_RP_TOS:
            dp.signal_mem_write(dp.rp, dp.tos)
        elif opcode is Opcode.STOREA:
            dp.signal_mem_write(self.arg, dp.tos)
        elif opcode is Opcode.ADDM:
            self.state = MEM_READ
            self.signal_mem_read_stage()
            return
        elif opcode is Opcode.JMP:
            self.signal_latch_pc(self.pc + self.arg)
        elif opcode is Opcode.JZ:
            if dp.tos == 0:
                self.signal_latch_pc(self.pc + self.arg)
            detail = f"JZ flag={dp.tos}"
        elif opcode in {Opcode.CALL, Opcode.CALLXT}:
            dp.signal_step("rp", 1)
            self.state = CALL_ENTER
            self.tick(EXECUTE, f"{detail} prepare")
            return
        elif opcode is Opcode.EI:
            dp.signal_latch_flags(flags_ctrl="SET_IE")
        elif opcode is Opcode.DI:
            dp.signal_latch_flags(flags_ctrl="CLEAR_IE")
        elif opcode is Opcode.GET_CARRY:
            dp.signal_latch_special("tos", dp.flags["C"])
        elif opcode is Opcode.LDI:
            dp.signal_latch_special("tos", self.arg)
        elif opcode is Opcode.PUSHN:
            self.pushn_remaining = self.arg
            self.state = FETCH_OPCODE if self.pushn_remaining == 0 else FETCH_PUSHN_VALUE
            self.tick(EXECUTE, f"PUSHN count={self.pushn_remaining}")
            return
        else:
            raise MachineError(f"unsupported opcode: {opcode.mnemonic}")

        self.signal_finish_execute()
        self.tick(EXECUTE, detail)

    def format_state(self, stage, detail):
        dp = self.data_path
        ir = self.ir.mnemonic if self.ir is not None else "-"
        flags = "".join(name if dp.flags[name] else name.lower() for name in ("Z", "N", "C", "V", "IE", "INT"))
        mode = "interrupt" if dp.flags["INT"] else "main"
        input_state = f"input={dp.input_char:02X}" if dp.input_ready else "input=--"
        detail_text = f" {detail}" if detail else ""
        return (
            f"tick={self._tick:05d} state={stage:<20} pc={self.pc:04X} "
            f"ir={ir:<15} arg={self.arg:>11} tos={dp.tos:>11} nos={dp.nos:>11} "
            f"sp={dp.sp:04X} rp={dp.rp:04X} tmp={dp.tmp:>11} mdr={dp.mdr:>11} "
            f"flags={flags} mode={mode:<9} {input_state}{detail_text}"
        )


def _command_memory_from_code(code):
    if isinstance(code, (bytes, bytearray)):
        return bytes(code)
    return isa.to_bytes(code)


def _interrupt_vector_from(interrupts):
    if interrupts is None:
        return None
    if isinstance(interrupts, int):
        return interrupts
    if not interrupts:
        return None
    if "on-input" in interrupts:
        return interrupts["on-input"]
    return interrupts[sorted(interrupts)[0]]


def simulation(code, data_words=None, limit=10000, interrupts=None, input_schedule=None):
    data_path = DataPath(data_words)
    control_unit = ControlUnit(
        _command_memory_from_code(code),
        data_path,
        interrupt_vector=_interrupt_vector_from(interrupts),
        input_schedule=input_schedule,
    )

    try:
        while control_unit.current_tick() < limit and not control_unit.halted:
            control_unit.process_next_tick()
    except StopIteration:
        pass

    if not control_unit.halted and control_unit.current_tick() >= limit:
        raise MachineError("tick limit exceeded")

    return {
        "output": "".join(data_path.output_buffer),
        "ticks": control_unit.current_tick(),
        "data_stack": data_path.data_stack(),
        "return_stack": data_path.return_stack(),
        "log": list(control_unit.log),
        "control_unit": control_unit,
        "data_path": data_path,
    }


def load_interrupts(filename):
    interrupts = {}
    if filename is None:
        return interrupts
    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                name, address = line.split(maxsplit=1)
                interrupts[name] = int(address, 0)
    return interrupts


def load_input_schedule(filename):
    if filename is None:
        return []

    escapes = {"\\0": "\0", "\\n": "\n", "\\r": "\r", "\\t": "\t"}
    schedule = []
    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tick_text, token = line.split(maxsplit=1)
            if token in escapes:
                char = escapes[token]
            elif token.startswith("\\x") and len(token) == 4:
                char = chr(int(token[2:], 16))
            else:
                char = token[0]
            schedule.append((int(tick_text, 0), char))
    return sorted(schedule, key=lambda item: item[0])


def default_interrupt_file(code_file):
    candidate = code_file + ".interrupts"
    return candidate if os.path.exists(candidate) else None


def main(code_file, data_file=None, interrupt_file=None, schedule_file=None, limit=10000):
    with open(code_file, "rb") as file:
        command_memory = file.read()

    if interrupt_file is None:
        interrupt_file = default_interrupt_file(code_file)

    data_words = None
    if data_file is not None:
        with open(data_file, "rb") as file:
            data_words = isa.data_from_bytes(file.read())

    result = simulation(
        command_memory,
        data_words=data_words,
        limit=int(limit),
        interrupts=load_interrupts(interrupt_file),
        input_schedule=load_input_schedule(schedule_file),
    )
    print(result["output"])
    print("ticks:", result["ticks"])


if __name__ == "__main__":
    assert 2 <= len(sys.argv) <= 5, "Wrong arguments: machine.py <code_file> [data_file] [schedule_file] [limit]"

    code_arg = sys.argv[1]
    data_arg = sys.argv[2] if len(sys.argv) >= 3 else None
    schedule_arg = sys.argv[3] if len(sys.argv) >= 4 else None
    limit_arg = sys.argv[4] if len(sys.argv) == 5 else 10000

    main(code_arg, data_arg, schedule_file=schedule_arg, limit=limit_arg)
