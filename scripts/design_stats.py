import logging
import snl

class DesignStats:
  def __init__(self):
    self.primitives = dict()
    self.flat_primitives = dict()
    self.ins = dict()
    self.flat_ins = dict()
  def add_ins_stats(self, ins_stats):
    for ins, nb in ins_stats.flat_ins.items():
      self.flat_ins[ins] = self.flat_ins.get(ins, 0) + nb
    for primitive, nb in ins_stats.flat_primitives.items():
      self.flat_primitives[primitive] = self.flat_primitives.get(primitive, 0) + nb

def compute_design_stats(design, designs_stats):
  if design in designs_stats:
    return designs_stats.get(design)
  design_stats = DesignStats()
  for ins in design.getInstances():
    model = ins.getModel()
    if model.isPrimitive():
      design_stats.primitives[model] = design_stats.primitives.get(model, 0) + 1
      design_stats.flat_primitives[model] = design_stats.flat_primitives.get(model, 0) + 1
    else:
      if model in designs_stats:
        model_stats = designs_stats[model]
      else:
        model_stats = compute_design_stats(model, designs_stats)
      design_stats.ins[model] = design_stats.ins.get(model, 0) + 1
      design_stats.flat_ins[model] = design_stats.flat_ins.get(model, 0) + 1
      design_stats.add_ins_stats(model_stats)
  designs_stats[design] = design_stats
  return design_stats

def dump_instances(stats_file, title, instances):
  if len(instances) == 0:
    return
  stats_file.write(title + ' ' + str(sum(instances.values())) + '\n')
  i = 0
  for instance, nb in instances.items():
    if i!=0:
      stats_file.write(",")
    if i>5:
      stats_file.write('\n')
      i = 0
    elif i!=0:
      stats_file.write(" ")
    i=i+1
    stats_file.write(instance.getName() + ":" + str(nb))
  stats_file.write('\n\n')

def dump_stats(design, stats_file, designs_stats, dumped_models):
  if design.isPrimitive():
    return
  if design in dumped_models:
    return
  dumped_models.add(design)
  stats_file.write('*** ' + design.getName() + ' ***\n')
  design_stats = designs_stats.get(design)
  if design_stats is None:
    print('Cannot find ' + str(design) + ' in design_stats')
    raise
  dump_instances(stats_file, 'Instances:', design_stats.ins)
  dump_instances(stats_file, 'Primitives:', design_stats.primitives)
  dump_instances(stats_file, 'Flat Instances:', design_stats.flat_ins)
  dump_instances(stats_file, 'Flat Primitives:', design_stats.flat_primitives)
  stats_file.write('\n')
  for ins in design.getInstances():
    model = ins.getModel()
    dump_stats(model, stats_file, designs_stats, dumped_models) 
  
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

  designs_stats = dict()
  compute_design_stats(top, designs_stats) 

  stats = open('design.stats', 'w')

  dumped_models = set()

  dump_stats(top, stats, designs_stats, dumped_models) 
