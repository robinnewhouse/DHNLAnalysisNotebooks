from ROOT import *
from math import *
import array as arr
import os
import random
import string

def format_for_drawing(histo, hist_type = "data"):

    color_dict  = {

      # "uuu_10mm" : TColor().GetColor("#01C0E0"), # purple
      "uuu_10mm" : TColor().GetColor("#86259B"), # purple
      "uuu_10G" : TColor().GetColor("#86259B"), # purple
      "uuu_5G" : TColor().GetColor("#86259B"), # purple
      "uuu_15G" : TColor().GetColor("#86259B"), # purple
      "OS_uu" : TColor().GetColor("#86259B"), # purple
      "OS_uu_passmat" : TColor().GetColor("#86259B"), # purple
      "OS_uu_2med" : TColor().GetColor("#AE2ED9"), # purple
      "uuu_1mm" : TColor().GetColor("#AE2ED9"), 
      "cutflow_uuu" : TColor().GetColor("#86259B"), # purple
      "SS_uuu" : TColor().GetColor("#848484"), # gray
      "SS_uu" : TColor().GetColor("#848484"), # gray
      # "SS_uuu" : TColor().GetColor("#86259B"), # purple
      "uu_2loose" : TColor().GetColor("#86259B"), # purple
      "uu_2med" :TColor().GetColor("#86259B"), # purple

      "eee_10mm" : TColor().GetColor("#01C0E0"), # blue
      "eee_10G" : TColor().GetColor("#01C0E0"), # blue
      "eee_5G" : TColor().GetColor("#01C0E0"), # blue
      "eee_15G" : TColor().GetColor("#01C0E0"), # blue
      # "eee_10mm" : TColor().GetColor("#00AC42"), # green
      "OS_ee" : TColor().GetColor("#01C0E0"), # blue
      "OS_ee_passmat" : TColor().GetColor("#01C0E0"), # blue

      # "OS_ee" : kBlack, # blue
      # "OS_ee_passmat" : kBlack, # blue


      "OS_ee_2vvl" : TColor().GetColor("#A0E2FF"), # blue
      "eee_1mm" : TColor().GetColor("#A0E2FF"), # blue
      "cutflow_eee" : TColor().GetColor("#01C0E0"), # blue
      "SS_eee" : TColor().GetColor("#848484"), # gray
      "SS_ee" : TColor().GetColor("#848484"), # gray
      # "SS_eee" : TColor().GetColor("#01C0E0"), # blue
      "ee_2loose" : TColor().GetColor("#01C0E0"), # blue
      "ee_2vvl" :TColor().GetColor("#01C0E0"), # blue

      "uue_10mm" : TColor().GetColor("#CC0063"), # pink
      "uue_10G" : TColor().GetColor("#CC0063"), # pink
      "uue_5G" : TColor().GetColor("#CC0063"), # pink
      "uue_15G" : TColor().GetColor("#CC0063"), # pink
      "OS_eu" : TColor().GetColor("#CC0063"), # pink
      "OS_eu_passmat" : TColor().GetColor("#CC0063"), # blue
      "OS_eu_med-vvl" : TColor().GetColor("#F7007A"), # pink
      "uue_1mm" : TColor().GetColor("#F7007A"), # pink
      
      "cutflow_uue" : TColor().GetColor("#CC0063"), # pink
      "SS_uue" : TColor().GetColor("#848484"), # gray
      "SS_eu" : TColor().GetColor("#848484"), # gray
      #  "SS_uue" : TColor().GetColor("#CC0063"), # pink
      "emu_med_vvl" :TColor().GetColor("#CC0063"), # pink

      "eeu_10mm" : TColor().GetColor("#FE9603"), # orange
      "eeu_10G" : TColor().GetColor("#FE9603"), # orange
      "eeu_5G" : TColor().GetColor("#FE9603"), # orange
      "eeu_15G" : TColor().GetColor("#FE9603"), # orange
      "eeu_1mm" : TColor().GetColor("#FFC402"), # orange
      "cutflow_eeu" : TColor().GetColor("#FE9603"), # orange
      "SS_eeu" : TColor().GetColor("#848484"), # gray
      # "SS_eeu" : TColor().GetColor("#FE9603"), # orange
        #51E5FF
      "ttbar" : TColor().GetColor("#01C0E0"), # blue
        #F86624 orange


      "uuu_100mm" : TColor().GetColor("#00AC42"), #green
      "uuu_1mm" : TColor().GetColor("#F9C80E"), #yellow

      "shuffling_ee" : TColor().GetColor("#01C0E0"),
      "fullrun2_ee" : TColor().GetColor("#848484"), # grey

      "shuffling_eu" : TColor().GetColor("#CC0063"),
      "fullrun2_eu" : TColor().GetColor("#848484"), # grey
    
      "data":kBlack, 

   
      
      #palette 1
      # F9C80E,  yellow
      # F86624, orange
      # EA3546,  red
      # #,43BCCD, teal
      # 662E9B purple

      #palette 2
      # 8962E4 purple
      # 8448AD dark purple
      # 48A9A6  teal
      # FC6322 orange
      # EF2E78 pink
    
      # palette 3
      
      # 86259B purple
      # CC0063 pink 
      # FE9603 orange
      # 01C0E0 light blue
      # 00B796 teal 
     #  00AC42 green
    }
    marker_dict  = {

      "eee_100mm":20, # circle full
      "uuu_100mm":22, # triangle full
      "uue_100mm": 23,# upside down triangle full
      "eeu_100mm": 21, # square full

      "uuu_10G":22, # triangle full
      "uuu_5G": 23,# upside down triangle full
      "uuu_15G": 21, # square full

      "eee_10G":22, # triangle full
      "eee_5G": 23,# upside down triangle full
      "eee_15G": 21, # square full

      "eeu_10G":22, # triangle full
      "eeu_5G": 23,# upside down triangle full
      "eeu_15G": 21, # square full

      "uue_10G":22, # triangle full
      "uue_5G": 23,# upside down triangle full
      "uue_15G": 21, # square full

      "eee_10mm":20, # circle full
      "uuu_10mm":22, # triangle full
      "uue_10mm": 23,# upside down triangle full
      "eeu_10mm": 21, # square full

      "eee_1mm":21, # # square full circle full
      "uuu_1mm":20, # circle full triangle full
      "uue_1mm": 22,# triangle full 
      "eeu_1mm": 23, # upside down triangle full

      "eee_1mm":20, # circle full
      "uuu_1mm":21, # triangle full
      "uue_1mm": 21,# upside down triangle full
      "eeu_1mm": 21, # square full

      "SS_eee":20, # circle full
      "SS_uuu":20, # tcircle full
      "SS_uue": 20,# circle full
      "SS_eeu": 20, # circle full

      "SS_ee":20, # circle full
      "SS_uu":20, # circle full
      "SS_eu": 20,# circle full

      "shuffling_ee" : 20,
      "fullrun2_ee" : 20,
      "shuffling_eu" : 20,
      "fullrun2_eu" : 20,

      "OS_ee":21, # square full
      "OS_uu":21, # square full
      "OS_eu": 21,# square full

      "OS_ee_2vvl":22, # triangle full
      "OS_uu_2med":22, # triangle full
      "OS_eu_med-vvl": 22,# triangle full

      "OS_ee_passmat": 24, # open circle
      "OS_eu_passmat": 24, # open circle
      "OS_uu_passmat": 24, # open circle



      "cutflow_eee":20, # circle full
      "cutflow_uuu":22, # triangle full
      "cutflow_uue": 23,# upside down triangle full
      "cutflow_eeu": 21, # square full
      
      "data":20, 
      "ttbar":23, 
    }
    histo.SetMarkerColor( color_dict[hist_type] )
    histo.SetMarkerStyle( marker_dict[hist_type] )
    histo.SetMarkerSize( 1.2 )
    # if hist_type == "uuu_10mm":
    #   histo.SetFillColor( color_dict[hist_type] )
    histo.SetLineColor( color_dict[hist_type] )
    if "cutflow" in hist_type:
      histo.SetFillColor( color_dict[hist_type] )
    if "_5G" in hist_type:
      histo.SetLineStyle( 2 )
    if "_15G" in hist_type:
      histo.SetLineStyle( 3 )

    histo.SetLineWidth(2)
    histo.GetXaxis().SetTitleOffset(1.2)
    histo.GetYaxis().SetTitleOffset(1.2)
    histo.GetXaxis().SetTitleSize(.05)
    histo.GetYaxis().SetTitleSize(.05)
    histo.GetXaxis().SetLabelSize(.05)
    histo.GetYaxis().SetLabelSize(.05)
    histo.GetXaxis().SetLabelOffset(0.01)

