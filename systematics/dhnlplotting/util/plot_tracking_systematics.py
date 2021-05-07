import plot_classes
import ROOT
ROOT.gROOT.SetStyle("ATLAS")


files ={ 
    "uuu_10_10" : "/Users/robinnewhouse/ATLAS/data/histograms_mc16e_uuu_10G_10mm.root",
    "uuu_10_10_tracksdropped" : "/Users/robinnewhouse/ATLAS/data/histograms_mc16e_uuu_10G_10mm_tracksdropped.root"
  
}

# hist_channels[i] = (<filename>, <legend label>,<vertex directory>, <selection directory>,<MCtype (LNC or LNV) if needed>)

hist_channels = [
    (files['uuu_10_10'], 'Nominal, DV type cut:', 'VSI_LeptonsMod', 'DVtype', 'LNC'),
    (files['uuu_10_10_tracksdropped'], 'Tracks dropped, DV type cut:', 'VSI_LeptonsMod', 'DVtype', 'LNC')
]
samples = ['uuu_10mm', 'uuu_10mm']
outputDir = '/Users/robinnewhouse/ATLAS/dhnlplotting/output'
scalelumi = 1
datalumi = 1
norm = False
draw_markers = True
vtx_channel = "VSI_LeptonsMod"

plot_classes.Hist1DRatio(hist_channels= hist_channels,

	types = samples,
    outputDir = outputDir,
    name="DV_r",
	x_title ="r_{DV}",
	x_units ="mm",
	# y_title = "Vertices (normalized)",
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
    extra_legend_lines = [vtx_channel],
	)