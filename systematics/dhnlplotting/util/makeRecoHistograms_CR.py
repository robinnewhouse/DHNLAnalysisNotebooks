# Plotting Script adapted from VH4b plotting and DHNLNtupleAnalaysis plotting scripts
# Last Major Overhaul of Code: Oct 16 2020 by D. Trischuk
import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from pylab import *
import atlas_style
import argparse
ROOT.gROOT.SetBatch(True)
from plot_classes import Hist1D,Hist2D,Hist1DRatio
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
# outputDir = '../output/3channels_SSandMC/' # change path here to save your histograms somewhere else!
outputDir = '../output/OSvSS_CR/' # change path here to save your histograms somewhere else!
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
norm = False
log_scale_y = True
draw_markers = True
use_ntuple = True
extra_cuts = "*(DV_mass < 20)"
cut_list =  extra_cuts.split('(')
for i in range(len(cut_list)): 
    cut_list[i] = cut_list[i].replace(")*", "")
    cut_list[i] = cut_list[i].replace(")", "")
del cut_list[0]
#############################################################################################################################################

# vtx_channels = ["VSI","VSI_Leptons","VSI_LRTR3_1p0","VSI_LeptonsMod_LRTR3_1p0"]
vtx_channels = ["VSI_LeptonsMod_LRTR3_1p0"]
vtx_channels = ["VSI_LeptonsMod"]
selection = "2trk"
# selection = "DVtype"
ln_type = "mixed"
for vtx_channel in vtx_channels:
    hist_channels = []
    # hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>)

    hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu 2-med", vtx_channel, selection])
    hist_channels.append([config_file["dataFile_CR"],"SS \\mu\\mu 2-med", vtx_channel, selection])
    samples = ["OS_uu","SS_uu"] 
    # samples = ["OS_uu"] 

    # hist_channels.append([config_file["dataFile_CR"],"OS e\\mu med-vvl", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS e\\mu med-vvl", vtx_channel, selection])  
    # samples = ["OS_eu","SS_eu"] 
    # samples = ["OS_eu"] 
    # samples = ["eee_10mm"] 

    # hist_channels.append([config_file["dataFile_CR"],"OS ee 2-vvl", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"SS ee 2-vvl", vtx_channel, selection])
    # samples = ["OS_ee","SS_ee"] 
    # hist_channels.append([config_file["dataFile_CR"],"All OS \\mu\\mu 2-med vertices", vtx_channel, selection])
    # hist_channels.append([config_file["dataFile_CR"],"OS \\mu\\mu 2-med vertices pass material veto", vtx_channel, selection])
  
    # samples = ["OS_uu","OS_uu_passmat"] 

    
    #10mm 3 GeV
    # hist_channels.append([config_file["mcFiles"][16], config_file["mcLabels"][16], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][17], config_file["mcLabels"][17], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][18], config_file["mcLabels"][18], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][19], config_file["mcLabels"][19], vtx_channel, selection,ln_type,])

      #1mm 3 GeV
    # hist_channels.append([config_file["mcFiles"][20], config_file["mcLabels"][20], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][21], config_file["mcLabels"][21], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][22], config_file["mcLabels"][22], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][23], config_file["mcLabels"][23], vtx_channel, selection,ln_type,])

    #100mm 3 GeV
    # hist_channels.append([config_file["mcFiles"][24], config_file["mcLabels"][24], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][25], config_file["mcLabels"][25], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][26], config_file["mcLabels"][26], vtx_channel, selection,ln_type,])
    # hist_channels.append([config_file["mcFiles"][27], config_file["mcLabels"][27], vtx_channel, selection,ln_type,])




    # define the sample type of the histograms you added to the hist channels list
   

    # Get integrated luminosity to scale MC files to 
    scalelumi = config_file["scaleLumi"] # luminosity you want to scale everything to 
    datalumi = config_file["dataLumi"] #  lumi of the data you are looking at
    # datalumi = 1.0 #  lumi of the data you are looking at
    # TODO: ideally lumi # should come from a value in the nutple, lumi still needs to be properly calculated - DT

#################################################################################################################################################################################################################################

        # DV Variables

