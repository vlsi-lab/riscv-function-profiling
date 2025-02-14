#!/bin/python
from wal.core import Wal
import os
import subprocess
from rv_profile.CallStack import CallStack

RET=(0x8082, )
MRET=(0x30200073,)


def ranges(binary_file):
    '''This functions extracts the functions from elf files using "nm"'''
    res = []

    if 'RISCV_PREFIX' in os.environ:
        proc = subprocess.Popen( [ os.environ['RISCV_PREFIX'] + 'nm' , '-S', binary_file], stdout=subprocess.PIPE )
    else:
        # print('Please add the location of you RISC-V toolchain to the "RISCV_PREFIX" variable.')
        # print('Now trying to fall back to the regular "nm"..\n')
        try:
            proc = subprocess.Popen( [ 'nm' , '-S', binary_file], stdout=subprocess.PIPE )
        except:
            print('"nm" not found on system')
            exit(1)
        
    stdout, _ = proc.communicate()
    symbols = stdout.decode('UTF-8')

    for line in symbols.split('\n'):
        cols = line.split()
        if len(cols) == 4 and cols[2] in ['T', 't']:
            name = cols[3]
            start = int(cols[0], 16)
            end = start + int(cols[1], 16) - 2
            res.append([name, start, end])

    return res



def riscv_profile_main(elf, fst, cfg, output, step):
    BIN         = elf
    VCD         = fst
    CFG_FILE    = cfg
    FG_DATA     = output

    cs      = CallStack(verbose=False)
    functions = ranges(BIN)
    buffer  = []

    wal     = Wal()
    wal.load(VCD)
    

    wal.eval_str(f'(eval-file {CFG_FILE})') # require config script to get concrete signal names

    def count_function(seval, args):
        addr = seval.eval(args[0])
        instr = seval.eval(args[1])
        mcycle = seval.eval(args[2])

        assert (len(buffer) == 0 or len(buffer) == 1)

        if (len(buffer) == 1):
            buffer.pop()

            # Return with the new func name
            for function in functions:
                if addr >= function[1] and addr <= function[2]:
                    cs.ret(function[0], addr, mcycle)
        
        if (instr in RET or instr in MRET):
            if (len(buffer) == 0):
                # buffer and wait for the next instruction
                buffer.append(addr)
                return

        for function in functions:
            if addr >= function[1] and addr <= function[2]:
                    cs.call(function[0], addr, mcycle)
                    return

    wal.step(step)

    wal.register_operator("count-function", count_function)

    instructions_executed = wal.eval_str('(whenever (fire) (count-function pc instr mcycle))', funcs=functions)

    cs.generate_flamegraph_data(FG_DATA)
