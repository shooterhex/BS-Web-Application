"""
@credit: zyb_as
"""
import cv2
import numpy as np
from scipy.signal import argrelextrema
from api.resource.upload import UploadPicture


def smooth(x, window_len=13, window='hanning'):
    s = np.r_[2 * x[0] - x[window_len:1:-1],
              x, 2 * x[-1] - x[-1:-window_len:-1]]

    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]


class Frame:
    def __init__(self, id, diff):
        self.id = id
        self.diff = diff

    def __lt__(self, other):
        if self.id == other.id:
            return self.id < other.id
        return self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.id == other.id and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)


def rel_change(a, b):
    x = (b - a) / max(a, b)
    return x


def frame_extract(videopath, dir):
    # smoothing window size
    len_window = 50

    # load video and compute diff between frames
    cap = cv2.VideoCapture(str(videopath))
    prev_frame = None
    frame_diffs = []
    frames = []
    success, frame = cap.read()
    i = 0
    while success:
        luv = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        curr_frame = luv
        if curr_frame is not None and prev_frame is not None:
            # logic here
            diff = cv2.absdiff(curr_frame, prev_frame)
            diff_sum = np.sum(diff)
            diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)
        prev_frame = curr_frame
        i = i + 1
        success, frame = cap.read()
    cap.release()

    # compute keyframe
    keyframe_id_set = set()
    diff_array = np.array(frame_diffs)
    sm_diff_array = smooth(diff_array, len_window)
    frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
    for i in frame_indexes:
        keyframe_id_set.add(frames[i - 1].id)

    # save all keyframes as image
    cap = cv2.VideoCapture(str(videopath))
    success, frame = cap.read()
    idx = 0
    while success:
        if idx in keyframe_id_set:
            name = "keyframe_" + str(idx) + ".jpg"
            img_dir = dir + '/images/' + name
            cv2.imwrite(img_dir, frame)
            UploadPicture.save_thumb(img_dir, name)
            keyframe_id_set.remove(idx)
        idx = idx + 1
        success, frame = cap.read()
    cap.release()
