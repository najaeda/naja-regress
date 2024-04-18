import logging
from naja import snl
import save_design_stats

def edit():
  logging.basicConfig(filename='pre_edit.log', filemode='w' ,level=logging.DEBUG)
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

  #clean_buffer_and_constants(top)
  save_design_stats.save_design_stats(top, 'init_design.stats')
