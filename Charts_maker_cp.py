import pandas as pd
import matplotlib.pyplot as plt
import subprocess

# Define the vis parameter of track1
vis1 = 'WSB_31_track1.rx240.lsb.cal.miriad'

# UvAver command
uvaver_command = [
    'uvaver',
    f'vis={vis1}',
    'line=channel,1024,1,4,4',
    f'out={vis1}.c'
]

# Run UvAver
subprocess.run(uvaver_command)

# UvAmp command
uvamp_command = [
    'uvamp',
    f'vis={vis1}.c',
    'bin=50,2,klam',
    f'log={vis1}.txt'
]

# Run UvAmp
subprocess.run(uvamp_command)

# Reading file with pandas for vis1
filename1 = f'{vis1}.txt'

df_csv1 = pd.read_csv(filename1, skiprows=3, skipfooter=3, header=None,
                     delim_whitespace=True, engine='python')

uv_dis_c1 = (df_csv1[0]+df_csv1[1])/2.0

# Define the x-axis values for vis1
x_values1 = uv_dis_c1 

# Define the y-axis values for vis1
y_values1 = df_csv1[2]

# Define the errorbar for vis1
error1 = df_csv1[3]

# Define the vis parameter of track2a
vis2a = 'WSB_31_track2a.rx240.lsb.cal.miriad'

# UvAmp command for vis2a
uvamp_command = [
    'uvamp',
    f'vis={vis2a}',
    'bin=50,4,klam',
    f'log={vis2a}.txt'
]

# Run UvAmp for vis2a
subprocess.run(uvamp_command)

# Reading file with pandas for vis2a
filename2a = f'{vis2a}.txt'

df_csv2a = pd.read_csv(filename2a, skiprows=3, skipfooter=3, header=None,
                     delim_whitespace=True, engine='python')

uv_dis_c2a = (df_csv2a[0]+df_csv2a[1])/2.0

# Define the x-axis values for vis2a
x_values2a = uv_dis_c2a 

# Define the y-axis values for vis2a
y_values2a = df_csv2a[2]

# Define the errorbar for vis2a
error2a = df_csv2a[3]

# Plot the data of vis1
plt.scatter(x_values1, y_values1, marker='o', label='track1')
plt.errorbar(x_values1, y_values1 , yerr=error1, fmt='o', elinewidth=1.5)

#Plot the data of vis2a
plt.scatter(x_values2a, y_values2a, marker='o', label='track2a')
plt.errorbar(x_values2a, y_values2a, yerr=error2a, fmt='o', elinewidth=1.5)

# Set labels and title
plt.xlabel('UVdistance (kλ)')
plt.ylabel('Amplitude (Jy)')
plt.title('WSB 31 visibility')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

