#!/bin/bash

targets='AS_206  DoAr_16  DoAr24E  DoAr_33  DoAr_44  GSS_26  GSS_39  HBC_266  IRS_37  IRS_39  IRS_41  IRS_51  VSSG_1  WSB_31  WSB_60  YLW_47  YLW_8'
sidebands='lsb usb'
rxs='rx240 rx345'

datadir='/home/arstinlin/DATA/Oph_SMA/compare_visibility/track1_2a'
outputdir='/home/arstinlin/DATA/Oph_SMA/compare_visibility/track1_2a_combined'

# Create output directory if it doesn't exist
mkdir -p $outputdir

# UvAver: combine visibility data
for target in $targets
do
	for sideband in $sidebands
	do
		for rx in $rxs
		do
			vis1="$datadir/${target}_track1.${rx}.${sideband}.cal.miriad.c"
			vis2="$datadir/${target}_track2a.${rx}.${sideband}.cal.miriad"
			
			echo "Checking files: '$vis1' and '$vis2'"
			if [ -e "$vis1" ] && [ -e "$vis2" ]; then
				uvaver vis=${vis1} ${vis2} \
				out=${target}_combined.${rx}.${sideband}.cal.miriad
			else
				echo "One or both files ($vis1, $vis2) do not exist. Skipping..."
			fi
		done
	done
done

