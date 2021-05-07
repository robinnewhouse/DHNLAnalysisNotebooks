from ROOT import *
import atlas_style

import os
import math
import numpy as np
from sys import argv, exit

from plot_base import *
from plot_util import format_for_drawing, format_simple_pad, format_simple_pad_2D, draw_hists, format_2pads_for_ratio, scale_hist,get_yield

gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0)
gStyle.SetLineWidth(2)


class Hist1D(PlotBase):
		def __init__(self, hist_channels, types, output_dir = "../output", draw_yield=True, HNLscale = False, draw_markers = True, y_axis_type = "Vertices", title="Vertex Types",extra_cuts="", hists = None,labels =None, vtx_alg="VSI_LeptonsMod", *args, **kwargs):

				super(Hist1D, self).__init__(
								legend_loc = [0.58,0.69,0.92, 0.89],
								# legend_loc = [0.52,0.71,0.92, 0.92],
								atlas_loc = [0.17,0.875],
								extra_lines_loc = [0.17,0.775],
								*args,
								**kwargs)
				self.ntup_1D = True
				if hists != None: # just send histograms from an input list of histograms
					self.histograms = hists
					self.labels = labels
					self.vtx_alg = [vtx_alg]
				else: # use custom HNL specific code to get histograms from DHNLNtuple analysis histogram output
					get_hist = self.get_hists(hist_channels,self.name,extra_cuts=extra_cuts)
					if not get_hist: 
						raise ValueError('Cant find histograms. Exiting.')

				legends = self.labels
				self.hists = self.histograms

				x_max = -1
				y_min = 10000000
				y_max = -1

				fits = []
				if self.norm ==True: draw_yield=False
				yields = []
				for h, t in zip(self.hists, types):
						if (self.rebin != None and self.use_ntuple == False):
								h.Rebin(self.rebin)
						if(self.norm == True):
								h.Scale(1.0/h.Integral())
						else:
							if HNLscale: 
								scale_hist(h,self.scaleLumi,self.dataLumi,t)
						
						if draw_yield: 
							Yield = get_yield(h,self.name)
							yields.append(Yield)
							yield_stat_error = round(h.GetBinError(1),0)
							if draw_markers:
								self.leg.AddEntry(h, legends[ self.hists.index(h)  ] +", {} ".format(int(Yield)) , 'lp')
								# self.leg.AddEntry(h, legends[ self.hists.index(h)  ] +" {} \\pm {}".format(int(Yield), int(yield_stat_error)) , 'lp')	
							else:
								self.leg.AddEntry(h, legends[ self.hists.index(h)  ]+", {}".format(Yield) , 'l')
								# self.leg.AddEntry(h, legends[ self.hists.index(h)  ]+" {} \\pm {}".format(Yield, yield_stat_error) , 'l')
						else: 
							if not self.ntup_2D:
								if draw_markers:
									self.leg.AddEntry(h, legends[ self.hists.index(h)  ], 'lp')
								else:
									self.leg.AddEntry(h, legends[ self.hists.index(h)  ], 'l')
						if self.name == "truth_DV_r": 
							res = h.Fit("expo","S")
							# print res.GetParameter(0)

						self.set_x_axis_bounds(h)
						self.set_y_min(h)
						self.set_y_max(h)
						self.set_titles(h, y_axis_type)
						format_for_drawing(h, t)
						h.GetYaxis().SetMaxDigits(3)

				self.x_max = x_max
				self.pad_empty_space(self.hists)
			 
				pad1 = self.canvas.cd(1)
				format_simple_pad(pad1)
				pad1.cd()
				if (self.log_scale_y):
						pad1.SetLogy()
				if (self.log_scale_x):
						pad1.SetLogx()

				if draw_markers:
					draw_hists(self.hists, "PE hist", types)
				else:
					draw_hists(self.hists, "hist", types)

				# s/ sqrtb text if only plotting signal and data
				# sig_text = TLatex()
				# sig_text.SetNDC()
				# sig_text.SetLineWidth(2)
				# sig_text.SetTextSize(0.045 * self.tex_size_mod)	
				# sig_text.SetTextFont(42)
				# sig = str(round(yields[1] / np.sqrt(yields[0] ) , 2))
				# sig_text.DrawLatex(0.17, 0.66, "s/#sqrt{b}=" + sig)
	
	
			
				if "_r" in self.name or "_alpha" in self.name:
					self.draw_material_layers()
				if "trk_d0" in self.name:
					line = TLine()
					line.SetLineColor(kBlack)
					line.SetLineWidth(2)
					line.SetLineStyle(3)
					cut = 2.0
					line.DrawLine(cut,0,cut,self.y_max * 1.0/self.empty_scale) if not self.norm else line.DrawLine(cut,0,cut,0.3)
					line.DrawLine(-1*cut,0,-1*cut,self.y_max * 1.0/self.empty_scale) if not self.norm else line.DrawLine(-1*cut,0,-1*cut,0.3	)

			
				if self.draw_cut:
						line = TLine()
						line.SetLineColor(kRed)
						line.SetLineWidth(2)
						line.SetLineStyle(2)
						cut = self.cut
						# line.DrawLine(cut,0,cut,self.hist_y_max) if not self.norm else line.DrawLine(cut,0,cut,1.0)
						arrow = TArrow(cut,self.hist_y_max, cut*1.2, self.hist_y_max) if not self.norm else TArrow(cut,1.0,cut + 0.1*(self.x_max), 1.0,0.02,"|>")
						arrow.SetLineWidth(2)
						arrow.SetLineStyle(1)
						arrow.SetLineColor(kRed)
						arrow.SetFillColor(kRed)
						arrow.Draw()
					#  self.draw_cut_line()

				self.print_to_file(output_dir, self.name + ".pdf")
				pad1.Close()
				self.canvas.Close()

		def draw_cut_line(self):
				line = TLine()
				line.SetLineColor(kRed)
				line.SetLineWidth(2)
				line.SetLineStyle(2)
				cut = self.cut
				# line.DrawLine(cut,0,cut,self.y_max * 1.0/self.empty_scale) if not self.norm else line.DrawLine(cut,0,cut,1.0)
				line.DrawLine(cut,0,cut,self.hist_y_max ) if not self.norm else line.DrawLine(cut,0,cut,1.0)
				
				# arrow = TArrow(cut,self.hist_y_max, cut*1.5, self.hist_y_max) if not self.norm else TArrow(cut,1.0,cut + 0.1*(self.x_max), 1.0,0.02,"|>")
				arrow = TArrow(cut,self.y_max*1.0/self.empty_scale, cut*1.5, self.y_max*1.0/self.empty_scale) if not self.norm else TArrow(cut,1.0,cut + 0.1*(self.x_max), 1.0,0.02,"|>")
				arrow.SetLineWidth(2)
				arrow.SetLineStyle(1)
				arrow.SetLineColor(kRed)
				arrow.SetFillColor(kRed)
				arrow.Draw()

		def draw_material_layers(self):
				coords = [33.5,50.5,88.5,122.5,299.0]
				for coord in coords:
						line = TLine()
						# line.SetLineColor(14) # grey
						line.SetLineColor(kRed)
						line.SetLineWidth(2)
						line.SetLineStyle(2)
						
						if self.ntup_2D: 
							line.DrawLine(coord,0,coord,7 )
						else: 
							# line.DrawLine(coord,0,coord,self.y_max * 1.2/self.empty_scale)
							line.DrawLine(coord,0,coord,self.hist_y_max)
							# line.DrawLine(coord,0,coord, self.ymax)
						if(coords.index(coord) == 0):
								self.leg.AddEntry(line, "Material Layers", "l")




