import os, math, ROOT, json,sys
import numpy as np
from ROOT import *
from pylab import *
import atlas_style
ROOT.gROOT.SetBatch(True)
from plot_classes import Hist1D,Hist1DRatio,Hist2D
sys.path.append('/home/dtrischuk/HNLAnalysis/DHNLNtupleAnalysis/python/')
import helpers, selections
gROOT.SetStyle("ATLAS") #might have to change how you set atlas style like this, depends how you have setup python

makeHist = False
plot = True

signal = "uuu"
f = ROOT.TFile('/data/hnl/v3_histograms/mar17_SSbkg/fullrun2_histograms_SSbkg_{}.root'.format(signal))
vtx_alg = "VSI_LeptonsMod"
selection = "DVtype"
tree = f.Get('{}_ntuples_{}'.format(vtx_alg, selection))  # get TTree
tree_offset = f.Get('{}_ntuples_{}'.format(vtx_alg, selection))  # get TTree
print "total {} entries: ".format(signal),tree.GetEntries()
nentries = tree.GetEntries()
offset = 1

h ={}
h["mDV"] = ROOT.TH1D('h_mDV', 'h_mDV', 50, 0, 50)
h["DVpt"] = ROOT.TH1D('h_DVpt', 'h_DVpt', 25, 0, 100)
h["DVeta"] = ROOT.TH1D('h_DVeta', 'h_DVeta', 100, -3, 3)
h["DVphi"] = ROOT.TH1D('h_DVphi', 'h_DVphi', 100, -4, 4)
h["plep_pt"] = ROOT.TH1D('h_plep_pt', 'h_plep_pt', 50, 0, 200)
h["plep_eta"] = ROOT.TH1D('h_plep_eta', 'h_plep_eta', 100, -3, 3)
h["plep_phi"] = ROOT.TH1D('h_plep_phi', 'h_plep_phi', 100, -4, 4)
h["Lxy"] = ROOT.TH1D('h_Lxy', 'h_Lxy', 30, 0, 300)
h["mHNL"] = ROOT.TH1D('h_mHNL', 'h_mHNL', 50, 0, 25)
h["mHNL_offset"] = ROOT.TH1D('h_mHNL_offset', 'h_mHNL_offset', 50, 0, 25)
h["mvis"] = ROOT.TH1D('h_mvis', 'h_mvis', 100, 0, 200)
h["mvis_offset"]  = ROOT.TH1D('h_mvis_offset', 'h_mvis_offset', 100, 0, 200)
h["mll_1"] = ROOT.TH1D('h_mll_1', 'h_mll_1', 100, 0, 200)
h["mll_0"] = ROOT.TH1D('h_mll_0', 'h_mll_0', 100, 0, 200)

outputDir = '../output/mHNL_shuffle_{}/'.format(signal) # change path here to save your histograms somewhere else!
if not os.path.exists(outputDir): os.mkdir(outputDir)
if not os.path.exists(outputDir + "plots/"): os.mkdir(outputDir + "plots/")
samples = ["SS_uu"]
samples = ["uuu_10G", "uue_10G"]
samples = ["SS_uu", "uuu_10G"]
ratio_samples = [ "uuu_10G","SS_uu"]
norm = True
log_scale_y = True
draw_markers= True

if signal == "uuu": 
    ch_str = "\\mu\\mu\\mu"
    y_min = 0.0001
if signal == "eee": 
    ch_str = "eee"
    y_min = 0.0001
if signal == "uue": 
    ch_str = "\\mu\\mue"
    y_min = 0.8
if signal == "eeu": 
    ch_str = "ee\\mu"
    y_min = 0.8

extra_info = "channel: {}".format(ch_str)

