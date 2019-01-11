#!/usr/bin/python
#I have created topology with help of miniedit
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station
from mn_wifi.cli import CLI_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call
import os
#class to use our controller my_controller
class pox_con(Controller):
  def start(self):
    self.pox='%s/pox/pox.py' %os.environ['HOME']
    self.cmd(self.pox, "my_controller &")
  def stop(self):
    self.cmd('kill %'+self.pox)

controllers = { 'poxcon': pox_con}
#below is the topology defined
def myNetwork():

    net = Mininet_wifi( topo=None, build=False,link=wmediumd,wmediumd_mode=interference,ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',controller=pox_con,ip='127.0.0.1',protocol='tcp',port=6633)

    info( '*** Add switches/APs\n')
    ap2 = net.addAccessPoint('ap2',  ssid='ap2-ssid',channel='1', mode='g', position='590,340,0')
    s1 = net.addSwitch('s1')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid',channel='1', mode='g', position='270,339,0')

    info( '*** Add hosts/stations\n')
    sta2 = net.addStation('sta2', ip='10.0.0.2',position='320,480,0')
    sta4 = net.addStation('sta4', ip='10.0.0.4',position='730,470,0')
    sta1 = net.addStation('sta1', ip='10.0.0.1',position='150,470,0')
    sta3 = net.addStation('sta3', ip='10.0.0.3',position='540,470,0')

    net.configureWifiNodes()
    info( '*** Add links\n')
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(ap2, sta3)
    net.addLink(ap2, sta4)
    net.addLink(s1, ap1)
    net.addLink(s1, ap2)

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap2').start([c0])
    net.get('s1').start([c0])
    net.get('ap1').start([c0])

    info( '*** Post configure nodes\n')

    CLI_wifi(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

