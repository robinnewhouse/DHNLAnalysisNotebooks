# Plotting Script
<<<<<<< HEAD
import os, math, ROOT, json,sys
import numpy as np
import commentjson
from ROOT import *
from ROOT import gPad
from pylab import *
sys.path.append('../python/')
# Considering your module contains a function called my_func, you could import it:
import plotting
import helpers
=======
import argparse, os, math, ROOT, glob, uproot, time, json
import numpy as np
import helpers
from ROOT import *
from ROOT import gPad
from pylab import *
import plotting
>>>>>>> 0ff170c09c658bf537d58ba778830564e3ec1fa2
import atlas_style

ROOT.gROOT.SetBatch(True)

<<<<<<< HEAD

#trying to  set ATLAS style a million different ways
gROOT.SetStyle("ATLAS") #might have to change how you set atlas style like this, depends how you have setup python
# atlas_style.AtlasStyle()	
# gROOT.LoadMacro("AtlasStyle.C")
# gROOT.LoadMacro("AtlasUtils.C")
# gROOT.LoadMacro("AtlasLabels.C")
# SetAtlasStyle()
=======
#trying to  set ATLAS style a million different ways
gROOT.SetStyle("ATLAS") #might have to change how you set atlas style like this, depends how you have setup python
# atlas_style.AtlasStyle()	
gROOT.LoadMacro("AtlasStyle.C")
gROOT.LoadMacro("AtlasUtils.C")
gROOT.LoadMacro("AtlasLabels.C")
SetAtlasStyle()
>>>>>>> 0ff170c09c658bf537d58ba778830564e3ec1fa2

logger = helpers.getLogger('dHNLAnalysis.plotHisotgrams')

#############################################################################################################################################
# globals
<<<<<<< HEAD
outputDir = '../output/significance_TRExcompare/' # change path here to save your histograms somewhere else!
# outputDir = '../output/TwoSR_LNC_LNV/' # change path here to save your histograms somewhere else!
# outputDir = '../output/LRTrun3_ueu_noFilterRun3/' # change path here to save your histograms somewhere else!
MATERIAL_LAYERS = [33.25, 50.5, 88.5, 122.5, 299]
lumi = 60
normalize = False
setlogy = False
drawRatio=False
draw_channel_info = True
do_cut_significance = True
=======
outputDir = '../output/plots/comparemass_scaleMC/' # change path here to save your histograms somewhere else!

>>>>>>> 0ff170c09c658bf537d58ba778830564e3ec1fa2

#############################################################################################################################################


<<<<<<< HEAD
def makeCutflows(config_file):
	vtx_channels = ["VSI", "VSI_Leptons"]
	for vtx_channel in vtx_channels:
		if "dataFile" in config_file.keys():
			plotting.plot_cutflow(file = config_file["dataFile"],
								  vertextype= vtx_channel,
								  output_dir=outputDir)
		nMCfiles = len(config_file["mcFiles"])

		for i in range(nMCfiles): 
			plotting.plot_cutflow(file = config_file["mcFiles"][i],
								  vertextype= vtx_channel,
								  output_dir=outputDir)


		# plotting.plot_cutflow(file = config_file["mcFiles"][2],
		# 						  vertextype= vtx_channel,
		# 						  output_dir=outputDir)

		


def check_rerunningVSI(config_file, selection):
	hist_channels = []
	# hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>)
	hist_channels.append([config_file["rerunVSIfile"],"VSI", "VSI", selection])
	hist_channels.append([config_file["rerunVSIfile"],"VSI_2", "VSI_2", selection])

	plotting.compare(hist_channels,
						 variable='DV_r',
						 nRebin=10,
						 setrange=(0, 350),
						 setlogy = setlogy,
						 scaleymax=2.5,
						 lumi = lumi,
						 normalize = True,
						 vertical_lines=MATERIAL_LAYERS,
						 vertical_legend="Material Layers",
						 output_dir= outputDir
						 )