class Hist1DRatio(PlotBase):
		def __init__(self, hist_channels, types, ratio_ymin=.9, ratio_ymax = 1.1,draw_yield=False, HNLscale = False,  draw_markers = True, output_dir = "../output", y_axis_type = "Vertices",extra_cuts="", hists = None,labels =None, vtx_alg="VSI_LeptonsMod", 
					 ymin=0, **kwargs):

				super(Hist1DRatio, self).__init__(
								# legend_loc = [0.62,0.71,0.92, 0.92],
								legend_loc = [0.52,0.71,0.92, 0.92],
								atlas_loc = [0.17,0.875],
								extra_lines_loc = [0.17,0.775],
								**kwargs)

				self.ntup_1D = True
				if hists != None:  # just send histograms from an input list of histograms
					self.histograms = hists
					self.labels = labels
					self.vtx_alg = [vtx_alg]
				else: # use custom HNL specific code to get histograms from DHNLNtuple analysis histogram output
					get_hist = self.get_hists(hist_channels,self.name,extra_cuts=extra_cuts)
					if not get_hist: 
						raise ValueError('Cant find histograms exiting.')


				legends = self.labels
				self.hists = self.histograms
				if len(self.hists) != 2: 
					raise ValueError('Only give the ratio class 2 inputs. Use Hist1D class instead for n>2 histograms.')
				
				num = self.hists[0]
				denom = self.hists[1]

				y_min = 10000000
				y_max = -1
				yields = []
				for h, t in zip(self.hists, types):
						if (self.rebin != None):
								h.Rebin(self.rebin)
						if(self.norm == True):
							h.Scale(1.0/h.Integral())
						elif HNLscale == True:
							scale_hist(h,self.scaleLumi,self.dataLumi,t)
						
						Yield = get_yield(h,self.name)
						yields.append(Yield)
				
						self.set_x_axis_bounds(h)
						self.set_y_min(h)
						self.set_y_max(h)
						self.set_titles(h, y_axis_type)
						format_for_drawing(h, t)
						h.GetYaxis().SetMaxDigits(3)

				self.pad_empty_space(self.hists)


				ratio = num.Clone("ratio")
				
				ratio.Divide(denom)
				ratio.Sumw2()
				# ratio.GetYaxis().SetTitle("Data/MC")
				ratio.GetYaxis().SetTitle("ratio")
				ratio.SetMarkerColor(kBlack)
				ratio.SetLineColor(kBlack)


				ratio.SetMarkerColor(kBlack)
				ratio.SetLineColor(kBlack)
				ratio.GetXaxis().SetTitleOffset(1.3)
				ratio.GetYaxis().SetTitleOffset(.37)
				ratio.GetXaxis().SetTitleSize(.14)
				ratio.GetYaxis().SetTitleSize(.14)
				ratio.GetXaxis().SetLabelSize(0.135)
				ratio.GetXaxis().SetLabelOffset(0.03)
				ratio.GetYaxis().SetLabelSize(0.125)
				ratio.GetYaxis().SetNdivisions(505)
				ratio.SetMarkerSize(0.9)

				pad1, pad2 = format_2pads_for_ratio(self.canvas)
				num.GetXaxis().SetLabelOffset(0.05)
				denom.GetXaxis().SetLabelOffset(0.05)

				pad1.Draw()
				pad2.Draw()

				pad1.cd()
				if (self.log_scale_y):
						pad1.SetLogy()

				
				denom.Draw("hist E")
				num.Draw("hist E same")

				self.draw_cut_line()
				if "_r" in self.name:
					self.draw_material_layers()
				

				pad1.Update()

				pad2.cd()
				ratio.SetMinimum(ratio_ymin)
				ratio.SetMaximum(ratio_ymax)
				ratio.Draw("hist E")
				if self.norm: 
					line = TLine(ratio.GetXaxis().GetXmin(),1.0,ratio.GetXaxis().GetXmax(),1.0)
				else:
					line = TLine(ratio.GetXaxis().GetXmin(),18.8,ratio.GetXaxis().GetXmax(),18.8)
				line.SetLineColor(kBlack)
				line.SetLineWidth(1)
				line.SetLineStyle(2)
				line.Draw("same")
				if "_r" in self.name:
					self.draw_material_layers(ymin = ratio_ymin)
					self.leg.AddEntry(self.line, "Material Layers", "l")

				if draw_yield: 
					if  draw_markers:  
						self.leg.AddEntry(num, legends[ 0 ] +" {}".format(int(yields[0])) , 'lp')
						self.leg.AddEntry(denom, legends[ 1 ] +" {}".format(int(yields[1])), 'lp')
					else:  
						self.leg.AddEntry(num, legends[ 0 ] +" {}".format(int(yields[0])) , 'l')
						self.leg.AddEntry(denom, legends[ 1 ] +" {}".format(int(yields[1])), 'l')
				else: 
					if  draw_markers:  
						self.leg.AddEntry(num, legends[ 0 ] , 'lp')
						self.leg.AddEntry(denom, legends[ 1 ], 'lp')
					else:  
						self.leg.AddEntry(num, legends[ 0 ] , 'l')
						self.leg.AddEntry(denom, legends[ 1 ], 'l')
			 
				self.draw_cut_line(ymin = ratio_ymin)

			 
				self.canvas.Update()
				self.canvas.Modified()

				self.print_to_file(output_dir, self.name + "_ratio.pdf")
				self.print_to_file(output_dir, self.name + "_ratio.png")
				pad1.Close()
				pad2.Close()
				self.canvas.Close()


		def draw_cut_line(self,ymin=0):
			if self.draw_cut:
				line = TLine()
				line.SetLineColor(kBlack)
				line.SetLineWidth(2)
				line.SetLineStyle(2)
				cut = self.cut
				line.DrawLine(cut,0,cut,self.hist_y_max ) if not self.norm else line.DrawLine(cut,0,cut,1.0)
				# line.DrawLine(cut,ymin,cut,self.hist_y_max * 0.2) if not self.norm else line.DrawLine(cut,0,cut,1.0)
				line.Draw("same")
				arrow = TArrow(cut,self.y_max*1.0/self.empty_scale, cut*1.5, self.y_max*1.0/self.empty_scale) if not self.norm else TArrow(cut,1.0,cut + 0.1*(self.x_max), 1.0,0.02,"|>")
				arrow.SetLineWidth(2)
				arrow.SetLineStyle(8)
				arrow.SetLineColor(kBlack)
				arrow.SetFillColor(kBlack)
				arrow.Draw("same")

		def draw_material_layers(self,ymin=0):
			coords = [33.5,50.5,88.5,122.5,299.0]
			for coord in coords:
					self.line = TLine()
					# line.SetLineColor(14)
					self.line.SetLineColor(kRed)
					self.line.SetLineWidth(2)
					self.line.SetLineStyle(2)
					self.line.DrawLine(coord,ymin,coord,self.hist_y_max)
					# line.DrawLine(coord,0,coord,self.y_max*0.2 )
					# if(coords.index(coord) == 0):
					# 		self.leg.AddEntry(line, "Material Layers", "l")


