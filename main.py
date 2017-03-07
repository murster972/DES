#!/usr/bin/env python3
import os
import sys
import base64
import random

class DES:
    def __init__(self, pt="", ct="", key=""):
        self.pt = pt
        self.key = key

        self.key_err = "Key must be 64-bits longs and represented as bin str i.e '1010110...'."

    def encrypt(self):
        if len(self.key) != 64 or not isinstance(self.key, str): raise KeyErrorException(self.key_err)
        if not isinstance(self.pt, str): raise PlaintextTypeException("Plaintext must be a string.")

        #puts text into 64-bit blocks
        blocks = self.get_blocks(self.pt)
        ct_blocks = []

        round_keys = self.key_schedule()

        #goes through each block performing initial permuation, 16 rounds of fiestel_network, and
        #then final permutation
        for i in blocks:
            #intial permutation
            perm = self.permutations("initial", i)
            #split into left and right halfs
            lt, rt = perm[:32], perm[32:]

            #16 rounds
            for r in range(16):
                f = self.f_function(rt, round_keys[r])
                lt = bin(int(lt, 2) ^ int(f, 2))[2:]
                lt = ("0" * (32 - len(lt))) + lt
                lt, rt = rt, lt
            #lt, rt = rt, lt
            p = self.permutations("final", rt + lt)
            ct_blocks.append(p)


    def decrypt(self):
        pass

    def fiestel_network(self):
        pass

    '''f-function - performs expansion, XOR with round-key and sboxes'''
    def f_function(self, r, k):
        e = self.permutations("E", r)
        e_xor_k = bin(int(e, 2) ^ int(k, 2))[2:]
        e_xor_k = ("0" * (48 - len(e_xor_k))) + e_xor_k

        sboxes = {1: [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
                  2: [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 24, 9]],
                  3: [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
                  4: [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 9, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
                  5: [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
                  6: [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
                  7: [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
                  8: [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]}

        six_bits = [e_xor_k[x:x + 6] for x in range(0, 48, 6)]
        four_bits = []
        for i in range(8):
            s = six_bits[i]
            f = bin(sboxes[i + 1][int(s[0] + s[5], 2)][int(s[1:5], 2)])[2:]
            four_bits.append(("0" * (4 - len(f))) + f)

        return self.permutations("P", "".join(four_bits))

    '''Convers stream of text into 64-bit binary blocks, by first
    converting to binary string and padding each ascii char to 8-bits,
    then padding binary string so its length is divisible by 64 by
    prepending zeros
    :param t: string to convert into 64-bit blocks
    :return blocks: 64-bit blocks of binary strings'''
    def get_blocks(self, t):
        bin_t = ""
        for i in t:
            b = bin(ord(i))[2:]
            bin_t += ("0" * (8 - len(b))) + b

        bin_t = ("0" * (len(bin_t) % 64)) + bin_t
        blocks = [bin_t[x:x + 64] for x in range(0, len(bin_t), 64)]
        return blocks

    def permutations(self, p, t):
        perms = {"initial": [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7],
                 "final": [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25],
                 "PC-1": [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 13, 4],
                 "PC-2": [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32],
                 "E": [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1],
                 "P": [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]}

        return "".join([t[x - 1] for x in perms[p]])

    ''' returns 16 round keys generated from the main key '''
    def key_schedule(self):
        #removes every parity - 8th - bit, and performs pc-1(permutated choice 1)
        k = self.permutations("PC-1", self.key)
        CD = k

        round_keys = []
        #NOTE: Unsure if the rotation occurs in both C and D, or if together in CD
        for i in range(16):
            if i + 1 in [1, 2, 9, 16]: CD = CD[1:] + CD[0]
            else: CD = CD[2:] + CD[:2]
            round_keys.append(self.permutations("PC-2", CD))
        return round_keys

class KeyErrorException(Exception):
    pass

if __name__ == '__main__':
    #not secure, user should not be allowed to pass key for encryption, for demo purposes only
    #TODO: have DES generate key for encryption
    key = "0011000011100000100110001001000111000100100010000100110000111010"
    pt = "Hello World!"
    d = DES(pt=pt, key=key)
    d.encrypt()
