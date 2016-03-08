# corsika_iact_caller

Calls [CORSIKA](https://www.ikp.kit.edu/corsika/) with [IACT](https://www.mpi-hd.mpg.de/hfm/~bernlohr/iact-atmo/) package in a thread safe and modern way.

## Usage
```bash
user@machine:~$ corsika_iact -c /home/user/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd -i corsika_input_card.txt 
```

or in python
```python
import corsika_iact_caller as cic
cic.corsika_iact('/home/sebastian/corsika/corsika-74005/run/corsika74005Linux_QGSII_urqmd', '/home/sebastian/corsika/thebiglebowsky_corsika_input_card.txt')
```

## Why
The corsika executable call is special by today's standards e.g. it demands stdin and must not be called in parallel within the same working directory. (Told so by Konrad Bernloeh and Dieter Heck).

