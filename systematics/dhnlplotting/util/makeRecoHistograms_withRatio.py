# Plotting Script adapted from VH4b plotting and DHNLNtupleAnalaysis plotting scripts
# Last Major Overhaul of Code: Oct 16 2020 by D. Trischuk
import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from pylab import *
import atlas_style
import argparse
ROOT.gROOT.SetBatch(True)
from plot_classes import Hist1D,Hist1DRatio
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
outputDir = '../output/OSvSS/' # change path here to save your histograms somewhere else!
if not os.path.exists(outputDir): os.mkdir(outputDir)
if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
with open(options.config, 'r') as json_config:
    config_file = json.load(json_config) # load JSON config file
#############################################################################################################################################

#############################################################################################################################################
# Globals
#############################################################################################################################################
norm = False
log_scale_y = False
draw_markers = True
#############################################################################################################################################

vtx_channels = ["VSI_LRTR3_1p0","VSI_LeptonsMod_LRTR3_1p0"]
selection = "2trk"
for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>,<sample type>)
    # hist_channels.append([config_file["dataFile"],config_file["dataLabel"], vtx_channel, selection])
    # hist_channels.append([config_file["mcFiles"][0], config_file["mcLabels"][0], vtx_channel, selection,"LNC"])
    # hist_channels.append([config_file["mcFiles"][1], config_file["mcLabels"][1], vtx_channel, selection,"LNC",])
    # hist_channels.append([config_file["mcFiles"][2], config_file["mcLabels"][2], vtx_channel, selection,"LNC",])

    # hist_channels.append([config_file["dataFile"],"SS \\mu\\mu", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"SS \\mu\\mu 2-med", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS \\mu\\mu", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS \\mu\\mu 2-med", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS \\mu\\mu 2-loose", vtx_channel, selection])
    # samples = ["uu","uu_2med"] 
    
    # hist_channels.append([config_file["dataFile"],"SS e\\mu", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS e\\mu", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS e\\mu loose-vvl", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS e\\mu med-vvlSi", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS e\\mu loose-vvlSi", vtx_channel, selection])
    samples = ["emu","emu_med_vvl"] 
    # hist_channels.append([config_file["dataFile"],"SS ee", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS ee", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS ee 2-vvl", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],"OS ee 2-vvlSi", vtx_channel, selection])
    # samples = ["ee","ee_2vvl"] 

    
    # define the sample type of the histograms you added to the hist channels list
   

    # Get integrated luminosity to scale MC files to 
    scalelumi = config_file["scaleLumi"] # luminosity you want to scale everything to 
    datalumi = config_file["dataLumi"] #  lumi of the data you are looking at
    # TODO: ideally lumi # should come from a value in the nutple, lumi still needs to be properly calculated - DT

#################################################################################################################################################################################################################################

        # DV Variables

#################################################################################################################################################################################################################################
    
    
    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_r",
	x_title ="r_{DV}",
	x_units ="mm",
	y_title = "Vertices",
    y_min = 1,
    x_min = 0,
    x_max = 300,
    rebin = 10,
    use_ntuple = True,
    ntup_nbins =500,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = True,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_mass",
	x_title ="DV mass",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 1,
    x_min = 0,
    x_max = 10,
    use_ntuple = True,
    ntup_nbins =100,
    draw_cut = True,
    cut = 2,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = True,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)
'''
    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_pt",
	x_title ="DV p_{T}",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_eta",
	x_title ="DV \\eta",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_phi",
	x_title ="DV \\phi",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


#################################################################################################################################################################################################################################
	
    # DV Track Variables 

#################################################################################################################################################################################################################################

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_pt",
	x_title ="DV track p_{T}",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_eta",
	x_title ="DV track \\eta",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_phi",
	x_title ="DV track \\phi",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_d0",
	x_title ="DV track d0",
	x_units ="mm",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -10,
    x_max = 10,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_z0",
	x_title ="DV track z0",
	x_units ="mm",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -500,
    x_max = 500,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_z0",
	x_title ="DV track |z0|",
	x_units ="mm",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 500,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_nSiHits",
	x_title ="DV track nSiHits",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 23,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_nSCTHits",
	x_title ="DV track nSCTHits",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 14,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_isLRT",
	x_title ="DV track isLRT",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 2,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_chi2",
	x_title ="DV track \\chi^{2}",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 10,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_dpt",
	x_title ="DV track \\Delta p_{T}",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 20,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_deta",
	x_title ="DV track \\Delta\\eta",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 3.2,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_deta",
	x_title ="DV track \\Delta\\phi",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 3.2,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_dR",
	x_title ="DV track \\Delta R",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 4,
    rebin = 10,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)
#################################################################################################################################################################################################################################
		
        # Mass Variables 

#################################################################################################################################################################################################################################

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="mvis",
	x_title ="Visble mass",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 200,
    rebin = 10,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="mtrans",
	x_title ="Transverse mass",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 200,
    rebin = 5,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_redmass",
	x_title ="Reduced DV mass",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 50,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_redmassvis",
	x_title ="Reduced visible mass",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 200,
    rebin = 5,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


#################################################################################################################################################################################################################################
		
        # HNL Variables 

#################################################################################################################################################################################################################################

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="HNLm",
	x_title ="HNL mass",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 20,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="HNLpt",
	x_title ="HNL p_{T}",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min =0,
    x_max = 200,
    rebin = 5,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="HNLeta",
	x_title ="HNL \\eta",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 5,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="HNLphi",
	x_title ="HNL \\phi",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


#################################################################################################################################################################################################################################
		
        # Prompt lepton Variables 

#################################################################################################################################################################################################################################


    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="plep_pt",
	x_title ="Prompt lepton p_{T}",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)







    # Hist1DRatio(hist_channels= hist_channels,
	# types = samples,
	# legends= [],
	# x_title ="r_{DV}",
	# x_units ="mm",
	# y_title = "Vertices",
	# rebin = 4,
	# norm = True,
	# log_scale_y = False,
	# draw_markers = True,
    # use_ntuple = False,
    # ntup_nbins =100,
    # x_min = 0,
    # x_max = 300,
	# name=variable,
    # drawRatio= True,
	# atlas_mod       = "Internal",
	# )
'''                        