def compare_histograms(config_file, selection):
	vtx_channels = ["VSI", "VSI_Leptons"]
	for vtx_channel in vtx_channels:
		hist_channels = []
		# hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>)
		# hist_channels.append([config_file["dataFile"],config_file["dataLabel"], vtx_channel, selection])
		hist_channels.append([config_file["dataFile_mumu"],config_file["dataLabel_mumu"], vtx_channel, selection])
		# hist_channels.append([config_file["mcFiles"][0],config_file["mcLabels"][0], vtx_channel, selection])
		# hist_channels.append([config_file["mcFiles"][1], config_file["mcLabels"][1], vtx_channel, selection])
		hist_channels.append([config_file["mcFiles"][2], config_file["mcLabels"][2], vtx_channel, selection])
		
		#get integrated luminosity to scale MC files to (ideally this should come from a value in the nutple TD DO) - DT
		scalelumi = config_file["scaleLumi"]

		if "dataLumi" in config_file.keys():
			datalumi = config_file["dataLumi"]
		else: 
			datalumi = 140.0
		
		if "ratioLabel" in config_file.keys():
			ratioLabel = config_file["ratioLabel"]
		else:
			ratioLabel = [""]


		# DV Variables
		plotting.compare(hist_channels,
						 variable='DV_r',
						 nRebin=10,
						 setrange=(0, 350),
						 # setrange=(0, 10),
						 setlogy = True,
						 scaleymax=1.6,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 vertical_lines=MATERIAL_LAYERS,
						 vertical_legend="Material Layers",
						 output_dir= outputDir
						 )

		# DV Track Variables 
		plotting.compare(hist_channels,
						 variable='DV_trk_pt',
						 setrange=(0, 100),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_eta',
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_phi',
						 nRebin = 2, 
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_eta',
						 setrange=(-3, 3),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_d0',
						 setrange=(-10, 10),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_z0',
						 setrange=(-10, 10),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_dpt',
						 setrange=(0, 20),
						 nRebin = 2, 
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_deta',
						 setrange=(0, 3.2),
						 nRebin = 2, 
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_dphi',
						 setrange=(0, 3.2),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_trk_dR',
						 setrange=(0, 10),
						 nRebin = 10, 
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir = outputDir
						 )

		# Mass Variables 
		plotting.compare(hist_channels,
						 variable='DV_mass',
						 setrange=(0, 20),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 vertical_lines=[4],
						 vertical_legend="DV mass cut",
						 output_dir= outputDir
						 )

		plotting.compare(hist_channels,
						 variable='mvis',
						 nRebin=5,
						 setrange=(0, 200),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )

		plotting.compare(hist_channels,
						 variable='mtrans',
						 nRebin=5,
						 setrange=(0, 200),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )
		plotting.compare(hist_channels,
						 variable='HNLm',
						 setrange=(0, 30),
						 setlogy = setlogy ,
						 scaleymax=1.4,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 do_cut_significance= False,
						 output_dir= outputDir
						 )
		plotting.compare(hist_channels,
					 variable='HNLm_altbinning',
					 setrange=(0, 30),
					 setlogy = setlogy,
					 scaleymax=1.4,
					 scalelumi = scalelumi,
					 datalumi = datalumi,
					 drawRatio = drawRatio,
					 ratioLabel = ratioLabel,
					 normalize = normalize,
					 draw_channel_info= draw_channel_info,
					 do_cut_significance= do_cut_significance,
					 output_dir= outputDir
					 )


		plotting.compare(hist_channels,
						 variable='DV_redmass',
						 setrange=(0, 50),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )

		plotting.compare(hist_channels,
						 variable='DV_redmassvis',
						 setrange=(0, 200),
						 nRebin=5,
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )
		plotting.compare(hist_channels,
						 variable='DV_redmassHNL',
						 setrange=(0, 50),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )

		# HNL quantities
		plotting.compare(hist_channels,
						 variable='HNLpt',
						 setrange=(0, 50),
						 nRebin=5,
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )

		plotting.compare(hist_channels,
						 variable='HNLeta',
						 setrange=(0, 50),
						 nRebin=5,
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )

		plotting.compare(hist_channels,
						 variable='HNLphi',
						 setrange=(-3,3),
						 setlogy = setlogy,
						 scalelumi = scalelumi,
						 datalumi = datalumi,
						 drawRatio = drawRatio,
						 ratioLabel = ratioLabel,
						 normalize = normalize,
						 draw_channel_info= draw_channel_info,
						 output_dir= outputDir
						 )
=======

