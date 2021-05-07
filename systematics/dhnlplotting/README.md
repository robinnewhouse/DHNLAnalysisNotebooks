# DHNL Plotting

`DHNLPlotting` is a framework for making plots. The base classes were modified from vh4b plotting framework. This framework is designed to take DHNL histograms files as an input and create plots using the histograms or micro-tuples produced by the [`DHNLNtupleAnalysis` code](https://gitlab.cern.ch/atlas-phys/exot/ueh/EXOT-2017-19/DHNLNtupleAnalysis).

## Getting Started

To clone the project: 

```
setupATLAS
lsetup git
git clone ssh://git@gitlab.cern.ch:7999/dtrischu/dhnlplotting.git
```

First you need to create a config file (e.g. config_3DVchannels.json) that contains the paths and labels for your input files (For more examples see files in configs/). Then to make plots run: 

```
cd util 
python makeRecoHistograms.py --config ../configs/config_fullrun2.json
```

The output plots will appear in DHNLPlotting/ouput/ folder. 


## Description of the Framework
This plotting framework makes use of a base class and then defines different types of plots that inherit properties from the base class. All the base class fuctionality can be found in the `plot_bas.py` in the `util/` folder. 

The "base class" contains only the objects/information that every ROOT plot would contain. Only classes derived from this should ever be initialized. For example this with included information such as `y_min`, `ymax`, whether you want a label on your plot etc. 

Then in the `plot_classes.py` folder different plotting classes are initialized. For example this include a standard 1DHistogram class `Hist1D`, as well as a class that will include a ratio insert plot for the 1D histogram called `Hist1DRatio`.

Then the steering file `makeRecoHisotgrams.py` sets up all the variables and provides the information for each plot that you want to make. An example of a histogram is copied below to demonstrate how to setup a new histogram. More examples can be found in the `makeRecoHistograms.py` file. 


```
Hist1D(hist_channels= hist_channels,  # give the list of hist channels which contains info about the vtx config,labels and file paths etc.
    types = samples, # a list of the samples you are plotting. This is used to define the plotting style (colours, markers etc.) 
    outputDir = outputDir, # where you want the plots to be saved
    name="DV_r", # name of the variable you want to plot, must be the variable name in the histograms file created by DHNLNtupleAnalysis
    x_title ="L_{xy}", 
    x_units ="mm", #  if none leave blank
    y_title = "Vertices", 
    y_min = 0.1, # y min
    x_min = 0,
    x_max = 300,
    rebin = 10,
    use_ntuple = False, # Set this option to true if you want to plot using micro-ntuples, otherwise you will plot the pre-filled histogram
    ntup_nbins =100, # number of bins to be used when plotting with micro-ntuples
    norm = norm, # normalize the histogram
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_channel,"LNC 10GeV 10mm"] # extra information you want to include on the plot
    )
```



