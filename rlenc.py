# RLE FILE ENCODER
#  takes any binary file and converts to RLE sequenced
#
# Input: any raw binary
# Output: Encoded w/ RLE, optionally trimmed square
#              Input $ff $ff $ff $ff $aa $ff 
#                 == $ff $ff $04 $aa $ff
# w/ 5 byte trim  == $ff $ff $04 $aa

# $ python3 ./rlenc.py <BIN FILENAME> (-b)

# OR: $ python3 ./rlenc.py <BIN FILENAME> (-b) <BYTESREAD> <BYTEBOUNDARY>

#    e.g. python3 ./rlenc.py file.bin 24 32
#   will read the first 24 out of every 32 bytes
#   from file.bin and compress it to file.rle.

# (c) 2019 Ben Ferguson

import os 
import sys 
import math 

input = sys.argv[1]

algorithm = 0

if len(sys.argv) == 1:
    print('Usage:\n $ python3 ./rlenc.py <BIN FILENAME>\nOptional usage:\n $ python3 ./rlenc.py <BIN FILENAME> <TRIM SIZE> <MATRIX SIZE>\n  where e.g. $ rlenc.py map1.bin 24 32\n  will only use the first 24 of every 32 bytes.\n\nFile will be output in .rle format.')
    sys.exit()

if len(sys.argv) == 3:
    if sys.argv[2] != "-b":
        print('Usage:\n $ python3 ./rlenc.py <BIN FILENAME>\nOptional usage:\n $ python3 ./rlenc.py <BIN FILENAME> <TRIM SIZE> <MATRIX SIZE>\n  where e.g. $ rlenc.py map1.bin 24 32\n  will only use the first 24 of every 32 bytes.\n\nFile will be output in .rle format.')
        sys.exit()
    else:
        algorithm = 1

trim = 0
size = 0


if len(sys.argv) == 4:
    trim = int(sys.argv[2])
    size = int(sys.argv[3])
    #print(trim, size)
if len(sys.argv) == 5:
    if sys.argv[2] != "-b":
        print('Usage:\n $ python3 ./rlenc.py <BIN FILENAME>\nOptional usage:\n $ python3 ./rlenc.py <BIN FILENAME> <TRIM SIZE> <MATRIX SIZE>\n  where e.g. $ rlenc.py map1.bin 24 32\n  will only use the first 24 of every 32 bytes.\n\nFile will be output in .rle format.')
        sys.exit()
    else:
        algorithm = 1
        trim = int(sys.argv[3])
        size = int(sys.argv[4])
    

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
            totalcount += count
            if count > 1:
                o.append(bytes([char]))
                o.append(bytes([count]))
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
        
    print(totalcount, 'bytes compresed to', len(o), 'using algorithm A.\n e.g. ff ff ff ff 0a ff  =>  ff ff 04 0a ff')
    return o

def compress_b(data):
    i = 1
    totalcount = 0
    o = []
    char = data[0]
    count = 1
        
    while i <= len(data):
        if i == len(data):
            o.append(bytes([count]))
            o.append(bytes([char]))
            totalcount += count
            break
        if char == data[i]:
            count += 1
            if count == 255:
                totalcount += count
                o.append(bytes([count]))
                o.append(bytes([char]))
                count = 0
            i += 1
            continue 
        else:
            totalcount += count
            o.append(bytes([count]))
            o.append(bytes([char]))
            count = 1
            char = data[i] 
            i += 1
            continue 
    print(totalcount, 'bytes compresed to', len(o), 'using algorithm B.\n e.g. ff ff ff ff 0a ff  =>  04 ff 01 0a 01 ff')
    return o

def loadm2s(input):
    inbytes = read_m2sfile(input)
    global algorithm 
    if algorithm == 0:
        ob = compress(inbytes)
    else:
        ob = compress_b(inbytes)
    f = None 
    try: 
        f = open(input.split('.')[0]+'.rle', 'wb')
        for b in ob:
            f.write(b)
    finally:
        f.close()

loadm2s(input)
print("File written successfully.")
