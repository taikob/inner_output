import os, cv2
import numpy as np

def main(read_list):
    signal=[]
    i=0
    with open(read_list, 'r') as f:
        datalist = f.readlines()
        for data in datalist:
            img = cv2.imread(data.replace('\n',''))
            signal.append([i, np.mean(img.astype(float))])
            i+=1

    np.savetxt(data.split('/')[0]+'/signal.txt',np.array(signal),delimiter=',')


if __name__ == '__main__' :
    read_list = 'barbar_n_vpf20_l167_ffNone_ln0_li0_imsw0_read_list.txt'
    main(read_list)