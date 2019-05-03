#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    File name: SerialPlot.py
    Author: Robert Niemöller ()
    Date created: 2019-05-03
    Based on: https://gist.github.com/electronut/d5e5f68c610821e311b0
'''

import serial, argparse
from collections import deque

import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import threading


# plot class
class SerialPlot:
    # constructor
    def __init__(self, plt_axes, strPort, baudrate, columns, history, separator, timeout): 
        self.history = history
        self.columns = columns
        self.separator = separator
        self.timeout = timeout   
        self.abort = False

         # open serial port
        self.ser = serial.Serial(strPort, baudrate, timeout = self.timeout)

        #init plots for the requested of colums 
        self.plots = []
        self.plot_data = []
        for _ in range(self.columns):
            self.plot_data.append(deque([0.0]*history))
            new_plot, = plt_axes.plot([], [])
            self.plots.append(new_plot)

    # read data from serial port
    def read_contiously(self):
        while not self.abort:
            try:
                line = self.ser.readline().decode('ascii')
                s = line.split(self.separator)
                if len(s) < 1:
                    continue
                data = [float(val) for val in s]
                #add data                
                for i in range(self.columns):
                    if len(data) > i:
                        if len(self.plot_data[i]) < self.history:
                            self.plot_data[i].append(data[i])
                        else:
                            self.plot_data[i].pop()
                            self.plot_data[i].appendleft(data[i])
            except ValueError:
                continue

    # update plot
    def update(self, frame):
        for i in range(self.columns):
            self.plots[i].set_data(range(self.history), self.plot_data[i])
        return self.plots[0],

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close() 


# main() function
def main():
    # create parser
    parser = argparse.ArgumentParser(description="Serial Plot")
    # add expected arguments
    parser.add_argument('port')
    parser.add_argument('baudrate', type=int)
    parser.add_argument('-c', '--columns', dest="columns", type=int, default=1, help="Number of columns in the serial output")
    parser.add_argument('-t', '--history', dest="history", type=int, default=100, help="Number of datasets to plot")
    parser.add_argument('--min', dest="min", type=float, default=0, help="Lowest y value to plot")
    parser.add_argument('--max', dest="max", type=float, default=1000, help="Highest y value to plot")
    parser.add_argument('-i', '--interval', dest="interval", type=float, default=10, help="Update interval for the plot, higher means faster update")
    parser.add_argument('-s', '--separator', dest="separator", default=",", help="Separator for the serial input")
    parser.add_argument('-o', '--timeout', dest="timeout", default=1, type=float, help="Timeout for serial data. Without this the reading could be blocked forever.")

    # parse args
    args = parser.parse_args()

    print('reading from serial port %s...' % args.port)
    # set up animation
    fig = plt.figure()
    ax = plt.axes(xlim=(0, args.history), ylim=(args.min, args.max))
    sp = SerialPlot(ax, args.port, args.baudrate, args.columns, args.history, args.separator, args.timeout)
    anim = FuncAnimation(fig, sp.update, interval=args.interval)
    read_thread = threading.Thread(target=sp.read_contiously)
    read_thread.start()
    # show plot
    plt.show()
    print('exiting.')
    #after plot was closed, stop the serial listener and wait for thread to close
    sp.abort = True
    read_thread.join()
    # clean up
    sp.close()

# call main
if __name__ == '__main__':
    main()