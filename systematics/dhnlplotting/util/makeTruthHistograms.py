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
outputDir = '../output/uuu_3_and_10GeV/' # change path here to save your histograms somewhere else!
outputDir = '../output/Jpsi/' # change path here to save your histograms somewhere else!
outputDir = '../output/MadGraph_tests/'
if not os.path.exists(outputDir): os.mkdir(outputDir)
if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
with open(options.config, 'r') as json_config:
    config_file = json.load(json_config) # load JSON config file
#############################################################################################################################################

#############################################################################################################################################
# Globals
#############################################################################################################################################
norm = True
log_scale_y = False
draw_markers = True
#############################################################################################################################################

ln_type = "LNC"
vtx_channels = ["VSI_LeptonsMod_LRTR3_1p0"]
# vtx_channels = ["VSI","VSI_Leptons"]
# vtx_channels = ["VSI"]
selection = "truth"
for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>,<sample type>)
    # hist_channels.append([config_file["dataFile"],config_file["dataLabel"], vtx_channel, selection])

    # hist_channels.append([config_file["ttbarFile"],config_file["ttbarLabel"], vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_uuu"],config_file["dataLabel_uuu"], vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_ueu"],config_file["dataLabel_ueu"], vtx_channel, selection])
    # hist_channels.append([config_file["dataFile"],config_file["dataLabel"], vtx_channel, selection])

    # hist_channels.append([config_file["mcFiles"][0], config_file["mcLabels"][0], vtx_channel, selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][1], config_file["mcLabels"][1], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][2], config_file["mcLabels"][2], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][3], config_file["mcLabels"][3], vtx_channel, selection,ln_type,])
    
    # hist_channels.append([config_file["mcFiles"][4], config_file["mcLabels"][4], vtx_channel, selection,ln_type,])

    # hist_channels.append([config_file["mcFiles"][3], config_file["mcLabels"][3], vtx_channel, selection,"LNC",])
    
    # hist_channels.append([config_file["mcFiles"][14], config_file["mcLabels"][14], vtx_channel, selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][15], config_file["mcLabels"][15], vtx_channel, selection,ln_type])

    # hist_channels.append(["/home/dtrischuk/HNLAnalysis/DHNLNtupleAnalysis/output/JPsi_test/histograms_mc_Jpsi.root", "Jpsi", vtx_channel, selection,"all"])
    # hist_channels.append([config_file["mcFiles"][16], config_file["mcLabels"][16], vtx_channel, selection,ln_type,])
    
    # hist_channels.append([config_file["mcFiles"][4], "VSI", vtx_channel, selection,"LNC",])
    # hist_channels.append([config_file["mcFiles"][4], "VSI_2", "VSI_2", selection,"LNC",])

    # Mad Graph Tests
    # hist_channels.append([config_file["mcFiles"][2], ln_type + config_file["mcLabels"][2], vtx_channel, selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][0], ln_type+" " + config_file["mcLabels"][0], vtx_channel, selection,ln_type])
    hist_channels.append([config_file["mcFiles"][1], ln_type + config_file["mcLabels"][1], vtx_channel, selection,ln_type])


    # hist_channels.append([config_file["mcFiles"][10], config_file["mcLabels"][10], vtx_channel, selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][11], config_file["mcLabels"][11], vtx_channel, selection,ln_type])
    hist_channels.append([config_file["mcFiles"][12], config_file["mcLabels"][12], vtx_channel, selection,ln_type])

    # hist_channels.append([config_file["mcFiles"][15], "no evt weight", "VSI", selection,ln_type])
    # hist_channels.append([config_file["mcFiles"][16], "no evt weight pythia", "VSI", selection,ln_type])
    hist_channels.append([config_file["mcFiles"][17], "monika MG 50 LNV evts", "VSI", selection,"LNV"])


    #nJetMax = 0 test
    # hist_channels.append([config_file["mcFiles"][0], config_file["mcLabels"][0], vtx_channel, selection,"LNC",])
    # hist_channels.append([config_file["mcFiles"][11], config_file["mcLabels"][11], vtx_channel, selection,"LNC",])
    # hist_channels.append([config_file["mcFiles"][14], config_file["mcLabels"][14], vtx_channel, selection,"LNC",])

    #SUSY15 validation



    # hist_channels.append([config_file["mcFiles"][13], config_file["mcLabels"][13], vtx_channel, selection,"LNC",])
    # hist_channels.append([config_file["mcFiles"][7], config_file["mcLabels"][7 ], vtx_channel, selection,"LNC",])


    # define the sample type of the histograms you added to the hist channels list
    # samples = ["SSuu","SSemu","ee","uu","emu"] 
    samples = ["eee","uuu","uue","eeu"] 
    samples = ["uuu","uuu_1mm"] 
    # samples = ["eee","uuu"] 
    # samples = ["uue","eeu"] 
    samples = ["uuu_10mm","eee_10mm", "uue_10mm","eeu_10mm"] 
    samples = ["uue_10mm","eeu_10mm","uuu_1mm","uuu_100mm","eee_10mm", "uuu_10mm"] 
    samples = ["uuu_10mm","eee_10mm", "uue_10mm"] 

    # samples = ["uu","emu"] 

    # Get integrated luminosity to scale MC files to 
    scalelumi = config_file["scaleLumi"] # luminosity you want to scale everything to 
    datalumi = 1.0 #  lumi of the data you are looking at
    # TODO: ideally lumi # should come from a value in the nutple, lumi still needs to be properly calculated - DT



    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_DV_r",
	x_title ="Truth DV L_{xy}",
	x_units ="mm",
    y_axis_type = "Events",
    y_min = 0.0001,
    # y_max = 0.4,
    x_min = 0.5,
    x_max = 300,
    rebin = 10,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = True, # log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)
    # continue