def scale_hist(histo, scaleLumi,dataLumi, hist_type = "data"):
    if hist_type == "OS_eu_med-vvl":  hist_type = "OS_eu"
    if hist_type == "OS_ee_2vvl":  hist_type = "OS_ee"
    if hist_type == "OS_uu_2med":  hist_type = "OS_uu"
    if hist_type == "OS_eu_passmat":  hist_type = "OS_eu"
    if hist_type == "OS_ee_passmat":  hist_type = "OS_ee"
    if hist_type == "OS_uu_passmat":  hist_type = "OS_uu"

    
    scale_dict  = {
      "HNL_10G_1mm": "HNLmc", 
      "HNL_10G_10mm": "HNLmc",
      "HNL_10G_100mm": "HNLmc",
      "LNV": "HNLmc",
      "LNC": "HNLmc",
      "uuu_10mm": "HNLmc",
      "eee_10mm": "HNLmc",
      "uue_10mm": "HNLmc",
      "eeu_10mm": "HNLmc",
      "uuu_100mm": "HNLmc",
      "eee_100mm": "HNLmc",
      "uue_100mm": "HNLmc",
      "eeu_100mm": "HNLmc",
      "uuu_1mm": "HNLmc",
      "eee_1mm": "HNLmc",
      "uue_1mm": "HNLmc",
      "eeu_1mm": "HNLmc",
      "uu_2med": "HNLmc",
      "uu_2loose": "HNLmc",
      "emu": "HNLmc",
      "emu_med_vvl": "HNLmc",
      "ee": "HNLmc",
      "ee_2vvl": "HNLmc",
      "data":"data", 
      "SS_uuu": "data",
      "SS_uue": "data",
      "SS_eee": "data",
      "SS_eeu": "data",
      "SS_eee_medpel" : "data",
      "SS_uu": "data",
      "SS_ee": "data",
      "SS_eu": "data",
      "OS_uu": "data",
      "OS_ee": "data",
      "OS_eu": "data",
      "shuffling_ee" : "data",
      "fullrun2_ee" : "data",
      "shuffling_eu" : "data",
      "fullrun2_eu" : "data",

      "ttbar" : "ttbar"
    }


    if scale_dict[hist_type] == "HNLmc": # scale HNL MC to given luminosity
      histo.Scale( scaleLumi )


    if scale_dict[hist_type] == "data":  # scale data histogram to 
      if hist_type == "SS_uuu": lumi = 57.91
      if hist_type == "SS_uue": lumi = 57.99
      if hist_type == "SS_eeu": lumi = 49.98
      if hist_type == "SS_eee": lumi = 57.79 # nov 3
      if hist_type == "SS_eee": lumi = 58.55 # nov 12

      # if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 58.49 # nov10 CR
      # if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 58.49 # nov10 CR

      # if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 59.01 # nov11 CR
      # if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 59.01 # nov11 CR

      # if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 59.48 # dec1 CR
      # if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 59.48 # dec1 CR

      # if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 56.97 # dec8 CR with matveto
      # if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 56.97 # dec8 CR with matveto

      # if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 52.17# jan16 CR with p perp and parallel
      # if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 52.17 # jan16 CR with p perp and parallel

      # if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 58.26 # jan28 CR prompt track selection
      # if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 58.26 # jan28 CR prompt track selection

      if (hist_type == "SS_uu" or hist_type == "SS_ee" or hist_type == "SS_eu"): lumi = 57.8 # feb3 CR prompt track selection
      if (hist_type == "OS_uu" or hist_type == "OS_ee" or hist_type == "OS_eu"): lumi = 57.8 # feb3 CR prompt track selection

      if hist_type == "shuffling_ee": lumi = 0.69 # shuffled lumi
      if hist_type == "fullrun2_ee": lumi = 139 # shuffled lumi
      if hist_type == "shuffling_eu": lumi = 0.69 # shuffled lumi
      if hist_type == "fullrun2_eu": lumi = 139 # shuffled lumi

      # if hist_type == "SS_eee": lumi = 58.63 # medpel
      scale_data = scaleLumi / lumi
      # scale_data = scaleLumi / dataLumi
      histo.Scale(scale_data)