def compareMCdata(config_file):

	#add plots here if you want to compare different distributions with with data & MC
	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel=  config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_mass", 
							scaleymax = 1.5,
							setrange= "0 20",					
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir=outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel=  config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],				
							hname = "cosmic_DV_mass", 
						    setrange= "0 20",
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir=outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_r",
							setrange= "0 300", 
							# setlogy=True,
							nRebin = 5, 
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_r", 
							nRebin = 5, 
							setrange= "0 300", 
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_pt",
							nRebin = 2, 
							setrange= "0 100",					
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_pt",
							nRebin = 2, 
							setrange= "0 100",
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_phi", 
							scaleymax = 2.2,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_phi", 
							scaleymax = 2.2,
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_eta", 
							scaleymax = 2.2,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"],
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"], 
							hname = "cosmic_DV_trk_eta", 
							scaleymax = 2.2,
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_d0",
							setrange= "-10 10",
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_d0", 
							setrange= "-10 10",							
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_dpt",
							nRebin = 2, 
							setrange= "0 20",
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_dpt",
							nRebin = 2, 
							setrange= "0 20",						
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_deta", 
							nRebin = 2, 
							setrange= "0 4",
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
						  	mcfiles=config_file["mcFile"],
						  	hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"], 
							hname = "cosmic_DV_trk_deta", 
							nRebin = 2, 
							setrange= "0 4",
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_dphi",
							setrange= "0 3.2",
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_dphi",  
							setrange= "0 3.2",	
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_dR", 
							nRebin = 10, 
							setrange= "0 5",							
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_DV_trk_dR", 
							nRebin = 10, 
							setrange= "0 10",
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_mvis", 
							nRebin = 5, 
							setrange= "0 200",
							scaleymax = 1.5,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_mvis", 
							nRebin = 5, 
							setrange= "0 200",
							scaleymax = 1.5,							
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_mtrans",
							nRebin = 5, 
							setrange= "0 200",
							scaleymax = 1.5,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_mtrans", 
							nRebin = 5, 
							setrange= "0 200",
							scaleymax = 1.5,
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)



	# plotting.compare_dataMC(datafile=config_file["dataFile"],
	# 						mcfiles=config_file["mcFile"],
	# 						hdatalabel= config_file["dataLabel"],
	# 						hmclabels = config_file["mcLabel"],
	# 						hname = "cosmic_DV_redmass",  
	# 						setrange= "0 20",
	# 						scaleymax = 1.5,
	# 						vertextype = "VSI Leptons",
	#  						outputDir= outputDir)

	# plotting.compare_dataMC(datafile=config_file["dataFile"],
	# 						mcfiles=config_file["mcFile"],
	# 						hdatalabel= config_file["dataLabel"],
	# 						hmclabels = config_file["mcLabel"],
	# 						hname = "cosmic_DV_redmass", 
	# 						setrange= "0 20",
	# 						scaleymax = 1.5,
	# 						vertextype = "VSI",
	# 						outputDir= outputDir)


	# plotting.compare_dataMC(datafile=config_file["dataFile"],
	# 						mcfiles=config_file["mcFile"], 
	# 						hdatalabel= config_file["dataLabel"],
	# 						hmclabels = config_file["mcLabel"],
	# 						hname = "cosmic_DV_redmassvis",
	# 						nRebin = 5, 
	# 						setrange= "0 200",
	# 						scaleymax = 1.5,
	# 						vertextype = "VSI Leptons",
	# 						outputDir= outputDir)

	# plotting.compare_dataMC(datafile=config_file["dataFile"],
	# 						mcfiles=config_file["mcFile"], 
	# 						hdatalabel= config_file["dataLabel"],
	# 						hmclabels = config_file["mcLabel"],
	# 						hname = "cosmic_DV_redmassvis", 
	# 						nRebin = 5, 
	# 						setrange= "0 200",
	# 						scaleymax = 1.5,
	# 						vertextype = "VSI",
 	#						outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_HNLm",
							setlogy=False,
							setrange= "0 30",
							scaleymax = 1.5,							 							
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_HNLm", 
							setrange= "0 30",
							scaleymax = 1.5,
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	# plotting.compare_dataMC(datafile=config_file["dataFile"],
	# 						mcfiles=config_file["mcFile"],
	# 						hdatalabel= config_file["dataLabel"],
	# 						hmclabels = config_file["mcLabel"], 
	# 						hname = "cosmic_DV_redmassHNL",
	# 						setrange= "0 50",
	# 						scaleymax = 1.5,
	# 						vertextype = "VSI Leptons",
	# 						outputDir= outputDir)
						

	# plotting.compare_dataMC(datafile=config_file["dataFile"],
	# 						mcfiles=config_file["mcFile"], 
	# 						hdatalabel= config_file["dataLabel"],
	# 						hmclabels = config_file["mcLabel"],
	# 						hname = "cosmic_DV_redmassHNL", 
	# 						nRebin = 1, 
	# 						setrange= "0 50",
	# 						scaleymax = 1.5,				
	# 						vertextype = "VSI",
	# 						outputDir= outputDir)
	

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_HNLpt",
							nRebin = 5, 
							setrange= "0 200",
							scaleymax = 1.5,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_HNLpt",
							nRebin = 5, 
							setrange= "0 200",
							scaleymax = 1.5,
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_HNLphi", 
							setrange= "-4 4",
							scaleymax = 1.5,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "cosmic_HNLphi", 
							setrange= "-4 4",
							scaleymax = 1.5,
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)


	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "DVtype_HNLeta",
							setrange= "-3 3",
							scaleymax = 1.5,
							vertextype = "VSI Leptons",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)

	plotting.compare_dataMC(datafile=config_file["dataFile"],
							mcfiles=config_file["mcFile"], 
							hdatalabel= config_file["dataLabel"],
							hmclabels = config_file["mcLabel"],
							hname = "DVtype_HNLeta",
							setrange= "-3 3",
							scaleymax = 1.5,			
							vertextype = "VSI",
							normalize = False,
							lumi = 4,
							outputDir= outputDir)




