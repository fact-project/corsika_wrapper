# corsika_iact_caller

Calls [CORSIKA](https://www.ikp.kit.edu/corsika/) with [IACT](https://www.mpi-hd.mpg.de/hfm/~bernlohr/iact-atmo/) package in a thread safe and modern way.

## Usage
```bash
user@machine:~$ corsika_iact -c /home/user/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd -i corsika_input_card.txt 
```

or in python
```python
import corsika_iact_caller as cic
cic.corsika_iact('/home/user/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd', '/home/user/corsika/corsika_input_card.txt')
```

## Why
The CORSIKA executable call is special by today's standards e.g. it demands stdin and must not be called in parallel within the same working directory. (Told so by Konrad Bernloeh and Dieter Heck).

## How
The corsika_iact_call wrapper first creates a temporary directory in the output path of CORSIKA which it knows from the input card. Second all CORSIKA and IACT dependencies are symbolically linked into the temporary working directory. The name of the temporary working directory is based on the output path but extended with a '_temp' and a random 6 digit number. CORSIKA is now called in the temporary working directory and gets the input card via stdin. After CORSIKA is done, the temporary working directory is removed. Finally the output's write protection is removed. The wrapper returns the CORSIKA return value and is transparent to CORSIKA's stdout and stderr. The wrapper will only talk to stdou and stderr in case of exceptions. Optionally, CORSIKA's stdout and stderr can be dumped into designated textfiles in the output path which shadow the name of the output.
