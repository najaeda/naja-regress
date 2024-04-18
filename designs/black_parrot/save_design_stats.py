from naja.stats import design_stats

def save_design_stats(top, stats_file):
  designs_stats = dict()
  design_stats.compute_design_stats(top, designs_stats) 

  #stats = open(stats_file, 'w')

  #dumped_models = set()
  #stats.design_stats.dump_stats(top, stats, designs_stats, dumped_models) 

  #analyzed_models = set()
  #design_stats.dump_constants(top, analyzed_models)
