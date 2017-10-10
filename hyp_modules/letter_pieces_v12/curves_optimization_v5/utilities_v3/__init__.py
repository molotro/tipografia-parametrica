### Modules
import numpy as np
from math import *




### Interpolation
def interpolate_values(v1, v2, f):
    I = v1 + (v2 - v1) * f
    return I


def interpolate_points(p1, p2, f):
    xI = interpolate_values(p1[0], p2[0], f)
    yI = interpolate_values(p1[1], p2[1], f)
    pI = xI, yI
    return pI




### Drawing
def draw_ply(glyph, lst_pts):
    pen = glyph.getPen()
    pen.moveTo(lst_pts[0])
    for pts in lst_pts[1:]:
        pen.lineTo(pts)
    pen.closePath()


def draw_crv(pen, cpt_1, cpt_2, apt_2, bez_typ):
    if bez_typ == 'cubic':
        pen.curveTo(cpt_1, cpt_2, apt_2)
    else:
        pen.qCurveTo(cpt_1, cpt_2, apt_2)


def draw_crv_pcs(glyph, apt, cpt, bez_typ_inr_otr):

    # unwrapping
    apt_1, apt_2, apt_3, apt_4 = apt
    cpt_1, cpt_2, cpt_3, cpt_4 = cpt
    bez_typ_inr, bez_typ_otr = bez_typ_inr_otr

    # drawing
    pen = glyph.getPen()
    pen.moveTo(apt_1)
    draw_crv(pen, cpt_1, cpt_2, apt_2, bez_typ_otr)
    pen.lineTo(apt_3)
    draw_crv(pen, cpt_3, cpt_4, apt_4, bez_typ_inr)
    pen.closePath()




### Maths
def m_q_from_apt(p1, p2):

    # unwrapping
    p1_x, p1_y = p1
    p2_x, p2_y = p2

    # line 1-2 equation
    m = (p2_y - p1_y) / (p2_x - p1_x)
    q = -m * p1_x + p1_y

    return m, q


def m_q_from_ang(apt, ang):

    # unwrapping
    apt_x, apt_y = apt

    m = tan(radians(ang))
    q = apt_y - m * apt_x

    return m, q


def line_intersection(m1, q1, m2, q2):

    # intersection
    A = np.array([[m1, -1],[m2, -1]])
    B = np.array([-q1, -q2])
    C = np.linalg.solve(A, B)
    s = float(C[0]), float(C[1])

    return s




###
def orientation_function(apt_hor, apt_ver):

    apt_hor_x = apt_hor[0]
    apt_hor_y = apt_hor[1]

    apt_ver_x = apt_ver[0]
    apt_ver_y = apt_ver[1]

    if apt_hor_x > apt_ver_x:
        if apt_hor_y < apt_ver_y:
            f_hor = +1
            f_ver = +1
        else:
            f_hor = +1
            f_ver = -1
    else:
        if apt_hor_y < apt_ver_y:
            f_hor = -1
            f_ver = +1
        else:
            f_hor = -1
            f_ver = -1

    return f_hor, f_ver