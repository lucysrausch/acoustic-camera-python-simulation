# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ReadOnly
import random

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


@cocotb.test()
def otter(dut):
    """Test for adding 2 random numbers multiple times"""
    dut.data = 0
    dut.rst = 0
    dut.clk = 0

    cocotb.fork(Clock(dut.clk,5000).start())
    yield RisingEdge(dut.clk)

    samplelenght = 4000
    t = np.linspace(0, 8, samplelenght, endpoint=False)
    dataout1 = np.arange(samplelenght, dtype=np.int16)
    dataout2 = np.arange(samplelenght, dtype=np.int16)
    dataout3 = np.arange(samplelenght, dtype=np.int16)
    #datain = np.arange(samplelenght, dtype=np.int16)

    sig = np.sin(2 * np.pi * t)
    #datain = np.arange(samplelenght, dtype=np.int16)#signal.square(2 * np.pi * 40 * t, duty=(sig + 1)/2) * 0.5 + 0.5
    datain = signal.square(2 * np.pi * 40 * t, duty=(sig + 1)/2) * 0.5 + 0.5
    #for i in datain:
    #    datain[i] = 1
    dut.rst = 1
    yield RisingEdge(dut.clk)
    dut.rst = 0
    yield RisingEdge(dut.clk)

    for i in range(samplelenght):
        data = int(datain[i])

        dut.data = data

        yield RisingEdge(dut.clk)

        #print int(dut.out3)
        dataout1[i] = int(dut.out1)
        dataout2[i] = int(dut.out2)
        dataout3[i] = int(dut.out3)

        #dut._log.info("Ok!")

    print("max:")
    print (np.max(dataout3))

    print("min:")
    print (np.min(dataout3))

    plt.plot(t, dataout1, label="L1")
    plt.plot(t, (sig* 0.5 + 0.5)*1024, label="original")
    plt.plot(t, dataout2, label="L2")
    plt.plot(t, dataout3, label="L3")

    plt.plot(t, datain* 1024, alpha=0.5, label="PDM")

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.xlabel('time (us)')
    plt.title('CRRS Filter for PDM')
    plt.grid(True)
    plt.savefig("test.png")
    plt.show()
