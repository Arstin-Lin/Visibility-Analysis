#!/bin/bash
targets='AS_206  DoAr_16  DoAr24E  DoAr_33  DoAr_44  GSS_26  GSS_39  HBC_266  IRS_37  IRS_39  IRS_41  IRS_51  VSSG_1  WSB_31  WSB_60  YLW_47  YLW_8'
sidebands='lsb usb'
rxs='rx240 rx345'

# UvAver
for target in $targets
do
    datadir='/home/arstinlin/DATA/image_Oph/imaging/track1/track1'
    output_dir='/home/arstinlin/DATA/image_Oph/imaging/track1/lined_track1'
    mkdir -p $output_dir

    for sideband in $sidebands
    do
        for rx in $rxs
        do
            vis="$datadir/${target}_track1.${rx}.${sideband}.cal.miriad"

            echo "Checking file: '$vis'"  # Debugging line
            if [ -e $vis ]; then
               uvaver vis=${vis} \
               line=channel,1024,1,4,4 out=${target}_track1.${rx}.${sideband}.cal.miriad.c
            else
               echo "File $vis does not exist. Skipping..."
            fi
        done
    done
done

