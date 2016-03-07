import struct
import time

samplesize2fmt = {
    4: "L",
    2: "H",
    1: "B"
}

with open("D:/mario.wav", "rb") as fin:
    #Read The Header
    header = fin.read(36)
    if header[:4].startswith("RIFF"):
        print "yay, RIFF"
    if header[8:12] == "WAVE":
        print "yay, WAVE"
    if header[12:15] =="fmt":
        print "yay, fmt"

    num_channels = struct.unpack("H", header[22:24])[0]
    print "num_channels:", num_channels
    bytes_per_sample = struct.unpack("H", header[34:36])[0]/8
    print "bps:", bytes_per_sample
    sample_size = struct.unpack("H", header[32:34])[0]
    print "sample size:", sample_size
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
        A_ = fin.read(1)
    print D+A+T+A_
    sample = fin.read(sample_size)
    while sample != "":
        magnitude = struct.unpack(fmt, sample)[0]
        if magnitude > 1000000:
            print magnitude
        sample = fin.read(sample_size)


    #Read Data