import sys
from astropy.io import fits
import numpy as np

def get_rms(data):
    ""Calculate the RMS noise level of an image data array.""
    # Select pixels with low absolute values (assumed to be mostly noise)
    threshold = 3 * np.median(np.abs(data))  # a typical threshold
    noise_data = data[np.abs(data) < threshold]
    rms = np.sqrt(np.mean(noise_data**2))
    return rms

def main():
    # Capture command-line arguments for the receiver (rx), sideband, target, and track
    rx = sys.argv[1]
    sideband = sys.argv[2]
    target = sys.argv[3]
    track = sys.argv[4]
    
    # Construct the filename for the image file
    filename = f"{target}_{track}.{rx}.{sideband}.dirty.fits"
    
    # Load the FITS file
    with fits.open(filename) as hdul:
        data = hdul[0].data.squeeze()  # Assume image is in primary HDU, remove empty dimensions
    
    # Calculate RMS
    rms = get_rms(data)
    
    # Define region of interest (arbitrary values; user should define actual regions)
    # Here, for simplicity, a default box is used; this would typically be based on image inspection
    region_box = [50, 50, 100, 100]  # Placeholder coordinates for bounding box
    
    # Output the result for the shell script to read
    print(f"{rms}   {region_box[0]}   {region_box[1]}   {region_box[2]}   {region_box[3]}")

if __name__ == "__main__":
    main()
