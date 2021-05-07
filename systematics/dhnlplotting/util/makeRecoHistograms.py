# Plotting Script adapted from VH4b plotting and DHNLNtupleAnalaysis plotting scripts
# Last Major Overhaul of Code: Oct 16 2020 by D. Trischuk
import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from pylab import *
import atlas_style
import argparse
ROOT.gROOT.SetBatch(True)
from plot_classes import Hist1D,Hist1DRatio,Hist2D
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

parser.add_argument("--output_dir",
                    dest="output_dir",
                    type = str,
                    help="Output Directory")

parent_parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter, parents = [parser]) 
options = parent_parser.parse_args()

#############################################################################################################################################
# Globals
#############################################################################################################################################
# selection options
signal = "uuu"
selection = "DVtype" # micro-ntuples saved for DVtype selection
ln_type = "mixed"
vtx_channels = ["VSI_LeptonsMod"] 


# where to save histograms 
output_dir = options.output_dir # change path here to save your histograms somewhere else!
if not os.path.exists(output_dir): os.mkdir(output_dir)
if not os.path.exists(output_dir): os.mkdir(output_dir)
if not os.path.exists(output_dir + "plots/"): os.mkdir(output_dir + "plots/")

# plotting options
gStyle.SetPalette(kPastel)
TColor().InvertPalette()
norm = False
log_scale_y = True
draw_markers = True
use_ntuple = True



#############################################################################################################################################
# Parse configs
#############################################################################################################################################
with open(options.config, 'r') as json_config:
    config_file = json.load(json_config) # load JSON config file

#############################################################################################################################################
# Make Histograms
#############################################################################################################################################


for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>)
    if signal == "uuu": 
        # hist_channels.append([config_file["uuu_5_10"], "m_{HNL} = 5 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["uuu_10_10"], "m_{HNL} = 10 GeV", vtx_channel, selection,ln_type])
        # hist_channels.append([config_file["uuu_15_10"], "m_{HNL} = 15 GeV", vtx_channel, selection,ln_type])
        # hist_channels.append([config_file["SS_uuu"], "SS bkg", vtx_channel, selection])
        # extra_cuts = "*(DV_mass > 2)*(HNLm < 25)*(DV_2medium ==1)*(mvis > 50)*(mvis < 84)" # defines any extra cuts you want to use if you are using micro ntuples
        samples = ["uuu_5G","uuu_10G","uuu_15G","SS_uu"] #defines your colour options
        extra_info = "\\mu\\mu\\mu, c\\tau = 10 mm"
    elif signal == "eee": 
        hist_channels.append([config_file["eee_5_10"], "m_{HNL} = 5 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["eee_10_10"], "m_{HNL} = 10 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["eee_15_10"], "m_{HNL} = 15 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["SS_eee"], "SS bkg", vtx_channel, selection])
        extra_cuts = "*(DV_mass > 2)*(mvis > 50)*(mvis < 84)*(HNLm < 25)*(DV_2veryveryloose ==1)*(DV_pass_mat_veto ==1)"
        samples = ["eee_5G","eee_10G","eee_15G","SS_ee"] 
        extra_info = "eee, c\\tau = 10 mm"
    elif signal == "uue": 
        hist_channels.append([config_file["uue_5_10"], "m_{HNL} = 5 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["uue_10_10"], "m_{HNL} = 10 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["uue_15_10"], "m_{HNL} = 15 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["SS_uue"], "SS bkg", vtx_channel, selection])
        extra_cuts = "*(DV_mass > 2)*(mvis > 50)*(mvis < 84)*(HNLm < 25)*(DV_medium_veryveryloose ==1)"
        samples = ["uue_5G","uue_10G","uue_15G","SS_eu"] 
        extra_info = "\\mu\\mue, c\\tau = 10 mm"
    elif signal == "eeu": 
        hist_channels.append([config_file["eeu_5_10"], "m_{HNL} = 5 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["eeu_10_10"], "m_{HNL} = 10 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["eeu_15_10"], "m_{HNL} = 15 GeV", vtx_channel, selection,ln_type])
        hist_channels.append([config_file["SS_eeu"], "SS bkg", vtx_channel, selection])
        extra_cuts = "*(DV_mass > 2)*(mvis > 50)*(mvis < 84)*(HNLm < 25)*(DV_medium_veryveryloose ==1)"
        samples = ["eeu_5G","eeu_10G","eeu_15G","SS_eu"] 
        extra_info = "ee\\mu, c\\tau = 10 mm"
    
    
    cut_list =  extra_cuts.split('(')
    for i in range(len(cut_list)): 
        cut_list[i] = cut_list[i].replace(")*", "")
        cut_list[i] = cut_list[i].replace(")", "")
    del cut_list[0]



#################################################################################################################################################################################################################################

        # DV Variables

#################################################################################################################################################################################################################################
    
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_r",
	x_title ="L_{xy}",
	x_units ="mm",
    y_min = 0.01,
    x_min = 0,
    x_max = 300,
    rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =60,
    extra_cuts = extra_cuts,
    empty_scale = 1.8,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_info]
	)
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_mass",
	x_title ="DV mass",
	x_units ="GeV",
    y_min = 0.01,
    x_min = 0,
    x_max = 20,
    use_ntuple = use_ntuple,
    ntup_nbins =40,
    extra_cuts = extra_cuts,
	norm = norm,
    draw_cut = False,
    cut = 4,
    empty_scale = 1.8,
    hide_lumi = True,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_info]
	)


    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_pt",
	x_title ="DV p_{T}",
	x_units ="GeV",
    y_min = 0.0001,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_info]
	)
   

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_eta",
	x_title ="DV \\eta",
	x_units ="",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_info]
	)


    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_phi",
	x_title ="DV \\phi",
	x_units ="",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, extra_info]
	)
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_alpha",
	x_title ="Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
	x_units ="rad",
    y_min = 0.1,
    x_min = 0,
    x_max = 1,
    # rebin = 2,
    empty_scale = 1.4,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = False,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,  extra_info]
	)



    
