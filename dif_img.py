import os, datetime,cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def prepare_dir(savedir):
    dirlist = []
    for dir in os.listdir(path1):
        if 'module' in dir and 'layer' in dir: dirlist.append(dir)
    if os.path.exists(savedir): print(savedir,'exist ');exit()
    for dir in dirlist:
        os.makedirs(savedir + '/' + dir)

    return dirlist

def main(path1, path2, savedir, rate):

    dirlist = prepare_dir(savedir)
    for img in os.listdir(path1+'/'+dirlist[0]):
        if not '.jpg' in img: continue
        for dir in dirlist:
            img1 = cv2.cvtColor(cv2.imread(path1+'/'+dir+'/'+img), cv2.COLOR_BGR2GRAY)
            img2 = cv2.cvtColor(cv2.imread(path2+'/'+dir+'/'+img), cv2.COLOR_BGR2GRAY)
            im = (img1.astype(float) - img2.astype(float))/255
            cv2.imwrite(savedir+'/'+dir+'/'+img,im)

            h = float(im.shape[0]*0.0129)
            w = float(im.shape[1]*0.0129)

            plt.figure(figsize=(w, h))
            sns.heatmap(im, vmax=rate, vmin=-rate, center=0, cbar=False)
            plt.axis('tight')
            plt.axis('off')
            plt.savefig(savedir+'/'+dir+'/'+img, bbox_inches='tight', pad_inches=0)
            plt.close('all')

            if not os.path.exists(savedir + '/legend.png'):
                plt.rcParams["font.family"] = "Times New Roman"
                plt.figure(figsize=(w, h))
                sns.heatmap(im, vmax=rate, vmin=-rate, center=0)
                plt.savefig(savedir + '/legend.png')
                plt.close('all')


if __name__ == '__main__':
    path1 = '105'
    path2 = '115'
    rate = 1
    savedir = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    main(path1, path2, savedir, rate)