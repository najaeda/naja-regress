import logging
from naja import snl

def edit():
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

  primitives = []
  fanout_file = open('fanout.list','w')
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

  for entry in primitives:
    inst = entry[0]
    path = entry[1]
    print(inst)
    print(path)
    for term in inst.getInstTerms():
      if term.getDirection() == snl.SNLTerm.Direction.Output:
        ito = snl.SNLNetComponentOccurrence(path.getHeadPath(), term)
        print('For primitive output:')
        print(ito)
        equi = snl.SNLEquipotential(ito)
        print('Fan out is:')
        print(len(tuple(equi.getInstTermOccurrences())) - 1)
        fanout_file.write(str(ito) + " " + str(len(tuple(equi.getInstTermOccurrences())) - 1))
        fanout_file.write("\n")


