#!/bin/bash
snmptrap -v 1 -c comunidadTRAPS localhost:163 1.2.3.4.5 192.168.1.1 2 0 "100" IF-MIB::ifIndex i 2
snmptrap -v 1 -c comunidadTRAPS localhost:163 1.2.3.4.5 192.168.1.1 3 0 "100" IF-MIB::ifIndex i 2
snmptrap -v 1 -c comunidadTRAPS localhost:163 1.2.3.4.5 192.168.1.1 1 0 "100" IF-MIB::ifIndex i 2
snmptrap -v 1 -c comunidadTRAPS localhost:163 1.2.3.4.5 192.168.1.1 0 0 "100" IF-MIB::ifIndex i 2
snmptrap -v 1 -c comunidadTRAPS localhost:163 '1.2.3.4.5.6' '192.168.1.1' 6 99 '55' 1.11.12.13.14.15 s "testString"
exit
 
