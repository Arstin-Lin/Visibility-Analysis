import pandas as pd
import matplotlib.pyplot as plt
import subprocess

# Define the vis parameter of track1
vis1 = 'WSB_31_track1.rx240.usb.cal.miriad'

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
    'bin=25,4,klam',
    f'log={vis1}.txt'
]

# Run UvAmp
subprocess.run(uvamp_command)

# Reading file with pandas for vis1
filename1 = f'{vis1}.txt'

df_csv1 = pd.read_csv(filename1, skiprows=3, skipfooter=3, header=None,
                     delim_whitespace=True, engine='python')

uv_dis_c1 = (df_csv1[0] + df_csv1[1]) / 2.0

# Define the x-axis values for vis1
x_values1 = uv_dis_c1 

# Define the y-axis values for vis1
y_values1 = df_csv1[2]

# Define the errorbar for vis1
error1 = df_csv1[3]

# Filter out zero values of vis1
non_zero_mask1 = y_values1 != 0
x_filtered1 = x_values1[non_zero_mask1]
y_filtered1 = y_values1[non_zero_mask1]
error_filtered1 = error1[non_zero_mask1]

# Define the vis parameter of track2a
vis2a = 'WSB_31_track2a.rx240.usb.cal.miriad'

# UvAmp command for vis2a
uvamp_command = [
    'uvamp',
    f'vis={vis2a}',
    'bin=25,8,klam',
    f'log={vis2a}.txt'
]

# Run UvAmp for vis2a
subprocess.run(uvamp_command)

# Reading file with pandas for vis2a
filename2a = f'{vis2a}.txt'

df_csv2a = pd.read_csv(filename2a, skiprows=3, skipfooter=3, header=None,
                     delim_whitespace=True, engine='python')

uv_dis_c2a = (df_csv2a[0] + df_csv2a[1]) / 2.0

# Define the x-axis values for vis2a
x_values2a = uv_dis_c2a 

# Define the y-axis values for vis2a
y_values2a = df_csv2a[2]

# Define the errorbar for vis2a
error2a = df_csv2a[3]

# Filter out zero values of vis2a
non_zero_mask2a = y_values2a != 0
x_filtered2a = x_values2a[non_zero_mask2a]
y_filtered2a = y_values2a[non_zero_mask2a]
error_filtered2a = error2a[non_zero_mask2a]

# Plot the data of vis1
plt.scatter(x_filtered1, y_filtered1, marker='o', label='track1')
plt.errorbar(x_filtered1, y_filtered1, yerr=error_filtered1, fmt='o', elinewidth=1.5)

# Plot the data of vis2a
plt.scatter(x_filtered2a, y_filtered2a, marker='o', label='track2a')
plt.errorbar(x_filtered2a, y_filtered2a, yerr=error_filtered2a, fmt='o', elinewidth=1.5)

# Set labels and title
plt.xlabel('UVdistance (kλ)')
plt.ylabel('Amplitude (Jy)')
plt.title('WSB 31 visibility')
plt.legend()

# Save the plot as a PDF file
plt.savefig(f'{vis1}.pdf', format='pdf')
plt.close()


# Define the y-axis values for vis1
y_values1 = df_csv1[2]

# Define the errorbar for vis1
error1 = df_csv1[3]

# Filter out zero values of vis1
x_filtered1 = x[y != 0]
y_filtered1 = y[y != 0]

# Define the vis parameter of track2a
vis2a = 'WSB_31_track2a.rx240.lsb.cal.miriad'

# UvAmp command for vis2a
uvamp_command = [
    'uvamp',
    f'vis={vis2a}',
    'bin=25,8,klam',
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

# Filter out zero values of vis2a
x_filtered2a = x[y != 0]
y_filtered2a = y[y != 0]

# Plot the data of vis1
plt.scatter(x_filtered1, y_filtered1, marker='o', label='track1')
plt.errorbar(x_filtered1, y_filtered1 , yerr=error1, fmt='o', elinewidth=1.5)

#Plot the data of vis2a
plt.scatter(x_filtered2a, y_filtered2a, marker='o', label='track2a')
plt.errorbar(x_filtered2a, y_filtered2a, yerr=error2a, fmt='o', elinewidth=1.5)

# Set labels and title
plt.xlabel('UVdistance (kλ)')
plt.ylabel('Amplitude (Jy)')
plt.title('WSB 31 visibility')
plt.legend()

# Saved the plot as a PDF file
plt.savefig(f'{vis1}.pdf', format='pdf')
plt.close()
