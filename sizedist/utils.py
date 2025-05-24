# http://www.vendian.org/mncharity/dir3/blackbody/UnstableURLs/bbr_color.html
fil = open('bbcolor.txt')
col = []
while True:
    s = fil.readline()
    fil.readline()
    if not s:
        break
    col.append(s.split()[-1])

def colorof(T):
    n = round(T/100)-10
    return col[n]

rsol = 2.3
pc = 1e8

def reel(s):
    s = s.split()
    if len(s) == 0:
        return
    print(s)
    rad = float(s[0])*rsol
    dis = float(s[1])*pc
    ad = 2*rad/dis / 5e-9
    T = float(s[2])
    M = float(s[3])
    if '~' in s[4]:
        g = 0
    else:
        lg = float(s[4])
        g = 10**(lg-2)
    dx = float(s[5])
    dy = float(s[6])
    name = ' '.join(s[7:])
    return name,M,rad,T,g,dis,dx,dy

