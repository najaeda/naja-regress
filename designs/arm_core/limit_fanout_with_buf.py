import logging
from naja import snl

def getPrimitives(top):
  primitives = []
    
  for inst in top.getInstances():
    path = snl.SNLPath(inst)
    stack = [[inst, path]]
    while stack:
        current = stack.pop()
        currentInst = current[0]    
        currentPath = current[1]
        for instChild in currentInst.getModel().getInstances():
            pathChild = snl.SNLPath(currentPath, instChild)
            if instChild.getModel().isPrimitive():
                primitives.append([instChild, pathChild])
            stack.append([instChild, pathChild])
  return primitives


def edit():

  N = 4
  fanout_file = open('fanout.list','w')
  logging.basicConfig(filename='edit.log', filemode='w' ,level=logging.DEBUG)
  universe = snl.SNLUniverse.get()
  if universe is None:
    logging.critical('No loaded SNLUniverse')
    return 1
  top = universe.getTopDesign()
  if top is None:
    logging.critical('SNLUniverse does not contain any top SNLDesign')
    return 1
  else:
    logging.info('Found top design ' + str(top))

  #print initial state
  if True :
    primitives = getPrimitives(top)

    for entry in primitives:
      inst = entry[0]
      path = entry[1]
      for term in inst.getInstTerms():
        if term.getDirection() == snl.SNLTerm.Direction.Output:
          ito = snl.SNLNetComponentOccurrence(path.getHeadPath(), term)
          equi = snl.SNLEquipotential(ito)
          primitiveCount = 0
          for to in equi.getInstTermOccurrences():
            if to.getInstTerm().getInstance().getModel().isPrimitive() and to.getInstTerm().getDirection() == snl.SNLTerm.Direction.Input:
              primitiveCount = primitiveCount + 1
          fanout_file.write(str(ito) + " " + str(primitiveCount))
          fanout_file.write("\n")

  primitives = []
  lib1 = top.getLibrary()
  bufferModel = None
  primitives = getPrimitives(top)
  primitiveLib = primitives[0][0].getModel().getLibrary()
  toLimitWithBuf = []

  #Create a buffer model with 1 in and 1 out
  bufferModel = snl.SNLDesign.createPrimitive(primitiveLib, "BUF")

  #bufferModel = snl.SNLDesign.create(top.getLibrary(), "BUF")
  i0 = snl.SNLScalarTerm.create(bufferModel, snl.SNLTerm.Direction.Input, "I")
  o0 = snl.SNLScalarTerm.create(bufferModel, snl.SNLTerm.Direction.Input, "O")
  netBuff = snl.SNLScalarNet.create(bufferModel, "net_buffer")
  i0.setNet(netBuff)
  o0.setNet(netBuff)

  #Collect the nets per context that need to be limited
  for entry in primitives:
    inst = entry[0]
    path = entry[1]
    for term in inst.getInstTerms():
      if term.getDirection() == snl.SNLTerm.Direction.Output:
        readersCountPerContext = dict()
        ito = snl.SNLNetComponentOccurrence(path.getHeadPath(), term)
        equi = snl.SNLEquipotential(ito)
        for to in equi.getInstTermOccurrences():
           if to.getInstTerm().getInstance().getModel().isPrimitive() == False or to.getInstTerm().getDirection() == snl.SNLTerm.Direction.Output:
              continue
           count = len(readersCountPerContext.get(str(to.getPath()), []))
           if to.getInstTerm().getInstance().getName() == "":
              continue
           if count == 0:
            readersCountPerContext[str(to.getPath())] = []
           readersCountPerContext[str(to.getPath())].append([to.getInstTerm().getBitTerm() , str(to.getInstTerm().getInstance().getName() ),to.getPath()])
          #  if len(readersCountPerContext.get(str(to.getPath()), [[]])) > N:
          #      print("found " + str(count))
        for key in readersCountPerContext:
            if (len(readersCountPerContext[key]) > N):
                toLimitWithBuf.append(readersCountPerContext[key])

  #Create the buffers to limit the fanout
  bufID = 0
  for entry in toLimitWithBuf:
      count = 0
      if (entry[0][2].size() == 0):
        #Context is top
        design = top
      else:
        #Context is deeper than top so need to be uniquified
        uniq = snl.SNLUniquifier(entry[0][2])
        instances = uniq.getPathUniqCollection()
        instancesList = [ins for ins in instances]
        lastInstance = instancesList[len(instancesList) - 1]
        design = lastInstance.getModel()
      termInstance = design.getInstance(entry[0][1])
      term = termInstance.getInstTerm(entry[0][0])
      net = term.getNet()
      currentBuffer = snl.SNLInstance.create(design, bufferModel, "buffer" + str(bufID))
      currentBuffer.getInstTerm(i0).setNet(net)
      netBuff = snl.SNLScalarNet.create(design, "net_buffer_" + str(bufID))
      currentBuffer.getInstTerm(o0).setNet(net)
      for term in entry:
          if count > N:
              count = 0
              bufID = bufID + 1
              currentBuffer = snl.SNLInstance.create(design, bufferModel, "buffer" + str(bufID))
              currentBuffer.getInstTerm(i0).setNet(net)
              netBuff = snl.SNLScalarNet.create(design, "net_buffer_" + str(bufID))
              currentBuffer.getInstTerm(o0).setNet(netBuff)
          termInstance = design.getInstance(term[1])
          termInstance.getInstTerm(term[0]).setNet(netBuff)
          count = count + 1
      bufID = bufID + 1

  print("Buffer model is " + str(bufferModel))  

  # print results
  if True :
    primitives = []
    fanout_file = open('fanoutBuf.list','w')
    primitives = getPrimitives(top)
    foundOverflow = False
    for entry in primitives:
      inst = entry[0]
      path = entry[1]
      for term in inst.getInstTerms():
        if term.getDirection() == snl.SNLTerm.Direction.Output:
          ito = snl.SNLNetComponentOccurrence(path.getHeadPath(), term)
          equi = snl.SNLEquipotential(ito)
          primitiveCount = 0
          bufcount = 0
          for to in equi.getInstTermOccurrences():
            if (str(to.getInstTerm().getInstance().getModel().getName()).count("BUF") == 0) and to.getInstTerm().getInstance().getModel().isPrimitive() and to.getInstTerm().getDirection() == snl.SNLTerm.Direction.Input:
              primitiveCount = primitiveCount + 1
            if (str(to.getInstTerm().getInstance().getModel().getName()).count("BUF") == 1) and to.getInstTerm().getInstance().getModel().isPrimitive() and to.getInstTerm().getDirection() == snl.SNLTerm.Direction.Input:
              bufcount = bufcount + 1
          if (primitiveCount > N):
            foundOverflow = True
          fanout_file.write(str(ito) + "(buf(" + str(bufcount) + ")) " + str(primitiveCount))
          fanout_file.write("\n")
    if foundOverflow:
        print("Found overflow afer limiting")