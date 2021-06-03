# ser2csv

Reads data from a serial port and sends to a csv file

## Install

```bash
install.ps1
```

## Example usage

```bash
python ser2csv.py --help
# Read data from COM1 continuously for 5 seconds at 0.1 second intervals:
python .\ser2csv.py --time-secs 5 --delta-t 0.1 COM1
```
