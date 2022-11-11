#!/usr/bin/env python
import rrdtool
ret = rrdtool.create("segmentosRed.rrd",
                     "--start",'N',
                     "--step",'300',
                     "DS:unicastPaq:COUNTER:120:U:U",
                     "DS:ipv4Paq:COUNTER:120:U:U",
                     "DS:echoICMP:COUNTER:120:U:U",
                     "DS:segmentoEntrada:COUNTER:120:U:U",
                     "DS:datagramaSalida:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:6:700",
                     "RRA:AVERAGE:0.5:1:1400")

if ret:
    print (rrdtool.error())
