import logging
from naja import snl
import codecs
import faulthandler 
from xilinx import constructPrimitives # from naja/install/share/primitives/xilinx.py
import netlist # from naja/src/python/netlist/netlist.py

def edit():
  faulthandler.enable()
  # Load primitives and design
  desingFiles = ["./arm_core_snl.v"]
  loader = netlist.Loader()
  loader.init()
  constructPrimitives(loader.getPrimitivesLibrary())
  loader.loadVerilog(desingFiles)
  loader.verify()

  # Get all primitives instances 
  primitives = netlist.getAllPrimitiveInstances()

  # Collect and dump all driver fanouts
  fanout_file = open('fanoutNaja.list','w')

  for inst in primitives:
    # Iterate over instance's terms
    for term in inst.getOutputInstTerms():
      fanout_file.write(term.getString() + " " + str(term.getFlatFanout()))
      fanout_file.write("\n")

edit()
