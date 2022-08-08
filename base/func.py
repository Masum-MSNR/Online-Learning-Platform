def time_format(seconds: int):
    if seconds is not None:
        seconds = int(seconds)
        h = seconds // 3600 % 24
        m = seconds % 3600 // 60
        s = seconds % 3600 % 60
        if h > 0:
            return '{:02d}:{:02d}:{:02d}s'.format(h, m, s)
        else:
            return '{:02d}:{:02d}'.format(m, s)