def make2Dcorrplots(config_file):

	# MC FILES
	# plotting.CorrPlot2D( file= config_file["mcFile"][0], 
	# 			hname="charge_DVmass_mvis", 
	# 			hlabel=config_file["mcLabel"][0],
	# 			rebinx=1,
	# 			rebiny=5,
	# 			vertextype="VSI",
	# 			setxrange="0 30",
	# 			setyrange="0 300",
	# 			outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D( file= config_file["mcFile"][0], 
	# 			hlabel=config_file["mcLabel"][0],
	# 			hname="charge_DVmass_mvis",
	# 			rebinx=1,
	# 			rebiny=5,
	# 			vertextype="VSI Leptons",
	# 			setxrange="0 30",
	# 			setyrange="0 300",
	# 			outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_DVmass_mtrans", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI",
	# 		setxrange="0 30",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_DVmass_mtrans", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 30",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		rebinx=5,
	# 		rebiny=5,
	# 		hname="charge_mvis_mtrans", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI",
	# 		setxrange="0 100",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		rebinx=5,
	# 		rebiny=5,
	# 		hname="charge_mvis_mtrans", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 100",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		hname="charge_DVmass_mhnl", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		hname="charge_DVmass_mhnl", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")


	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		rebinx=5,
	# 		rebiny=1,
	# 		hname="charge_mvis_mhnl", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI",
	# 		setxrange="0 300",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		rebinx=5,
	# 		rebiny=1,
	# 		hname="charge_mvis_mhnl", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 300",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		hname="charge_mhnl_hnlpt", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		hname="charge_mhnl_hnlpt", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		hname="charge_mhnl2D", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI",
	# 		setxrange="0 100",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][0], 
	# 		hname="charge_mhnl2D", 
	# 		hlabel=config_file["mcLabel"][0],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 100",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt1_")


