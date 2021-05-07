# Plotting Script adapted from VH4b plotting and DHNLNtupleAnalaysis plotting scripts
# Last Major Overhaul of Code: Oct 16 2020 by D. Trischuk
import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from pylab import *
import atlas_style
import argparse
ROOT.gROOT.SetBatch(True)
from plot_classes import Hist1D,Hist1D,Hist2D
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
charge = "OS"
outputDir = '../output/BE_shuffling_{}/'.format(charge) # change path here to save your histograms somewhere else!
if not os.path.exists(outputDir): os.mkdir(outputDir)
if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
with open(options.config, 'r') as json_config:
    config_file = json.load(json_config) # load JSON config file
#############################################################################################################################################

#############################################################################################################################################
# Globals
#############################################################################################################################################
gStyle.SetPalette(kPastel)
TColor().InvertPalette()
draw_markers = True
norm = False
log_scale_y = True
draw_markers = True
use_ntuple = True

# extra_cuts = "*(DV_r > 4)*(DV_r < 300)"  #"*(DV_mass < 20)"
# extra_cuts = "*(DV_r > 4 && DV_r < 300)"  #"*(DV_mass < 20)"
extra_cuts = "*(DV_ee==1)*(DV_pass_mat_veto ==1)*(DV_mass > 4)*(DV_mass < 20)"  #"*(DV_mass < 20)"
#############################################################################################################################################

vtx_channels = ["VSI_LeptonsMod","VSI_Leptons"]
# vtx_channels = ["VSI_LeptonsMod"]
for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>,<sample type>)
    
    # hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu 2-med", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS \\mu\\mu 2-med", vtx_channel, selection])
    # samples = ["OS_uu","SS_uu"] 

   
    # hist_channels.append([config_file["realDAOD_regionB"],config_file["realDAOD_regionB_label"], vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_regionB"],"region B, not shuffled", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["realDAOD_regionB"],config_file["realDAOD_regionB_label"], vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_regionD"],"region D, shuffled", vtx_channel, "RegionD"])
    # PV check
    # hist_channels.append([config_file["realDAOD"],"original DAOD", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_sameHost"],"do nothing, same host", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_sameHost_VSILepModTrkSel"],"do nothing, VSILepMod trk sel", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_differentHost"],"do nothing, orig. hadrons", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_diffHost_trkAttachment"],"do nothing, hadrons from Host", vtx_channel, "RegionB"])
    
   # hadron overlay test from BEtestRun config
    # hist_channels.append([config_file["realDAOD_regionB"],"original DAOD", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["realDAOD_regionB_VSILep"],"original DAOD", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_donothing"],"donothing, orig. hadrons", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_donothing"],"donothing, host hadrons", vtx_channel + "_hostHad", "RegionB"])

    # OS
    if charge == "OS":
        hist_channels.append([config_file["fakeDAOD_donothing"],"donothing, A'", vtx_channel , "RegionAprime"])
        hist_channels.append([config_file["fakeDAOD_donothing"],"shuffled, C'", vtx_channel , "RegionCprime"])
    if charge == "SS":
        hist_channels.append([config_file["fakeDAOD_donothing"],"donothing, A'", vtx_channel , "RegionAprime"])
        hist_channels.append([config_file["fakeDAOD_donothing"],"shuffled, C'", vtx_channel , "RegionCprime"])


    samples = ["OS_ee","OS_uu","OS_eu"] 
    samples = ["OS_uu","OS_eu"] 

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
    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_r",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
    x_title ="L_{xy}",
	x_units ="mm",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 35,
    x_min = 0,
    x_max = 300,
    # z_max =50,
    # x_max = 30,
    # rebin = 5,
    HNLscale=False,
    use_ntuple =  use_ntuple,
    ntup_nbins =30,
    ntup_nbins_y =35,
    # ntup_nbins =60,
    # ntup_nbins_y =50,
    ntup_2D = True,
    # ntup_1D = True,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"Region B, ee DV","With mat. veto, 4 < m_{DV} < 20"]  
	)
    exit()
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    HNLscale = False,
    outputDir = outputDir,
    name="DV_r",
	x_title ="r_{DV}",
	x_units ="mm",
    y_min = 0.5,
    x_min = 0,
    x_max = 300,
    use_ntuple = True,
    ntup_nbins =30,
    ratio_ymin = -0.5,
    ratio_ymax = 2.2,
    extra_cuts = extra_cuts,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Region B"]
	)
    # exit()
    

    Hist1D(hist_channels= hist_channels,
	types = samples,
    HNLscale = False,
    outputDir = outputDir,
    name="DV_mass",
	x_title ="DV mass",
	x_units ="GeV",
    y_min = 0.5,
    x_min = 0,
    x_max = 30,
    use_ntuple = True,
    ntup_nbins = 60,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = -0.5,
    ratio_ymax = 2.2,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 1.6,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Region B"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    HNLscale = False,
    outputDir = outputDir,
    name="DV_pt",
	x_title ="DV p_{T}",
	x_units ="GeV",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = True,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"Region B"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    HNLscale = False,
    outputDir = outputDir,
    name="DV_eta",
	x_title ="DV \\eta",
	x_units ="",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = True,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"Region B"]
	)


    Hist1D(hist_channels= hist_channels,
	types = samples,
    HNLscale = False,
    outputDir = outputDir,
    name="DV_phi",
	x_title ="DV \\phi",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = True,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"Region B"]
	)