class CutFlow(PlotBase):
		def __init__(self, hist_channels, types, output_dir = "../output", draw_yield=True, HNLscale = True, draw_markers = True, y_axis_type = "Vertices", title="Vertex Types", *args, **kwargs):

				super(CutFlow, self).__init__(
								legend_loc = [0.62,0.71,0.92, 0.92],
								atlas_loc = [0.62,0.875],
								extra_lines_loc = [0.62,0.775],
								*args,
								**kwargs)
				
				get_hist = self.get_cutflows(hist_channels)
				if not get_hist: 
					raise ValueError('Cant find histograms exiting.')
				legends = self.labels
				self.hists = self.histograms
				self.name = types[0] + "_newtriggers"


				for h, t in zip(self.hists, types):
					self.set_x_axis_bounds(h)
					# if x_title == "L_{xy}":
					# h.SetMaximum(10)
					# h.SetMinimum(10e4)
					# # else: 
					self.set_y_min(h)
					self.set_y_max(h)
					self.set_titles(h, y_axis_type)
					format_for_drawing(h, t)
					h.GetXaxis().SetLabelSize(0.04)
					h.GetXaxis().SetRange(1,16)
				
				self.pad_empty_space(self.hists)
				
			 
				pad1 = self.canvas.cd(1)
				format_simple_pad(pad1)
				pad1.cd()
				if (self.log_scale_y):
						pad1.SetLogy()
				if (self.log_scale_x):
						pad1.SetLogx()

			
				draw_hists(self.hists, "hist", types)

				# Print rounded numbers on histogram

				for h, t in zip(self.hists, types):
					text = TLatex()
					# text.SetTextAlign(21)
					# text.SetTextColor(h.GetMarkerColor())
					text.SetTextColor(kBlack)
					text.SetTextSize(0.03*h.GetMarkerSize())
					text.SetTextAngle(35)
					# for j in xrange(1, h.GetNbinsX()+1):
					for j in xrange(1, h.GetNbinsX()):
						x  = h.GetXaxis().GetBinCenter(j)
						y  = h.GetBinContent(j)
						if y != 0.0: 
							text.DrawLatex(x, y+100, '%.0f' % y)
				
				self.print_to_file(output_dir=output_dir, filename=self.name + ".pdf",cutflow=True)
				pad1.Close()
				self.canvas.Close()

