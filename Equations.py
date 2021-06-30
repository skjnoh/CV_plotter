from numpy import exp
from numpy import log
from numpy import abs
from numpy import where

def Langmuir(E,*popt):
    # F/RT = 38.94
    K, MaxCharge = popt
    return MaxCharge*(K*exp(38.94*E))/(1+K*exp(38.94*E))

def Frumkin(charge, *popt):
    #RT = 2477
    K, Maxcharge, r = popt
    theta = charge/Maxcharge

    return where(
        charge < Maxcharge,
        log((theta/(1-theta))*exp(r/2477*theta)/K)/38.94,
        -0.5)

def linear(x, a, b):
    return a*x + b