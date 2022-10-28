import os, cv2
from natsort import natsorted


def hconcat_resize_max(im_list, interpolation=cv2.INTER_CUBIC):
    w_max = max(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * w_max / im.shape[0]), w_max), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)

def vconcat_resize_max(im_list, interpolation=cv2.INTER_CUBIC):
    w_max = max(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_max, int(im.shape[0] * w_max / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)

def make_blankimg(dir,m,l,f,nm):
    img = None
    for i in range(1,nm+1):
        if i==m: continue
        impath = dir + '/module' + str(i) + '_layer' + str(l) + '/' + str(f) + '.jpg'
        if os.path.exists(impath):
            img=cv2.imread(impath)
            img[:,:,:] = 0
            break
    return img

def combine_img(dir,nm,nl,f,test=None,predict=None):

    mimglist=[]
    for m in range(1, nm+1):
        limglist=[]
        for l in range(nl):
            impath= dir+'/module'+str(m)+'_layer'+str(l)+'/'+str(f)+'.jpg'
            if os.path.exists(impath): limglist.append(cv2.imread(impath))
            else:
                blank = make_blankimg(dir,m,l,f,nm)
                if blank is not None: limglist.append(blank)

        mimglist.append(hconcat_resize_max(limglist, interpolation=cv2.INTER_CUBIC))

    if predict is not None:
        imglist = [cv2.imread(predict + '/test_' + str(f) + 'y_0.jpg')]
        if test is not None:
            imglist.append(cv2.imread(test    +'/'+ '0'*(int(5-len(str(f)))) + str(f) + '.jpg'))

        mimglist.append(hconcat_resize_max(imglist, interpolation=cv2.INTER_CUBIC))

    return vconcat_resize_max(mimglist, interpolation=cv2.INTER_CUBIC)

def make_video(imglist,dir,onoff='on',fps=50):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(dir + '_fps' + str(fps) + '.mp4', fourcc, fps, (imglist[0].shape[1], imglist[0].shape[0]))

    for f,img in enumerate(imglist):
        if onoff=='on':
            cv2.putText(img, text=str(f),
                        org=(130, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5, color=(0, 0, 0),
                        thickness=2, lineType=cv2.LINE_4)
            cv2.putText(img, text='y',
                        org=(10, 20), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5, color=(0, 0, 0),
                        thickness=2, lineType=cv2.LINE_4)
        video.write(img)
    video.release()

def main(dir,nm,nl, onoff='on',fps=50,test=None,predict=None):
    nf = ''.join(os.listdir(dir+'/module'+str(nm)+'_layer'+str(nl-1))).count('.jpg') #nf: frame number

    imglist=[]
    for f in range(nf): imglist.append(combine_img(dir, nm, nl, f, test=test, predict=predict))

    make_video(imglist,dir,onoff,fps)


if __name__ == '__main__':
    dir='20221028162846' #dir of images for the movie
    onoff='on' #on: write frame number to movie
    fps=10
    nm=3 #number module
    nl=2 #number layer
    testimgpath= None#'bnhm/data/1-8-7-0-9-3-9-1-5218709391_23'
    predictpath= None#'bnhm/3ch_benham/back_read_list.txt/EW_model/mit_440000.pth'

    main(dir,nm,nl, onoff=onoff, fps=fps,test=testimgpath,predict=predictpath)
