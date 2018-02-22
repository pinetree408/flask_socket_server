import numpy as np
import math

def data_parser(raw, windows):
    data_list = raw.rstrip().split(',')
    data_type = int(data_list[0])
    data_time = int(data_list[1]) / 1000000
    data_x = float(data_list[2])
    data_y = float(data_list[3])
    data_z = float(data_list[4])

    data_dict = {
            'time': data_time,
            'x': data_x,
            'y': data_y,
            'z': data_z,
            }

    window = windows[data_type]
    if len(window) != 0 and (data_time - window[0]['time']) > 1000:
        window.pop(0)
    window.append(data_dict)

    prepared = False
    for window_v in list(windows.values()):
        if len(window_v) == 0:
            break
        interval = window_v[len(window_v)-1]['time'] - window_v[0]['time']
        if interval > 990 and interval < 1050:
            prepared = True
        else:
            break
    return prepared

def feature_generate(windows):
    features = []
    for index in [1, 4, 10]:
        window = windows[index]
        start_time = window[0]['time']
        interp = [i for i in range(start_time, start_time + 1000, 10)]
        time = [data['time'] for data in window]
        x = [data['x'] for data in window]
        y = [data['y'] for data in window]
        z = [data['z'] for data in window]

        rinterp_x = np.interp(interp, time, x)
        rinterp_y = np.interp(interp, time, y)
        rinterp_z = np.interp(interp, time, z)

        rinterp_m = []
        for x, y, z in zip(rinterp_x, rinterp_y, rinterp_z):
            rinterp_m.append(math.sqrt(math.pow(x, 2)+math.pow(y, 2)+math.pow(z, 2)))

        rinterp_xy = []
        for x, y in zip(rinterp_x, rinterp_y):
            rinterp_xy.append(math.sqrt(math.pow(x, 2)+math.pow(y, 2)))
        rinterp_yz = []
        for y, z in zip(rinterp_y, rinterp_z):
            rinterp_yz.append(math.sqrt(math.pow(y, 2)+math.pow(z, 2)))
        rinterp_xz = []
        for x, z in zip(rinterp_x, rinterp_z):
            rinterp_xz.append(math.sqrt(math.pow(x, 2)+math.pow(z, 2)))

        raw_features = [
                rinterp_x,
                rinterp_y,
                rinterp_z,
                rinterp_m,
                rinterp_xy,
                rinterp_yz,
                rinterp_xz,
                ]
        # feature
        for rinterp in raw_features:
            mean = np.mean(rinterp)
            sd = np.std(rinterp)
            max_f = np.amax(rinterp)
            min_f = np.amin(rinterp)
            q1 = np.percentile(rinterp, 25)
            q2 = np.percentile(rinterp, 50)
            q3 = np.percentile(rinterp, 75)
            fft_f = np.absolute(np.divide(np.fft.fft(rinterp), 100))[0:51]
            fft_f[1:len(fft_f)] = 2*fft_f[1:len(fft_f)]

            features.extend(np.array([mean, sd, max_f, min_f, q1, q2, q3]).tolist() + fft_f[1:11].tolist())

    return features
