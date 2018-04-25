import random

#RFC 2409, group ID 14
p = int("0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF", 16)
q = (p-1)//2
g = 2

size = 10

def cToA(c):
    return chr(ord('A')+c)

def AToc(a):
    return ord(a) - ord('A')

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

    def __str__(self):
        if self.v == 0:
            vv = '?'
        elif self.v == 10:
            vv = 'S'
        elif self.v == 11:
            vv = 'b'
        elif self.v == 12:
            vv = 'F'
        else:
            vv = str(self.v)
        return self.color + vv

    def commit(self, c=0):
        if self.mine:
            self.c = (pow(g, self.v, p)*pow(self.h, self.r, p)) % p
        else:
            self.c = c

    def setH(self, h):
        if self.mine and 0 < h < p:
            self.h = h

    def setV(self, v):
        if ~self.mine:
            self.v = v

    def setR(self, r):
        if ~self.mine:
            self.r = r

    def verify(self, v, r):
        self.setV(v)
        self.setR(r)
        if ~self.mine:
            return self.c == (pow(g, self.v, p)*pow(self.h, self.r, p)) % p
        else:
            return True


class Board:
    def __init__(self, color):
        self.board = []
        for r in range(size):
            temp = []
            for c in range(size):
                val = 0
                if r <= 3:
                    if color == 'R':
                        #val = int(input("%s%d: " % (cToA(c), r)))
                        pass
                    temp.append(Piece((r, c), color=='R', 'R', v=val))
                elif r >= 6:
                    if color == 'B':
                        #val = int(input("%s%d: " % (cToA(c), r)))
                        pass
                    temp.append(Piece((r, c), color=='B', 'B', v=val))
                else:
                    temp.append(None)

            self.board.append(temp)

    def __str__(self):
        s = "  A  B  C  D  E  F  G  H  I  J\n"
        for r in range(size):
            s += "  --" + " --"*(size-1) + " \n%d|" % (size-r-1)
            for c in range(size):
                if (4 <= r <= 5) and ((2 <= c <=3) or (6 <= c <= 7)):
                    s += "XX|"
                elif self.board[9-r][c] == None:
                    s += "  |"
                else: 
                    s += str(self.board[9-r][c]) + "|"
            s += "%d\n" % (size-r-1)
        s += "  --" + " --"*(size-1) + "\n  A  B  C  D  E  F  G  H  I  J"

        return s

    def writeHValues(self, file):
        f = open(file, "w")
        for r in range(size):
            for c in range(size):
                if self.board[r][c] != None:
                    f.write("%s%d: %s\n" % (cToA(c), r, hex(self.board[r][c].h)))

        f.close()

    def readHValues(self, file):
        f = open(file, "r")
        content = [x.strip('\n') for x in f.readlines()]
        for i in range(len(content)):
            data = content[i]
            r = int(data[1])
            c = AToc(data[0])
            self.board[r][c].setH(int(data[4:], 16))

    def writeCValues(self, file):
        f = open(file, "w")
        for r in range(size):
            for c in range(size):
                if self.board[r][c] != None:
                    self.board[r][c].commit()
                    f.write("%s%d: %s\n" % (cToA(c), r, hex(self.board[r][c].c)))

        f.close()

    def readCValues(self, file):
        f = open(file, "r")
        content = [x.strip('\n') for x in f.readlines()]
        for i in range(len(content)):
            data = content[i]
            r = int(data[1])
            c = AToc(data[0])
            self.board[r][c].commit(int(data[4:], 16))
