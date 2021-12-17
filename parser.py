import functools
import sys


class CodeParser:
    def __init__(self):
        self._instruction = []
        self._binary = ""

    def _r_type(self, function_code):
        self._opcode = format(0, "b").zfill(6)
        self._function_code = function_code.zfill(6)
        rs = format(int(self._instruction[2]), "b").zfill(5)
        rt = format(int(self._instruction[3]), "b").zfill(5)
        rd = format(int(self._instruction[1]), "b").zfill(5)
        shamt = format(0).zfill(5)

        self._binary = str(self._opcode) + str(rs) + str(rt) + str(rd) + str(shamt) + str(self._function_code)

    def _i_type(self, opcode):
        self._opcode = opcode.zfill(6)
        rs = format(int(self._instruction[3]), "b").zfill(5)
        rt = format(int(self._instruction[1]), "b").zfill(5)
        im = format(int(self._instruction[2]), "b").zfill(16)

        self._binary = str(self._opcode) + str(rs) + str(rt) + str(im)

    def parse(self, string):
        _code = string
        charset = [',', '$', '0x', ')']

        for c in charset:
            _code = _code.replace(c, "")
        _code = _code.replace('(', " ")

        self._instruction = _code.split()

        {
            "add": functools.partial(self._r_type, format(32, "b")),
            "and": functools.partial(self._r_type, format(36, "b")),
            "or": functools.partial(self._r_type, format(37, "b")),
            "sub": functools.partial(self._r_type, format(42, "b")),

            "lw": functools.partial(self._i_type, format(35, "b")),
            "sw": functools.partial(self._i_type, format(43, "b")),
            "addi": functools.partial(self._i_type, format(8, "b")),
            "andi": functools.partial(self._i_type, format(12, "b")),
        }.get(self._instruction[0])()

        return self._binary


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parser.py <source file name>")
        sys.exit()

    src = open(sys.argv[1], 'r')
    dst = open('Input.txt', 'w')

    parser = CodeParser()
    while True:
        line = src.readline()
        if not line:
            break

        dst.write(parser.parse(line) + "\n")

    print("Done.")


if __name__ == '__main__':
    main()

