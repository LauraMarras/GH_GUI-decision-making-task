import pyxdf

data, header = pyxdf.load_xdf(r'block_trial_laura_final2.xdf')
streams = {}
initial_time = None
trial_n = 0
Stim_n = 0

struct = {}

for stream in data:
    markers = stream['time_series']

    if isinstance(markers, list):
        # list of strings
        all_streams = zip(stream['time_stamps'], markers)
        for timestamp, marker in all_streams:
            if initial_time is None:
                initial_time = timestamp

            #print(f'{marker[0]} @ {(timestamp-initial_time):.3f} s')
            streams[(round((timestamp-initial_time), 3))] = marker[0]

        for value in streams.values():
            if 'Sum' in value:
                string2 = value.replace(',', '')
                string3 = string2.replace('Sum Trail: ', '')
                my_list = string3.split(' ')
                struct[my_list[0]] = my_list[1:]

    else:
        raise RuntimeError('Unknown stream format')
    
print(streams)
print(struct)

# Analyze data per stimulus repetition
rep1 = []
rep2 = []
rep3 = []
rep4 = []

for trial in struct.values():
    if trial[1] == '1':
        rep1.append(trial[3])
    elif trial[1] == '2':
        rep2.append(trial[3])
    elif trial[1] == '3':
        rep3.append(trial[3])
    elif trial[1] == '4':
        rep4.append(trial[3])


rep1_c = rep1.count('Correct')
rep1_i = rep1.count('Incorrect')
rep1_n = rep1.count('No')
rep2_c = rep2.count('Correct')
rep2_i = rep2.count('Incorrect')
rep2_n = rep2.count('No')
rep3_c = rep3.count('Correct')
rep3_i = rep3.count('Incorrect')
rep3_n = rep3.count('No')
rep4_c = rep4.count('Correct')
rep4_i = rep4.count('Incorrect')
rep4_n = rep4.count('No')

total_c = rep1_c + rep2_c + rep3_c + rep4_c
total_i = rep1_i + rep2_i + rep3_i + rep4_i
total_n = rep1_n + rep2_n + rep3_n + rep4_n

accuracy_total = [total_c, total_i, total_n]


accuracy_per_repetition = {}
accuracy_per_repetition[1] = [rep1_c, rep1_i, rep1_n]
accuracy_per_repetition[2] = [rep2_c, rep2_i, rep2_n]
accuracy_per_repetition[3] = [rep3_c, rep3_i, rep3_n]
accuracy_per_repetition[4] = [rep4_c, rep4_i, rep4_n]

print(accuracy_per_repetition)
print(accuracy_total)
