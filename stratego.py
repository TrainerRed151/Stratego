import random

p = int("0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)
q = (p-1)//2
g = 2

class Piece:
    def __init__(self, sLoc, mine, color, v=0):
        self.sLoc = sLoc
        self.cLoc = sLoc
        self.mine = mine
        self.color = color
        if self.mine:
            self.r = random.randint(1, q-1)
            self.v = v
            self.h = 0
        else:
            self.r = 0
            self.v = 0
            a = random.randint(1, q-1)
            self.h = pow(g, a, p)

    def commit(self, c=0):
        if self.mine:
            self.c = (pow(g, self.v, p)*pow(self.h, self.r, p)) % p
        else:
            self.c = c

    def getH(self, h):
        if self.mine:
            self.h = h

    def setV(self, v):
        if ~self.mine:
            self.v = v

    def setR(self, r):
        if ~self.mine:
            self.r = r

    def verify(self, v, r):
        setV(v)
        setR(r)
        if ~self.mine:
            return self.c == (pow(g, self.v, p)*pow(self.h, self.r, p)) % p
        else:
            return True