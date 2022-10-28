import os
import cv2
import numpy as np
from natsort import natsorted

def channel_number(layer,module):
    if layer=='0':
        h=120
        w=160
        nh=1
        nv=3
    elif layer=='1':
        h=60
        w=80
        nh=6
        nv=8
    elif layer=='2':
        h=30
        w=40
        nh=12
        nv=8
    elif layer=='3':
        h=15
        w=20
        nh=24
        nv=8

    return nh, nv, h, w

def module_output(fol,module,layer):
    signal = []
    nh, nv, h, w = channel_number(layer, module)

    for file in natsorted(os.listdir(fol)):
        if not '.jpg' in file: continue
        img = cv2.cvtColor(cv2.imread(fol+'/'+file), cv2.COLOR_BGR2GRAY)
        frame=int(file.replace('.jpg',''))

        i=0
        for ih in range(nh):
            for iv in range(nv):
                trmimg=img[2+ih*(h+2):(ih+1)*(h+2),2+iv*(w+2):(iv+1)*(w+2)]
                #cv2.imwrite('frame'+str(frame)+'_channel'+str(i)+'.jpg', trmimg)
                signal.append([i,frame,np.mean(trmimg.astype(float))])
                i+=1
    signal = np.array(signal)
    np.savetxt(fol+'/'+module+'_layer'+layer+'.txt',signal,delimiter=',')
    return signal

def main(path):

    for fol in natsorted(os.listdir(path)):
        if not 'module' in fol or 'module_spec' in fol: continue
        layer = fol.split('/')[-1].split('_')[1].replace('layer', '')
        module = fol.split('/')[-1].split('_')[0]
        print(fol, module, layer)

        signal = module_output(path+'/'+fol, module, layer)
        ad = np.empty((signal.shape[0], 2))
        ad[:,0] = int(module.replace('module',''))
        ad[:,1] = int(layer)
        signal = np.concatenate([ad, signal], 1)

        if not 'total' in locals(): total = signal
        else: total = np.concatenate([total, signal], 0)

    np.savetxt(path + '/total.txt', total, delimiter=',')


if __name__ == '__main__':
    path='data/Aug19_16-51-40_deep2'
    main(path)