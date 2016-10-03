# The CORSIKA wrapper

Calls [CORSIKA](https://www.ikp.kit.edu/corsika/) in a thread safe and more comfortable way.

## Usage
### 1st) (only needed once)
```bash
user@machine:~$ corsika -c /home/user/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd
```
### 2nd)
```bash
user@machine:~$ corsika -i /home/user/reaserch/my_steering_card.txt -o /home/user/results/my_run.evtio
```
## Why
The CORSIKA executable call is special by today's standards e.g. it demands stdin and must not be called in parallel within the same working directory. (Told so by Konrad Bernloeh and Dieter Heck).

## How
The CORSIKA wrapper first creates a temporary directory. Second, all CORSIKA dependencies in CORSIKA's 'run' directory are copied into the temporary working directory. Third, CORSIKA is called in the temporary working directory and gets the steering card piped in via stdin. If an output path is specified on the command line [-o], the output path in the steering card piped into CORSIKA is overwritten. Fourth, when CORSIKA is done, the temporary working directory is removed. Finally the output file's write protection is removed. The CORSIKA wrapper returns the CORSIKA return value. Optionally [-s], CORSIKA's stdout and stderr can be dumped into textfiles in the output path which shadow the name of the output.
