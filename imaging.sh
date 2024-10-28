#!/bin/bash
flagval="f"

targets='AS_206  DoAr_16  DoAr24E  DoAr_33  DoAr_44  GSS_26  GSS_39  HBC_266  IRS_37  IRS_39  IRS_41  IRS_51  VSSG_1  WSB_31  WSB_60  YLW_47  YLW_8'
tracks='track1'
sidebands='lsb usb'
rxs='rx240 rx345'

for track in $tracks
do
	cd ch0/
	rm -rf $track
  	mkdir $track
 	cd ../

	for rx in $rxs
	do
		for sideband in $sidebands
		do
			if [ $track = 'track1' ]
			then
				cellsize=0.25
				imsize=256
			fi
			if [ $track = 'track2' ]
			then
				cellsize=0.25
				imsize=256
			fi

			for target in $targets
			do
				datadir='../calibrated_Miriad/'$track'/'
 			        vis=$target'_'$track'.'$rx'.'$sideband'.cal.miriad'
          			cp -r $datadir$vis ./

				uvaver vis=$vis options=nocal,nopass,nopol, line=channel,1024,1,4,4, out=$vis'.c'
				uvflag vis=$vis edge=64,64,0 flagval="f"

				# creating non-self-calibrated image
          			rm -rf $target'.'$track'.'$rx'.'$sideband'.dirty'
          			rm -rf $target'.'$track'.'$rx'.'$sideband'.beam'
				invert vis=$vis \
					options=systemp,double,mfs robust=2.0 \
					map=$target'_'$track'.'$rx'.'$sideband'.dirty' \
					beam=$target'_'$track'.'$rx'.'$sideband'.beam' cell=$cellsize imsize=$imsize
					select='uvrange(0,80)'

         			rm -rf $target'.'$track'.'$rx'.'$sideband'.dirty.fits'
          			rm -rf $target'.'$track'.'$rx'.'$sideband'.beam.fits'
          			fits in=$target'.'$track'.'$rx'.'$sideband'.dirty' op=xyout out=$target'.'$track'.'$rx'.'$sideband'.dirty.fits'
          			fits in=$target'.'$track'.'$rx'.'$sideband'.beam' op=xyout out=$target'.'$track'.'$rx'.'$sideband'.beam.fits'

          			rm -rf $target'.'$track'.'$rx'.'$sideband'.10.model'
         			rm -rf $target'.'$track'.'$rx'.'$sideband'.10.model.fits'
				clean map=$target'_'$track'.'$rx'.'$sideband'.dirty' \
					beam=$target'_'$track'.'$rx'.'$sideband'.beam' \
					out=$target'.'$track'.'$rx'.'$sideband'.10.model' cutoff=0.01 niters=10 \
					options=positive
				fits in=$target'.'$track'.'$rx'.'$sideband'.10.model' op=xyout out=$target'.'$track'.'$rx'.'$sideband'.10.model.fits'

				rm -rf $target'.'$track'.'$rx'.'$sideband'.clean'
				rm -rf $target'.'$track'.'$rx'.'$sideband'.clean.fits'
				restor map=$target'.'$track'.'$rx'.'$sideband'.dirty' \
				        beam=$target'.'$track'.'$rx'.'$sideband'.beam' \
				        model=$target'.'$track'.'$rx'.'$sideband'.10.model' \
				        mode=clean out=$target'.'$track'.'$rx'.'$sideband'.clean'
				fits in=$target'.'$track'.'$rx'.'$sideband'.clean' op=xyout out=$target'.'$track'.'$rx'.'$sideband'.clean.fits'

				rm -rf $target'.'$track'.'$rx'.'$sideband'.residual'
			        rm -rf $target'.'$track'.'$rx'.'$sideband'.residual.fits'
			        restor map=$target'.'$track'.'$rx'.'$sideband'.dirty' \
			                beam=$target'.'$track'.'$rx'.'$sideband'.beam' \
			                model=$target'.'$track'.'$rx'.'$sideband'.10.model' \
			                mode=residual out=$target'.'$track'.'$rx'.'$sideband'.residual'
			        fits in=$target'.'$track'.'$rx'.'$sideband'.residual' op=xyout out=$target'.'$track'.'$rx'.'$sideband'.residual.fits'
			done
		done
	done
done