#################################################################################################################################################################################################################################
	
    # DV Track Variables 

#################################################################################################################################################################################################################################

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_pt",
	x_title ="DV track p_{T}",
	x_units ="GeV",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_eta",
	x_title ="DV track \\eta",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_phi",
	x_title ="DV track \\phi",
	x_units ="",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_d0",
	x_title ="DV track d0",
	x_units ="mm",
    y_min = 0.1,
    x_min = -10,
    x_max = 10,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_z0",
	x_title ="DV track z0",
	x_units ="mm",
    y_min = 0.1,
    x_min = -500,
    x_max = 500,
    rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_z0",
	x_title ="DV track |z0|",
	x_units ="mm",
    y_min = 0.1,
    x_min = 0,
    x_max = 500,
    rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_pt",
	x_title ="Leading Track p_{T}",
    y_axis_type="Tracks",
	x_units ="GeV",
    y_min = 0.1,
    x_min = -0.5,
    x_max = 20.5 ,
    # rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =21,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_eta",
	x_title ="Leading Track \\eta",
    y_axis_type="Tracks",
	x_units ="",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_phi",
	x_title ="Leading track \\phi",
     y_axis_type="Tracks",
	x_units ="",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_pt",
	x_title ="Sub-leading Track p_{T}",
	x_units ="GeV",
    y_min = 0.1,
    y_axis_type="Tracks",
    x_min = -0.5,
    x_max = 20.5,
    # rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =21,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_eta",
	x_title ="Sub-leading Track \\eta",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_phi",
	x_title ="Sub-leading track \\phi",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_nSiHits",
	x_title ="DV track nSiHits",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 23,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_nSCTHits",
	x_title ="DV track nSCTHits",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 14,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_isLRT",
	x_title ="DV track isLRT",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 2,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_chi2",
	x_title ="DV track \\chi^{2}",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 10,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_dpt",
	x_title ="DV track \\Delta p_{T}",
	x_units ="GeV",
    y_min = 0.1,
    x_min = 0,
    x_max = 20,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_deta",
	x_title ="DV track \\Delta\\eta",
	x_units ="",
    y_min = 0.1,
    x_min = 0,
    x_max = 3.2,
    rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)


    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_deta",
	x_title ="DV track \\Delta\\phi",
	x_units ="",
    y_min = 0.1,
    x_min = 0,
    x_max = 3.2,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_dR",
	x_title ="DV track \\Delta R",
	x_units ="",
    y_min = 0.1,
    x_min = 0,
    x_max = 4,
    rebin = 10,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_mom_frac_parall",
	x_title ="Leading track p_{\\parallel}/ p_{tot}",
	x_units ="",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.00001,
    # y_max = 1,
    x_min = 0,
    x_max = 1,
    use_ntuple = use_ntuple,
    ntup_nbins = 50,
    # draw_cut = True,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]+ cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_mom_frac_parall",
	x_title ="Subleading track p_{\\parallel}/ p_{tot}",
	x_units ="",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.00001,
    x_min = 0,
    # y_max = 1,
    x_max = 1,
    use_ntuple = use_ntuple,
    ntup_nbins = 50,
    # draw_cut = True,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_mom_parall",
	x_title ="Leading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.001,
    x_min = -100,
    x_max = 100,
    use_ntuple = use_ntuple,
    ntup_nbins = 40,
    # draw_cut = True,
    ratio_ymin = 0,
    ratio_ymax = 2.5,
    cut = 1.5,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]+cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_mom_parall",
	x_title ="Subleading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.001,
    x_min = -100,
    x_max = 100,
    use_ntuple = use_ntuple,
    ntup_nbins = 40,
    # draw_cut = True,
    ratio_ymin = 0,
    ratio_ymax = 2.5,
    cut = 1.5,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_mom_perp",
	x_title ="Leading track p_{\\perp}",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.001,
    x_min = 0,
    x_max = 100,
    use_ntuple = use_ntuple,
    ntup_nbins = 20,
    # draw_cut = True,
    ratio_ymin = 0,
    ratio_ymax = 2.5,
    cut = 1.5,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_mom_perp",
	x_title ="Subleading track p_{\\perp}",
	x_units ="GeV",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.001,
    x_min = 0,
    x_max = 100,
    use_ntuple = use_ntuple,
    ntup_nbins = 20,
    # draw_cut = True,
    ratio_ymin = 0,
    ratio_ymax = 2.1,
    cut = 1.5,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.1,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel] + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    # name="DV_r",
    name="DV_trk_0_mom_parall",
    name_y = "DV_trk_1_mom_parall",
    x_title ="Leading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Subleading track p_{\\parallel} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"\\mu\\mu\\mu, 10 GeV, 10mm"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    # name="DV_r",
    name="DV_trk_0_mom_perp",
    name_y = "DV_trk_1_mom_perp",
    x_title ="Leading track p_{\\perp}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Subleading track p_{\\perp} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    x_max = 400,
    use_ntuple = use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
    ntup_2D = True,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"\\mu\\mu\\mu, 10 GeV, 10mm"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    # name="DV_r",
    name="DV_trk_0_mom_parall",
    name_y = "DV_trk_0_mom_perp",
    x_title ="Leading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Leading track p_{\\perp} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
    # ntup_nbins =60,
    # ntup_nbins_y =50,
    ntup_2D = True,
    
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"\\mu\\mu\\mu, 10 GeV, 10mm"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_mom_parall",
    name_y = "DV_trk_1_mom_perp",
    x_title ="Subleading track p_{\\parallel}",
	x_units ="GeV",
    y_title = "Subleading track p_{\\perp} [GeV]",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    x_max = 400,
    use_ntuple = use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
    ntup_2D = True,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"\\mu\\mu\\mu, 10 GeV, 10mm"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_0_mom_parall",
    name_y = "DV_trk_1_mom_perp",
    x_title ="Leading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Subleadingtrack p_{\\perp} [GeV]",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    x_max = 400,
    use_ntuple = use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
    ntup_2D = True,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"\\mu\\mu\\mu, 10 GeV, 10mm"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_trk_1_mom_parall",
    name_y = "DV_trk_0_mom_perp",
    x_title ="Subeading track p_{\\parallel}",
	x_units ="GeV",
    y_title = "Leading track p_{\\perp} [GeV]",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    x_max = 400,
    use_ntuple = use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
    ntup_2D = True,
    extra_cuts = extra_cuts,

	norm = norm,
	log_scale_y = False,
    empty_scale = 2,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"\\mu\\mu\\mu, 10 GeV, 10mm"]  + cut_list
	)


