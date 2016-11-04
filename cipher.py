'''
@Title: cipher.py
@Author: Nathan North
@Org: North
@Description: Encoding and Decoding library!
'''
 
def ENCODE(plainText, passcode):
    passLen = len(passcode)
    cipherText = ''
    count = 0
    i = 0
    for character in plainText:
        haNum = ord(character) #Ascii Number
        cyNum = ord(passcode[count])^haNum
        cChar = format(cyNum, '#04x')
        cipherText = cipherText + cChar
        count = i%passLen
        i += 1
    return cipherText
 
def DECODE(cipherText, passcode):
    passLen = len(passcode)
    textLen = int(len(cipherText)/4)
    plainText = ''
    count = 0
    itt = 0
    for i in range(textLen):
        aNum = int(cipherText[itt:itt+4], 16) #Ascii Number
        ciNum = ord(passcode[count])^aNum
        cChar = chr(ciNum)
        plainText = plainText + cChar
        count = i%passLen
        itt += 4
    return plainText
 