# MC FILES
	# plotting.CorrPlot2D( file= config_file["mcFile"][1], 
	# 			hname="charge_DVmass_mvis", 
	# 			hlabel=config_file["mcLabel"][1],
	# 			rebinx=1,
	# 			rebiny=5,
	# 			vertextype="VSI",
	# 			setxrange="0 30",
	# 			setyrange="0 300",
	# 			outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D( file= config_file["mcFile"][1], 
	# 			hlabel=config_file["mcLabel"][1],
	# 			hname="charge_DVmass_mvis",
	# 			rebinx=1,
	# 			rebiny=5,
	# 			vertextype="VSI Leptons",
	# 			setxrange="0 30",
	# 			setyrange="0 300",
	# 			outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_DVmass_mtrans", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI",
	# 		setxrange="0 30",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_DVmass_mtrans", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 30",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		rebinx=5,
	# 		rebiny=5,
	# 		hname="charge_mvis_mtrans", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI",
	# 		setxrange="0 100",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		rebinx=5,
	# 		rebiny=5,
	# 		hname="charge_mvis_mtrans", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 100",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		hname="charge_DVmass_mhnl", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		hname="charge_DVmass_mhnl", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")


	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		rebinx=5,
	# 		rebiny=1,
	# 		hname="charge_mvis_mhnl", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI",
	# 		setxrange="0 300",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		rebinx=5,
	# 		rebiny=1,
	# 		hname="charge_mvis_mhnl", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 300",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		hname="charge_mhnl_hnlpt", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		hname="charge_mhnl_hnlpt", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		hname="charge_mhnl2D", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI",
	# 		setxrange="0 100",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][1], 
	# 		hname="charge_mhnl2D", 
	# 		hlabel=config_file["mcLabel"][1],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 100",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt10_")


	# # MC FILES
	# plotting.CorrPlot2D( file= config_file["mcFile"][2], 
	# 			hname="charge_DVmass_mvis", 
	# 			hlabel=config_file["mcLabel"][2],
	# 			rebinx=1,
	# 			rebiny=5,
	# 			vertextype="VSI",
	# 			setxrange="0 30",
	# 			setyrange="0 300",
	# 			outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D( file= config_file["mcFile"][2], 
	# 			hlabel=config_file["mcLabel"][2],
	# 			hname="charge_DVmass_mvis",
	# 			rebinx=1,
	# 			rebiny=5,
	# 			vertextype="VSI Leptons",
	# 			setxrange="0 30",
	# 			setyrange="0 300",
	# 			outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_DVmass_mtrans", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 30",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_DVmass_mtrans", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 30",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=5,
	# 		rebiny=5,
	# 		hname="charge_mvis_mtrans", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 100",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=5,
	# 		rebiny=5,
	# 		hname="charge_mvis_mtrans", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 100",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		hname="charge_DVmass_mhnl", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		hname="charge_DVmass_mhnl", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")


	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=5,
	# 		rebiny=1,
	# 		hname="charge_mvis_mhnl", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 300",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=5,
	# 		rebiny=1,
	# 		hname="charge_mvis_mhnl", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 300",
	# 		setyrange="0 50",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")



	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_mhnl_mtrans", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		rebinx=1,
	# 		rebiny=5,
	# 		hname="charge_mhnl_mtrans", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 300",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		hname="charge_mhnl_hnlpt", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 50",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		hname="charge_mhnl_hnlpt", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 50",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		hname="charge_mhnl2D", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI",
	# 		setxrange="0 100",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")

	# plotting.CorrPlot2D(file= config_file["mcFile"][2], 
	# 		hname="charge_mhnl2D", 
	# 		hlabel=config_file["mcLabel"][2],
	# 		vertextype="VSI Leptons",
	# 		setxrange="0 100",
	# 		setyrange="0 100",
	# 		outputDir=outputDir + "2Dcorrplots/mc/lt100_")



	# DATA FILES
	plotting.CorrPlot2D(config_file["dataFile"], 
			hname="sel_DVmass_mvis", 
			hlabel=config_file["dataLabel"],
			rebinx=1,
			rebiny=5,
			vertextype="VSI",
			setxrange="0 30",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			hname="sel_DVmass_mvis", 
			hlabel=config_file["dataLabel"],
			rebinx=1,
			rebiny=5,
			vertextype="VSI Leptons",
			setxrange="0 30",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=1,
			rebiny=5,
			hname="sel_DVmass_mtrans", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 30",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=1,
			rebiny=5,
			hname="sel_DVmass_mtrans", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 30",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=5,
			rebiny=5,
			hname="sel_mvis_mtrans", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 100",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=5,
			rebiny=5,
			hname="sel_mvis_mtrans", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 100",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			hname="sel_DVmass_mhnl", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 50",
			setyrange="0 50",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			hname="sel_DVmass_mhnl", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 50",
			setyrange="0 50",
			outputDir=outputDir +"2Dcorrplots/data/")


	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=5,
			rebiny=1,
			hname="sel_mvis_mhnl", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 300",
			setyrange="0 50",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=5,
			rebiny=1,
			hname="sel_mvis_mhnl", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 300",
			setyrange="0 50",
			outputDir=outputDir +"2Dcorrplots/data/")


	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=1,
			rebiny=5,
			hname="sel_mhnl_mtrans", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 50",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(config_file["dataFile"], 
			rebinx=1,
			rebiny=5,
			hname="sel_mhnl_mtrans", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 50",
			setyrange="0 300",
			outputDir=outputDir +"2Dcorrplots/data/")

	plotting.CorrPlot2D(file= config_file["dataFile"], 
			hname="sel_mhnl_hnlpt", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 50",
			setyrange="0 100",
			outputDir=outputDir + "2Dcorrplots/data/")

	plotting.CorrPlot2D(file= config_file["dataFile"], 
			hname="sel_mhnl_hnlpt", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 50",
			setyrange="0 100",
			outputDir=outputDir + "2Dcorrplots/data/")

	plotting.CorrPlot2D(file= config_file["dataFile"], 
			hname="sel_mhnl2D", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI",
			setxrange="0 100",
			setyrange="0 100",
			outputDir=outputDir + "2Dcorrplots/data/")

	plotting.CorrPlot2D(file= config_file["dataFile"], 
			hname="sel_mhnl2D", 
			hlabel=config_file["dataLabel"],
			vertextype="VSI Leptons",
			setxrange="0 100",
			setyrange="0 100",
			outputDir=outputDir + "2Dcorrplots/data/")



