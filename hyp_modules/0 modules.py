### MODULES
from bezier_x import *
from letter_pieces_v12 import *






### VARIABLES
apt_hor_inr = 0, 0
apt_ver = 200, 100

tck_hor = 20
tck_ver = 40

ang_inr = 60
ang_otr = 50

sqr_inr = .6
sqr_otr = .6






### INSTRUCTIONS
# si determinano i due punti verticali
apt_ver_inr = apt_ver[0], apt_ver[1] - tck_ver/2
apt_ver_otr = apt_ver[0], apt_ver[1] + tck_ver/2

# si determina l'arco interno
cpt_hor_inr, cpt_ver_inr = cpt_hor_ver(apt_hor_ver=(apt_hor_inr, apt_ver_inr), ang_hor_ver=(ang_inr, 0), sqr_hor_ver=(sqr_inr, sqr_inr))

# x del punto virtuale che giace sull'arco interno
xxx = apt_hor_inr[0] + tck_hor*cos(radians(ang_otr))

# y del punto virtuale che giace sull'arco interno
yyy = getYfromXforBezSegment(apt_hor_inr, cpt_hor_inr, cpt_ver_inr, apt_ver_inr, xxx)

apt_hor_otr = apt_hor_inr[0], yyy + tck_hor*sin(radians(ang_otr))

# si determina l'arco esterno
cpt_hor_otr, cpt_ver_otr = cpt_hor_ver(apt_hor_ver=(apt_hor_otr, apt_ver_otr), ang_hor_ver=(ang_otr, 0), sqr_hor_ver=(sqr_otr, sqr_otr))






### DRAWING
fnt = CurrentFont()

gly = fnt['A']
gly.clear()

pen = gly.getPen()
pen.moveTo(apt_hor_inr)
pen.curveTo(cpt_hor_inr, cpt_ver_inr, apt_ver_inr)
pen.lineTo(apt_ver_otr)
pen.curveTo(cpt_ver_otr, cpt_hor_otr, apt_hor_otr)
pen.closePath()