#################################################################################################################################################################################################################################
    
    
    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_r",
	x_title ="L_{xy}",
	x_units ="mm",
	# y_title = "Vertices / 5 mm",
    # y_title = "m_{DV} [GeV]",
    y_min = 0.1,
    # y_max = 5,
    x_min = 0,
    x_max = 300,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    # ntup_nbins =75,
    # ntup_nbins_y =75,
    ntup_nbins =60,
    ntup_nbins_y =50,
    # ntup_2D = True,
    leg_size_mod = 0.7,
    ntup_1D = True,
    extra_cuts = extra_cuts,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
    draw_yield = True,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"]   + cut_list
	)

    Hist1D(hist_channels= hist_channels,
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
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "CR with prompt track cut"]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="HNLm",
	x_title ="HNL mass",
	x_units ="GeV",
    y_min = 1,
    # y_max = 20 ,
    x_min = 0,
    x_max = 30,
    # rebin = 2,
    use_ntuple = True,
    ntup_nbins= 60,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
    norm = norm,
    extra_cuts = extra_cuts,
    empty_scale = 1.8,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"CR with prompt track cut"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="HNLm",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
    x_title ="HNL mass",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = 0,
    # x_max = 300,
    x_max = 30,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =60,
    ntup_nbins_y =20,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)



    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_mom_parall",
	x_title ="Leading parallel track mommentum (p_{\\parallel})",
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
    ratio_ymax = 2.5,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_mom_parall",
	x_title ="Subleading parallel track mommentum (p_{\\parallel} )",
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
    ratio_ymax = 2.5,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_mom_perp",
	x_title ="Leading perpendicular track mommentum (p_{\\perp} )",
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
    ratio_ymax = 2.5,
    cut = 1.5,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
    empty_scale = 2.5,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel, "Control Region"] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_mom_perp",
	x_title ="Subleading perpendicular track mommentum (p_{\\perp} )",
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
    extra_legend_lines = [vtx_channel, "Control Region"] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_0_mom_frac_parall",
	x_title ="Leading track p_{\\parallel}/ p_{tot}",
	x_units ="",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = -1,
    x_max = 1,
    use_ntuple = True,
    ntup_nbins = 100,
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
    extra_legend_lines = [vtx_channel, "Control Region"] + cut_list
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_1_mom_frac_parall",
	x_title ="Subleading track p_{\\parallel}/ p_{tot}",
	x_units ="",
	# y_title = "Vertices / 0.5 GeV",
    y_min = 0.5,
    x_min = -1,
    x_max = 1,
    use_ntuple = True,
    ntup_nbins = 100,
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
    extra_legend_lines = [vtx_channel, "Control Region"] + cut_list
	)

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="ptrk_pt",
	# x_title ="Prompt Track p_{T}",
	# x_units ="GeV",
	# # y_title = "Vertices / 0.5 GeV",
    # y_min = 0.00001,
    # y_max = 0.3,
    # x_min = 0,
    # x_max = 200,
    # use_ntuple = True,
    # ntup_nbins = 40,
    # extra_cuts = extra_cuts,
    # # draw_cut = True,
    # # extra_cuts = extra_cuts,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = True,
	# log_scale_y = False,
    # empty_scale = 2.1,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [vtx_channel, "Control Region"] 
	# )


    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_parall",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
    x_title ="Leading parallel track mommentum (p_{\\parallel})",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =80,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_1_mom_parall",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
    x_title ="Subleading parallel track mommentum (p_{\\parallel})",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =80,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_perp",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
    x_title ="Leading perpendicular track mommentum (p_{\\perp})",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =80,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_1_mom_perp",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
    x_title ="Subleading perpedicular track mommentum (p_{\\perp})",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =80,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)


    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_frac_parall",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
	x_title ="Leading track p_{\\parallel}/ p_{tot}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = 0,
    x_max = 1,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =50,
    ntup_nbins_y =80,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_1_mom_frac_parall",
    name_y = "DV_mass",
    extra_cuts = extra_cuts,
	x_title ="Subleading track p_{\\parallel}/ p_{tot}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = 0,
    x_max = 1,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =50,
    ntup_nbins_y =80,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_parall",
    name_y = "DV_trk_1_mom_parall",
    extra_cuts = extra_cuts,
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
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_perp",
    name_y = "DV_trk_1_mom_perp",
    extra_cuts = extra_cuts,
    x_title ="Leading track p_{\\perp}  ",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Subleading track p_{\\perp} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)
    continue

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_parall",
    name_y = "DV_trk_0_mom_perp",
    extra_cuts = extra_cuts,
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
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_1_mom_parall",
    name_y = "DV_trk_1_mom_perp",
    extra_cuts = extra_cuts,
    x_title ="Subleading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Subleading track p_{\\perp} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_0_mom_parall",
    name_y = "DV_trk_1_mom_perp",
    extra_cuts = extra_cuts,
    x_title ="Leading track p_{\\parallel}",
	x_units ="GeV",
	# y_title = "Vertices",
    y_title = "Subleadingtrack p_{\\perp} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = -400,
    y_max = 400,
    x_min = -400,
    # x_max = 300,
    x_max = 400,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)

    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_trk_1_mom_parall",
    name_y = "DV_trk_0_mom_perp",
    extra_cuts = extra_cuts,
    x_title ="Subeading track p_{\\parallel}",
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
    use_ntuple =  use_ntuple,
    ntup_nbins =160,
    ntup_nbins_y =160,
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
    extra_legend_lines = [vtx_channel,"Control Region"]  + cut_list
	)




    continue 
    Hist2D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    # name="DV_r",
    name="DV_alpha",
    name_y = "DV_mass",
    extra_cuts = "*(DV_mass < 20)*(DV_cosmic_sep > 0.05)",
    x_title ="Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
	x_units ="rad",
	# y_title = "Vertices",
    y_title = "m_{DV} [GeV]",
    # y_title = " Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
    y_min = 0,
    y_max = 10,
    x_min = 0,
    # x_max = 300,
    x_max = 3.5,
    # rebin = 5,
    use_ntuple =  use_ntuple,
    ntup_nbins =175,
    ntup_nbins_y =20,
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
    extra_legend_lines = [vtx_channel]
	)


    continue

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_alpha",
	# x_title ="DV mass",
    x_title ="Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
	x_units ="rad",
	# y_title = "Vertices",
    # y_title = "DV masss [GeV]",
    y_min = 0.1,
    # y_max = 20,
    x_min = 0,
    x_max = 0.5,
    use_ntuple =  use_ntuple,
    ntup_nbins =40,
    ntup_nbins_y =200,
    # ntup_2D = True,
    ntup_1D = True,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = True,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_mass",
	x_title ="DV mass",
	x_units ="GeV",
	# y_title = "Vertices",
    y_min = 0.1,
    # y_max = 20,
    x_min = 0,
    x_max = 20,
    use_ntuple =  use_ntuple,
    ntup_nbins =40,
    ntup_nbins_y =200,
    # ntup_2D = True,
    ntup_1D = True,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
    cut = 1.5,
	log_scale_y = True,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)


    continue
    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="DV_pt",
	# x_title ="DV p_{T}",
	# x_units ="GeV",
	# y_title = "Vertices",
    # y_min = 0.1,
    # x_min = 0,
    # x_max = 100,
    # rebin = 4,
    # use_ntuple =  use_ntuple,
    # ntup_1D = True,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [vtx_channel]
	# )

    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="DV_eta",
	# x_title ="DV \\eta",
	# x_units ="",
	# y_title = "Vertices",
    # y_min = 0.1,
    # x_min = -3,
    # x_max = 3,
    # rebin = 2,
    # use_ntuple =  use_ntuple,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [vtx_channel]
	# )


    # Hist1D(hist_channels= hist_channels,
	# types = samples,
    # outputDir = outputDir,
    # name="DV_phi",
	# x_title ="DV \\phi",
	# x_units ="",
	# y_title = "Vertices",
    # y_min = 0.1,
    # x_min = -4,
    # x_max = 4,
    # rebin = 2,
    # use_ntuple =  use_ntuple,
    # ntup_nbins =100,
    # scaleLumi = scalelumi,
    # dataLumi = datalumi,
	# norm = norm,
	# log_scale_y = log_scale_y,
	# draw_markers = draw_markers,
	# atlas_mod = "Internal",
    # extra_legend_lines = [vtx_channel]
	# )


    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_angle_bw_rDV_pDV",
	x_title ="Angle between \\vec{r}_{DV} and \\vec{p}_{DV}",
	x_units ="",
	y_title = "Vertices",
    y_min = 0.1,
    x_min = 0,
    x_max = 3.5,
    # rebin = 2,
    use_ntuple =  use_ntuple,
    ntup_1D = True,
    ntup_nbins =35,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)




    continue
