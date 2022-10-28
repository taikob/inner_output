import argparse
import pathlib
import numpy as np
import datetime
import cv2,os
from tensorboard.backend.event_processing import event_accumulator


def main(path, outdir):

    print('Y',path)
    event_acc = event_accumulator.EventAccumulator(
        path, size_guidance={'images': 0})
    event_acc.Reload()

    print('YY')
    outdir = pathlib.Path(outdir)
    outdir.mkdir(exist_ok=True, parents=True)

    for tag in event_acc.Tags()['images']:
        events = event_acc.Images(tag)

        tag_name = tag.replace('/', '_')
        dirpath = outdir / tag_name
        dirpath.mkdir(exist_ok=True, parents=True)

        for event in events:
            s = np.frombuffer(event.encoded_image_string, dtype=np.uint8)
            image = cv2.imdecode(s, cv2.IMREAD_COLOR)
            dt = datetime.datetime.fromtimestamp(event.wall_time)
            outpath = dirpath / '{}_{}step.jpg'.format(dt.date(), event.step)
            cv2.imwrite(outpath.as_posix(), image)

if __name__ == '__main__':
    root = 'runs'
    savedir = 'runsimg'
    if not os.path.exists(savedir): os.mkdir(savedir)
    for dir in os.listdir(root):
        for path in os.listdir(root+'/'+dir):
            if 'events.out.tfevents' in path:
                if not os.path.exists(savedir+'/'+dir): os.mkdir(savedir+'/'+dir)
                main(root+'/'+dir+'/'+path, savedir+'/'+dir)
