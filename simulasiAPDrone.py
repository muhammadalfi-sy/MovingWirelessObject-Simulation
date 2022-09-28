#!/usr/bin/env python
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi

def topology(args):

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    h1 = net.addHost( 'h1', mac='00:00:00:00:00:01', ip='192.168.100.5/24' )
    sta1 = net.addStation( 'sta1', mac='00:00:00:00:00:02', ip='192.168.100.1/24', range='30' )
    ap1 = net.addAccessPoint( 'ap1', ssid= 'AlfiCorp-01', mode= 'g', channel= '1', position='50,50,0', range='60' )
    ap2 = net.addAccessPoint( 'ap2', ssid= 'AlfiCorp-02', mode= 'g', channel= '1', position='200,50,0', range='60' )
    ap3 = net.addAccessPoint( 'ap3', ssid= 'AlfiCorp-03', mode= 'g', channel= '1', position='200,200,0', range='60' )
    ap4 = net.addAccessPoint( 'ap4', ssid= 'AlfiCorp-04', mode= 'g', channel= '1', position='50,200,0', range='60' )
    c1 = net.addController( 'c1' )

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Associating and Creating links\n")
    net.addLink(ap1, h1)
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)
    net.addLink(ap3, ap4)
    net.addLink(ap1, ap4)

    if '-p' not in args:
        net.plotGraph(max_x=250, max_y=250)

    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=250, max_y=250, seed=20)
    
    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap4.start([c1])

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology(sys.argv)