if makeHist: 

    for i in range(nentries):
        if i % 10000 == 0:
            print "Processing event {} / {}".format(i, nentries)
        if signal == "uuu":
            if i % 10 == 0:
                print "Processing event {} / {}".format(i, nentries)

        tree.GetEntry(i)
        # print i, i+offset

        rDV = np.sqrt(tree.DV_x**2 + tree.DV_y**2)
        dv = ROOT.TVector3( tree.DV_x, tree.DV_y ,tree.DV_z)
        pv = ROOT.TVector3(tree.PV_x,tree.PV_y,tree.PV_z)
        
        pt_0 = tree.DV_trk_0_pt
        eta_0 = tree.DV_trk_0_eta
        phi_0 = tree.DV_trk_0_phi
        pt_1 = tree.DV_trk_1_pt
        eta_1 = tree.DV_trk_1_eta
        phi_1 = tree.DV_trk_1_phi
        M = 0.139 # pion mass assumption
        
        lepVec_0 = ROOT.TLorentzVector()
        lepVec_1 = ROOT.TLorentzVector()
        lepVec_0.SetPtEtaPhiM(pt_0, eta_0, phi_0, M)
        lepVec_1.SetPtEtaPhiM(pt_1, eta_1, phi_1, M)
        DV_4vec = lepVec_0 + lepVec_1

        plep_vec = ROOT.TLorentzVector()
        plep_pt = tree.plep_pt
        plep_eta = tree.plep_eta
        plep_phi= tree.plep_phi
        plep_vec.SetPtEtaPhiM(plep_pt, plep_eta, plep_phi, M)

        elVec = [lepVec_0,lepVec_1]
        muVec = []
        Mhnl = selections.Mhnl(tree, "ee", plep=plep_vec, dMu=muVec,dEl=elVec,truth_pv=pv, truth_dv=dv,use_truth=True)
        Mlll = selections.Mlll(dv_type="ee", plep=plep_vec, dMu=muVec, dEl=elVec)
        mll_0 = lepVec_0 + plep_vec
        mll_1 = lepVec_1 + plep_vec
        # only fill histograms if DV passes some basic criteria
        if signal == "uuu": extra_cuts = tree.DV_mass > 2 and tree.DV_2loose == 1
        if signal == "eee": extra_cuts = tree.DV_mass > 2 and tree.DV_2veryveryloose == 1 and tree.DV_pass_mat_veto == 1
        if signal == "eeu": extra_cuts = tree.DV_mass > 2
        if extra_cuts:  # for eee channel
            h["mDV"].Fill(DV_4vec.M())
            h["DVpt"].Fill(DV_4vec.Pt())
            h["DVeta"].Fill(DV_4vec.Eta())
            h["DVphi"].Fill(DV_4vec.Phi())
            h["Lxy"].Fill(rDV)

            h["plep_pt"].Fill(plep_pt)
            h["plep_eta"].Fill(plep_eta)
            h["plep_phi"].Fill(plep_phi)

            h["mHNL"].Fill(Mhnl.mhnl)
            h["mvis"].Fill(Mlll.mlll)

            h["mll_1"].Fill(mll_1.M())
            h["mll_0"].Fill(mll_0.M())

            # n+ 1 offset 1-> 1 
            # if i == nentries -1: tree_offset.GetEntry(0)
            # else: tree_offset.GetEntry(i+offset)

            for j in range(nentries): 
                tree_offset.GetEntry(j)
                # if tree_offset.DV_mass > 2 and tree_offset.DV_2loose == 1:  # apply the same cuts as the DV uuu channel 
                if signal == "uuu": offset_extra_cuts = tree_offset.DV_mass > 2 and tree_offset.DV_2loose == 1
                if signal == "eee": offset_extra_cuts = tree_offset.DV_mass > 2 and tree_offset.DV_2veryveryloose == 1 and tree_offset.DV_pass_mat_veto == 1
                if signal == "eeu": offset_extra_cuts = tree_offset.DV_mass > 2

                if offset_extra_cuts:
                    plep_offset_vec = ROOT.TLorentzVector()
                    plep_offset_pt = tree_offset.plep_pt
                    plep_offset_eta = tree_offset.plep_eta
                    plep_offset_phi= tree_offset.plep_phi
                    plep_offset_vec.SetPtEtaPhiM(plep_offset_pt, plep_offset_eta, plep_offset_phi, M)

                    # print "correct: ", plep_pt, plep_eta, plep_phi
                    # print "offset: ", plep_offset_pt, plep_offset_eta, plep_offset_phi
                    

                    
                    Mhnl_offset = selections.Mhnl(tree, "ee", plep=plep_offset_vec, dMu=muVec,dEl=elVec,truth_pv=pv, truth_dv=dv,use_truth=True)
                    Mlll_offset = selections.Mlll("ee", plep=plep_offset_vec, dMu=muVec,dEl=elVec)
                    # print "recalculated mhnl: ", Mhnl.mhnl
                    # print "offset mhnl: ", Mhnl_offset.mhnl

                    h_mHNL_offset.Fill(Mhnl_offset.mhnl)
                    h_mvis_offset.Fill(Mlll_offset.mlll)
    # os.remove(outputDir+"plots/{}/".format(vtx_alg) +  "hist.root")
    file = ROOT.TFile.Open(outputDir+"plots/{}/".format(vtx_alg) +  "hist.root", 'update')
    for key in h:
        h[key].Write(key)
    file.Close