class Hist2D(PlotBase):
	def __init__(self, hist_channels,types,output_dir = "../output",name_y="DV_mass", extra_cuts = "", HNLscale=False, profile=False,**kwargs):
		super(Hist2D, self).__init__(
				legend_loc = [0.62,0.71,0.92, 0.92],
				atlas_loc = [0.17,0.875],
				extra_lines_loc = [0.17,0.775],
				**kwargs)

		self.ntup_2D = True
		self.show_overflow = False
		self.show_underflow = False

		get_hist = self.get_hists(hist_channels,self.name, name_y,extra_cuts)
		if not get_hist: 
			raise ValueError('Cant find histograms exiting.')
		legends = self.labels
		self.hist = self.histograms[0]
	
		self.set_x_axis_bounds(self.hist)
		self.set_y_axis_bounds(self.hist)
		self.set_z_min(self.hist)
		self.set_z_max(self.hist)
		self.hist.GetZaxis().SetLabelSize(0.03)
		# self.hist.GetZaxis().SetMaxDigits(3);
		self.set_titles(self.hist,"")
		pad1 = self.canvas.cd(1)
		format_for_drawing(self.hist)
		format_simple_pad_2D(pad1)
		# format_simple_pad(pad1)
		pad1.cd()
		if (self.log_scale_y):
			pad1.SetLogy()
		if (self.log_scale_x):
			pad1.SetLogx()
		if (self.log_scale_z):
			pad1.SetLogz()
		# gStyle.SetPalette(kPastel)
		# TColor().InvertPalette()

		if HNLscale: 
			scale_hist(self.hist,self.scaleLumi,self.dataLumi,types[0])
		
		# draw_hists(self.hist, "colz", types)
		self.hist.Draw("colz")
		self.canvas.SetRightMargin(80)

		# self.hist.Draw("TEXTE colz")
		#self.hist.Draw("HIST SAME")
		# py = self.hist.ProfileX("py",1,25,"o")
		# if(profile):
		# 	py.Draw("same")

		self.print_to_file(output_dir,name_y+"_v_"+self.name + ".pdf")
		pad1.Close()
		self.canvas.Close()
