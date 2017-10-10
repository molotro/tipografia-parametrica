#!/usr/bin/env python
# -*- coding: utf-8 -*-



"""
Letter pieces, a script by I Triennio 16-17 ISIA Urbino
Fixed and optimized by Giovanni Abbatepaolo
"""



### Modules
from robofab.world import *

from math import atan, sin, cos, radians, tan, pi
import numpy as np

from curves_optimization_v5 import *




### Constants
ACCEPTED_ORIENTATIONS = ('NW', 'NE', 'SE', 'SW')
LETTER_PIECES = ('quarter', 'shoulder', 'half_spine', 'comma', 'termination')
BEZIER_TYPES  = ('quadratic', 'cubic')




### Functions
def stem(glyph, opt, thickness, height, ang_top_bot, ang_lft_rgt, clockwise):

    # unwrapping
    opt_x, opt_y = opt
    ang_top, ang_bot = ang_top_bot
    ang_lft, ang_rgt = ang_lft_rgt

    # points
    apt_bot_lft = (round(opt_x - thickness/2                                 ), round(opt_y          - thickness/2 * tan(radians(ang_bot))))
    apt_bot_rgt = (round(opt_x + thickness/2                                 ), round(opt_y          + thickness/2 * tan(radians(ang_bot))))
    apt_top_lft = (round(opt_x - thickness/2 + height * tan(radians(ang_lft))), round(opt_y + height - thickness/2 * tan(radians(ang_top))))
    apt_top_rgt = (round(opt_x + thickness/2 - height * tan(radians(ang_rgt))), round(opt_y + height + thickness/2 * tan(radians(ang_top))))

    # list
    pts = [apt_bot_lft, apt_bot_rgt, apt_top_rgt, apt_top_lft]

    # drawing
    if clockwise == True:
        draw_ply(glyph, pts[::-1])
    else:
        draw_ply(glyph, pts)

    return pts



def bar(glyph, opt, length, thickness, ang_top_bot, ang_lft_rgt, clockwise):

    # unwrapping
    opt_x, opt_y = opt
    ang_top, ang_bot = ang_top_bot
    ang_lft, ang_rgt = ang_lft_rgt

    # points
    apt_bot_lft = (round(opt_x          - thickness/2 * tan(radians(ang_lft))), round(opt_y - thickness/2                                 ))
    apt_bot_rgt = (round(opt_x + length - thickness/2 * tan(radians(ang_rgt))), round(opt_y - thickness/2 + length * tan(radians(ang_bot))))
    apt_top_lft = (round(opt_x          + thickness/2 * tan(radians(ang_lft))), round(opt_y + thickness/2                                 ))
    apt_top_rgt = (round(opt_x + length + thickness/2 * tan(radians(ang_rgt))), round(opt_y + thickness/2 - length * tan(radians(ang_top))))

    # list
    pts = [apt_bot_lft, apt_bot_rgt, apt_top_rgt, apt_top_lft]

    # drawing
    if clockwise == True:
        draw_ply(glyph, pts[::-1])
    else:
        draw_ply(glyph, pts)

    return pts



def leg(glyph, apt_top_bot, cor_top_bot, ang_top_bot, thickness, clockwise):

    # unwrapping
    apt_top, apt_bot = apt_top_bot
    cor_top, cor_bot = cor_top_bot
    ang_top, ang_bot = ang_top_bot

    assert apt_top[1] > apt_bot[1]

    # calculating anchor points
    leg_ang = atan(abs(apt_top[1]-apt_bot[1])/abs(apt_top[0]-apt_bot[0]))

    apt_top_rgt_y = apt_top[1]
    apt_top_rgt_x = apt_top[0] + (thickness/2) / sin(leg_ang)

    apt_top_lft_y = apt_top[1]
    apt_top_lft_x = apt_top[0] - (thickness/2) / sin(leg_ang)

    apt_bot_rgt_y = apt_bot[1]
    apt_bot_rgt_x = apt_bot[0] + (thickness/2) / sin(leg_ang)

    apt_bot_lft_y = apt_bot[1]
    apt_bot_lft_x = apt_bot[0] - (thickness/2) / sin(leg_ang)

    # applying top and bottom correction
    apt_top_rgt_x = apt_top_rgt_x + cor_top
    apt_top_lft_x = apt_top_lft_x - cor_top
    apt_bot_rgt_x = apt_bot_rgt_x + cor_bot
    apt_bot_lft_x = apt_bot_lft_x - cor_bot
    
    # anchor points
    apt_top_rgt = apt_top_rgt_x, apt_top_rgt_y
    apt_top_lft = apt_top_lft_x, apt_top_lft_y
    apt_bot_rgt = apt_bot_rgt_x, apt_bot_rgt_y
    apt_bot_lft = apt_bot_lft_x, apt_bot_lft_y

    # right side equation
    m_rgt, q_rgt = m_q_from_apt(apt_top_rgt, apt_bot_rgt)

    # left side equation
    m_lft, q_lft = m_q_from_apt(apt_top_lft, apt_bot_lft)

    # bottom side equation
    m_bot = tan(radians(ang_bot))
    q_bot = apt_bot[1] - m_bot * apt_bot[0]
    # bot_x * m_bot - bot_y = -bot_q

    # top side equation
    m_top = tan(radians(ang_top))
    q_top = apt_top[1] - m_top * apt_top[0]
    # top_x * m_top - top_y = -top_q

    # top_lft_point
    apt_top_lft = line_intersection(m_top, q_top, m_lft, q_lft)

    # top_rgt_point
    apt_top_rgt = line_intersection(m_top, q_top, m_rgt, q_rgt)

    # bot_rgt_point
    apt_bot_rgt = line_intersection(m_bot, q_bot, m_rgt, q_rgt)

    # bot_lft_point
    apt_bot_lft = line_intersection(m_bot, q_bot, m_lft, q_lft)

    apt_bot_lft = round(apt_bot_lft[0]), round(apt_bot_lft[1])
    apt_bot_rgt = round(apt_bot_rgt[0]), round(apt_bot_rgt[1])
    apt_top_lft = round(apt_top_lft[0]), round(apt_top_lft[1])
    apt_top_rgt = round(apt_top_rgt[0]), round(apt_top_rgt[1])

    pts = [apt_bot_lft, apt_bot_rgt, apt_top_rgt, apt_top_lft]

    # drawing
    if clockwise == True:
        draw_ply(glyph, pts[::-1])
    else:
        draw_ply(glyph, pts)

    return pts



