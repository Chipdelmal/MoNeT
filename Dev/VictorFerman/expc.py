import scipy.stats as stats
import numpy as np
import MoNeT_MGDrivE as monet

def approx_equals(a, b, margin):
    dif = np.fabs(a-b)
    if dif <= margin:
        return True
    else:
        return False
    return False

def trunc_exp(x, rate, a ,b):
    if(a>b):
        return None

    scale = 1.0/rate

    gA = stats.expon.cdf(a,scale=scale)
    gB = stats.expon.cdf(b,scale=scale)
    if approx_equals(gA,gB, 0.000001):
        return None

    density = stats.expon.pdf(x,scale=scale)/ (stats.expon.cdf(b,scale=scale)-stats.expon.cdf(a,scale=scale))

    return round(density, 10)



print(trunc_exp(1023.1,1/800.0,50,5e3))
monet.truncatedExponential(1023.1, params=[1/800,50,5e3])
