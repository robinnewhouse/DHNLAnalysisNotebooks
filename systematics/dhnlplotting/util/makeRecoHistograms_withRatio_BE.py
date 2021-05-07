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
charge = "SS"
outputDir = '../output/BE_shuffling_{}/'.format(charge) # change path here to save your histograms somewhere else!
outputDir = '../output/BE_plots/'.format(charge) # change path here to save your histograms somewhere else!
if not os.path.exists(outputDir): os.mkdir(outputDir)
if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
with open(options.config, 'r') as json_config:
    config_file = json.load(json_config) # load JSON config file
#############################################################################################################################################

#############################################################################################################################################
# Globals
#############################################################################################################################################
norm = True
HNLscale = False
if norm:
    y_min = 0.0001
    empty_scale = 3.8
else: 
    y_min = 0.1
    empty_scale = 3.8
log_scale_y = True
draw_markers = True
# extra_cuts = "*(DV_r > 4)*(DV_r < 300)"  #"*(DV_mass < 20)"
# extra_cuts = "*(DV_r > 4 && DV_r < 300)"  #"*(DV_mass < 20)"
extra_cuts = "*(DV_emu == 1)*(DV_mass> 4)"  # *(DV_pass_mat_veto == 1) *(DV_2veryveryloose ==1) *(DV_mass > 4)*(DV_mass < 20) (DV_pass_mat_veto ==1)
# extra_cuts = "*(DV_ee == 1)"  # *(DV_pass_mat_veto == 1) *(DV_2veryveryloose ==1) *(DV_mass > 4)*(DV_mass < 20) (DV_pass_mat_veto ==1)

extra_label="CR Region, {} ee DVs".format(charge)
extra_label="SS e\\mu DV"
mat_label = ""
#############################################################################################################################################

vtx_channels = ["VSI_LeptonsMod"]