def quarter(glyph, bez_typ_inr_otr,
            apt_hor_ver, ang_hor_ver, tck_hor_ver,
            sqr_inr_hor_ver, sqr_otr_hor_ver,
            adj_hor_inr_otr, adj_ver_inr_otr,
            clockwise):

    pts = curved_piece(glyph, 'quarter', bez_typ_inr_otr,
                 apt_hor_ver, tck_hor_ver, ang_hor_ver,
                 (0,0), (0,0),
                 sqr_inr_hor_ver, sqr_otr_hor_ver,
                 adj_hor_inr_otr, adj_ver_inr_otr,
                 clockwise)

    return pts



def junction(glyph, bez_typ_inr_otr, 
            apt_hor_ver, ang_hor_ver, tck_hor_ver, 
            ang_inr_otr,
            sqr_inr_hor_ver, sqr_otr_hor_ver,
            adj_hor_inr_otr, adj_ver_inr_otr,
            clockwise):

    pts = curved_piece(glyph, 'shoulder', bez_typ_inr_otr,
                              apt_hor_ver, tck_hor_ver, ang_hor_ver,
                              ang_inr_otr, (0,0),
                              sqr_inr_hor_ver, sqr_otr_hor_ver,
                              adj_hor_inr_otr, adj_ver_inr_otr,
                              clockwise)
    return pts



def termination(glyph, bez_typ_inr_otr, 
            apt_hor_ver, ang_hor_ver, tck_hor_ver, 
            ang_inr_otr,
            sqr_inr_hor_ver, sqr_otr_hor_ver,
            adj_hor_inr_otr, adj_ver_inr_otr,
            clockwise):

    pts = curved_piece(glyph, 'termination', bez_typ_inr_otr,
                              apt_hor_ver, tck_hor_ver, ang_hor_ver,
                              ang_inr_otr, (0,0),
                              sqr_inr_hor_ver, sqr_otr_hor_ver,
                              adj_hor_inr_otr, adj_ver_inr_otr,
                              clockwise)
    return pts



def half_spine(glyph, bez_typ_inr_otr, 
               apt_hor_ver, ang_hor_ver, tck_hor_ver,
               ang_inr_otr, 
               sqr_inr_hor_ver, sqr_otr_hor_ver,
               adj_hor_inr_otr, adj_ver_inr_otr,
               clockwise):

    pts = curved_piece(glyph, 'half_spine', bez_typ_inr_otr,
                              apt_hor_ver, tck_hor_ver, ang_hor_ver,
                              (0,0), ang_inr_otr,
                              sqr_inr_hor_ver, sqr_otr_hor_ver,
                              adj_hor_inr_otr, adj_ver_inr_otr,
                              clockwise)
    return pts



def comma(glyph, bez_typ_inr_otr, 
          apt_hor_ver, ang_hor_ver, tck_hor_ver,
          ang_inr_otr, 
          sqr_inr_hor_ver, sqr_otr_hor_ver,
          adj_hor_inr_otr, adj_ver_inr_otr,
          clockwise):

    pts = curved_piece(glyph, 'comma', bez_typ_inr_otr,
                              apt_hor_ver, tck_hor_ver, ang_hor_ver,
                              (0,0), ang_inr_otr,
                              sqr_inr_hor_ver, sqr_otr_hor_ver,
                              adj_hor_inr_otr, adj_ver_inr_otr,
                              clockwise)
    return pts



