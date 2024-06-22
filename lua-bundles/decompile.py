import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "luajit-decompiler"))

import ljd.rawdump.parser as parser
import ljd.rawdump.code
import ljd.bytecode.instructions
import ljd.lua.writer
import ljd.bytecode.prototype
import main
import re
import hashlib

dummy_opcodes = []
for i in range(256):
    dummy_opcodes.append((i, ljd.bytecode.instructions.UNKNW))

ljd.rawdump.code.init(dummy_opcodes)

pattern_name = r"^[a-zA-Z0-9_]+(?!.*\.\.).*$"
names = {}


def add_name(name):
    h = hashlib.md5(name.encode()).hexdigest()
    if h not in names:
        names[h] = name
    elif names[h] != name:
        print(f"Collision: {name} -> {name} and {names[h]}")


def extract_names(prototype):
    for constant in prototype.constants.complex_constants:
        if isinstance(constant, str):
            if re.match(pattern_name, constant):
                name = constant.replace(".", "/") + ".lua"
                add_name(name)
        elif isinstance(constant, ljd.bytecode.prototype.Prototype):
            extract_names(constant)


if len(sys.argv) < 3:
    print("Usage: python lua-bundles/decompile.py <extracted-dir> <output-dir>")
    sys.exit(1)

print("Extracting names")

# add hardcoded names
add_name("tolua.lua")
add_name("booter/BootStarter.lua")

for root, _, files in os.walk(sys.argv[1]):
    for file in files:
        try:
            _, prototype = parser.parse(os.path.join(root, file))
            extract_names(prototype)
        except Exception:
            print(f"Error processing {file}")


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


decompile_options = Struct(
    **{
        "options": Struct(
            **{
                "catch_asserts": True,
                "output_pseudoasm": False,
                "dump_ast": False,
                "no_unwarp": False,
                "unsafe_extra_pass": True,
            }
        )
    }
)

for root, _, files in os.walk(sys.argv[1]):
    for file in files:
        name = file[: file.index(".")]
        output = f"unmapped/{name}.lua"
        if name in names:
            output = f"{names[name]}"

        print(f"Decompiling {output}")

        output = os.path.join(sys.argv[2], output)
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))

        with open(output, "w") as f:
            f.write(f"-- File Id: {name}\n")
            f.write(f"-- https://github.com/hax0r31337/re1999-tools\n\n")

            try:
                ast = main.Main.decompile(decompile_options, os.path.join(root, file))
                ljd.lua.writer.write(f, ast)
            except Exception:
                print(f"Error processing {file}")
                f.write("-- Error processing file\n")
