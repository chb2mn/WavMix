import struct
import time
import math
from numpy import fft

def print_eq(equalizer):
    #Return Cursor
    print("\033["+str(len(equalizer)+3)+"A\r")
    eq_viz = "-------------------\n"
    for level in equalizer:
        eq_viz += "." * level + "#"+" " * (10-level) + "\n"
    print(eq_viz)

def rms(values):
    subtotal = 0
    for sample in values:
        subtotal += sample**2
    return math.sqrt(subtotal/len(values))

samplesize2fmt = {
    4: "L",
    2: "H",
    1: "B"
}

with open("mario.wav", "rb") as fin:
    #Read The Header
    header = fin.read(36)
    if header[:4] == ("RIFF"):
        print ("yay, RIFF")
    if header[8:12] == "WAVE":
        print ("yay, WAVE")
    if header[12:15] =="fmt":
        print ("yay, fmt")

    num_channels = struct.unpack("H", header[22:24])[0]
    print ("num_channels:", num_channels)
    sample_rate = struct.unpack("I", header[24:28])[0]
    print ("sample rate:", sample_rate)
    bytes_per_sample = int(struct.unpack("H", header[34:36])[0]/8)
    print ("bps:", bytes_per_sample)
    sample_size = struct.unpack("H", header[32:34])[0]
    print ("sample size:", sample_size)
    fmt = "Q"
    if sample_size in samplesize2fmt:
        fmt = samplesize2fmt[sample_size]

    #Find The Data Section
    D = ""
    A = ""
    T = ""
    A_ = ""
    while not (D+A+T+A_).startswith("data"):
        
        D = A
        A = T
        T = A_
        A_ = fin.read(1).decode("utf-8")
    
    size_of_data = struct.unpack("I", fin.read(4))[0]/(sample_size)
    print ("size_of_data:", size_of_data)

    #Read Data
    frame_num = 0
    equalizer = [0 for i in range(16)]
    print(equalizer)
    volume_memory = []
    all_samples = []
    merged_sample = 0
    while frame_num < size_of_data:
        t_start = time.time()
        frame = fin.read(sample_size)
        frame_num += 1
        for i in range(num_channels):
            sample = frame[i * bytes_per_sample:(i+1) * bytes_per_sample] #Divide the frame into each channel's sample
            sample_int = 0
            try:
                sample_int = struct.unpack(fmt, sample)[0]
            except:
                print("failed on sample:", frame_num)
                break
            merged_sample += sample_int
        all_samples.append(merged_sample/num_channels)
    #merged samples now contains all of the data in numbers, let's run fft
    fft_result = fft.fft(all_samples)
    print(len(all_samples), len(fft_result), fft_result)
    print (fft_result[0])
    magnitudes = [math.sqrt(x.real**2+x.imag**2) for x in fft_result]
    print(magnitudes[0])
    for i in range(len(magnitudes)):
        #print("-"*int(magnitudes[i]/100000000000)+"#")
        print(len(str(magnitudes[i])))
        time.sleep(.0001)
"""
    sample_str = format(sample_int, '016b')
    sample_vol = 0
    for j in range(len(sample_str)):
        if sample_str[j] == '1':
            equalizer[j] = 10
            sample_vol += 1
        elif equalizer[j] > 0:
            equalizer[j] -= 2
    volume_memory.append(sample_vol)
    if len(volume_memory) > 5:
        volume_memory.pop(0)
    if frame_num < 15000:
        volume = rms(volume_memory)
        if volume > 8:
            print(volume)
    #print_eq(equalizer)
    #print(hex(frame_num * bytes_per_sample),'\t', equalizer)
t_delta = (time.time() - t_start)/1000000000 #to seconds
if t_delta < 1/sample_rate:
    time.sleep(1/sample_rate - t_delta)
"""