#################################################################################################################################################################################################################################
	
    # DV Track Variables 

#################################################################################################################################################################################################################################

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_pt",
	x_title ="DV track p_{T}",
	x_units ="GeV",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 100,
    rebin = 4,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_eta",
	x_title ="DV track \\eta",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -3,
    x_max = 3,
    rebin = 2,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_phi",
	x_title ="DV track \\phi",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -4,
    x_max = 4,
    rebin = 2,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_d0",
	x_title ="DV track d0",
	x_units ="mm",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -10,
    x_max = 10,
    rebin = 1,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_z0",
	x_title ="DV track z0",
	x_units ="mm",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = -500,
    x_max = 500,
    rebin = 4,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_z0",
	x_title ="DV track |z0|",
	x_units ="mm",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 500,
    rebin = 4,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_nSiHits",
	x_title ="DV track nSiHits",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 23,
    rebin = 1,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_nSCTHits",
	x_title ="DV track nSCTHits",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 14,
    rebin = 1,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_isLRT",
	x_title ="DV track isLRT",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 2,
    rebin = 1,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
	types = samples,
    outputDir = outputDir,
    name="DV_trk_chi2",
	x_title ="DV track \\chi^{2}",
	x_units ="",
	y_title = "Tracks",
    y_min = 0.1,
    x_min = 0,
    x_max = 10,
    rebin = 1,
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
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
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
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
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)


    Hist1D(hist_channels= hist_channels,
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
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,selection]
	)

    Hist1D(hist_channels= hist_channels,
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
    use_ntuple =  use_ntuple,
    ntup_nbins =100,
    scaleLumi = scalelumi,
    dataLumi = datalumi,
	norm = norm,
	log_scale_y = log_scale_y,
	draw_markers = draw_markers,
	atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel]
	)
