# Plotting Script
import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from ROOT import gPad
from pylab import *
sys.path.append('../python/')
# Considering your module contains a function called my_func, you could import it:
import plotting
import helpers
import atlas_style

ROOT.gROOT.SetBatch(True)


#trying to  set ATLAS style a million different ways
gROOT.SetStyle("ATLAS") #might have to change how you set atlas style like this, depends how you have setup python
# atlas_style.AtlasStyle()	
# gROOT.LoadMacro("AtlasStyle.C")
# gROOT.LoadMacro("AtlasUtils.C")
# gROOT.LoadMacro("AtlasLabels.C")
# SetAtlasStyle()

logger = helpers.getLogger('dHNLAnalysis.plotHisotgrams')

#############################################################################################################################################
# globals
outputDir = '../output/plotting_updates/' # change path here to save your histograms somewhere else!
MATERIAL_LAYERS = [33.25, 50.5, 88.5, 122.5, 299]
normalize = True
setlogy = False
drawRatio=False
draw_channel_info = not normalize
do_cut_significane = True

#############################################################################################################################################


def sv_validation(config_file, selection):
	hist_channels = []
	# hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>)
	hist_channels.append([config_file["rerunVSIfile"],"VSI", "VSI", selection])
	hist_channels.append([config_file["rerunVSIfile"],"VSI_2", "VSI_2", selection])

	plotting.compare(hist_channels,
						 variable='DV_r',
						 nRebin=10,
						 setrange=(0, 350),
						 vertical_lines=MATERIAL_LAYERS,
						 vertical_legend="Material Layers",
						 output_dir= outputDir
						 )



if __name__ == '__main__':
	import argparse
	class AppendActionCleanDefault(argparse._AppendAction):
		def __init__(self, *args, **kwargs):
			super(argparse._AppendAction, self).__init__(*args,**kwargs)
			self.index = 0
		def __call__(self, parser, namespace, values, option_string = None):
			items = argparse._copy.copy(argparse._ensure_value(namespace, self.dest, [])) if self.index else []
			if values:
				self.index += 1
				items.append(values)
				setattr(namespace, self.dest, items)


	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, add_help=False)

	parser.add_argument("--config",
						dest="config",
						type = str,
						required = True,
						help="Input config file for plotHisotgrams.py.")

	parent_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, parents = [parser]) 

	options = parent_parser.parse_args()


	if not os.path.exists(outputDir): os.mkdir(outputDir)
	if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
	if not os.path.exists(outputDir + "Cutflows/"): os.mkdir(outputDir + "Cutflows/")
	if not os.path.exists(outputDir + "2Dmassplots"): os.mkdir(outputDir + "2Dmassplots")
	if not os.path.exists(outputDir + "2Dmassplots/data/"): os.mkdir(outputDir + "2Dmassplots/data/")
	if not os.path.exists(outputDir + "2Dmassplots/data/"): os.mkdir(outputDir + "2Dmassplots/data/")




	with open(options.config, 'r') as json_config:
		config_file = json.load(json_config) # load JSON config file


	#execute plotting here, comment out functions in you dont want to plot them again.	
	sv_validation(config_file)
	# compare_reco_histograms(config_file, 'DVtype')
	# compare_truth_histograms(config_file, 'truth')
	# compare_Wboson_asymmetry(config_file, 'truth')
	# check_rerunningVSI(config_file,"all")

	
	