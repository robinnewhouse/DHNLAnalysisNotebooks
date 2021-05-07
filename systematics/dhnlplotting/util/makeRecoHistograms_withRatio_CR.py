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
outputDir = '../output/OSvSS_CR/' # change path here to save your histograms somewhere else!
outputDir = '../output/BE_plots/' # change path here to save your histograms somewhere else!
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

vtx_channels = ["VSI_LeptonsMod_LRTR3_1p0"]
vtx_channels = ["VSI_LeptonsMod"]
selection = "2trk"
for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>,<sample type>)
    
    hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu 2-med", vtx_channel, selection])
    hist_channels.append([config_file["dataFile_CR"],"SS \\mu\\mu 2-med", vtx_channel, selection])
    samples = ["OS_uu","SS_uu"] 

    # hist_channels.append([config_file["Cprime_file"],"C': shuffled, OS", vtx_channel, "RegionCprime"])
    # hist_channels.append([config_file["Dprime_file"],"D': shuffled, SS", vtx_channel, "RegionDprime"])
    # samples = ["OS_uu","SS_uu"] 
                                          
    # hist_channels.append([config_file["dataFile_CR"],"OS e\\mu", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS e\\mu", vtx_channel, selection])

    # hist_channels.append([config_file["dataFile_CR"],"OS e\\mu med-vvl", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS e\\mu med-vvl", vtx_channel, selection])  
    # samples = ["OS_eu","SS_eu"] 
    # samples = ["OS_eu","OS_eu_med-vvl"]                                 

    # hist_channels.append([config_file["dataFile_CR"],"OS ee", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS ee", vtx_channel, selection])
    # samples = ["OS_ee","SS_ee"] 

    # hist_channels.append([config_file["dataFile_CR"],"OS ee 2-vvl", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS ee 2-vvl", vtx_channel, selection])
    # samples = ["OS_ee","SS_ee"] 


    # hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu 2-med", vtx_channel, selection])
    # samples = ["OS_uu","OS_uu_2med"] 
    

    

    # Get integrated luminosity to scale MC files to 
    scalelumi = config_file["scaleLumi"] # luminosity you want to scale everything to 
    datalumi = config_file["dataLumi"] #  lumi of the data you are looking at
    # TODO: ideally lumi # should come from a value in the nutple, lumi still needs to be properly calculated - DT

#################################################################################################################################################################################################################################

        # DV Variables

#################################################################################################################################################################################################################################
    
    extra_cuts = "*(DV_mass < 20)"
    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_r",
	x_title ="r_{DV}",
	x_units ="mm",
	# y_title = "Vertices",
    y_min = 0.5,
    x_min = 0,
    x_max = 300,
    # rebin = 10,
    use_ntuple = True,
    ntup_nbins =30,
    ratio_ymin = 0,
    ratio_ymax = 3.5,
    extra_cuts = extra_cuts,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Shuffled Events"]
	)
    

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_mass",
	x_title ="DV mass",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = 0,
    x_max = 20,
    use_ntuple = True,
    ntup_nbins = 40,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Shuffled Events"]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_mom_parall",
	x_title ="Largest p_{T} parallel track mommentum (p\\parallel )",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = -100,
    x_max = 100,
    use_ntuple = True,
    ntup_nbins = 40,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_mom_parall",
	x_title ="Smallest p_{T} perpendicular track mommentum (p\\parallel )",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = -100,
    x_max = 100,
    use_ntuple = True,
    ntup_nbins = 40,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"]
	)


    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_mom_perp",
	x_title ="Largest p_{T} perpendicular track mommentum (p\\perp )",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = 0,
    x_max = 100,
    use_ntuple = True,
    ntup_nbins = 20,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_mom_perp",
	x_title ="Smallest p_{T} parallel track mommentum (p\\perp )",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = 0,
    x_max = 100,
    use_ntuple = True,
    ntup_nbins = 20,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"]
	)



    continue  
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