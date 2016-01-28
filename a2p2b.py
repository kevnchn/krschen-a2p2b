# a2p2b.py
# CO 487 - Assignment 2, Problem 2b
# January 29, 2016
# Description: Finds magnitude of bias given plaintext-ciphertext pairs stored in files
# Collaborators: Kevin Rui Shen Chen, Cindy You


def mapxint(y_int):
    sbox_mapping = [[0,14],[1,4],[2,13],[3,1],[4,2],[5,15],[6,11],[7,8],[8,3],[9,10],[10,6],[11,12],[12,5],[13,9],[14,0],[15,7]]
    u4 = [i for i in sbox_mapping if i[1] == y_int]
    return u4[0][0]
    
def getMagnitudeBias():
    cipher_text_lines = [line.rstrip('\n') for line in open('ciphertext84.txt')] # change file source according to UWID
    plain_text_lines = [line.rstrip('\n') for line in open('plaintexts.txt')]
    u4 = ''
    v4 = ''
    sbox1 = ''
    sbox2 = ''
    la_list = []
    mag_bias_key = ''
    mag_bias_lin_approx = 10000
    linApprox = 0
    for partial_key in range(0,256): 
        partial_key_string = format(partial_key, '08b')
        plain_index = 0
        la_list = []
        for cipher_lines in cipher_text_lines:
            u4 = ''
            v4 = ''
            cipher_lines = cipher_lines[4:8] + cipher_lines[12:]
            key_index = 0
            for cipher_bit in cipher_lines:
                v4 = v4 + str(int(partial_key_string[key_index]) ^ int(cipher_bit))
                key_index = key_index + 1
            sbox1 = int(v4[:4],2)
            u4 = u4 + format(mapxint(sbox1), '04b')
            sbox2 = int(v4[4:],2)
            u4 = u4 + format(mapxint(sbox2), '04b')
            la_list.append([u4[1], u4[3], u4[5], u4[7], plain_text_lines[plain_index][4], plain_text_lines[plain_index][6], plain_text_lines[plain_index][7]])
            plain_index+=1
        linApprox = calculateLinApprox(la_list)
        if abs(10000-linApprox) > abs(10000-mag_bias_lin_approx):
            mag_bias_lin_approx = linApprox
            mag_bias_key = partial_key_string
        print "partial key: " + partial_key_string + " Linear Approximation:" + str(linApprox) + "/20000"
    print "RESULT - Partial key string: " + mag_bias_key + " Linear Approximation:" + str(mag_bias_lin_approx) + "/20000" + " Magnitude of Bias:" + str(abs(10000-mag_bias_lin_approx)) + "/20000"
    
def calculateLinApprox(la_list):
    linapprox = 0
    for la in la_list:
        la_value = int(la[0]) ^ int(la[1]) ^ int(la[2]) ^ int(la[3]) ^ int(la[4]) ^ int(la[5]) ^ int(la[6])
        if la_value == 0:
            linapprox = linapprox + 1
    return linapprox
    
def main():
    getMagnitudeBias()
                    
main()