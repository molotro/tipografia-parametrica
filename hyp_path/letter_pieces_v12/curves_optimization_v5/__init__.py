### Modules
import numpy as np
from math import cos, sin, tan, radians, pi
from utilities_v3 import *



### Constants
LETTER_PIECES = ('quarter', 'shoulder', 'half_spine', 'comma', 'termination', 'b_curve')
BEZIER_TYPES = ('cubic', 'quadratic')




###
def apt_lst(letter_piece, apt_hor_ver, tck_hor_ver, ang_hor_ver, adj_hor_inr_otr, adj_ver_inr_otr):

    assert letter_piece in LETTER_PIECES

    # unwrapping
    apt_hor, apt_ver = apt_hor_ver
    tck_hor, tck_ver = tck_hor_ver
    ang_hor, ang_ver = ang_hor_ver

    adj_hor_inr, adj_hor_otr = adj_hor_inr_otr 
    adj_ver_inr, adj_ver_otr = adj_ver_inr_otr

    apt_hor_x, apt_hor_y = apt_hor
    apt_ver_x, apt_ver_y = apt_ver

    f_hor, f_ver = orientation_function(apt_hor, apt_ver)

    # conditional execution
    if   letter_piece == 'quarter':

        f_apt_ver_otr_x = tan(radians(ang_ver))
        f_apt_ver_otr_y = 1

        f_apt_ver_inr_x = tan(radians(ang_ver))
        f_apt_ver_inr_y = 1

        f_apt_hor_otr_x = 1
        f_apt_hor_otr_y = tan(radians(ang_hor))

        f_apt_hor_inr_x = 1
        f_apt_hor_inr_y = tan(radians(ang_hor))

    elif letter_piece == 'shoulder' or letter_piece == 'termination':

        f_apt_ver_otr_x = tan(radians(ang_ver))
        f_apt_ver_otr_y = 1

        f_apt_ver_inr_x = tan(radians(ang_ver))
        f_apt_ver_inr_y = 1

        f_apt_hor_otr_x = cos(radians(ang_hor))
        f_apt_hor_otr_y = sin(radians(ang_hor))

        f_apt_hor_inr_x = cos(radians(ang_hor))
        f_apt_hor_inr_y = sin(radians(ang_hor))

    elif letter_piece == 'half_spine' or letter_piece == 'comma':

        f_apt_ver_otr_x = cos(radians(ang_ver))
        f_apt_ver_otr_y = sin(radians(ang_ver))

        f_apt_ver_inr_x = cos(radians(ang_ver))
        f_apt_ver_inr_y = sin(radians(ang_ver))

        f_apt_hor_otr_x = 1
        f_apt_hor_otr_y = tan(radians(ang_hor))

        f_apt_hor_inr_x = 1
        f_apt_hor_inr_y = tan(radians(ang_hor))

    if letter_piece == 'comma':
        f_cmm_otr = 0
        f_cmm_inr = 2
    else:
        f_cmm_otr = 1
        f_cmm_inr = 1

    if letter_piece == 'termination':
        f_trm_ver_inr = 1
        f_trm_ver_otr = 1
        f_trm_hor_inr = 2
        f_trm_hor_otr = 0
    else:
        f_trm_ver_inr = 1
        f_trm_ver_otr = 1
        f_trm_hor_inr = 1
        f_trm_hor_otr = 1

    # outer vertical point
    apt_ver_otr_x = apt_ver_x + f_hor * (tck_ver/2 + adj_ver_otr[0]) * f_apt_ver_otr_x * f_cmm_otr * f_trm_ver_otr
    apt_ver_otr_y = apt_ver_y + f_ver * (tck_ver/2 + adj_ver_otr[1]) * f_apt_ver_otr_y * f_cmm_otr * f_trm_ver_otr
    apt_ver_otr = round(apt_ver_otr_x), round(apt_ver_otr_y)

    # inner vertical point
    apt_ver_inr_x = apt_ver_x - f_hor * (tck_ver/2 + adj_ver_inr[0]) * f_apt_ver_inr_x * f_cmm_inr * f_trm_ver_inr
    apt_ver_inr_y = apt_ver_y - f_ver * (tck_ver/2 + adj_ver_inr[1]) * f_apt_ver_inr_y * f_cmm_inr * f_trm_ver_inr
    apt_ver_inr = round(apt_ver_inr_x), round(apt_ver_inr_y)

    # outer horizontal point
    apt_hor_otr_x = apt_hor_x + f_hor * (tck_hor/2 + adj_hor_otr[0]) * f_apt_hor_otr_x * f_cmm_otr * f_trm_hor_otr
    apt_hor_otr_y = apt_hor_y + f_ver * (tck_hor/2 + adj_hor_otr[1]) * f_apt_hor_otr_y * f_cmm_otr * f_trm_hor_otr
    apt_hor_otr = round(apt_hor_otr_x), round(apt_hor_otr_y)

    # inner horizontal point
    apt_hor_inr_x = apt_hor_x - f_hor * (tck_hor/2 + adj_hor_inr[0]) * f_apt_hor_inr_x * f_cmm_inr * f_trm_hor_inr
    apt_hor_inr_y = apt_hor_y - f_ver * (tck_hor/2 + adj_hor_inr[1]) * f_apt_hor_inr_y * f_cmm_inr * f_trm_hor_inr
    apt_hor_inr = round(apt_hor_inr_x), round(apt_hor_inr_y)

    # list
    apt = [apt_ver_otr, apt_hor_otr, apt_hor_inr, apt_ver_inr]
    return apt


