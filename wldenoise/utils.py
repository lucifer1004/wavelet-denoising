import math

# 求不小于整数n的最小的2的方幂
def closest_two_power(n):
    rval = 1
    while rval < n:
        rval <<= 1
    return rval


# 获取噪声方差
def get_var(cD):
    coeffs = cD
    abs_coeffs = []
    for coeff in coeffs:
        abs_coeffs.append(math.fabs(coeff))
    abs_coeffs.sort()
    pos = math.ceil(len(abs_coeffs) / 2)
    var = abs_coeffs[pos] / 0.6745
    return var


def predict_and_update(e, o):
    cD = o - e
    cA = e + cD * 0.5
    return cA, cD