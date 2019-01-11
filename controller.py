#i have taken refernce from http://www.anshumanc.ml
#we are implementing a kind of firewall that blocks some flows (one way)
#and allows others
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.revent import *
from pox.lib.addresses import EthAddr
log = core.getLogger()
#adding hosts MACs in a list 
rules = [['02:00:00:00:03:00','02:00:00:00:02:00'],['02:00:00:00:01:00', '02:00:00:00:00:00']]

class block (EventMixin):
    
    def __init__ (self):
        self.listenTo(core.openflow)
        
    def _handle_ConnectionUp (self, event): #blocking some flows here as per assignmnet rules
         for rule in rules:
            block = of.ofp_match()

            block.dl_src = EthAddr(rule[0]) 
            block.dl_dst = EthAddr(rule[1]) 
	    
            flow_mod = of.ofp_flow_mod()
            flow_mod.match = block
            event.connection.send(flow_mod)
         msg = of.ofp_flow_mod() #from below here just forwarding packets from port1 to port 2 and vice versa
         msg.priority =1
         msg.idle_timeout = 0
         msg.hard_timeout = 0
         msg.match.in_port =1
         msg.actions.append(of.ofp_action_output(port = 2))
         event.connection.send(msg)
         msg = of.ofp_flow_mod()
         msg.priority =1
         msg.idle_timeout = 0
         msg.hard_timeout = 0
         msg.match.in_port =2
         msg.actions.append(of.ofp_action_output(port = 1))
         event.connection.send(msg)
         
         
        
def launch ():
    core.registerNew(block)