#################################################################################################################################################################################################################################

        # Weights

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_event_type_MCweight",
	x_title ="Lepton Number Event Weight",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -1,
    x_max = 5,
    rebin = 10 ,
    use_ntuple = False,
    ntup_nbins =200,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

################################################################################################################################################################################################################################

        # On-Shell W boson variables

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_W_pt",
	x_title ="Truth W p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 100,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_W_eta",
	x_title ="Truth W \\eta",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
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
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_W_phi",
	x_title ="Truth W \\phi",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)


    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_W_mass",
	x_title ="Truth W mass",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 40,
    x_max = 120,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

################################################################################################################################################################################################################################

        # Mass variables

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_DV_mass",
	x_title ="Truth DV Mass",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 1,
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
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_plep_eta",
	x_title ="Truth Prompt Lepton \\eta",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
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
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_plep_phi",
	x_title ="Truth Prompt Lepton \\phi",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)
    

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_mHNLcalc",
	x_title ="Truth HNL Mass Calculation",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 20,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

################################################################################################################################################################################################################################

        # Prompt Lepton variables

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_plep_pt",
	x_title ="Truth Prompt Lepton p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 80,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
    empty_scale = 1.2,
	log_scale_y = log_scale_y,
    hide_lumi = True,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_plep_eta",
	x_title ="Truth Prompt Lepton \\eta",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
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
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_plep_phi",
	x_title ="Truth Prompt Lepton \\phi",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)


#################################################################################################################################################################################################################################

        # Displaced leptons variables (pT ordered)

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_dlep1_pt",
	x_title ="Truth Highest p_{T} Disp. Lepton p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 50,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_dlep2_pt",
	x_title ="Truth 2^{nd} Highest p_{T} Disp. Lepton p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 50,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_dlep3_pt",
	x_title ="Truth Lowest p_{T} Disp. Lepton p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 50,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)


#################################################################################################################################################################################################################################

        # Displaced leptons variables (ordered topologically)

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_lep1_trk_pt",
	x_title ="Truth Lepton 1 p_{T}", 
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 50,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_lep2_trk_pt",
	x_title ="Truth Lepton 2 p_{T}", 
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 50,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_nu_trk_pt",
	x_title ="Truth Lepton 3 p_{T}", 
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 50,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_lep1_trk_eta",
	x_title ="Truth Lepton 1 \\eta", 
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -10,
    x_max = 10,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_lep2_trk_eta",
	x_title ="Truth Lepton 2 \\eta", 
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -10,
    x_max = 10,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_nu_trk_eta",
	x_title ="Truth Lepton 3 \\eta", 
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -10,
    x_max = 10,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_lep1_trk_phi",
	x_title ="Truth Lepton 1 \\phi", 
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_lep2_trk_phi",
	x_title ="Truth Lepton 2 \\phi", 
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_nu_trk_phi",
	x_title ="Truth Lepton 3 \\phi", 
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)


