import os, cv2, sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from natsort import natsorted

def get_imglist(fol,target):

    pathlist =os.listdir(fol)
    pathlistt=os.listdir(fol)
    for i in reversed(range(len(pathlist))):
        path=pathlist[i]
        if not target in path or '_30%' in path:
            del pathlist[i],pathlistt[i]
        else:
            pathlist[i] =fol+'/'+path
            pathlistt[i]=fol+'/'+path.replace('.','_30%.')

    return [natsorted(pathlist),natsorted(pathlistt)]

def get_module(fol):
    mlist=list()
    for path in os.listdir(fol):
        path = os.path.splitext(path.replace('_cmp','').replace('_30%',''))[0]
        path = path.split('_')
        del path[0]
        path = '_'.join(path)
        if not path in mlist and not 'legend' in path and path!='': mlist.append(path)

    return mlist

def make_movie(fol,target, onoff='on',fps=50):

    ill=get_imglist(fol+'/img',target)
    fol +='/mov'
    addname = ['','_30%']
    if not os.path.exists(fol): os.makedirs(fol)

    for j, il in enumerate(ill):
        for i in range(len(il)):
            na=il[0]
            img = cv2.imread(il.pop(0))
            if onoff=='on':
                cv2.putText(img, text=str(i),
                            org=(130, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5, color=(0, 127, 0),
                            thickness=2, lineType=cv2.LINE_4)
                cv2.putText(img, text='y',
                            org=(10, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5, color=(0, 127, 0),
                            thickness=2, lineType=cv2.LINE_4)

            if not 'video' in locals():
                fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
                video = cv2.VideoWriter(fol+'/'+ target +addname[j]+'_fps'+str(fps)+ '.mp4', fourcc, fps, (img.shape[1], img.shape[0]))
            video.write(img)

        video.release()
        del video

def cmp_img(cmp1, cmp2,savepath):
    img1 = cv2.cvtColor(cv2.imread(cmp1), cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(cv2.imread(cmp2), cv2.COLOR_BGR2GRAY)

    cmp = img1.astype(float) - img2.astype(float)
    cmp =cmp/np.abs(cmp).max()
    h=float(cmp.shape[0]*0.013)
    w=float(cmp.shape[1]*0.013)

    plt.figure(figsize=(w,h))
    sns.heatmap(cmp, vmax=1, vmin=-1, center=0, cbar=False)
    plt.axis('tight')
    plt.axis('off')
    plt.savefig(savepath+'_cmp.png', bbox_inches='tight',pad_inches = 0)
    plt.close('all')

    plt.figure(figsize=(w,h))
    sns.heatmap(cmp, vmax=0.3, vmin=-0.3, center=0, cbar=False)
    plt.axis('tight')
    plt.axis('off')
    plt.savefig(savepath+'_cmp_30%.png', bbox_inches='tight',pad_inches = 0)
    plt.close('all')

    if not os.path.exists(os.path.dirname(savepath)+'/legend.png'):
        plt.rcParams["font.family"] = "Times New Roman"
        plt.figure(figsize=(w,h))
        sns.heatmap(cmp, vmax=1, vmin=-1, center=0)
        plt.savefig(os.path.dirname(savepath)+'/legend.png')
        plt.close('all')

        plt.figure(figsize=(w,h))
        sns.heatmap(cmp, vmax=0.3, vmin=-0.3, center=0)
        plt.savefig(os.path.dirname(savepath)+'/legend_30%.png')
        plt.close('all')

def cmp_folder(cmp1,cmp2, ext='jpg'):
    root = cmp1.split('/')[-1]+'-'+cmp2.split('/')[-1]
    fol = root +'/img'
    if not os.path.exists(fol): os.makedirs(fol)
    listdir=os.listdir(cmp1)
    for i, f in enumerate(listdir):
        sys.stdout.write("\r{}".format(str(i+1)+' / '+str(len(listdir)))); sys.stdout.flush()
        if os.path.isdir(cmp1 + '/' + f) and not 'ext' in f:
            fn=f.split('_')
            step = fn[-1].replace('time','')
            del fn[-1]
            del fn[0:3]
            name = step + '_' + '_'.join(fn)
            fnd='_' + step + 'step.' + ext

            for img1 in os.listdir(cmp1+'/'+f):
                if fnd in img1: break
            for img2 in os.listdir(cmp2+'/'+f):
                if fnd in img2: break

            cmp_img(cmp1+'/'+f+'/'+img1, cmp2+'/'+f+'/'+img2,fol+'/'+name)
    return root

if __name__ == '__main__':

    cmp1='images/2'
    cmp2='images/3'
    fol = cmp_folder(cmp1, cmp2)

    for target in get_module(fol+'/img'):
        print(target)
        make_movie(fol, target,fps=10)