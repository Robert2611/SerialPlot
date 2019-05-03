# SerialPlot
A simple python script to plot incomming data from a serial port

Example usage:
```console
SerialPlot.py COM5 9600
```

On Windows you might need to tell the system to use python to open the script:
```console
C:\Your\Python\Path\python.exe SerialPlot.py COM5 9600
```

Or, if you added python to your path variable:
```console
python SerialPlot.py COM5 9600
```


For plotting more than one input column use the `--column` parameter:
```console
SerialPlot.py COM5 9600 --colum 2
```

If you do not see your data try using the `--min` and `--max` parameters:
```console
SerialPlot.py COM5 9600 --min -10 --max 10
```

For more detailed usage information type:
```console
SerialPlot.py --help
```