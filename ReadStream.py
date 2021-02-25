import pyxdf

data, header = pyxdf.load_xdf(r'block_Default.xdf')

for stream in data:
    y = stream['time_series']

    if isinstance(y, list):
        # list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream['time_stamps'], y):
            print(f'Marker "{marker[0]}" @ {timestamp:.4f} s')
            if (marker[0])
    else:
        raise RuntimeError('Unknown stream format')
    
