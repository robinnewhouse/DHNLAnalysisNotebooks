import uproot
import uproot_methods
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import glob
from IPython.display import Image, display

# Set SNS dislay settings
sns.set(
    context='notebook',
    style='darkgrid',
    palette='cool',
    font_scale=2,
    color_codes=False,
    rc=None,
)


# these dataframes have been pre-produced using kshort_selection.py
print("Loading dataframes")
# Read MC dataframes
df = pd.read_pickle('/data/hnl/KShort/ntuples/dijet_mc16e/output.pkl')
# read data dataframes
df_data = pd.read_pickle('/data/hnl/KShort/ntuples/data_output.pkl')
print("Dataframes loaded")


print("Selecting vertices in kshort mass window")
df = df.query('secVtx_VSI_LRTR3_1p0_mass < .4977 + .01 & \
               secVtx_VSI_LRTR3_1p0_mass > .4977 - .01 ')
df_data = df_data.query('secVtx_VSI_LRTR3_1p0_mass < .4977 + .01 & \
                         secVtx_VSI_LRTR3_1p0_mass > .4977 - .01 ')


# Define pt bins
pt_bins = [2, 4, 6, 8, 10, 15, 20, 25, 30, 35, np.inf] # Good compromise.
bin_pairs = list(zip(pt_bins, pt_bins[1:] + pt_bins[:1]))[:-1]
# Define dvr bins
dvr_bins = [0, 24, 44, 64, 84, 104, 124, 144, 164, 184, 204, 224, 244, 264, 284, 300]


# Plotting histograms using ROOT for easier histogram division

import ROOT
from array import array
ROOT.gROOT.SetStyle('ATLAS')
import time
import matplotlib.pyplot as plt
import itertools

FONT_SIZE = 0.05
def draw_note(x, y, text, size=.05, font=42):
    l = ROOT.TLatex()
    l.SetTextColor(1)
    l.SetTextFont(font)
    l.SetTextSize(size)
    l.SetNDC()
    l.DrawLatex(x, y, text)

def atlas_label(x, y, text=None, color=1):
    draw_note(x, y, r"#bf{#it{ATLAS}} " + text)

def divide0(n, d):
    return n / d if d else 0

def get_markers():
    return itertools.cycle([22,21,33,29,30,31,32,34,35])

def get_colors():
    return itertools.cycle([ROOT.kBlack, 
                            ROOT.kAzure+6, 
                            ROOT.kViolet+8, 
                            ROOT.kRed, 
                            ROOT.kGreen+1, 
                            ROOT.kOrange -3])


def make_root_hist(pt_bin, pt_idx):
    hist_colors = get_colors()
    hist_markers = get_markers()
    
    bin_string = "{}_{}".format(pt_bin[0], pt_bin[1]).replace('.', 'p')
    print('processing', bin_string)
    pt_query = f'secVtx_VSI_LRTR3_1p0_pt >= {pt_bin[0]} & secVtx_VSI_LRTR3_1p0_pt < {pt_bin[1]}'
    entries_data, edges_data = np.histogram(
#                                         df
                                        df_data
                                        .query(pt_query)
                                        .secVtx_VSI_LRTR3_1p0_r, bins=dvr_bins)
    entries_mc, edges_mc = np.histogram(
                                        df
                                        .query(pt_query)
                                        .secVtx_VSI_LRTR3_1p0_r, bins=dvr_bins)

    
    
