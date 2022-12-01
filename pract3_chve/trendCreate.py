import rrdtool
ret = rrdtool.create("/home/chve117/Documentos/pract3-20221130T151730Z-001/pract3/RRD/trend.rrd",
                     "--start",'N',
                     "--step",'60',
                     "DS:CPUload:GAUGE:60:0:100",
                     "DS:RAMused:GAUGE:60:0:100",
                     "DS:Diskused:GAUGE:60:0:100",
                     "RRA:AVERAGE:0.5:1:24")
if ret:
    print (rrdtool.error())
