from time import sleep
from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

base = BaseOverlay("base.bit")

base.rgbleds[5].write(0)
hdmi_width = 1920
hdmi_height = 1080

# monitor configuration: 640*480 @ 60Hz
Mode = VideoMode(width = 1920, height = 1080, bits_per_pixel = 24, fps = 60, stride = None)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(Mode,PIXEL_RGB)
hdmi_out.start()

#
# Copyright (C) 2018-2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PS2000 Series (A API) STREAMING MODE EXAMPLE
# This example demonstrates how to call the ps4000A driver API functions in order to open a device, setup 2 channels and collects streamed data (1 buffer).
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time
import cv2

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

base.rgbleds[5].write(4)

# Open PicoScope 2000 Series device
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)

try:
    assert_pico_ok(status["openunit"])
except:

    powerStatus = status["openunit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])


enabled = 1
disabled = 0
analogue_offset = 0.0

# Set up channel A
# handle = chandle
# channel = PS4000A_CHANNEL_A = 0
# enabled = 1
# coupling type = PS4000A_DC = 1
# range = PS4000A_2V = 7
# analogue offset = 0 V
channel_range = 7
status["setChA"] = ps.ps4000aSetChannel(chandle,
                                        ps.PS4000A_CHANNEL['PS4000A_CHANNEL_A'],
                                        enabled,
                                        ps.PS4000A_COUPLING['PS4000A_DC'],
                                        channel_range,
                                        analogue_offset)
assert_pico_ok(status["setChA"])

# Set up channel B
# handle = chandle
# channel = PS4000A_CHANNEL_B = 1
# enabled = 1
# coupling type = PS4000A_DC = 1
# range = PS4000A_2V = 7
# analogue offset = 0 V
status["setChB"] = ps.ps4000aSetChannel(chandle,
                                        ps.PS4000A_CHANNEL['PS4000A_CHANNEL_B'],
                                        enabled,
                                        ps.PS4000A_COUPLING['PS4000A_DC'],
                                        channel_range,
                                        analogue_offset)
assert_pico_ok(status["setChB"])

# Size of capture
sizeOfOneBuffer = 500
numBuffersToCapture = 10

totalSamples = sizeOfOneBuffer * numBuffersToCapture

# Create buffers ready for assigning pointers for data collection
bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
bufferBMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)