################################################################################################################################################################################################################################

        # HNL 4-vector

#################################################################################################################################################################################################################################


    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_HNLpt",
	x_title ="Truth HNL p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
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
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_HNLeta",
	x_title ="Truth HNL \\eta",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -10,
    x_max = 10,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_HNLphi",
	x_title ="Truth HNL \\phi",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = -4,
    x_max = 4,
    rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_HNLm",
	x_title ="Truth HNL Mass",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 20,
    # rebin = 1,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)


################################################################################################################################################################################################################################

        # Displaced leptons (muons & electrons)

#################################################################################################################################################################################################################################

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_El_pt",
	# x_title ="Truth Disp. Electron p_{T}", 
	# x_units ="GeV",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # x_min = 0,
    # x_max = 50,
    # rebin = 2,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_El_eta",
	# x_title ="Truth Disp. Electron \\eta", 
	# x_units ="",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # x_min = -10,
    # x_max = 10,
    # rebin = 4,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_El_phi",
	# x_title ="Truth Disp. Electron \\phi", 
	# x_units ="",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # x_min = -4,
    # x_max = 4,
    # rebin = 4,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )



    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_Mu_pt",
	# x_title ="Truth Disp. Muon p_{T}", 
	# x_units ="GeV",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # x_min = 0,
    # x_max = 50,
    # rebin = 2,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_Mu_eta",
	# x_title ="Truth Disp. Muon \\eta", 
	# x_units ="",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # x_min = -10,
    # x_max = 10,
    # rebin = 4,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_Mu_phi",
	# x_title ="Truth Disp. Muon \\phi", 
	# x_units ="",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # x_min = -4,
    # x_max = 4,
    # rebin = 4,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )


#################################################################################################################################################################################################################################

        # Mandlstam Variables (mass squared!)

#################################################################################################################################################################################################################################
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_s12",
	x_title ="s_{12}", 
	x_units ="GeV^{2}",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 6000,
    rebin = 500,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_s13",
	x_title ="s_{13}", 
	x_units ="GeV^{2}",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 6000,
    rebin = 500,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_s14",
	x_title ="s_{14}", 
	x_units ="GeV^{2}",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 6000,
    rebin = 500,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_s23",
	x_title ="s_{23}", 
	x_units ="GeV^{2}",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 25,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_s24",
	x_title ="s_{24}", 
	x_units ="GeV^{2}",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 25,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_s34",
	x_title ="s_{34}", 
	x_units ="GeV^{2}",
    y_axis_type = "Events",
    y_min = 0.001,
    x_min = 0,
    x_max = 25,
    rebin = 2,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)




#################################################################################################################################################################################################################################

        # DV Variables

#################################################################################################################################################################################################################################
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_DV_trk_pt",
	x_title ="Truth DV track p_{T}",
	x_units ="GeV",
    y_axis_type = "Events",
    y_min = 0.001,
    # y_max = 0.4,
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
    extra_legend_lines = [ln_type, "\\mu\\mue"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_DV_trk_d0",
	x_title ="Truth DV track d_{0}",
	x_units ="mm",
    y_axis_type = "Events",
    y_min = 0.001,
    # y_max = 0.4,
    x_min = -10,
    x_max = 10,
    # rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "10GeV"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="truth_DV_d0_cut",
	x_title ="Both Signal Tracks have Truth d_{0} < 2mm",
	x_units ="",
    y_axis_type = "Events",
    y_min = 0.001,
    # y_max = 0.4,
    # x_min = -10,
    # x_max = 10,
    # rebin = 4,
    use_ntuple = False,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [ln_type, "10GeV"]
	)




    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="truth_DV_r",
	# x_title ="Truth DV L_{xy}",
	# x_units ="mm",
	
    # y_axis_type = "Events",
    # y_min = 0.001,
    # # y_max = 0.4,
    # x_min = 0,
    # x_max = 300,
    # rebin = 10,
    # use_ntuple = False,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [ln_type, "\\mu\\mue"]
	# )