### Control points for a single curve
def cpt_hor_ver(apt_hor_ver, ang_hor_ver, sqr_hor_ver):

    # unwrapping
    apt_hor, apt_ver = apt_hor_ver
    ang_hor, ang_ver = ang_hor_ver
    sqr_hor, sqr_ver = sqr_hor_ver
    f_hor  , f_ver   = orientation_function(apt_hor, apt_ver)

    apt_hor_x, apt_hor_y = apt_hor
    apt_ver_x, apt_ver_y = apt_ver

    # vertical line
    m_ver = tan(radians(- f_hor * f_ver * ang_ver))
    q_ver = apt_ver_y - m_ver * apt_ver_x

    # horizontal line
    if ang_hor != 0:
        m_hor = tan(radians(90 + f_hor * f_ver * ang_hor))
        q_hor = apt_hor_y - m_hor * apt_hor_x

        cpt_max = line_intersection(m_ver, q_ver, m_hor, q_hor)

    else:
        cpt_max = (apt_hor_x, m_ver * apt_hor_x + q_ver)

    cpt_hor = interpolate_points(apt_hor, cpt_max, sqr_hor)
    cpt_hor = round(cpt_hor[0]), round(cpt_hor[1])

    cpt_ver = interpolate_points(apt_ver, cpt_max, sqr_ver)
    cpt_ver = round(cpt_ver[0]), round(cpt_ver[1])

    return cpt_hor, cpt_ver


### Full curved piece
def curved_piece(glyph, letter_piece, bez_typ_inr_otr,
                 apt_hor_ver, tck_hor_ver, ang_hor_ver,
                 ang_hor_inr_otr, ang_ver_inr_otr,
                 sqr_inr_hor_ver, sqr_otr_hor_ver,
                 adj_hor_inr_otr, adj_ver_inr_otr,
                 clockwise):

    assert letter_piece in LETTER_PIECES
    assert (bez_typ_inr_otr[0] in BEZIER_TYPES) and (bez_typ_inr_otr[1] in BEZIER_TYPES)

    # orientation
    f_hor, f_ver = orientation_function(apt_hor_ver[0], apt_hor_ver[1])

    # unwrapping
    ang_hor_inr, ang_hor_otr = ang_hor_inr_otr
    ang_ver_inr, ang_ver_otr = ang_ver_inr_otr

    adj_hor_inr, adj_hor_otr = adj_hor_inr_otr 
    adj_ver_inr, adj_ver_otr = adj_ver_inr_otr

    sqr_inr_hor, sqr_inr_ver = sqr_inr_hor_ver
    sqr_otr_hor, sqr_otr_ver = sqr_otr_hor_ver

    # anchor points
    apt = apt_lst(letter_piece, apt_hor_ver, tck_hor_ver, ang_hor_ver, adj_hor_inr_otr, adj_ver_inr_otr)
    apt_ver_otr = apt[0]
    apt_hor_otr = apt[1]
    apt_hor_inr = apt[2]
    apt_ver_inr = apt[3]

    # outer control points
    cpt_otr = cpt_hor_ver((apt_hor_otr, apt_ver_otr), (ang_hor_otr, ang_ver_otr), sqr_otr_hor_ver)
    cpt_hor_otr = cpt_otr[0]
    cpt_ver_otr = cpt_otr[1]

    # inner control points
    cpt_inr = cpt_hor_ver((apt_hor_inr, apt_ver_inr), (ang_hor_inr, ang_ver_inr), sqr_inr_hor_ver)
    cpt_hor_inr = cpt_inr[0]
    cpt_ver_inr = cpt_inr[1]

    # drawing
    apt = [apt_hor_otr, apt_ver_otr, apt_ver_inr, apt_hor_inr]
    cpt = [cpt_hor_otr, cpt_ver_otr, cpt_ver_inr, cpt_hor_inr]

    if clockwise == True and f_hor * f_ver == -1:
        draw_crv_pcs(glyph, apt, cpt, bez_typ_inr_otr)
    else:
        draw_crv_pcs(glyph, apt[::-1], cpt[::-1], bez_typ_inr_otr)

    return apt