def get_yield(h,name): 
    # if name == "HNLm": 
    #   # print name
    #   # only calculate yield up to 22 GeV
    #   binx_max = h.GetXaxis().FindBin(25)
    #   Yield=round(h.Integral(h.FindFirstBinAbove(0,1), binx_max),2)
    #   total_Yield=round(h.Integral(h.FindFirstBinAbove(0,1), -1),2)
    #   print Yield,  total_Yield
    # else: 
    # Yield=round(h.Integral(h.FindFirstBinAbove(0,1), -1),0) # only work if not underflow?? -DT 
    Yield=round(h.Integral(-1, -1),0)
  
    return Yield

def format_simple_pad(pad):
    pad.SetPad(0.0, 0.0, 1., 1.)
    pad.SetTopMargin(0.065)
    pad.SetRightMargin(0.04)
    pad.SetLeftMargin(0.13)
    pad.SetBottomMargin(0.13)
    pad.SetBorderSize(0)
    pad.SetGridy(0)
    pad.SetBorderSize(0)

def format_simple_pad_2D(pad):
    pad.SetPad(0.0, 0.0, 1., 1.)
    pad.SetTopMargin(0.0675)
    pad.SetRightMargin(0.14)
    pad.SetLeftMargin(0.13)
    pad.SetBottomMargin(0.15)
    pad.SetBorderSize(0)
    pad.SetGridy(0)
    pad.SetBorderSize(0)

