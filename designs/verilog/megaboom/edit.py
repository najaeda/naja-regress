import logging
from naja import snl
from naja.stats import design_stats

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
  design_stats.compute_design_stats(top, designs_stats) 

  stats = open('design.stats', 'w')

  dumped_models = set()
  design_stats.dump_stats(top, stats, designs_stats, dumped_models) 

  analyzed_models = set()
  #design_stats.dump_constants(top, analyzed_models)