if plot: 
    pfile  = ROOT.TFile.Open(outputDir+"plots/{}/".format(vtx_alg) +  "hist.root")
    h_to_plot ={}
    for key in h:
        h_to_plot[key] = pfile.Get(key) 
    # pfile.Close()

    Hist1D(hist_channels= [],
    hists = [h_to_plot["plep_pt"]],
    labels = ["ch. {}".format(ch_str) ],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="plep_pt",
    x_title ="Prompt lepton p_{T}",
    x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 200,
    scaleLumi = 139.0,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg]
    )

    Hist1D(hist_channels= [],
    hists = [h_to_plot["plep_eta"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="plep_eta",
    x_title ="Prompt Lepton \\eta",
    x_units ="",
    y_min = y_min,
    x_min = -3,
    x_max = 3,
    ntup_nbins =100,
    scaleLumi = 139.0,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )

    Hist1D(hist_channels= [],
    hists = [h_to_plot["plep_phi"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="plep_phi",
    x_title ="Prompt Lepton \\phi",
    x_units ="",
    y_min = y_min,
    x_min = -4,
    x_max = 4,
    ntup_nbins =100,
    scaleLumi = 139.0,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )

    # Hist1D(hist_channels= [],
    # hists = [h_to_plot["mHNL"]],
    # labels = ["orig. plep"],
    # vtx_alg = vtx_alg,
    # types = samples,
    # outputDir = outputDir,
    # name="HNLm",
    # x_title ="HNL mass",
    # x_units ="GeV",
    # y_min = y_min,
    # y_max = 10e3,
    # # y_min = 0.0001,
    # x_min = 0,
    # x_max = 24,
    # rebin = 2,
    # ratio_ymin = -0.5,
    # ratio_ymax =2.5,
    # ntup_nbins= 48,
    # scaleLumi = 139.0,
    # show_overflow = False,
    # show_underflow = False,
    # norm = norm,
    # empty_scale = 2.6,
    # log_scale_y = log_scale_y,
    # draw_markers = draw_markers,
    # atlas_mod = "Internal",
    # extra_legend_lines = [vtx_alg,extra_info]
    # )

    Hist1DRatio(hist_channels= [],
    hists = [h_to_plot["mHNL_offset"],h_to_plot["mHNL"]],
    labels = ["random plep","orig. plep"],
    vtx_alg = vtx_alg,
    types = ratio_samples,
    outputDir = outputDir,
    name="HNLm",
    x_title ="HNL mass",
    x_units ="GeV",
    y_min = y_min,
    # y_min = 0.0001,
    x_min = 0,
    x_max = 24,
    rebin = 2,
    ratio_ymin =  -0.5,
    ratio_ymax =2.5,
    ntup_nbins= 48,
    scaleLumi = 139.0,
    show_overflow = False,
    show_underflow = False,
    norm = norm,
    empty_scale = 3.1,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg,extra_info]
    )

    Hist1DRatio(hist_channels= [],
    hists = [h_to_plot["mvis_offset"],h_to_plot["mvis"]],
    labels = ["random plep","orig. plep"],
    vtx_alg = vtx_alg,
    types = ratio_samples,
    outputDir = outputDir,
    name="mvis",
    x_title ="Visble mass",
    x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 200,
    ratio_ymin = -0.5,
    ratio_ymax = 2.5,
    rebin =4,
    ntup_nbins =100,
    scaleLumi = 139.0,
    show_overflow = False,
    show_underflow = False,
    norm = norm,
    empty_scale = 3.1,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg,extra_info]
    )


    Hist1D(hist_channels= [],
    hists = [h_to_plot["Lxy"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="DV_r",
    x_title ="L_{xy}",
    x_units ="mm",
    y_min = y_min,
    x_min = 0,
    x_max = 300,
    ntup_1D= True,
    ntup_nbins =60,
    scaleLumi = 139.0,
    empty_scale = 1.8,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )
        
    Hist1D(hist_channels= [],
    hists = [h_to_plot["mDV"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="DV_mass",
    x_title ="DV mass",
    x_units ="GeV",
    # y_min = y_min,
    x_min = 0,
    x_max = 50,
    ntup_nbins =0,
    scaleLumi = 139.0,
    ntup_1D = True,
    norm = norm,
    draw_cut = False,
    cut = 4,
    empty_scale = 1.8,
    hide_lumi = True,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )

    Hist1D(hist_channels= [],
    hists = [h_to_plot["mll_0"]],
    labels = ["SS bkg. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="mll_0",
    x_title ="Mass of plep + Leading p_{T} Track",
    x_units ="GeV",
    # y_min = y_min,
    x_min = 0,
    x_max = 200,
    ntup_nbins =0,
    scaleLumi = 139.0,
    ntup_1D = True,
    norm = norm,
    draw_cut = False,
    cut = 4,
    rebin = 2,
    empty_scale = 1.8,
    hide_lumi = True,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )

    Hist1D(hist_channels= [],
    hists = [h_to_plot["mll_1"]],
    labels = ["SS bkg. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="mll_1",
    x_title ="Mass of plep + Sub-leading p_{T} Track",
    x_units ="GeV",
    # y_min = y_min,
    x_min = 0,
    x_max = 200,
    ntup_nbins =0,
    scaleLumi = 139.0,
    ntup_1D = True,
    norm = norm,
    draw_cut = False,
    cut = 4,
    rebin = 2,
    empty_scale = 1.8,
    hide_lumi = True,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )



    Hist1D(hist_channels= [],
    hists = [h_to_plot["DVpt"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="DV_pt",
    x_title ="DV p_{T}",
    x_units ="GeV",
    y_min = y_min,
    x_min = 0,
    x_max = 100,
    ntup_nbins =100,
    scaleLumi = 139.0,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )


    Hist1D(hist_channels= [],
    hists = [h_to_plot["DVeta"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="DV_eta",
    x_title ="DV \\eta",
    x_units ="",
    y_min = y_min,
    x_min = -3,
    x_max = 3,
    ntup_nbins =100,
    scaleLumi = 139.0,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )


    Hist1D(hist_channels= [],
    hists = [h_to_plot["DVphi"]],
    labels = ["ch. {}".format(ch_str)],
    vtx_alg = vtx_alg,
    types = samples,
    outputDir = outputDir,
    name="DV_phi",
    x_title ="DV \\phi",
    x_units ="",
    y_min = y_min,
    x_min = -4,
    x_max = 4,
    ntup_nbins =100,
    scaleLumi = 139.0,
    norm = norm,
    log_scale_y = log_scale_y,
    draw_markers = draw_markers,
    atlas_mod = "Internal",
    extra_legend_lines = [vtx_alg ]
    )
