import mmap
import os
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

def create_name(name):
    i = 0
    nombre_final = ''
    while name[i] != '.':
        nombre_final += name[i]
        i += 1
    nombre_final += '.huf'
    return nombre_final

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

def crear_cabezal(archivo, sym_arraylen, sym_arraysize, magic):

    magic_nbr = struct.pack('!H', magic)#dos bytes
    sym_arraylen = struct.pack('B',sym_arraylen)#un byte
    sym_arraysize = struct.pack('!B', sym_arraysize) #no se si esto esta bien le puse 8 por la cantidad de bits
    filelen = struct.pack('!I', os.path.getsize(archivo))#cuatro bytes

    cabezal = [magic_nbr, sym_arraylen, sym_arraysize, filelen]

    return cabezal

def elements_array(huff):

    lista_total = []

    for x in huff:
        lista_individual = []
        #Primer byte es el simbolo
        lista_individual.append(struct.pack('!B', ord(x[0])))
        #Segundo byte es valor entero que indica cantidad de bits que usa el codigo huffman
        lista_individual.append(struct.pack('!B', len(x[1])))
        #bytes del 3 al 6 son el codigo huffman
        lista_individual.append(struct.pack('!i', int(x[1], 2)))

        #agregamos a la lista total
        lista_total.append(lista_individual)

    return lista_total

if __name__ == '__main__':

    archivo = sys.argv[1]

    f = open(archivo, "r")

    txt = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    huff = table(txt)

    print(huff)

    codigo_string = codificar(huff, txt)

    final_list = to_binary(codigo_string)

    elementos = elements_array(huff)

    cabezal = crear_cabezal(archivo, len(elementos), 6, 55555)

    newFile = open(create_name(archivo), "wb")

    for x in cabezal:
        newFile.write(x)

    for x in elementos:
        for y in x:
            newFile.write(y)

    for x in final_list:
        newFile.write(x)
