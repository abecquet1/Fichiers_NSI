from random import randint
from math import sqrt, gcd

def est_premier(n):
    """teste si n est premier"""
    if n<2:
        return False
    for d in range(2,int(sqrt(n)+1)):
        if n%d==0:
            return False
    return True


def euclide(a,b):
    """algorithme d'euclide étendu renvoyant r, u, v tq r = pgcd(a,b), au+bv = r"""
    r, u, v, rp, up, vp = a, 1, 0, b, 0, 1
    while rp != 0:
        q = r//rp
        r, u, v, rp, up, vp = rp, up, vp, r - q *rp, u - q*up, v - q*vp
    return (r,u,v)

def premier(N, interdit = 0):
    """renvoie un nombre premier aléatoire à N octets différent de interdit"""
    p = randint(256**(N-1), 256**N-1)
    p = p+1-p%2
    while not(est_premier(p)) or p == interdit:
        p+=2
    return p

def exposants(phi):
    """renvoie e premier avec phi et d, l'inverse modulo phi de e (e*u mod phi = 1)"""
    e = 0
    pgcd = 100
    while pgcd!=1:
        e = randint(1,phi)
        pgcd, u, v = euclide(e, phi)
    return e, u%phi

def generer_cles(taille = 4):
    p = premier(taille//2)
    q = premier(taille//2, p)
    n = p*q
    phi = (p-1)*(q-1)
    e, d = exposants(phi)
    return n, e, d

def nb_octets(n):
    """renvoie le nombre d'octet minimum sur lequel on peut encoder le nombre n"""
    res = 1
    puis = 256
    while n>puis:
        puis*=256
        res+=1
    return res

def exporter_cle(n, k):
    """renvoie un bytes contenant n et e"""
    N = nb_octets(n)
    return int.to_bytes(n, N, 'big')+int.to_bytes(k, N, 'big')

def importer_cle(b):
    n = int.from_bytes(b[:len(b)//2], 'big')
    k = int.from_bytes(b[len(b)//2:], 'big')
    return n, k

def chiffrer(b, n, k):
    """chiffre un message avec la clé k = e ou d"""
    res = b""
    N = nb_octets(n)-1 # taille des paquets

    for i in range(len(b)//N):
        x = int.from_bytes(b[N*i:N*(i+1)], 'big')
        y = pow(x, k, n)
        res+=int.to_bytes(y, N+1, 'big')
    reste = len(b)%N
    if reste > 0:
        x = int.from_bytes(b[-reste:], 'big')
        y = pow(x, k, n)
        res+=int.to_bytes(y, N+1, 'big')
    res+=int.to_bytes(reste, 4, 'big')
    return res

def dechiffrer(b, n, k):
    """déchiffre un message chiffré avec la clé k = e ou d"""
    res = b""
    N = nb_octets(n) # taille des paquets

    reste = int.from_bytes(b[-4:], 'big')
    if reste > 0:
        b, fin = b[:-N-4], b[-N-4:-4]
    else:
        b = b[:-4]

    for i in range(len(b)//N):
        x = int.from_bytes(b[N*i:N*(i+1)], 'big')
        y = pow(x, k, n)
        res+=int.to_bytes(y, N-1, 'big')

    if reste > 0 :
        x = int.from_bytes(fin, 'big')
        y = pow(x, k, n)
        res+=int.to_bytes(y, reste, 'big')
    return res

