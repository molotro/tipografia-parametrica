import numpy as np


def getYfromXforBezSegment(P0, P1, P2, P3, x):
    '''For a cubic Bezier segment described by the 2-tuples P0, ..., P3, return
    the y-value associated with the given x-value.

    Ex: getXfromYforCubicBez((0,0), (1,1), (2,1), (2,2), 3.2)'''

    #First, get the t-value associated with x-value, where t is the
    #parameterization of the Bezier curve and ranges from 0 to 1.
    #We need the coefficients of the polynomial describing cubic Bezier
    #(cubic polynomial in t)
    coefficients = [-P0[0] + 3*P1[0] - 3*P2[0] + P3[0],
                    3*P0[0] - 6*P1[0] + 3*P2[0],
                    -3*P0[0] + 3*P1[0],
                    P0[0] - x]
    #find roots of this polynomial to determine the parameter t
    roots = np.roots(coefficients)
    #find the root which is between 0 and 1, and is also real
    correct_root = None
    for root in roots:
        if np.isreal(root) and 0 <= root <= 1:
            correct_root = root

    #check to make sure a valid root was found
    if correct_root is None:
        print('Error, no valid root found. Are you sure your Bezier curve '
              'represents a valid function when projected into the xy-plane?')
    param_t = correct_root

    #from our value for the t parameter, find the corresponding y-value using formula for
    #cubic Bezier curves
    y = (1-param_t)**3*P0[1] + 3*(1-param_t)**2*param_t*P1[1] + 3*(1-param_t)*param_t**2*P2[1] + param_t**3*P3[1]
    assert np.isreal(y)
    # typecast y from np.complex128 to float64   
    y = y.real
    return y