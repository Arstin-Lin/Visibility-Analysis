import pandas as pd
import matplotlib.pyplot as plt
import subprocess

# Define the vis parameter
vis = 'WSB_31_track1.rx240.lsb.cal.miriad'

# UvAver command
uvaver_command = [
    'uvaver',
    f'vis={vis}',
    'line=channel,1024,1,4,4',
    f'out={vis}.c'
]

# Run UvAver
subprocess.run(uvaver_command)

# UvAmp command
uvamp_command = [
    'uvamp',
    f'vis={vis}.c',
    'bin=50,2,klam',
    f'log={vis}.txt'
]

# Run UvAmp
subprocess.run(uvamp_command)

# Reading file with pandas
filename = f'{vis}.txt'

df_csv = pd.read_csv(filename, skiprows = 3, skipfooter = 3, header = None,
                     delim_whitespace=True)

uv_dis_c = (df_csv[0]+df_csv[1])/2.0

# Define the x-axis values
x_values = uv_dis_c 

# Define the y-axis values
y_values = df_csv[2]

# Define the errorbar
error = df_csv[3]

# Plot the data
plt.scatter(x_values, y_values, marker='o')
plt.errorbar(x_values, y_values , yerr=error, fmt='o', ecolor='hotpink', elinewidth=1.5, capsize=2.5)

# Set labels and title
plt.xlabel('UVdistance (kλ)')
plt.ylabel('Amplitude (Jy)')
plt.title('WSB 31 visibility')

# Show the plot
plt.grid(True)
plt.show()

