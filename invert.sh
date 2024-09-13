#!/bin/bash

vis='WSB_31_combined.rx240.lsb.cal.miriad'

uvflag vis=${vis} \
	edge=64,64,0 flagval="f" 

invert vis=${vis} \
	options=systemp,double,mfs robust=2.0 \
	map=${vis}.dirty \
	beam=${vis}.beam cell=0.25 imsize=512
