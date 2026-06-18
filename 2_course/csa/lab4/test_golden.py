import base64
import os
import subprocess
import sys
import tempfile
import unittest

import machine
import translator

ROOT = os.path.dirname(os.path.abspath(__file__))
GOLDEN_DIR = os.path.join(ROOT, "golden")
LOG_HEAD_LINES = 100
LOG_TAIL_LINES = 100
MAX_LOG_LINES = LOG_HEAD_LINES + LOG_TAIL_LINES


def read_text(filename):
    with open(filename, encoding="utf-8") as file:
        return file.read()


def read_golden(filename):
    result = {}
    lines = read_text(filename).splitlines()
    pos = 0
    while pos < len(lines):
        line = lines[pos]
        pos += 1
        if not line:
            continue

        key, marker = line.split(":", 1)
        marker = marker.strip()

        if marker in {"|-", "|", "!!binary |"}:
            block = []
            while pos < len(lines) and (lines[pos].startswith("  ") or lines[pos] == ""):
                if lines[pos].startswith("  "):
                    block.append(lines[pos][2:])
                else:
                    block.append("")
                pos += 1
            text = "\n".join(block)
            if marker == "|" and text:
                text += "\n"
            if marker == "!!binary |":
                result[key] = base64.b64decode("".join(text.split()))
            else:
                result[key] = text
        else:
            result[key] = int(marker)
    return result


def golden_files():
    for name in sorted(os.listdir(GOLDEN_DIR)):
        if name.endswith(".yml"):
            yield os.path.join(GOLDEN_DIR, name)


def data_target_name(target):
    if target.endswith(".bin"):
        return target[:-4] + ".data.bin"
    return target + ".data"


def selected_log_lines(log):
    if len(log) <= MAX_LOG_LINES:
        return log
    return log[:LOG_HEAD_LINES] + log[-LOG_TAIL_LINES:]


class GoldenTest(unittest.TestCase):
    def test_golden_cases(self):
        for filename in golden_files():
            with self.subTest(case=os.path.basename(filename)):
                self.run_case(filename)

    def run_case(self, filename):
        golden = read_golden(filename)
        source_text = golden["in_source"]
        limit = str(golden.get("in_limit", 10000))

        with tempfile.TemporaryDirectory() as tmpdirname:
            source = os.path.join(tmpdirname, "source.fth")
            target = os.path.join(tmpdirname, "program.bin")
            data_target = data_target_name(target)
            schedule_target = os.path.join(tmpdirname, "input.schedule")

            with open(source, "w", encoding="utf-8") as file:
                file.write(source_text)
            with open(schedule_target, "w", encoding="utf-8") as file:
                file.write(golden["in_stdin"])

            subprocess.run(
                [sys.executable, "translator.py", source, target],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            machine_result = subprocess.run(
                [sys.executable, "machine.py", target, data_target, schedule_target, limit],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            with open(target, "rb") as file:
                self.assertEqual(file.read(), golden["out_code"])
            with open(data_target, "rb") as file:
                self.assertEqual(file.read(), golden["out_data"])
            self.assertEqual(read_text(target + ".hex"), golden["out_code_hex"])
            self.assertEqual(read_text(data_target + ".hex"), golden["out_data_hex"])
            self.assertEqual(read_text(target + ".interrupts"), golden["out_interrupts"])
            self.assertEqual(machine_result.stdout, golden["out_stdout"])

        translated = translator.translate(source_text)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as schedule_file:
            schedule_file.write(golden["in_stdin"])
            schedule_file.flush()
            schedule_data = machine.load_input_schedule(schedule_file.name)
        sim = machine.simulation(
            translated["code"],
            data_words=translated["data"],
            limit=int(limit),
            interrupts=translated["interrupts"],
            input_schedule=schedule_data,
        )
        expected_log = golden["out_log"]
        log_lines = len(expected_log.splitlines())
        self.assertLessEqual(log_lines, MAX_LOG_LINES)
        selected_log = "\n".join(selected_log_lines(sim["log"]))
        if selected_log:
            selected_log += "\n"
        self.assertEqual(selected_log, expected_log)


if __name__ == "__main__":
    unittest.main()
