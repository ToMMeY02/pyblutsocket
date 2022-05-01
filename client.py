import random 
import math
import sys
from Crypto.Cipher import AES
import socket
from sympy import symbols
from sympy.solvers.diophantine.diophantine import diop_solve





def generateur_tup () : 
    val1,val2,val3 = random.randint(3,400) , random.randint(3,400) , random.randint(3,400)
    if val1 <= val2  or val3%math.gcd(val1 , val2) != 0 :
        return generateur_tup()
    else :
        return (val1,val2,val3)


def solver(val1,val2,val3) :
    x, y= symbols("x, y", integer=True)
    return diop_solve(val1*x + val2*y - val3)

def toBinary(a):
    l,m=[],[]
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(bin(i)[2:])
    a = "".join(m)
    return  a


def nskey(key) : 
    if len(key) <= 13:
        key_bin = toBinary(key)
        k = int(key_bin , 2) % (2**104)
        key_bin = bin(k)[2:]
        key_bin = key_bin + (128 - len(key_bin))* '0'
        iii = int(key_bin , 2)
        return iii.to_bytes(16 , byteorder='big')
    else :
        key1 = ''
        for lettre in key:
            if lettre.isupper() :
                key1 = key1 + str(ord(lettre) %  ord('A'))
            elif lettre.islower() :
                key1 = key1 + str(ord(lettre) %  ord('a'))
            else :
                key1 = key1 +lettre
        key1 = int(key1) % (2**104)
        key_bin = bin(key1)[2:]
        key_bin = key_bin + (128 - len(key_bin))* '0'
        iii = int(key_bin , 2)
        return iii.to_bytes(16 , byteorder='big')
    
def nskeywithz(key_byes,z):
    z = z % (2**24)
    return key_byes[:-3] + z.to_bytes(3, byteorder='big')
        
            
    
        


def encrypt(msg , key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce  = cipher.nonce
    ciphertext , _ = cipher.encrypt_and_digest(msg)
    return ciphertext+nonce  


def solution (a , k):
    t_0 = symbols("t_0", integer=True)
    sulution = a.subs({t_0 : k})
    return int(sulution[0])**2 + int(sulution[1])**2 



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("vous  avez pas saisis le numéro de série")
        sys.exit(1)
    k = 0
    key = nskey(sys.argv[1])
    val1,val2,val3 = generateur_tup()
    triple = "{} , {} , {} ".format(str(val1) ,str(val2) , str(val3))
    serverMACAddress = '00:1A:7D:DA:71:13'
    port = 6667
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.connect((serverMACAddress,port))
    val1,val2,val3  = generateur_tup()
    tt = ','.join([str(val1),str(val2),str(val3)])
    tt="tripler "+tt
    a = solver(val1,val2,val3)
    e = encrypt(bytes(tt, 'UTF-8') , key)
    s.send(e)
    while 1:
        text = input("LAY LAY :  ")
        if text == "quit":
            break
        
        z = solution(a, k) 
        kkk = nskeywithz(key,z)
        val1,val2,val3  = generateur_tup()
        tt = ','.join([str(val1),str(val2),str(val3)])
        data =bytes(tt+"data:"+text, 'UTF-8')
        c2 = encrypt(data , kkk)
        s.send(c2)
        a = solver(val1,val2,val3)
        k = 0
    s.close()    
    
   