def format_2pads_for_ratio(c):
    c.Divide(1,1)
    c.cd(1)
    pad1 = TPad("pad1", "pad1", 0, 0.25, 1., 1.0)
    pad1.SetTopMargin(0.065)
    pad1.SetRightMargin(0.04)
    pad1.SetLeftMargin(0.13)
    pad1.SetBottomMargin(0.02)
    pad1.SetBorderSize(0)
    pad1.SetGridy(0)
    pad1.SetBorderSize(0)
    
    pad2 = TPad("pad2", "pad2", 0, 0.0, 1, 0.25)
    pad2.SetTopMargin(0.01)
    pad2.SetRightMargin(0.04)
    pad2.SetLeftMargin(0.13)
    pad2.SetBottomMargin(0.4)
    pad2.SetFillColorAlpha(0, 0.)
    pad2.SetBorderSize(0)
    pad2.SetGridy(0)
    pad2.SetBorderSize(0)

    return pad1, pad2

def draw_hists(hlist, options, types):
    assert(len(hlist) > 0)

    hlist[0].Draw(options)
    if "hist" in options.lower():
        hlist[0].Draw("hist same")

    for i in range(len(hlist)):
        hlist[i].Draw(options + ",same")
        if "hist" in options.lower() and types[i] != "data":
            hlist[i].Draw("hist same")


