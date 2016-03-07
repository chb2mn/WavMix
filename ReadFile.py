import struct
import time

def bitfield(n, field_size):
    bitlist = [1 if digit=='1' else 0 for digit in bin(n)[2:]]
    #This is bad and linear
    while len(bitlist) < field_size:
        bitlist.insert(0, 0)
    return bitlist

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
    sample_size
    while frame_num < size_of_data:
        frame = fin.read(sample_size)
        frame_num += 1
        for i in range(num_channels):
            sample = frame[i * bytes_per_sample:(i+1) * bytes_per_sample] #Divide the frame into each channel's sample
            try:
                sample_int = struct.unpack(fmt, sample)[0]
            except:
                print("failed on sample:", frame_num)
                break
