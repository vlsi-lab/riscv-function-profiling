# RISC-V Function Profiling from Waveforms + FlameGraph

This project implements a function-level RISC-V profiler that extracts the time spent in each function out of a simulation waveform (`.vcd` and `.fst` are supported).
This project is built upon the existing [RISC-V Function Profiling](https://github.com/LucasKl/riscv-function-profiling) project by LucasKl and [WAL](https://github.com/ics-jku/wal).

The output of the profiler is a flamegraph that visualizes the time spent in each function. The flamegraph is generated using the [FlameGraph](https://github.com/brendangregg/FlameGraph).

Example of generated flamegraph (click to zoom in):
![FlameGraph](./docs/flamegraph.svg)

## Dependencies
The only requirement for this script is Python < 3.10 and the `wal-lang` Python package (tested with Python 3.9).

Install WAL by typing:
```
pip install wal-lang==0.8.2 pylibfst
```

## Getting Started
To set up the project and run an example test, use the following commands:
```bash
git clone https://github.com/Vincenzo-Petrolo/riscv-function-profiling.git
cd riscv-function-profiling
make vendor-update
make test
```
This will generate the `flamegraph.svg` image in the `build` directory for an example application running on the [cv32e40x](https://github.com/openhwgroup/cv32e40x) core in
the [X-HEEP](https://github.com/esl-epfl/x-heep) system.

## Profiling Waveforms
To profile a waveform you need to have a RISC-V `.elf` binary and a `.vcd`/`.fst` waveform of a RISC-V core running the binary.
This repository contains an example for the cv32e40x core. More will be added in the future (where possible).

## Usage
To get a grasp of how to use the script please take a look into the [Makefile](https://github.com/Vincenzo-Petrolo/riscv-function-profiling/blob/main/makefile). Additionally, you can run the script with the following command:
```bash
python3 profile.py <.elf file> <.vcd/.fst file> <.data flamegraph output file>
```

## How does it work?
1. This program extracts information about the functions from the `.elf` file using the "nm" command. This command prints a list of all symbols and their sizes.
2. Using this information the start and end addresses of functions are calculated. Then, the WAL code, which is embedded into the main script similar to SQL queries, searches the waveform for all executed instructions and their location in the binary.
3. The script further tracks the calls/returns of functions and calculates the time spent in each function and each of the child calls. The output is a flamegraph (`.data` file). 
4. Eventually, the `.data` file is converted to a `.svg` image using the FlameGraph perl script.

## Adapting to Other Cores
To adapt a new core to this script is easy. All you have to do is to know the name of the clk signal, detect when an instruction is committed, which address this instruction had and the raw value of the instruction (i.e. the 32-bit value).
This information can then be entered in a new `config.wal` file just like the ones in [cv32e40x](https://github.com/Vincenzo-Petrolo/riscv-function-profiling/blob/main/cv32e40x/config.wal).

The config file specifies three names at which the WAL program finds the information it needs.

```
(alias clk      ...cv32e40x_core_i.clk)
(alias pc       ...cv32e40x_core_i.debug_pc_o)
(alias instr    ...cv32e40x_core_i.ex_wb_pipe.instr.bus_resp.rdata)
```

So you have to change `(alias clk ....)` to `(alias clk your.clk.signal)`