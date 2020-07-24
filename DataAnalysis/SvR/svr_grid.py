
import decimal
import numpy as np

np.arange(0, 1, .025)


svList= [
     0.0000009, 0.0000014, 0.0000023, 0.0000038, 0.0000062, 0.0000101, 0.0000164,
     0.0000266, 0.0000432, 0.0000702, 0.0001139, 0.0001848, 0.0003000, 0.0004868,
     0.0007899, 0.0012818, 0.0020800, 0.0033753, 0.0054772, 0.0088879, 0.0144224
]

len(svList)/2
svList[10]



def float_to_str(f):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    """
    ctx = decimal.Context()
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


# #############################################################################
# Sampling evenly through log-scale
# https://stackoverflow.com/questions/32784047/numbers-logarithmically-spaced-between-two-floats-in-numpy
# #############################################################################
N = 25
(lo, hi) = (10E-7, .1)
yStep = .025
y1 = np.arange(yStep, 1, yStep)
x1 = np.geomspace(lo-10E-7/10, hi, num=N)
stry = ', '.join([float_to_str(i)[:9] for i in x1])
'c(0.0, {})'.format(stry)


(929880/60)
15498*100

1400/365
5*365 - 358
5 * 365
