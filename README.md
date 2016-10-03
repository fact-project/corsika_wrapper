# The CORSIKA wrapper [![Build Status](https://travis-ci.org/fact-project/corsika_wrapper.svg?branch=call_it_like_a_sane_program)](https://travis-ci.org/fact-project/corsika_wrapper)
A wrapper for the [CORSIKA](https://www.ikp.kit.edu/corsika/) cosmic ray air shower simulation by the [Karlsruhe Institute for Technology](https://www.kit.edu/)

The CORSIKA simulation is certainly one of the most advanced simulation tools in modern particle physics, and even beyond its practicle use, you have to admire the sheer efficiency and speed of the fortran77 based CORSIKA. However, over the years multithread machines showed up, and todays students might not be used anymore to the user interface of CORSIKA. This CORSIKA call wrapper trys to overcome some of these issues. It allows you to:

- Run multiple CORSIKA instances in parallel (thread safe)
- Call CORSIKA from anywhere, systemwide on your machine
- Specify the output path in the CORSIKA call on the command line [optional `-o`]
- Have write access to your CORSIKA output files
- Store the CORSKA stdout and stderror next to your output [optional `-s`]

## How to use
### Once
Tell the corsika wrapper __once__ which CORISKA executable you want to run with the `-c` option.
```bash
user@machine:~$ corsika -c /home/user/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd
```

### For every CORSIKA call
Call corsika like a modern program and specify (if you want) your output path on the command line.
```bash
user@machine:~$ corsika -i /home/user/reaserch/my_steering_card.txt -o /home/user/results/my_run.evtio
```
## Python API
Use the corsika wrapper API directly in python to script your corsika calls.

```python
In [1]: import corsika_wrapper as cw
In [2]: return_value = cw.corsika(
                        steering_card=cw.read_steering_card('/home/user/reaserch/my_steering_card.txt'), 
                        output_path='/home/user/results/my_run.evtio', 
                        save_stdout=True)
```

## How it is done
1. The CORSIKA wrapper creates a temporary directory. 
2. All CORSIKA dependencies in CORSIKA's 'run' directory are copied into the temporary working directory. 
3. CORSIKA is called in the temporary working directory and gets the steering card piped in via stdin. If an output path is specified on the command line `[-o]`, the output path in the steering card piped into CORSIKA is overwritten. 
4. When CORSIKA is done, the temporary working directory is removed. 
5. Finally the output file's write protection is removed. The CORSIKA wrapper returns the CORSIKA return value. 

Optionally `[-s]`, CORSIKA's stdout and stderr can be dumped into textfiles in the output path which shadow the name of the output.

## Why
Calling CORSIKA is special. CORSIKA demands stdin, it can only be called in a certain 'run' directory environment, and it must not be called in parallel within the same working directory. (Told so by Konrad Bernloeh and Dieter Heck).
Further, the output path can not be specified on the command line and the output files are write protected.
