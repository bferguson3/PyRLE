# RLE FILE ENCODER
#  takes any binary file and converts to RLE sequenced
#
# Input: any raw binary
# Output: Encoded w/ RLE, optionally trimmed square
#              Input $ff $ff $ff $ff $aa $ff 
#                 == $ff $ff $04 $aa $ff
# w/ 5 byte trim  == $ff $ff $04 $aa

# $ python3 ./rlenc.py <BIN FILENAME>

# OR: $ python3 ./rlenc.py <BIN FILENAME> <BYTESREAD> <BYTEBOUNDARY>

#    e.g. python3 ./rlenc.py file.bin 24 32
#   will read the first 24 out of every 32 bytes
#   from file.bin and compress it to file.rle.

# (c) 2019 Ben Ferguson

import os 
import sys 
import math 

input = sys.argv[1]

if len(sys.argv) == 1 or len(sys.argv) == 3 or len(sys.argv) > 4:
    print('Usage:\n $ python3 ./rlenc.py <BIN FILENAME>\nOptional usage:\n $ python3 ./rlenc.py <BIN FILENAME> <TRIM SIZE> <MATRIX SIZE>\n  where e.g. $ rlenc.py map1.bin 24 32\n  will only use the first 24 of every 32 bytes.\n\nFile will be output in .rle format.')
    sys.exit()
trim = 0
size = 0

if len(sys.argv) > 2:
    trim = int(sys.argv[2])
    size = int(sys.argv[3])
    #print(trim, size)

def read_m2sfile(file):
    with open(file, 'rb') as f:
        return f.read()

def compress(data):
    i = 1
    totalcount = 0
    o = []
    char = data[0]
    count = 1
        
    while i <= len(data):
        if i == len(data):
            o.append(bytes([char]))
            totalcount += 1
            break
        if size > 0 and trim > 0:
            if (i % size) >= trim:
                i += 1
                continue
        if char == data[i]:
            if count < 255:
                count += 1
                i += 1
                continue
            else:
                totalcount += count
                o.append(bytes([char]))
                o.append(bytes([char]))
                o.append(bytes([count]))
                count = 1
                i += 1
                continue
        else:
            # last char is no longer the same
            totalcount += count
            if count > 1:   # here
                o.append(bytes([char]))
                o.append(bytes([char]))
                o.append(bytes([count]))
            else:
                o.append(bytes([char]))
            char = data[i]
            count = 1
            i += 1
            continue 
        
    print(totalcount, 'bytes compresed to', len(o))
    return o

def loadm2s(input):
    inbytes = read_m2sfile(input)
    ob = compress(inbytes)
    f = None 
    try: 
        f = open(input.split('.')[0]+'.rle', 'wb')
        for b in ob:
            f.write(b)
    finally:
        f.close()

loadm2s(input)
print("File written successfully.")