memory_segment = 0

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS4000A_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# segment index = 0
# ratio mode = PS4000A_RATIO_MODE_NONE = 0
status["setDataBuffersA"] = ps.ps4000aSetDataBuffers(chandle,
                                                     ps.PS4000A_CHANNEL['PS4000A_CHANNEL_A'],
                                                     bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersA"])

# Set data buffer location for data collection from channel B
# handle = chandle
# source = PS4000A_CHANNEL_B = 1
# pointer to buffer max = ctypes.byref(bufferBMax)
# pointer to buffer min = ctypes.byref(bufferBMin)
# buffer length = maxSamples
# segment index = 0
# ratio mode = PS4000A_RATIO_MODE_NONE = 0
status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle,
                                                     ps.PS4000A_CHANNEL['PS4000A_CHANNEL_B'],
                                                     bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersB"])

# Begin streaming mode:
sampleInterval = ctypes.c_int32(250)
sampleUnits = ps.PS4000A_TIME_UNITS['PS4000A_US']
# We are not triggering:
maxPreTriggerSamples = 0
autoStopOn = 1
# No downsampling:
downsampleRatio = 1

actualSampleInterval = sampleInterval.value
actualSampleIntervalNs = actualSampleInterval * 1000

nextSample = 0
autoStopOuter = False
wasCalledBack = False

# We need a big buffer, not registered with the driver, to keep our complete capture in.
bufferCompleteA = np.zeros(shape=totalSamples, dtype=np.int16)
bufferCompleteB = np.zeros(shape=totalSamples, dtype=np.int16)


def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
    global wasCalledBack, autoStopOuter
    global bufferCompleteA, bufferCompleteB
    global nextSample
    wasCalledBack = True
    destEnd = nextSample + noOfSamples
    sourceEnd = startIndex + noOfSamples
    bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
    bufferCompleteB[nextSample:destEnd] = bufferBMax[startIndex:sourceEnd]
    nextSample += noOfSamples
    if autoStop:
        autoStopOuter = True

def take_measurements():
    global autoStopOuter
    global wasCalledBack
    global status
    global nextSample
    
    maxADC = ctypes.c_int16()

    nextSample = 0
    autoStopOuter = False
    wasCalledBack = False

    base.rgbleds[5].write(1)
    while (base.buttons[0].read()==0):
        continue

    status["runStreaming"] = ps.ps4000aRunStreaming(chandle,
                                                    ctypes.byref(sampleInterval),
                                                    sampleUnits,
                                                    maxPreTriggerSamples,
                                                    totalSamples,
                                                    autoStopOn,
                                                    downsampleRatio,
                                                    ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'],
                                                    sizeOfOneBuffer)
    base.rgbleds[5].write(4)
    assert_pico_ok(status["runStreaming"])

    print("Capturing at sample interval %s ns" % actualSampleIntervalNs)

    # Convert the python function into a C function pointer.
    cFuncPtr = ps.StreamingReadyType(streaming_callback)

    base.rgbleds[5].write(7)
    # Fetch data from the driver in a loop, copying it out of the registered buffers and into our complete one.
    while nextSample < totalSamples and not autoStopOuter:
        wasCalledBack = False
        status["getStreamingLastestValues"] = ps.ps4000aGetStreamingLatestValues(chandle, cFuncPtr, None)
        if not wasCalledBack:
            # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
            # again.
            time.sleep(0.01)

    base.rgbleds[5].write(4)
    print("Done grabbing values.")

    # Find maximum ADC count value
    # handle = chandle
    # pointer to value = ctypes.byref(maxADC)
    status["maximumValue"] = ps.ps4000aMaximumValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maximumValue"])

    # Convert ADC counts data to mV
    adc2mVChAMax = adc2mV(bufferCompleteA, channel_range, maxADC)
    adc2mVChBMax = adc2mV(bufferCompleteB, channel_range, maxADC)

    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps4000aStop(chandle)
    assert_pico_ok(status["stop"])
    return adc2mVChAMax, adc2mVChBMax

def fig2data ( fig ):
    """
    @brief Convert a Matplotlib figure to a 4D numpy array with RGBA channels and return it
    @param fig a matplotlib figure
    @return a numpy 3D array of RGBA values
    """
    # draw the renderer
    fig.canvas.draw ( )
 
    # Get the RGBA buffer from the figure
    w,h = fig.canvas.get_width_height()
    buf = np.frombuffer ( fig.canvas.tostring_rgb(), dtype=np.uint8 )
    buf.shape = ( h, w, 3 )
 
    return buf

def plot_data():
    fig = plt.figure()

    # Plot the signal
    fig.set_figwidth(10)
    fig.set_figheight(10)

    plt.subplot(211)
    plt.plot(adc2mVChAMax)
    plt.plot(adc2mVChBMax)
    plt.xlabel('Sample')
    plt.ylabel('Voltage (mV)')

    # Plot the spectrogram
    plt.subplot(212)
    powerSpectrum_, freqenciesFound_, time_, imageAxis_ = plt.specgram(adc2mVChAMax, Fs=1/(actualSampleInterval*1e-6))
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')

    data = fig2data(fig)
    return data

def hdmi_out_data():
    outframe = hdmi_out.newframe()
    outframe[:] = 0

    y1 = int(hdmi_height/2) - int(data.shape[0]/2)
    y2 = int(hdmi_height/2) + int(data.shape[0]/2)

    x1 = int(hdmi_width/2) - int(data.shape[1]/2)
    x2 = int(hdmi_width/2) + int(data.shape[1]/2)

    outframe[y1:y2, x1:x2, 0]=data[:,:,0]
    outframe[y1:y2, x1:x2, 1]=data[:,:,1]
    outframe[y1:y2, x1:x2, 2]=data[:,:,2]
    hdmi_out.writeframe(outframe)

while base.buttons[3].read()==0:
    adc2mVChAMax, adc2mVChBMax = take_measurements()
    data = plot_data()
    hdmi_out_data()

# Disconnect the scope
# handle = chandle
status["close"] = ps.ps4000aCloseUnit(chandle)
assert_pico_ok(status["close"])
base.rgbleds[5].write(0)
# Display status returns
print(status)

hdmi_out.stop()
del hdmi_out