def punctuation_quarter(glyph, bez_typ, opt, rad_hor_ver, ang_hor_ver, bez_ang_hor_ver, sqr_hor_ver, orientation, clockwise):

    # unwrapping
    opt_x, opt_y = opt
    rad_hor, rad_ver = rad_hor_ver
    ang_hor, ang_ver = ang_hor_ver
    sqr_hor, sqr_ver = sqr_hor_ver
    bez_ang_hor, bez_ang_ver = bez_ang_hor_ver

    # conditional orientation
    if orientation == 'NW':
        f_hor = -1
        f_ver = +1
    elif orientation == 'NE':
        f_hor = +1
        f_ver = +1
    elif orientation == 'SW':
        f_hor = -1
        f_ver = -1
    else:
        f_hor = +1
        f_ver = -1

    # anchor points coordinates
    apt_hor_x = opt_x + rad_hor * f_hor
    apt_hor_y = opt_y + f_ver * rad_hor * tan(radians(ang_hor))
    apt_hor = round(apt_hor_x), round(apt_hor_y)

    apt_ver_x = opt_x + f_hor * rad_ver * tan(radians(ang_ver))
    apt_ver_y = opt_y + rad_ver * f_ver
    apt_ver = round(apt_ver_x), round(apt_ver_y)

    # ver line
    m_ver = tan(radians(bez_ang_ver))
    q_ver = -m_ver * apt_ver[0] + apt_ver[1]

    # hor line
    if bez_ang_hor != 0:
        m_hor = tan(radians(90 - bez_ang_hor))
        q_hor = -m_hor * apt_hor[0] + apt_hor[1]

        cpt_max = line_intersection(m_hor, q_hor, m_ver, q_ver)

    else:
        cpt_max = (apt_hor_x, m_hor*apt_hor_x + q_hor)

    # control points coordinates
    cpt_ver = interpolate_points(apt_ver, cpt_max, sqr_ver)
    cpt_ver = round(cpt_ver[0]), round(cpt_ver[1])

    cpt_hor = interpolate_points(apt_hor, cpt_max, sqr_hor)
    cpt_hor = round(cpt_hor[0]), round(cpt_hor[1])

    # drawing
    pen = glyph.getPen()
    pen.moveTo(opt)

    if (clockwise == True):

        if f_hor*f_ver == -1:
            pen.lineTo(apt_hor)
            if bez_typ == 'cubic':
                pen.curveTo(cpt_hor, cpt_ver, apt_ver)
            else:
                pen.qCurveTo(cpt_hor, cpt_ver, apt_ver)

        else:
            pen.lineTo(apt_ver)
            if bez_typ == 'cubic':
                pen.curveTo(cpt_ver, cpt_hor, apt_hor)
            else:
                pen.qCurveTo(cpt_ver, cpt_hor, apt_hor)

    else:
        if f_hor*f_ver == -1:
            pen.lineTo(apt_ver)
            if bez_typ == 'cubic':
                pen.curveTo(cpt_ver, cpt_hor, cpt_hor)
            else:
                pen.qCurveTo(cpt_ver, cpt_hor, cpt_hor)

        else:
            pen.lineTo(apt_hor)
            if bez_typ == 'cubic':
                pen.curveTo(cpt_hor, cpt_ver, cpt_ver)
            else:
                pen.qCurveTo(cpt_hor, cpt_ver, cpt_ver)

    pen.closePath()

    pts = [apt_hor, apt_ver]
    return pts



def freeform    (glyph,

                 bez_typ_inr_otr,

                 apt_hor_inr_otr,
                 apt_ver_inr_otr,

                 ang_hor_inr_otr,
                 ang_ver_inr_otr,

                 sqr_inr_hor_ver,
                 sqr_otr_hor_ver,

                 clockwise):


    assert (bez_typ_inr_otr[0] in BEZIER_TYPES) and (bez_typ_inr_otr[1] in BEZIER_TYPES)

    # unwrapping
    apt_hor_inr, apt_hor_otr = apt_hor_inr_otr
    apt_ver_inr, apt_ver_otr = apt_ver_inr_otr

    ang_hor_inr, ang_hor_otr = ang_hor_inr_otr
    ang_ver_inr, ang_ver_otr = ang_ver_inr_otr

    sqr_inr_hor, sqr_inr_ver = sqr_inr_hor_ver
    sqr_otr_hor, sqr_otr_ver = sqr_otr_hor_ver

    # orientation
    f_hor, f_ver = orientation_function(apt_hor_inr, apt_ver_inr)

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