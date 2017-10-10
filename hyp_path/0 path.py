### MODULES
from letter_pieces_v12 import * 






### VARIABLES
apt_hor = 0, 0
apt_ver = 150, 200

tck_hor = 30
tck_ver = 70

ang_inr = 30
ang_otr = 10

sqr_inr = .8
sqr_otr = .6

acc = 100






### FUNCTIONS
def calc_dist(p1, p2):
    d = sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    return d






### INSTRUCIONS

### Determinare lo scheletro
ang_skl = (ang_inr + ang_otr)/2
sqr_skl = (sqr_inr + sqr_otr)/2

cpt_hor, cpt_ver = cpt_hor_ver(apt_hor_ver = (apt_hor, apt_ver), ang_hor_ver = (ang_skl, 0), sqr_hor_ver = (sqr_skl, sqr_skl))



### Ricerca approssimata del punto intermedio
points = []

for i in range(acc):

    t = 1/acc*i

    pA = [apt_hor, cpt_hor, cpt_ver, apt_ver]

    x0 = pA[0][0]
    x1 = pA[1][0]
    x2 = pA[2][0]
    x3 = pA[3][0]


    pB = []
    for i in range(len(pA)-1):
        p = interpolate_points(pA[i], pA[i+1], t)
        pB.append(p)

    pC = []
    for i in range(len(pB)-1):
        p = interpolate_points(pB[i], pB[i+1], t)
        pC.append(p)

    pD = []
    for i in range(len(pC)-1):
        p = interpolate_points(pC[i], pC[i+1], t)
        pD.append(p)

    apt_mid = pD[0]

    m = m_q_from_apt(pC[0], pC[1])[0]

    q = apt_mid[1] - (1/m)*apt_mid[0]

    y = (1/m)*apt_hor[0] + q

    dst = calc_dist(apt_mid, (apt_hor[0], y))

    if dst > tck_hor/2:
        break

    points.append((apt_hor[0], y))



apt_hor_otr = points[-1]
apt_hor_inr = apt_hor[0], 2*apt_hor[1] - apt_hor_otr[1]

apt_ver_otr = apt_ver[0], apt_ver[1] + tck_ver/2
apt_ver_inr = apt_ver[0], apt_ver[1] - tck_ver/2


# archi
cpt_hor_otr, cpt_ver_otr = cpt_hor_ver(apt_hor_ver = (apt_hor_otr, apt_ver_otr), ang_hor_ver = (ang_otr, 0), sqr_hor_ver = (sqr_otr, sqr_otr))
cpt_hor_inr, cpt_ver_inr = cpt_hor_ver(apt_hor_ver = (apt_hor_inr, apt_ver_inr), ang_hor_ver = (ang_inr, 0), sqr_hor_ver = (sqr_inr, sqr_inr))






### Disegno test
fnt = CurrentFont()

gly = fnt['A']
gly.clear()

pen = gly.getPen()
pen.moveTo(apt_hor_inr)
pen.curveTo(cpt_hor_inr, cpt_ver_inr, apt_ver_inr)
pen.lineTo(apt_ver_otr)
pen.curveTo(cpt_ver_otr, cpt_hor_otr, apt_hor_otr)
pen.closePath()