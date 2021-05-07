# Plotting Script adapted from VH4b plotting and DHNLNtupleAnalaysis plotting scripts
# Last Major Overhaul of Code: Oct 16 2020 by D. Trischuk
import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from pylab import *
import atlas_style
import argparse
ROOT.gROOT.SetBatch(True)
from plot_classes import CutFlow
import argparse


#trying to  set ATLAS style a million different ways
gROOT.SetStyle("ATLAS") #might have to change how you set atlas style like this, depends how you have setup python
# atlas_style.AtlasStyle()	
# gROOT.LoadMacro("AtlasStyle.C")
# gROOT.LoadMacro("AtlasUtils.C")
# gROOT.LoadMacro("AtlasLabels.C")
# SetAtlasStyle()

#############################################################################################################################################
# Config Parser Setup
#############################################################################################################################################
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
                    help="Input config file for makeHisotgrams.py.")

parent_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, parents = [parser]) 
options = parent_parser.parse_args()

#############################################################################################################################################
# Make output dirs and Parse Configs
#############################################################################################################################################
outputDir = '../output/susy15_validation/' # change path here to save your histograms somewhere else!
if not os.path.exists(outputDir): os.mkdir(outputDir)
if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
if not os.path.exists(outputDir + "cutflows/"): os.mkdir(outputDir + "cutflows/")
with open(options.config, 'r') as json_config:
    config_file = json.load(json_config) # load JSON config file
#############################################################################################################################################

#############################################################################################################################################
# Globals
#############################################################################################################################################
log_scale_y = False
#############################################################################################################################################

# vtx_channels = ["VSI","VSI_Leptons","VSI_LRTR3_1p0","VSI_LeptonsMod_LRTR3_1p0","VSI_Leptons_LRTR3_1p0"]
vtx_channels = ["VSI_LeptonsMod_LRTR3_1p0"]
ln_type = "mixed"
selection = "DVtype"
for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>)
    # hist_channels.append([config_file["dataFile"],config_file["dataLabel"], vtx_channel, selection])

    # hist_channels.append([config_file["ttbarFile"],config_file["ttbarLabel"], vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_eee"],config_file["dataLabel_eee"], vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_uuu"],config_file["dataLabel_uuu"], vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_uue"],config_file["dataLabel_uue"], vtx_channel, selection])


    # hist_channels.append([config_file["mcFiles"][0], config_file["mcLabels"][0], vtx_channel, selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][1], config_file["mcLabels"][1], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][2], config_file["mcLabels"][2], vtx_channel, selection,ln_type,])
   
    hist_channels.append([config_file["mcFiles"][13], config_file["mcLabels"][13], vtx_channel, selection,ln_type,])
    samples = ["cutflow_eeu"] 

    # hist_channels.append([config_file["mcFiles"][14], config_file["mcLabels"][14], vtx_channel, selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][15], config_file["mcLabels"][15], vtx_channel, selection,ln_type])

    
    # hist_channels.append([config_file["mcFiles"][3], config_file["mcLabels"][3], vtx_channel, selection,ln_type,])

    # hist_channels.append([config_file["mcFiles"][4], "VSI", vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][4], "VSI_2", "VSI_2", selection,ln_type,])


    # define the sample type of the histograms you added to the hist channels list
    # samples = ["cutflow_eeu"] 
    # samples = ["cutflow_uuu"] 
   

    # Get integrated luminosity to scale MC files to 
    scalelumi = config_file["scaleLumi"] # luminosity you want to scale everything to 
    # datalumi = config_file["dataLumi"] #  lumi of the data you are looking at
    datalumi = 1.0 #  lumi of the data you are looking at
    # TODO: ideally lumi # should come from a value in the nutple, lumi still needs to be properly calculated - DT

    CutFlow(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    height  = 800,
	width  = 1400,
	x_title ="",
	x_units ="",
	y_title = "MC Events",
    y_min = 0.1,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    empty_scale = 1.2,
    hide_lumi = True,
	log_scale_y = log_scale_y,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"{} {} signal, 10GeV, 10mm".format(ln_type,samples[0].split("_")[1]),]
	)