#!/bin/bash

vis='WSB_31_combined.rx240.lsb.cal.miriad'

# Clean the map
clean map=${vis}.dirty \
	beam=${vis}.beam \
	out=${vis}.10.model \
	cutoff=0.01 \
	niters=10 \
	options=positive

restor map=${vis}.dirty \
	beam=${vis}.beam \
	model=${vis}.10.model \
	mode=clean out=${vis}.clean

# Restore the map
restor map=${vis}.dirty \
	model=${vis}.10.model \
	beam=${vis}.beam \
	mode=residual \
	out=${vis}.residual