#     bin_string = 'all'
    # Prepare canvas
    c = None
    c = ROOT.TCanvas("c", "", int(1200), int(800))

    # Upper plot will be in pad1
    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0.02);  # Upper and lower plot are not joined
    # pad1.SetGridx();           # Vertical grid
    pad1.Draw()                  # Draw the upper pad: pad1
 
    # lower plot will be in pad 2
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.4)
    # pad2.SetGridx() # vertical grid
    pad2.SetGridy() # horizontal grid
    pad2.Draw('goff')

    #########################
    # Main plot
    #########################
    pad1.cd() # pad1 becomes the current pad
    
    
    # Define histograms
    rdv = {'data': ROOT.TH1D('rdv_data'+bin_string,'Displaced Vertex Radius', len(dvr_bins)-1, array('d', dvr_bins)),
           'mc': ROOT.TH1D('rdv_mc'+bin_string,'Displaced Vertex Radius', len(dvr_bins)-1, array('d', dvr_bins))}

    for i, (val, edge) in enumerate(zip(entries_data, edges_data)):
        rdv['data'].SetBinContent(i+1,val)
    
    for i, (val, edge) in enumerate(zip(entries_mc, edges_mc)):
        rdv['mc'].SetBinContent(i+1,val)
                
    # Set draw properties
    for h in rdv.values():
        # Histogram properties
        h.SetMarkerSize(1.5)
        h.SetLineWidth(int(3))
        hcolor = next(hist_colors)
        h.SetLineColor(hcolor)
        h.SetMarkerColor(hcolor)
        hmarker = next(hist_markers)
        h.SetMarkerStyle(hmarker)
        # X axis
        x_ax = h.GetXaxis()
        x_ax.SetTitle("Displaced vertex radius [mm]")
        x_ax.SetLabelSize(0)
        x_ax.SetTitle('DV_r')
        # Y axis
        y_ax = h.GetYaxis()
        y_ax.SetTitle("Vertices (normalized to first bin)")
        y_ax.SetMaxDigits(6);
        y_ax.SetTitleOffset(1.0)
        y_ax.SetRangeUser(0,1);
        y_ax.SetLabelFont(42)
        y_ax.SetLabelSize(FONT_SIZE);   
        y_ax.SetTitleFont(42)
        y_ax.SetTitleSize(FONT_SIZE*1.2)

    for h in rdv.values():
        # Normalize the histograms to unity
        scale = divide0(1, h.Integral())
        h.Scale(scale)
        
        
        
    # Normalize to the first bin
    # We do this assuming that the vertices closest to the interaction point 
    # are most reliable between data and MC
    first_bin_ratio = divide0( # safe divide
        rdv['data'].GetBinContent(1), # bin 0 is underflow
        rdv['mc'].GetBinContent(1)) 
    rdv['mc'].Scale(first_bin_ratio)

    # Draw the histograms
    rdv['mc'].Draw('E0 HIST SAME')
    rdv['data'].Draw('E0 HIST SAME')
    
    
        
    # format legend
    x = 0.6
    y = 0.7
    dy = .07
    leg = ROOT.TLegend(x, y, x+.3, y+0.2)
    leg.SetTextSize(0.05)
    leg.SetBorderSize(0)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetShadowColor(ROOT.kWhite)
    leg.AddEntry(rdv['data'], 'Data', "lp")
    leg.AddEntry(rdv['mc'], 'Dijet JZXW', "lp")
    leg.Draw("SAME")
    draw_note(x, y-dy, f'Vertexing: {vtx_alg_string}')
    draw_note(x, y-2*dy, f'p_{{T}} bin: [{pt_bin[0]}, {pt_bin[1]}] GeV')
    draw_note(x, y-3*dy, 'Selected K_{S}^{0}')
    atlas_label(x-.2,y+dy, 'Internal')
    

    #########################
    # Ratio plot
    #########################
    pad2.cd() # pad2 becomes the current pad
    
    hist_markers = get_markers()
    hist_colors = get_colors()
    hmarker = next(hist_markers)
    hcolor = next(hist_colors)
    # Define the ratio plot
    h3 = rdv['data'].Clone('h3');
    h3.SetLineColor(hcolor);
    h3.SetMarkerSize(1.5)
    h3.SetLineWidth(int(3))
    h3.SetMarkerColor(hcolor)
    h3.SetMarkerStyle(hmarker);
    h3.SetMinimum(0.3);  # Define Y ..
    h3.SetMaximum(1.7); # .. range
    # h3.Sumw2();
    # h3.SetStats(0);      # No statistics on lower plot
    h3.Divide(rdv['mc']); # This takes in to account uncertainties in both MC and data histogrmas
    # TODO could make a clone of the MC histogram with 0 uncertainties (setbinerror 0)
    max_bin_content = h3.GetBinContent(h3.GetMaximumBin())
    min_bin_content = h3.GetBinContent(h3.GetMinimumBin())
    # h3.SetMaximum(1.4 if max_bin_content > 1.3 else max_bin_content + .1);
    # h3.SetMinimum(min_bin_content - .1);
    hline = ROOT.TLine(h3.GetBinCenter(h3.FindFirstBinAbove()), 1, h3.GetBinCenter(h3.FindLastBinAbove()), 1)
    hline.SetLineColor(next(hist_colors))
    pad2.SetFillStyle(0)
    h3.Draw() # Draw the axes 
    hline.Draw("same")
    h3.Draw("hist same") # Draw the ratio plot 
    h3.Draw("e same") # Draw the ratio plot errors

    # Y axis ratio plot settings
    h3.GetYaxis().SetTitle("ratio #frac{data}{mc}")
    h3.GetYaxis().SetNdivisions(505)
    h3.GetYaxis().SetTitleSize(FONT_SIZE*4)
    h3.GetYaxis().SetTitleFont(42)
    h3.GetYaxis().SetTitleOffset(0.3)
    h3.GetYaxis().SetLabelFont(42) 
    h3.GetYaxis().SetLabelSize(FONT_SIZE*3)
    # X axis ratio plot settings
    h3.GetXaxis().SetTitle("Displaced vertex radius [mm]")
    h3.GetXaxis().SetTitleSize(FONT_SIZE*4);
    h3.GetXaxis().SetTitleFont(42);
    h3.GetXaxis().SetTitleOffset(0.9);
    h3.GetXaxis().SetLabelFont(42); 
    h3.GetXaxis().SetLabelSize(FONT_SIZE*3);  


    c.Draw()
    c.SaveAs(f'{output_dir}vertex_comparison_{bin_string}.png')    
    display(Image(f'{output_dir}vertex_comparison_{bin_string}.png'))
    print(f'{output_dir}vertex_comparison_{bin_string}.png')

    
    # fill 2d plot
    dv_r_2d_bins = []
    for r_idx in range(1, h3.GetNbinsX()+1):
        dv_r_2d_bins.append(h3.GetBinContent(r_idx)) 
        # h2d.SetBinContent(r_idx, pt_idx, h3.GetBinContent(r_idx))
    dv_r_pt_2d_bins.append(dv_r_2d_bins)