def makeCutflows(config_file):
	# make Cutflow plots here
	plotting.plot_cutflow(file = config_file["mcFile"][0],
						  vertextype= "VSI Leptons",
						  outputDir=outputDir + "Cutflows/")

	plotting.plot_cutflow(file = config_file["dataFile"],
						  vertextype= "VSI Leptons",
						  outputDir=outputDir + "Cutflows/")


def compareHistograms(config_file):
	# compare different histograms from the same file here
	# plotting.compareN(file=config_file["mcFile"][0],
	# 		hname = ["sel_DV_mass","sel_mvis","sel_HNLm","sel_mtrans","sel_DV_redmass"],
	# 		hlabel = ["DV mass","Visible mass","m_{HNL}", "m_{T}","Reduced mass"], 
	# 		setxrange= "0 100",
	# 		scaleymax=1.5,
	# 		nRebin=5,
	# 		vertextype= "VSI Leptons",
	# 		savefilename="selMC_mass",
	# 		outputDir=outputDir)

	plotting.compareN(file=config_file["mcFile"][0],
			hname = ["charge_DV_trk_dR","charge_DV_trk_dR2"],
			hlabel = ["\DeltaR by hand","\DeltaR from 4-vector class"], 
			setxrange= "0 8",
			scaleymax=1.5,
			nRebin=10,
			vertextype= "VSI",
			savefilename="dRdefCompare",
			outputDir=outputDir)


	plotting.compareN(file=config_file["mcFile"][0],
			hname = ["charge_DV_trk_dphi","charge_DV_trk_dphi2"],
			hlabel = ["\Delta\phi by hand","\Delta\phi from 4-vector class"], 
			setxrange= "0 8",
			scaleymax=1.5,
			vertextype= "VSI",
			savefilename="dPhidefCompare",
			outputDir=outputDir)

>>>>>>> 0ff170c09c658bf537d58ba778830564e3ec1fa2




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

<<<<<<< HEAD

	if not os.path.exists(outputDir): os.mkdir(outputDir)
	if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
	if not os.path.exists(outputDir + "Cutflows/"): os.mkdir(outputDir + "Cutflows/")
	if not os.path.exists(outputDir + "2Dmassplots"): os.mkdir(outputDir + "2Dmassplots")
	if not os.path.exists(outputDir + "2Dmassplots/data/"): os.mkdir(outputDir + "2Dmassplots/data/")
	if not os.path.exists(outputDir + "2Dmassplots/data/"): os.mkdir(outputDir + "2Dmassplots/data/")
	if os.path.exists(outputDir + "Asimov_dataset.root"): os.remove(outputDir + "Asimov_dataset.root")

=======
	if os.path.exists(outputDir):
		pass
	else: 
		logger.info('Making output directories...')
		os.mkdir(outputDir)
		os.mkdir(outputDir + "Cutflows/")
		os.mkdir(outputDir + "2Dcorrplots")
		os.mkdir(outputDir + "2Dcorrplots/data/")
		os.mkdir(outputDir + "2Dcorrplots/mc/")
>>>>>>> 0ff170c09c658bf537d58ba778830564e3ec1fa2



	with open(options.config, 'r') as json_config:
		config_file = json.load(json_config) # load JSON config file


	#execute plotting here, comment out functions in you dont want to plot them again.	
<<<<<<< HEAD
	makeCutflows(config_file)
	compare_histograms(config_file, 'DVtype')
	# check_rerunningVSI(config_file,"all")
=======
	compareMCdata(config_file)
	# makeCutflows(config_file)
	# compareHistograms(config_file)
	# make2Dcorrplots(config_file)
>>>>>>> 0ff170c09c658bf537d58ba778830564e3ec1fa2

	
	