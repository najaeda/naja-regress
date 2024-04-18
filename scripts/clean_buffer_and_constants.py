import logging
import snl

def clean_constant(ins):
  model = ins.getModel()
  out = ins.getInstTerm(model.getScalarTerm('Z'))
  if out is None:
    raise('Cannot find Z output')
  outNet = out.getNet()
  if model.getName() == 'LOGIC0_X1':
    outNet.setType(snl.SNLNet.Type.Assign0)
  elif model.getName() == 'LOGIC1_X1':
    outNet.setType(snl.SNLNet.Type.Assign1)
  logging.info('Remove: ' + ins.getName() + ':' + model.getName() + " in " + ins.getDesign().getName())
  logging.info('Change ' + str(outNet) + ' to ' + outNet.getTypeAsString())
  ins.destroy()

def clean_buffer(ins):
  model = ins.getModel()
  if 'BUF_X' in model.getName():
    a = ins.getInstTerm(model.getScalarTerm('A'))
    z = ins.getInstTerm(model.getScalarTerm('Z'))
    aNet = a.getNet()
    zNet = z.getNet()
    for component in zNet.getComponents():
      component.setNet(aNet)
    if type(zNet) is snl.SNLScalarNet:
      zNet.destroy()
    ins.destroy()

def clean_buffer_and_constants(design):
  for ins in design.getInstances():
    model = ins.getModel()
    if 'LOGIC' in model.getName():
      clean_constant(ins)
    elif 'BUF_X' in model.getName():
      clean_buffer(ins)
    elif not model.isPrimitive():
      clean_buffer_and_constants(model)
