import logging
from naja import snl
import codecs
import faulthandler 
from xilinx import constructPrimitives
import netlist

def edit():
  faulthandler.enable()
  # Load primitives and design
  desingFiles = ["./arm_core_snl.v"]
  loader = netlist.Loader()
  loader.init()
  constructPrimitives(loader.getPrimitivesLibrary())
  loader.loadVerilog(desingFiles)
  loader.verify()

  # Collect and dump all driver fanouts
  fanout_file = open('fanoutNaja.list','w')
  primitives = netlist.getAllPrimitivesInstances()
  for entry in primitives:
    getInstTerms = entry.getInstTerms()
    for term in getInstTerms:
      if term.isOutput():
        equi = term.getEuiqpotential()
        primitiveCount = 0
        for equiTerm in equi.getInstTerms():
          if equiTerm.getInstance().isPrimitive() and equiTerm.isOutput() == False:
            primitiveCount = primitiveCount + 1
        fanout_file.write(equiTerm.getString() + " " + str(primitiveCount))
        fanout_file.write("\n")

edit()