for vtx_channel in vtx_channels:

    if norm or charge == "OSvSS" or charge == "OSvSS_shuffled": 
        ratio_ymin = 0
        ratio_ymax =2.1

    # if vtx_channel == "VSI_Leptons": 
    #     ratio_ymin = 0
    #     ratio_ymax =10.5
    

    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>,<sample type>)
    
    # hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu 2-med", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS \\mu\\mu 2-med", vtx_channel, selection])
    # samples = ["OS_uu","SS_uu"] 

   
    # hist_channels.append([config_file["realDAOD_regionB"],config_file["realDAOD_regionB_label"], vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_regionB"],"region B, not shuffled", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["realDAOD_regionB"],config_file["realDAOD_regionB_label"], vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_regionD"],"region D, shuffled", vtx_channel, "RegionD"])
    # hist_channels.append([config_file["fakeDAOD_sameHost"],"do nothing, same host", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_differentHost"],"do nothing, diff. host", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["realDAOD"],"original DAOD", vtx_channel, "RegionB"])


    # hadron overlay test from BEtestRun config
    # hist_channels.append([config_file["realDAOD_regionB"],"original DAOD", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["realDAOD_regionB_VSILep"],"original DAOD", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_donothing"],"donothing, orig. hadrons", vtx_channel, "RegionB"])
    # hist_channels.append([config_file["fakeDAOD_donothing"],"donothing, host hadrons", vtx_channel + "_hostHad", "RegionB"])
    samples = ["OS_ee","OS_uu"] 

   
    
    if charge == "OS":
        hist_channels.append([config_file["fakeDAOD_Cprime"],"shuffled, C'", vtx_channel , "RegionCprime"])
        hist_channels.append([config_file["fakeDAOD_Aprime"],"donothing, A'", vtx_channel , "RegionAprime"])
        samples = ["OS_uu","OS_eu"] 
    if charge == "SS":
        hist_channels.append([config_file["fakeDAOD_Dprime"],"shuffled, D'", vtx_channel , "RegionDprime"])
        hist_channels.append([config_file["fakeDAOD_Bprime"],"donothing, B'", vtx_channel , "RegionBprime"])
        # hist_channels.append([config_file["fullRun2_eeu"],"fullrun2 SR'", vtx_channel , "DVtype"])
        # hist_channels.append([config_file["dataFile_CR"],"CR data 2018", vtx_channel , "2trk"])


        # samples = ["OS_ee","eeu_10mm"] 
        samples = ["shuffling_eu", "fullrun2_ee"]
    if charge == "OSvSS":
        hist_channels.append([config_file["fakeDAOD_Aprime"],"donothing, A'", vtx_channel , "RegionAprime"])
        hist_channels.append([config_file["fakeDAOD_Bprime"],"donothing, B'", vtx_channel , "RegionBprime"])
        samples = ["OS_eu" ,"eeu_10mm" ]

    
    if charge == "OSvSS_shuffled":
        hist_channels.append([config_file["fakeDAOD_Cprime"],"shuffled, C'", vtx_channel , "RegionCprime"])
        hist_channels.append([config_file["fakeDAOD_Dprime"],"shuffled, D'", vtx_channel , "RegionDprime"])
        samples = ["OS_uu" ,"OS_ee" ]

    # samples = ["OS_ee","OS_uu","OS_eu"] 
    
    

    

    

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
	x_title ="L_{xy}",
	x_units ="mm",
    y_min = y_min,
    x_min = 0,
    x_max = 300,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =30,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
    extra_cuts = extra_cuts,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)
    # exit()
    

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_mass",
	x_title ="DV mass",
	x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 50,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins = 50,
    # draw_cut = True,
    extra_cuts = extra_cuts,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_pt",
	x_title ="DV p_{T}",
	x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 4.2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_eta",
	x_title ="DV \\eta",
	x_units ="",
    y_min = y_min,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_phi",
	x_title ="DV \\phi",
	x_units ="",
    y_min = y_min,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_pt",
	x_title ="Leading DV track p_{T}",
	x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = 4.2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_pt",
	x_title ="Subleading DV track p_{T}",
	x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_eta",
	x_title ="Leading DV track \\eta",
	x_units ="",
    y_min = y_min,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts= extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = 4.2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_eta",
	x_title ="Subeading DV track \\eta",
	x_units ="",
    y_min = y_min,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    extra_cuts= extra_cuts,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_phi",
	x_title ="Leading DV track \\phi",
	x_units ="",
    y_min = y_min,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_phi",
	x_title ="Subleading DV track \\phi",
	x_units ="",
    y_min = y_min,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_d0",
	x_title ="Leading DV track d0",
	x_units ="mm",
    y_min = y_min,
    x_min = -50,
    x_max = 50,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =50,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_d0",
	x_title ="Subleading DV track d0",
	x_units ="mm",
    y_min = y_min,
    x_min = -50,
    x_max = 50,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =50,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_z0",
	x_title ="Leading DV track z0",
	x_units ="mm",
    y_min = y_min,
    x_min = -200,
    x_max = 200,
    # rebin = 4,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =50,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_z0",
	x_title ="Subleading DV track z0",
	x_units ="mm",
    y_min = y_min,
    x_min = -200,
    x_max = 200,
    # rebin = 4,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =50,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
    empty_scale = empty_scale,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_label, mat_label]
	)
    continue
    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_nSiHits",
	x_title ="DV track nSiHits",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0.5,
    x_max = 23.5,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =24,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_nSCTHits",
	x_title ="DV track nSCTHits",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0.5,
    x_max = 14.5,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =15,
    scaleLumi = scalelumi,
    extra_cuts = extra_cuts,
    dataLumi = datalumi,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_isLRT",
	x_title ="DV track isLRT",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0.5,
    x_max = 2.5,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =3,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_chi2",
	x_title ="DV track \\chi^{2}",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0,
    x_max = 10,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_dpt",
	x_title ="DV track \\Delta p_{T}",
	x_units ="GeV",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0,
    x_max = 20,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_deta",
	x_title ="DV track \\Delta\\eta",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0,
    x_max = 3.2,
    rebin = 2,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)


    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_deta",
	x_title ="DV track \\Delta\\phi",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0,
    x_max = 3.2,
    rebin = 1,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)

    Hist1DRatio(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_dR",
	x_title ="DV track \\Delta R",
	x_units ="",
	y_title = "Vertices",
    y_min = y_min,
    x_min = 0,
    x_max = 4,
    rebin = 10,
    use_ntuple = True,
    HNLscale = HNLscale,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    extra_cuts = extra_cuts,
	norm = norm,
    ratio_ymin = ratio_ymin,
    ratio_ymax = ratio_ymax,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_label, mat_label]
	)