#################################################################################################################################################################################################################################
		
        # Mass Variables 

#################################################################################################################################################################################################################################
  
    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="mvis",
	x_title ="Visble mass",
	x_units ="GeV",
	y_title = "Events",
    y_min = 0.1,
    x_min = 0,
    x_max = 200,
    rebin = 10,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="mtrans",
	x_title ="Transverse mass",
	x_units ="GeV",
    y_min = 0.1,
    x_min = 0,
    x_max = 200,
    rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_redmass",
	x_title ="Reduced DV mass",
	x_units ="GeV",
    y_min = 0.1,
    x_min = 0,
    x_max = 50,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="DV_redmassvis",
	x_title ="Reduced visible mass",
	x_units ="GeV",
	y_title = "Events",
    y_min = 0.1,
    x_min = 0,
    x_max = 200,
    rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)
   
#################################################################################################################################################################################################################################
		
        # HNL Variables 

#################################################################################################################################################################################################################################

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="HNLm",
	x_title ="HNL mass",
	x_units ="GeV",
	# y_title = "Events",
    y_min = 0.1,
    # y_max = 20 ,
    x_min = 0,
    x_max = 25,
    # rebin = 2,
    use_ntuple = use_ntuple,
    ntup_nbins= 50,
    extra_cuts = extra_cuts,
    norm = norm,
    empty_scale = 1.6,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,extra_info]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="HNLpt",
	x_title ="HNL p_{T}",
	x_units ="GeV",
	y_title = "Events",
    y_min = 0.1,
    x_min =0,
    x_max = 200,
    rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="HNLeta",
	x_title ="HNL \\eta",
	x_units ="",
	y_title = "Events",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 5,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="HNLphi",
	x_title ="HNL \\phi",
	x_units ="",
	y_title = "Events",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 1,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


#################################################################################################################################################################################################################################
		
        # Prompt lepton Variables 

#################################################################################################################################################################################################################################


    Hist1D(hist_channels= hist_channels,
	types = samples,
    output_dir = output_dir,
    name="plep_pt",
	x_title ="Prompt lepton p_{T}",
	x_units ="GeV",
	y_title = "Events",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple = use_ntuple,
    ntup_nbins =100,
    extra_cuts = extra_cuts,
    norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)
