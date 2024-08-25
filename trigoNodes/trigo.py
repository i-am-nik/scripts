def adjust_phase(ang_in_deg):
    """
    Normalize an angle in degrees to the range [-180, 180].

    Parameters:
    ang_in_deg (float): The angle in degrees to be normalized.

    Returns:
    float: The normalized angle in the range [-180, 180] degrees.
    """
    # Normalize the angle to the range [0, 360) degrees
    normalized_ang_in_deg = ang_in_deg % 360
    
    # Adjust to the range [-180, 180] degrees
    if normalized_ang_in_deg > 180:
        return normalized_ang_in_deg - 360
    elif normalized_ang_in_deg < -180:
        return normalized_ang_in_deg + 360
    else:
        return normalized_ang_in_deg

def chev_poly(x):
    """
    Evaluate the Chebyshev polynomial of the first kind of degree 5.

    Parameters:
    x (float): The input value for the Chebyshev polynomial.

    Returns:
    float: The evaluated Chebyshev polynomial value.
    """
    # Coefficients for the Chebyshev polynomial of degree 5
    C0 = 1.276278962
    C1 = -0.285261569
    C2 = 0.009118016
    C3 = -0.000136587
    C4 = 0.000001185
    C5 = -0.000000007

    # Calculate Chebyshev polynomial terms
    T0 = 1
    T1 = x
    T2 = (2*x**2 -1)
    T3 = (4*x**3 - 3*x)
    T4 = (8*x**4 - 8*x**2 + 1)
    T5 = (16*x**5 - 20*x**3 + 5*x)

    # Evaluate the polynomial using the coefficients
    return float(C0 * T0 + C1 * T1 + C2 * T2 + C3 * T3 + C4 * T4 + C5 * T5)
    
def sin(ang_in_deg):
    """
    Compute the sine of an angle given in degrees using Chebyshev polynomial approximation.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the sine.

    Returns:
    float: The sine of the angle, rounded to six decimal places.
    """
    # Normalize the angle
    value = adjust_phase(ang_in_deg)
    
    # Convert angle to range [-1, 1] for polynomial evaluation
    x = value / 360
    
    # Compute intermediate values for Chebyshev polynomial
    w = 4 * x
    z = 2 * w * w - 1
    
    # Compute the sine value using the Chebyshev polynomial
    result = chev_poly(z) * w
    
    # Round the result to six decimal places
    return float(round(result, 6))

def cos(ang_in_deg):
    """
    Compute the cosine of an angle given in degrees based on its sine value.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the cosine.

    Returns:
    float: The cosine of the angle, rounded to six decimal places, or 'UNDEFINED' if the cosine is zero.
    """
    # Determine the sign of the cosine based on the quadrant
    quad_sign = 1
    if (90 <= ang_in_deg <= 270) or (-270 <= ang_in_deg <= -90):
        quad_sign = -1
    
    # Calculate the cosine value from the relation cos(x)^2 + sin(x)^2 = 1
    result = (1 - sin(ang_in_deg) ** 2) ** 0.5
    
    # Return the result with the appropriate sign and rounded to six decimal places
    return float(round(quad_sign * result, 6))

def tan(ang_in_deg):
    """
    Compute the tangent of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the tangent.

    Returns:
    float: The tangent of the angle, rounded to six decimal places, or 'UNDEFINED' if the cosine of the angle is zero.
    """
    # Compute cosine and check for undefined tangent
    cos_val = cos(ang_in_deg)
    if cos_val == 0:
        return "UNDEFINED"
    
    # Compute the tangent value tan(x)=sin(x)/cos(x) and round to six decimal places
    return float(round(sin(ang_in_deg) / cos_val))

def cot(ang_in_deg):
    """
    Compute the cotangent of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the cotangent.

    Returns:
    float: The cotangent of the angle, rounded to six decimal places, or 'UNDEFINED' if the tangent of the angle is zero or undefined.
    """
    # Compute tangent and check for undefined cotangent
    tan_val = tan(ang_in_deg)
    if tan_val == "UNDEFINED" or tan_val == 0:
        return "UNDEFINED"
    
    # Compute the cotangent value cot(x)=1/tan(x) and round to six decimal places
    return float(round(1 / tan_val))
    
def sec(ang_in_deg):
    """
    Compute the secant of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the secant.

    Returns:
    float: The secant of the angle, rounded to six decimal places, or 'UNDEFINED' if the cosine of the angle is zero.
    """
    # Compute cosine and check for undefined secant
    cos_val = cos(ang_in_deg)
    if cos_val == 0:
        return "UNDEFINED"
    
    # Compute the secant value sec(x)=1/cos(x) and round to six decimal places
    return float(round(1 / cos_val))

def csc(ang_in_deg):
    """
    Compute the cosecant of an angle given in degrees.

    Parameters:
    ang_in_deg (float): The angle in degrees for which to compute the cosecant.

    Returns:
    float: The cosecant of the angle, rounded to six decimal places, or 'UNDEFINED' if the sine of the angle is zero.
    """
    # Compute sine and check for undefined cosecant
    sin_val = sin(ang_in_deg)
    if sin_val == 0:
        return "UNDEFINED"
    
    # Compute the cosecant value csc(x)=1/sin(x) and round to six decimal places
    return float(round(1 / sin_val))