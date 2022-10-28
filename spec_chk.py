import numpy as np
from data_prcs import get as g
import os

def numc(module,layer):#number of channel
    if layer == 0:return 3
    elif layer == 1: return 48
    elif layer == 2: return 96
    elif layer == 3: return 192

def removedata(data,start,end):
    for i in reversed(range(data.shape[0])):
        if data[i,3]<start or data[i,3]>end: data = np.delete(data, i, 0)
    return data

def getsignal(data, module, layer, channel, start, end):

    signal = np.empty((end-start+1,channel+1))
    signal[:,0] = [n for n in range(start,end+1,1)]
    for i in reversed(range(data.shape[0])):
        if data[i, 0] == module and data[i, 1] == layer:
            signal[int(data[i,3]-start),int(data[i,2]+1)] = data[i,4]
            data = np.delete(data, i, 0)

    return data, signal

def getspec(signal):
    for i in range(signal.shape[1]-1):
        sig = signal[:,i+1]

        F = np.fft.fft(sig)
        freq = np.fft.fftfreq(signal.shape[0])[:,np.newaxis]
        Amp = np.abs(F/(signal.shape[0]/2))[:,np.newaxis]

        sp = np.concatenate([np.linspace(i, i, signal.shape[0])[:,np.newaxis], freq, Amp], 1)
        if not 'spec' in locals():
            spec = sp
            mspec = np.concatenate([freq, Amp], 1)
        else:
            spec = np.concatenate([spec,sp], 0)
            mspec[:,1] += Amp[:,0]
    mspec[:, 1] /=signal.shape[1]-1

    return spec, mspec


def main(path,start,end):
    data = np.loadtxt(path, delimiter=',')
    cnfl = g.set_cnfl([[1,2,3],[0,1,2,3]]) # module,layer
    data = removedata(data,start,end)

    for cnf in cnfl:
        if cnf[0]==1 and cnf[1]==4: continue
        data, signal = getsignal(data, cnf[0], cnf[1], numc(cnf[0],cnf[1]), start, end)

        sp, msp = getspec(signal)
        param = np.empty((sp.shape[0],2))
        param[:,0]=cnf[0]
        param[:,1]=cnf[1]
        sp = np.concatenate([param, sp], 1)
        msp = np.concatenate([np.linspace(cnf[0], cnf[0], msp.shape[0])[:, np.newaxis],
                        np.linspace(cnf[1], cnf[1], msp.shape[0])[:, np.newaxis], msp], 1)
        if not 'spec' in locals(): spec = sp; mspec = msp
        else: spec =np.concatenate([spec, sp], 0); mspec =np.concatenate([mspec, msp], 0)

    np.savetxt(os.path.dirname(path)+'/'+'channel_spec'+'_start'+str(start)+'_end'+str(end)+'.txt',spec,delimiter=',')
    np.savetxt(os.path.dirname(path)+'/'+'module_spec' +'_start'+str(start)+'_end'+str(end)+'.txt',mspec,delimiter=',')


if __name__ == '__main__':
    path = 'data/Aug19_16-51-40_deep2/total.txt'
    start = 48
    end = 118
    main(path,start,end)