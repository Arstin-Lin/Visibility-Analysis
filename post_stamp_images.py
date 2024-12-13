import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import math

def write_to_file(file, field, value):
    txt_file = file
    new_row = 1
    add_line = str(value)+'   '
    try:
        with open(txt_file, 'r') as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.split()[0] == field:
                new_line=line[:-1]+add_line+'\n'
                lines[i]=new_line
                new_row = 0
                break
        if new_row == 1:
            with open(txt_file, 'a') as f:
                f.write('\n')
                f.write(''.join(field+'   '+add_line))
        else:
            with open(txt_file, 'w') as f:
                f.writelines(lines)
    except:
        with open(txt_file, 'w') as f:
            f.write(''.join(field+'   '+add_line))

# List of targets
targets = ['AS_206', 'DoAr_16', 'DoAr_24E', 'DoAr_25', 'DoAr_33', 'DoAr_44', 'GSS_26', 'GSS_39', 
           'HBC_266', 'IRS_37', 'IRS_39', 'IRS_41', 'IRS_51', 'VSSG_1', 'WSB_31', 'WSB_60', 
           'YLW_47', 'YLW_8']

# Imaging settings
tracks = ['track1']
rxs = ['rx240', 'rx345']
sidebands = ['lsb', 'usb']

for track in tracks:
    for rx in rxs:
        for sideband in sidebands:
            fig = plt.figure(figsize=(16, 10))
            for i, target in enumerate(targets):
                filename = f"{target}_{track}.{rx}.{sideband}.sel.clean.fits"
                if_success = False
                try:
                    # Open the FITS file and extract data
                    with fits.open(filename) as hdul:
                        hdul.info()
                        hdu = hdul[0]
                        data = hdu.data[0][0]  # Access image data
                        if_success = True
                except:
                    print(f"Unable to read the intensity FITS image: {filename}")
                    write_to_file(f'beam_{track}.sel.txt', target, "0.0 0.0")
                    # Placeholder for missing or unreadable FITS
                    ax = plt.subplot2grid((5, 8), (math.floor(i / 8), i % 8))
                    ax.text(0.5, 0.5, target.replace('_', ' '), fontsize=10, ha='center', va='center')
                    ax.axis('off')
                    continue

                if if_success:
                    try:
                        # Extract WCS and header parameters
                        wcs = WCS(hdu.header).dropaxis(2).dropaxis(2)
                        naxis1 = hdu.header['naxis1']
                        naxis2 = hdu.header['naxis2']
                        cdelt1 = hdu.header['cdelt1']
                        cdelt2 = hdu.header['cdelt2']
                        bmaj = hdu.header['bmaj']
                        bmin = hdu.header['bmin']
                        bpa = hdu.header['bpa']
                        
                        # Write beam parameters to the file
                        write_to_file(f'beam_{track}.sel.txt', target, f"{bmaj} {bmin}")

                        # Calculate cropping box centered on the image
                        cen_x = naxis1 / 2
                        cen_y = naxis2 / 2
                        crop_size = 4 / (abs(cdelt2) * 3600)  # 4 arcsec half-size
                        box0 = max(0, int(cen_x - crop_size))
                        box1 = max(0, int(cen_y - crop_size))
                        box2 = min(naxis1, int(cen_x + crop_size))
                        box3 = min(naxis2, int(cen_y + crop_size))

                        # Crop the data
                        cutdata = data[box1:box3, box0:box2]

                        # Plot the data
                        ax = plt.subplot2grid((5, 8), (math.floor(i / 8), i % 8), projection=wcs)
                        ax.set_xlabel(' ')
                        ax.set_ylabel(' ')
                        ax.tick_params(axis='x', which='both', labelbottom=False)
                        ax.tick_params(axis='y', which='both', labelbottom=False)

                        vmax = np.nanmax(data) * 1.2
                        vmin = 0.0
                        ax.imshow(cutdata, origin='lower', vmax=vmax, vmin=vmin, cmap='viridis')

                        # Add target name
                        ax.text(0.02, 0.98, target.replace("_", " "), 
                                transform=ax.transAxes, fontsize=10, color="white", 
                                verticalalignment='top', horizontalalignment='left')

                        # Add the synthesized beam
                        beam = Ellipse((cutdata.shape[0] / 5, cutdata.shape[1] / 5), 
                                       width=bmin / abs(cdelt1), 
                                       height=bmaj / abs(cdelt2), 
                                       angle=bpa, facecolor="None", edgecolor='white', lw=1)
                        ax.add_patch(beam)

                    except Exception as e:
                        print(f"Error processing data for {target}: {e}")
                        # Add placeholder if processing fails
                        ax = plt.subplot2grid((5, 8), (math.floor(i / 8), i % 8))
                        ax.text(0.5, 0.5, target.replace('_', ' '), fontsize=10, ha='center', va='center')
                        ax.axis('off')

            fig.tight_layout()
            output_filename = f"{track}_{rx}_{sideband}_poststamp.pdf"
            plt.savefig(output_filename, format='PDF', transparent=True)
            plt.close(fig)

