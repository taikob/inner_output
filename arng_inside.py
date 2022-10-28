import os,shutil
from natsort import natsorted

def module_to_number(module):
    if 'UpdateA'==module: return 1
    elif 'Conv_sequential'==module: return 2
    elif 'ConvLSTMCell'==module: return 3
    else: return None

def main(path,name):

    for dir in os.listdir(path):
        if not 'time' in dir: continue

        layer=dir.split('_')[-2].replace('layer','')
        module=dir.replace('test_0_0_','').split('_')
        frame=int(module[-1].replace('time',''))

        del module[-1]
        del module[-1]
        module = module_to_number('_'.join(module))
        if module is None: continue
        
        if module==1: layer = str(int(layer)+1)
        mod = 'module'+str(module)+'_layer'+str(layer)
        if not os.path.exists(name+'/'+mod): os.makedirs(name+'/'+mod)

        for file in natsorted(os.listdir(path+'/'+dir)):
            if '_'+str(frame)+'step' in file:
                shutil.copyfile(path+'/'+dir+'/'+file, name+'/'+mod+'/'+str(frame)+'.jpg')
                break

if __name__ == '__main__':
    path = 'runsimg'
    name = 'output_test'
    main(path,name)
