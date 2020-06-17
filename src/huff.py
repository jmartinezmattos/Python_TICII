import mmap
import struct
import sys
from heapq import heappush, heappop, heapify
from collections import defaultdict

def table(txt):

    symb2freq = defaultdict(int)

    for ch in txt:
        symb2freq[ch] += 1

    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def codificar(tabla, texto):
    dict_huff = {}

    for num in tabla:
        dict_huff[num[0]] = num[1]

    txt_bin = ''

    for letra in texto:
        txt_bin += dict_huff[letra]

    return txt_bin

def to_binary(entrada, bits=8, pack_format = 'B'):


    byte_list = []
    for i in range(0, len(entrada), bits):  # separo en bytes
        byte_list.append(entrada[i:(i + bits)])

    while len(byte_list[-1]) != bits:  # hacemos que el ultimo byte este completo
        byte_list[-1] += '0'

    final_list = []
    pack_form = '!' + pack_format
    for x in byte_list:
        final_list.append(struct.pack(pack_form, int(x, 2)))

    return final_list


if __name__ == '__main__':

    archivo = sys.argv[1]

    f = open(archivo, "r")

    #Esto hay que cambiarlo por mmap
    #txt = f.read()

    txt = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    huff = table(txt)

    codigo_string = codificar(huff, txt)

    #print(codigo_string)

    final_list = to_binary(codigo_string)

    #print(final_list)

    # make file
    newFile = open("nuevo", "wb")
    # write to file
    for x in final_list:
        newFile.write(x)
