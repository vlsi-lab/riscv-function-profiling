# rv_profile 
[![PyPI version](https://img.shields.io/pypi/v/rv-profile)](https://pypi.org/project/rv-profile/)
![License](https://img.shields.io/pypi/l/rv-profile)

![FlameGraph](https://vincenzo-petrolo.github.io/flamegraph_example/flamegraph.svg)

This project implements a cycle-accurate RISC-V profiler that extracts the cycles spent in each function from RTL simulations.


An interactive example is found [here](https://vincenzo-petrolo.github.io/flamegraph_example/flamegraph.svg).

## Installing
```
pip install rv-profile
```

## Using
To profile a waveform you need to have a RISC-V `.elf` binary and a `.vcd`/`.fst` waveform of a RISC-V core running the binary.
This repository contains an example for the [cv32e40x](https://github.com/Vincenzo-Petrolo/riscv-function-profiling/blob/main/cv32e40x/) core. More will be added in the future.

```bash
rv_profile --elf <.elf> --fst <.vcd/.fst file> --cfg <.wal file> [--out <flamegraph.svg>]
```

<!-- ## How does it work?
1. This program extracts information about the functions from the `.elf` file using the "nm" command. This command prints a list of all symbols and their sizes.
2. Using this information the start and end addresses of functions are calculated. Then, the WAL code, which is embedded into the main script similar to SQL queries, searches the waveform for all executed instructions and their location in the binary.
3. The script further tracks the calls/returns of functions and calculates the time spent in each function and each of the child calls using the `mcycle` performance counter. The output is a flamegraph (`.data` file). 
4. Eventually, the `.data` file is converted to a `.svg` image using the FlameGraph perl script. -->

## Adapting to Other Cores
To adapt a new core to this script is easy. All you have to do is to know the name of the clk signal, detect when an instruction is committed, which address this instruction had and the raw value of the instruction (i.e. the 32-bit value).
This information can then be entered in a new `config.wal` file just like the ones in [cv32e40x](https://github.com/Vincenzo-Petrolo/riscv-function-profiling/blob/main/cv32e40x/config.wal).

The config file specifies 

```
(alias clk          ...cv32e40x_core_i.clk                              )
(alias pc           ...cv32e40x_core_i.debug_pc_o                       )
(alias instr        ...cv32e40x_core_i.ex_wb_pipe.instr.bus_resp.rdata  )
(alias fire-signal  ...cv32e40x_core_i.debug_pc_valid_o                 )
(alias mcycle       ...cv32e40x_core_i.cs_registers_i.mcycle_o          )
```

So you have to change `(alias clk ....)` to `(alias clk your.clk.signal)`

## Contributing
If you want to contribute to this project, please open an issue or a pull request. We are happy to help you with any questions you might have.

If you use this tool on a different RISC-V core please open a pull request so that we can include it in the repository.

### Repositories that made this possible
* [RISC-V Function Profiling](https://github.com/LucasKl/riscv-function-profiling) 
* [WAL](https://github.com/ics-jku/wal)
* [FlameGraph](https://github.com/brendangregg/FlameGraph).
