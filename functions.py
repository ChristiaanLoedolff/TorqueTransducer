import numpy as np
import matplotlib.pyplot as plt

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w




def signal(fs=2400, cycles=1, rpm=100, offset=0):

    staticStart = 30
    gapLen = 30


    cHz = rpm/60
    nPoints = np.int64(cycles*fs/cHz)
    nPointC = np.int64(fs/cHz)
    time = np.linspace(cHz/fs, cycles/cHz, num=nPoints)
    timeCycle = np.linspace(cHz/fs, cycles/cHz, num=nPointC)

    gapStart = (staticStart+offset)/360
    gapEnd = (staticStart+gapLen+offset)/360
    openP = np.int64(gapStart*fs/cHz - 1)
    closeP = np.int64(gapEnd*fs/cHz -1)

    riseTime = 0.001
    fallTime = 0.06
      

    buffer = fs
    s = np.zeros(len(timeCycle)+buffer)

    
    steepLen = np.int64(fs*riseTime+2) 
    shiftError1 = (1/riseTime)*(time[openP] - gapStart/cHz)
    shiftError2 = (10/fallTime)*(time[openP+steepLen] - ((gapStart/cHz)+riseTime))

    expLen = np.int64(fs*0.06+2)
    expRange = np.linspace(-4+shiftError2, 6+shiftError2, num=expLen)
    expShape = np.power(0.5, expRange) 

    if steepLen != 0:
        steepRange = np.linspace(0, 1, num=steepLen)
        steepShape = 16*(steepRange+shiftError1)

        #plt.figure(0)
        #plt.plot(steepRange, steepShape, ".-k")
        #plt.show()

        if shiftError1 > 0:
            steepShape = np.delete(steepShape, -1)

        if shiftError1 < 0:
            steepShape[0] = 0

        if abs(steepShape[-1] - expShape[0]) < 0.05:
            expShape = np.delete(expShape, 0)
    
        pulseShape = np.append(steepShape,expShape)
    else:
        pulseShape = expShape

    pulseLen = len(pulseShape)

    
    
    s[openP:openP+pulseLen] += pulseShape
    s[closeP:closeP+pulseLen] -= pulseShape

    s = s[:-buffer]
    sC = s
    for i in range(cycles-1):
        s = np.append(s,sC)

    avgLen = 4
    noise = np.random.normal(0, 0.05, len(s) + avgLen -1)
    noise = moving_average(noise, avgLen)
    #s += noise

    return time, s


def V_cross (t, V, DV):

    ic = np.where(np.diff(np.sign(V-DV)))[0]  # sign change
    ic = ic[0::2]                             # - to +
    #ic = ic[1::2]                             # + to -
    #print(ic)

    Vc = np.ones(len(ic)) * DV
    tc = np.zeros(len(ic))

    for i in range(len(ic)):                  # interpolate (TODO: vectorise?)

        ta, tb = t[ic[i]], t[ic[i]+1]
        Va, Vb = V[ic[i]], V[ic[i]+1]
        tc[i] = (DV-Va)*(tb-ta)/(Vb-Va) + ta

    return tc, Vc