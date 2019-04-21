#!/usr/bin/python
# Generate almost all possible combination for instructions from instruction
# tables

import sys

argspecTbl = {
    'A': "A",
    'B': "B",
    'C': "C",
    'D': "D",
    'E': "E",
    'H': "H",
    'L': "L",
    'h': "HL",
    'l': "(HL)",
    'd': "DE",
    'e': "(DE)",
    'b': "BC",
    'c': "(BC)",
    'a': "AF",
    'f': "AF'",
    'x': "(IX)",
    'y': "(IY)",
    's': "SP",
    'p': "(SP)",
    'Z': "Z",
    'z': "NZ",
    '=': "NC",
    '+': "P",
    '-': "M",
    '1': "PO",
    '2': "PE",
}

argGrpTbl = {
    chr(0x01): "bdha",
    chr(0x02): "ZzC=",
    chr(0x03): "bdhs",
    chr(0x0a): "ZzC=+-12",
    chr(0x0b): "BCDEHLA",
}

def cleanupLine(line):
    line = line.strip()
    idx = line.rfind(';')
    if idx >= 0:
        line = line[:idx]
    return line

def getDbLines(fp, tblname):
    lookingFor = f"{tblname}:"
    line = fp.readline()
    while line:
        line = cleanupLine(line)
        if line == lookingFor:
            break
        line = fp.readline()
    else:
        raise Exception(f"{tblname} not found")

    result = []
    line = fp.readline()
    while line:
        line = cleanupLine(line)
        if line:
            if not line.startswith('.db'):
                break
            result.append([s.strip() for s in line[4:].split(',')])
        line = fp.readline()
    return result

def genargs(argspec):
    if not argspec:
        return ''
    if not isinstance(argspec, str):
        argspec = chr(argspec)
    if argspec in 'nmNM':
        bits = 16 if argspec in 'NM' else 8
        nbs = [str(1 << i) for i in range(bits)]
        if argspec in 'mM':
            nbs = [f"({n})" for n in nbs]
        return nbs
    if argspec in argspecTbl:
        return [argspecTbl[argspec]]
    grp = argGrpTbl[argspec]
    return [argspecTbl[a] for a in grp]


def main():
    asmfile = sys.argv[1]
    with open(asmfile, 'rt') as fp:
        instrTbl = getDbLines(fp, 'instrTBl')
    for row in instrTbl:
        n = eval(row[0])
        # we need to adjust for zero-char name filling
        arg1index = 5 - len(n)
        a1 = eval(row[arg1index])
        a2 = eval(row[arg1index+1])
        args1 = genargs(a1)
        if args1:
            for arg1 in args1:
                args2 = genargs(a2)
                if args2:
                    for arg2 in args2:
                        print(f"{n} {arg1}, {arg2}")
                else:
                    print(f"{n} {arg1}")
        else:
            print(n)
    pass

if __name__ == '__main__':
    main()
