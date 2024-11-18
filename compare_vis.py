import os
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

targets = ['AS_206', 'DoAr_16', 'DoAr24E', 'DoAr_33', 'DoAr_44', 'GSS_26', 
           'GSS_39', 'HBC_266', 'IRS_37', 'IRS_39', 'IRS_41', 'IRS_51', 
           'VSSG_1', 'WSB_31', 'WSB_60', 'YLW_47', 'YLW_8']
tracks = ['track1', 'track2a']
rxs = ['rx240']
sidebands = ['usb', 'lsb']

def process_visibility(target, track, rx, sideband):
    vis = f"{target}_{track}.{rx}.{sideband}.cal.miriad"

    uvaver_command = [
        'uvaver',
        f'vis={vis}',
        'line=channel,1,1,1024,1',
        f'out={vis}.c'
    ]
    subprocess.run(uvaver_command)

    uvamp_command = [
        'uvamp',
        f'vis={vis}.c',
        'bin=25,4,klam' if track == 'track1' else 'bin=25,8,klam',
        f'log={vis}.txt'
    ]
    subprocess.run(uvamp_command)

    # Read the log file and process data
    filename = f"{vis}.txt"
    if not os.path.exists(filename):
        print(f"File {filename} does not exist. Skipping...")
        return None, None, None

    # Read the file into a DataFrame
    df_csv = pd.read_csv(
        filename, skiprows=3, skipfooter=3, header=None, 
        delim_whitespace=True, engine='python'
    )

    uv_dis_c = (df_csv[0] + df_csv[1]) / 2.0
    y_values = df_csv[2]
    error = df_csv[3]

    # Filter out zero values
    non_zero_mask = y_values != 0
    x_filtered = uv_dis_c[non_zero_mask]
    y_filtered = y_values[non_zero_mask]
    error_filtered = error[non_zero_mask]

    return x_filtered, y_filtered, error_filtered

# Loop over all targets
for target in targets:
    for sideband in sidebands: 
        plt.figure(figsize=(10, 6))
        
        for track in tracks:
            for rx in rxs:
                print(f"Processing: Target={target}, Track={track}, Rx={rx}, Sideband={sideband}")
                x_filtered, y_filtered, error_filtered = process_visibility(target, track, rx, sideband)
                
                if x_filtered is not None: 
                    plt.scatter(x_filtered, y_filtered, marker='o', label=f'{track} ({rx})')
                    plt.errorbar(x_filtered, y_filtered, yerr=error_filtered, fmt='o', elinewidth=1.5) 
                    
        plt.xlabel('UVdistance (kλ)')
        plt.ylabel('Amplitude (Jy)')
        plt.title(f'{target} visibility ({sideband.upper()})')
        plt.legend()

        output_file = f"{target}_{rx}_{sideband}_visibility.pdf"
        plt.savefig(output_file, format='pdf')
        print(f"Saved plot to {output_file}")
        plt.close()
