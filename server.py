import socket
from Crypto.Cipher import AES
import sys
import random 
import math
from sympy import symbols
from sympy.solvers.diophantine.diophantine import diop_solve


def solver(val1,val2,val3) :
    x, y= symbols("x, y", integer=True)
    return diop_solve(val1*x + val2*y - val3)


def generateur_tup () : 
    val1,val2,val3 = random.randint(3,400) , random.randint(3,400) , random.randint(3,400)
    if val1 <= val2  or val3%math.gcd(val1 , val2) != 0 :
        return generateur_tup()
    else :
        return (val1,val2,val3 )



def toBinary(a):
    l,m=[],[]
    for i in a:
        l.append(ord(i))
    for i in l:
        m.append(bin(i)[2:])
    a = "".join(m)
    return  a


def decrypt(nonce , ciphertext  , key) : 
    cipher = AES.new(key, AES.MODE_EAX , nonce = nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


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


def check_tripler (s):
    s = s.decode("utf-8") 
    return s.startswith("tripler ")

def triple_val(l) :
    m  = l.replace("tripler ","")
    ll = m.split(',')
    iii = []
    for i in ll :
        iii.append(int(i))
    return iii
def solution (a , k):
    t_0 = symbols("t_0", integer=True)
    sulution = a.subs({t_0 : k})
    return int(sulution[0])**2 + int(sulution[1])**2 

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("vous  avez pas saisis le numéro de série")
        sys.exit(1)
    hostMACAddress = '00:1A:7D:DA:71:13' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
    port = 6667 # 3 is an arbitrary choice. However, it must match the port used by the client.
    backlog = 1
    size = 1024
    key = nskey(sys.argv[1])
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((hostMACAddress,port))
    s.listen(backlog)
    try:
        client, address = s.accept() 
        first = True
        k = 0
        while 1:
            data = client.recv(size)
            if data and first:
                t = decrypt(data[-16:] ,data[:-16] ,key )
                print("ta3 la boucle :", end=" ")
                print(check_tripler(t))
                m = t.decode("utf-8")
                print(m)
                a  = triple_val(m)
                eq  = solver(a[0] , a[1] , a[2])
                first = False 
            elif data and not first :
                z = solution(eq , k) 
                kkk = nskeywithz(key,z)
                t = decrypt(data[-16:] ,data[:-16] ,kkk)
                l = t.decode('utf-8').split('data:')
                print("ta3 la boucle :", end=" ")
                print(l[1])
                a = triple_val(l[0])
                # print(a)
                eq  = solver(a[0] , a[1] , a[2])
                
                
    except:	
        print("Closing socket")	
        client.close()
        s.close()
    