# global_h3 = 0
# set up 2d plot
# pt_bins = [2, 2.5, 3, 4, 6, 8, 10, np.inf] # old paper bins. too low.
pt_bins = [2, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50, np.inf] # What we want, but not really enough stats.
# pt_bins = [2, 3, 5] # testing

dvr_bins = [0, 24, 44, 64, 84, 104, 124, 144, 164, 184, 204, 224, 244, 264, 284, 300]
dvr_bins = [0,         64, 84, 104, 124, 144, 164, 184, 204, 224, 244, 264, 284, 300]
dvr_bins_lowpt  = [0,         44, 84, 104, 124, 144, 164, 184, 204, 224, 244, 264, 284, 300]
dvr_bins_highpt = [0,             84, 104, 124, 144, 164, 184, 204, 224, 244, 264, 284, 300]

vtx_alg_string = 'VSI_LRTR3_1p0'
output_dir = "/data/hnl/KShort/plots/"


# Set up 2d plot
dv_r_pt_2d_bins = []


for i, pt_bin in enumerate(zip(pt_bins, pt_bins[1:]), start=1):
    if pt_bin[1] >= 25:
        dvr_bins = dvr_bins_highpt
    else:
        dvr_bins = dvr_bins_lowpt

    make_root_hist(pt_bin, i)






# hi
print("hi")

