from ROOT import *
import uuid
import array

class PlotBase(object):
	''' A base class that contains only the objects/information
	that every ROOT plot would contain. Only classes derived
	from this should ever be initialized. '''
	def __init__(self,
			x_title         = None,
			y_title         = None,
			x_units         = "",
			y_units         = "",
			x_min           = None,
			x_max           = None,
			y_min           = None,
			y_max           = None,
			z_min           = None,
			z_max           = None,
			x_axis_scale    = None,
			show_overflow   = True,
			show_underflow  = True,
			draw_cut        = False,
			cut             = 0.0,
			height          = 600,
			width           = 800,
			name            = None,
			log_scale_y     = False,
			log_scale_x     = False,
			log_scale_z     = False,
			empty_scale     = 1.8,
			legend_loc      = None,
			atlas_loc       = None,
			extra_lines_loc = None,
			tex_size_mod    = 1.0,
			leg_size_mod    = 0.9,
			tex_spacing_mod = 1.0,
			debug           = False,
			atlas_mod       = "Internal", # 'Internal', 'Preliminary', etc
			lumi_val        = "X.X",      # ex: '3.2'
			hide_lumi       = True,
			lumi_units      = "fb",       # ex: 'fb'
			com_energy      = "13",       # in TeV
			extra_legend_lines = [],
			rebin = None,
			norm = None,
			rename_log_plot = True,
			use_ntuple = False,
			ntup_nbins = 1,
			ntup_nbins_y = 1,
			ntup_2D = False,
			ntup_1D = False,
			scaleLumi = 139.0,
			dataLumi = 1.0,
			**kwargs):

#        super(PlotBase, self).__init__(**kwargs)

		self.log = []

		self.x_title = x_title
		self.y_title = y_title
		self.x_units = x_units
		self.y_units = y_units

		self.x_min = x_min
		self.x_max = x_max

		self.y_min = y_min
		self.y_max = y_max
		self.z_min = z_min
		self.z_max = z_max

		self.x_axis_scale = x_axis_scale
		self.use_ntuple = use_ntuple
		self.ntup_nbins = ntup_nbins
		self.ntup_nbins_y = ntup_nbins_y
		self.scaleLumi = scaleLumi
		self.dataLumi = dataLumi
		self.ntup_2D = ntup_2D
		self.ntup_1D = ntup_1D
		
		self.show_overflow = show_overflow
		self.show_underflow = show_underflow

		if self.ntup_2D: 
			self.show_overflow = False
			self.show_underflow = False
		

		if (name == None):
			# random unique default name to avoid name overlap
			self.name = "canvas"
		else:
			self.name = str(name)

		self.width  = width
		self.height = height

		# if (log_scale_y and rename_log_plot): self.name += "_log"

		self.log_scale_y = log_scale_y
		self.log_scale_x = log_scale_x
		self.log_scale_z = log_scale_z

		self.empty_scale = empty_scale

		self.x_units_str = ""
		if self.x_units != "":
			self.x_units_str = "[" + self.x_units + "]"

		self.legend_loc = [0.69,0.90,0.92,0.80]
		if (legend_loc):
			assert(len(legend_loc) == 4)
			self.legend_loc = legend_loc

		self.atlas_loc = [0.2,0.90]
		if (atlas_loc):
			assert(len(atlas_loc) == 2)
			self.atlas_loc = atlas_loc

		self.extra_lines_loc = [0.2,0.82]
		if (extra_lines_loc):
			assert(len(extra_lines_loc) == 2)
			self.extra_lines_loc = extra_lines_loc

		self.tex_size_mod = tex_size_mod
		self.leg_size_mod = leg_size_mod
		self.tex_spacing_mod = tex_spacing_mod

		self.extra_legend_lines = extra_legend_lines

		self.atlas_mod  = atlas_mod
		self.lumi_val   = str(scaleLumi)
		self.hide_lumi  = hide_lumi
		self.lumi_units = lumi_units
		self.com_energy = com_energy

		self.rebin = rebin
		self.norm = norm

		self.draw_cut = draw_cut
		self.cut      = cut

		self._make_canvas()
		self._make_decorations()

	def determine_y_axis_title(self, histo, label = "Events", show_binwidth = True):
		bin_width = histo.GetXaxis().GetBinWidth(1)
		if self.y_title == None:
			self.y_title = ""
			if self.norm:
				self.y_title = "Fraction of "
			self.y_title += label
			if (show_binwidth and self.x_units):
				if (bin_width >= 1):
					self.y_title += " / " + str(int(bin_width))
				else:
					self.y_title += " / " + str(round(bin_width,2))
			if (self.x_units):
				self.y_title += " " + self.x_units
		else:
			if(self.y_units != ""):
				self.y_title += " [" + self.y_units + "]" 
			else:
				self.y_title = self.y_title

	def set_titles(self, histo, label="Events"):
		if(self.x_units != ""):
			histo.GetXaxis().SetTitle(self.x_title + " [" + self.x_units + "]")
		else:
			histo.GetXaxis().SetTitle(self.x_title)

		self.determine_y_axis_title(histo, label)
		histo.GetYaxis().SetTitle(self.y_title)

	def set_titles_graph(self, histo):
		if(self.x_units != ""):
			histo.GetXaxis().SetTitle(self.x_title + " [" + self.x_units + "]")
		else:
			histo.GetXaxis().SetTitle(self.x_title)

		self.determine_y_axis_title(histo)
		histo.GetYaxis().SetTitle(self.y_title)

	def set_x_axis_bounds(self, histo):
		if (self.x_max or self.x_min):
			tmp_x_min = histo.GetXaxis().GetXmin()
			tmp_x_max = histo.GetXaxis().GetXmax()
			if (self.x_max != None): tmp_x_max = self.x_max
			if (self.x_min != None): tmp_x_min = self.x_min
			if (self.x_axis_scale):
				a = histo.GetXaxis()
				a.Set(a.GetNbins(), self.x_axis_scale * a.GetXmin(), a.GetXmax() * self.x_axis_scale)			
			else:
				binx_min = histo.GetXaxis().FindBin(tmp_x_min)
				binx_max = histo.GetXaxis().FindBin(tmp_x_max)
				if self.show_overflow:
					overflow = histo.Integral(binx_max+1,histo.GetNbinsX())
					histo.SetBinContent(binx_max, histo.GetBinContent(binx_max) + overflow) # merge overflow into last bin
				if self.show_underflow:
					underflow = histo.Integral(0,binx_min-1)
					histo.SetBinContent(binx_min, histo.GetBinContent(binx_min) + underflow) # merge overflow into last bin
				histo.GetXaxis().SetRange(binx_min,binx_max)

				self.x_min = tmp_x_min
				self.x_max = tmp_x_max

		else:
			self.x_min = histo.GetXaxis().GetXmin()
			self.x_max = histo.GetXaxis().GetXmax()

		# if self.show_overflow:
		#   histo.SetBinContent(histo.GetNbinsX(), histo.GetBinContent(histo.GetNbinsX()) + histo.GetBinContent(histo.GetNbinsX() + 1)) # merge overflow into last bin
			
		# if self.show_underflow:
		#   histo.SetBinContent(1, histo.GetBinContent(1) + histo.GetBinContent(0)) # merge underflow into first bin

	def set_y_axis_bounds(self, histo):
		tmp_y_min = histo.GetYaxis().GetXmin()
		tmp_y_max = histo.GetYaxis().GetXmax()

		if (self.y_max or self.y_min):
			if (self.y_max): tmp_y_max = self.y_max
			if (self.y_min): tmp_y_min = self.y_min

		histo.GetYaxis().SetRangeUser(tmp_y_min , tmp_y_max)

	def pad_empty_space(self, histos):
		if (self.y_max != None):
			print("WARNING: attempted to pad empty space and set y-maximum at the same time.")
			return
		''' rescale y-axis to add/subtract empty space '''
		if self.y_max != None:
			print("warning: attmempted to set y_max and pad empty space at the same time")
			return
		self.y_max = max(map(lambda h: h.GetMaximum(), histos))
		self.hist_y_max = max(map(lambda h: h.GetMaximum(), histos))

		if self.log_scale_y:
			self.y_max *= 5**self.empty_scale
		else:
			self.y_max *= self.empty_scale

		for h in histos:
			h.SetMaximum(self.y_max)

	def set_y_min(self, histo):
		if (self.y_min != None):
			histo.SetMinimum(self.y_min)

	def set_y_max(self, histo):
		if (self.y_max != None):
			# histo.SetMaximum(self.y_max)
			histo.GetYaxis().SetRangeUser(self.y_min, self.y_max)

	def set_z_min(self, histo):
		if (self.z_min != None):
			histo.SetMinimum(self.z_min)

	def set_z_max(self, histo):
		if (self.z_max != None):
			histo.SetMaximum(self.z_max)

	def _make_canvas(self):
		canvas_name = "c_" + self.name
		self.canvas = TCanvas(canvas_name, canvas_name, self.width, self.height)
		self.canvas.Draw()
		self.canvas.Modified()

	def _make_decorations(self):
		''' Make the ATLAS label, luminosity, extra lines, legend, etc '''
		self.canvas.cd()

		def set_default_tex_props(tex):
			tex.SetNDC()
			tex.SetLineWidth(2)
			tex.SetTextSize(0.045 * self.tex_size_mod)

		self.ATLAS_tex = TLatex(self.atlas_loc[0], self.atlas_loc[1], "ATLAS")
		set_default_tex_props(self.ATLAS_tex)
		self.ATLAS_tex.SetTextFont(72)

		self.ATLAS_MOD_tex = TLatex(self.atlas_loc[0], self.atlas_loc[1], (14 * ' ') + self.atlas_mod)
		set_default_tex_props(self.ATLAS_MOD_tex)
		self.ATLAS_MOD_tex.SetTextFont(42)

		lum_str = "" if self.hide_lumi else ", " + self.lumi_val + " " + self.lumi_units + "^{-1}"

		self.ILUM_tex = TLatex(self.atlas_loc[0], self.atlas_loc[1] - 0.05,
				"#sqrt{s} = " + self.com_energy + " TeV" + lum_str)
		set_default_tex_props(self.ILUM_tex)
		self.ILUM_tex.SetTextFont(42)

		self.extra_latex = []
		y_tmp = self.extra_lines_loc[1]
		for txt_line in self.extra_legend_lines:
			tex = TLatex(self.extra_lines_loc[0], y_tmp, txt_line);
			set_default_tex_props(tex)
			tex.SetTextFont(42)
			self.extra_latex.append(tex)
			y_tmp -= self.tex_spacing_mod * 0.05

		self.leg = TLegend(self.legend_loc[0], self.legend_loc[1],
				self.legend_loc[2], self.legend_loc[3])

		self.leg.SetFillStyle(0)
		self.leg.SetTextSize(0.03*self.leg_size_mod) 
		self.leg.SetTextFont(42)
		self.leg.SetBorderSize(0)

	def log_line(self, text_line):
		self.log.append(text_line)

	def _draw_decorations(self):
		''' Draw the ATLAS label, luminosity, extra lines, legend, etc '''
		self.canvas.cd()
		self.leg.Draw()
		self.ATLAS_tex.Draw()
		self.ATLAS_MOD_tex.Draw()
		self.ILUM_tex.Draw()
		for tex in self.extra_latex:
			tex.Draw()
		self.canvas.Update()
		self.canvas.Modified()

	def print_to_file(self, output_dir, filename, cutflow=False,index = None, num_plots = None):
		''' Assumes the derived class has already called Draw on all of its content,
		populated the legend, etc
		'''
		self._draw_decorations()
		import os
		if cutflow == True: 
			output_dir = os.path.join(os.path.abspath(output_dir), 'cutflows/{}/'.format(self.vtx_alg[0]))
		else:
			output_dir = os.path.join(os.path.abspath(output_dir))+'/'
		if not os.path.exists(output_dir): os.makedirs(output_dir, exist_ok=True)

		if (index is None):
			self.canvas.SaveAs(output_dir+filename)
			return

		if (index == 0):
			self.canvas.Print(filename + ".pdf(", "pdf")
		elif index == num_plots - 1:
			self.canvas.Print(filename + ".pdf)", "pdf")
		else:
			self.canvas.Print(filename + ".pdf", "pdf")

	def get_hists(self,hist_channels,variable,variable_y="DV_mass",extra_cuts=""): 
		self.histograms = []
		self.filenames = []
		self.labels = []
		self.vtx_alg = []
		self.tfiles = []  # root is stupid and will close the file if you're not careful
		if "truth" in variable: 
			#strip truth from the variable name to get the hist
			variable=variable.split("truth_")[1]
		for nhist in range(len(hist_channels)):
			filename = hist_channels[nhist]['filename']
			label = hist_channels[nhist]['label']
			vtx_alg = hist_channels[nhist]['vtx_alg']
			selection = hist_channels[nhist]['selection']
			extra_cuts = hist_channels[nhist]['extra_cuts']
			print(hist_channels[nhist].keys())
			if 'MCtype' in hist_channels[nhist].keys(): 
				MCtype = hist_channels[nhist]['MCtype']
			else: 
				MCtype = None
			self.tfiles.append(TFile(filename))  # get file
			if  MCtype != None: 
				if "truth" in selection:  #truth has this extra folder to get to all...small hack -DT
					if MCtype == "all": 
						hist_path = f'{vtx_alg}/{selection}/all/{selection}'
					else: 
						hist_path = f'{vtx_alg}/{selection}/all/{MCtype}/{variable}'
				else: 
					if MCtype == "mixed": 
						hist_path_LNC = f'{vtx_alg}/{selection}/LNC/{variable}'
						hist_path_LNV = f'{vtx_alg}/{selection}/LNV/{variable}'
					else: 
						hist_path = f'{vtx_alg}/{selection}/{MCtype}/{variable}'
			else: 
				hist_path = f'{vtx_alg}/{selection}/{variable}'
			
			###################################################################################################
			# Plot with micro-ntuples
			###################################################################################################
			if self.use_ntuple:
				if MCtype != None: # running on HNL signal 
					if MCtype == "mixed":
						tmp_hist_name_LNC = f'{vtx_alg}_LNC_{selection}_{variable}'
						tmp_hist_name_LNV = f'{vtx_alg}_LNV_{selection}_{variable}'
					else:  
						tmp_hist_name = f'{vtx_alg}_{MCtype}_{selection}_{variable}'
				else: # not running on signal
					tmp_hist_name = f'{vtx_alg}_{selection}_{variable}'

				if MCtype != None: 
					if MCtype == "mixed": 
						ttree_LNC = self.tfiles[nhist].Get(f'{vtx_alg}_ntuples_LNC_{selection}')  # get TTree
						ttree_LNV = self.tfiles[nhist].Get(f'{vtx_alg}_ntuples_LNV_{selection}')  # get TTree
						if not ttree_LNC:
							raise KeyError(f'Cannot find {vtx_alg}_ntuples_LNC_{selection} in file {self.tfiles[nhist]}')
						if not ttree_LNV:
							raise KeyError(f'Cannot find {vtx_alg}_ntuples_LNV_{selection} in file {self.tfiles[nhist]}')
					else: 
						ttree = self.tfiles[nhist].Get(f'{vtx_alg}_ntuples_{MCtype}_{selection}')  # get TTree
						if not ttree:
							raise KeyError(f'Cannot find {vtx_alg}_ntuples_{MCtype}_{selection} in file {self.tfiles[nhist]}')
				else: 
					ttree = self.tfiles[nhist].Get(f'{vtx_alg}_ntuples_{selection}')  # get TTree
					if not ttree:
						raise KeyError(f'Cannot find {vtx_alg}_ntuples_{MCtype}_{selection} in file {self.tfiles[nhist]}')

				if self.ntup_1D == True and self.ntup_2D == True: 
					raise KeyError('You have configured a 2D and 1D histogram at the same time. You cannot do this!!')
				if self.ntup_1D == False and self.ntup_2D == False: 
					raise KeyError('You need to set either ntup_1D or ntup_2D to True.')
				
				if MCtype == "mixed": 
					if self.ntup_1D: 
						ntup_hist = self.mixLNCLNV_hist_1d(ttree_LNC,ttree_LNV,tmp_hist_name_LNC,tmp_hist_name_LNV,variable,label,extra_cuts)
					elif self.ntup_2D: 
						ntup_hist = self.mixLNCLNV_hist_2d(ttree_LNC,ttree_LNV,tmp_hist_name_LNC,tmp_hist_name_LNV,variable,label,variable_y,extra_cuts)
				else: 
					if self.ntup_1D: 
						ntup_hist = self.hist_1d(ttree,tmp_hist_name,variable,label,extra_cuts)
					elif self.ntup_2D: 
						if MCtype != None: 
							continue
						else:  
							ntup_hist = self.hist_2d(ttree,tmp_hist_name,variable,label,variable_y,extra_cuts)
					else: 
						ntup_hist = TH1D(tmp_hist_name, tmp_hist_name, self.ntup_nbins, self.x_min, self.x_max)  # create empty histogram
						ttree.Draw(variable+'>>'+tmp_hist_name, 'DV_weight') 
		
				self.histograms.append(ntup_hist)

			###################################################################################################
			# Plot with pre-binned histograms 
			################################################################################################### 
			else:
				if MCtype == "mixed": 
					h_LNC = self.tfiles[nhist].Get(hist_path_LNC) 
					h_LNV = self.tfiles[nhist].Get(hist_path_LNV) 
					h_LNC.Scale(0.5)
					h_LNV.Scale(0.5)
					histogram = h_LNC + h_LNV
				else: 
					histogram = self.tfiles[nhist].Get(hist_path)
				if not histogram:  # no histogram object. don't even try
					print(f'cannot find {variable}. Exiting.')
					return
				histogram.SetTitle("")
				self.histograms.append(histogram)  # get variable with suffix

			self.filenames.append(filename)
			self.labels.append(label)
			self.vtx_alg.append(vtx_alg)

		return True

	def get_cutflows(self,hist_channels): 
		self.histograms = []
		self.filenames = []
		self.labels = []
		self.vtx_alg = []
		self.tfiles = []  # root is stupid and will close the file if you're not careful
	
		for nhist in range(len(hist_channels)):
			filename = hist_channels[nhist][0]
			label = hist_channels[nhist][1]
			vtx_alg = hist_channels[nhist][2]
			if len(hist_channels[nhist]) > 4: 
				MCtype = hist_channels[nhist][4]
			else: 
				MCype = None
			self.tfiles.append(TFile(filename))  # get file
			if MCtype != None: 
				if MCtype == "mixed": 
					hist_path_LNC = f'{vtx_alg}/CutFlow/CutFlow_LNC'
					hist_path_LNV = f'{vtx_alg}/CutFlow/CutFlow_LNV'
				else: 
					hist_path = f'{vtx_alg}/CutFlow/CutFlow_{MCtype}'
			else: 
				hist_path = f'{vtx_alg}/CutFlow/CutFlow'
			
			if MCtype == "mixed": 
				h_LNC = self.tfiles[nhist].Get(hist_path_LNC) 
				h_LNV = self.tfiles[nhist].Get(hist_path_LNV) 
				# h_LNC.Scale(0.5)
				# h_LNV.Scale(0.5)
				histogram = h_LNC + h_LNV
			else: 
				histogram = self.tfiles[nhist].Get(hist_path) 
			if not histogram:  # no histogram object. don't even try
				print('Cannot find cutflow histogram. Exiting')
				return
			self.histograms.append(histogram)
			self.labels.append(label)
			self.vtx_alg.append(vtx_alg)

		return True

	def mixLNCLNV_hist_1d(self, ttree_LNC,ttree_LNV,tmp_hist_name_LNC,tmp_hist_name_LNV,variable,label,extra_cuts=""):
		ntup_hist_LNC = TH1D(tmp_hist_name_LNC, tmp_hist_name_LNC, self.ntup_nbins, self.x_min, self.x_max)  # create empty histogram
		ntup_hist_LNV = TH1D(tmp_hist_name_LNV, tmp_hist_name_LNV, self.ntup_nbins, self.x_min, self.x_max)  # create empty histogram
		
		ttree_LNC.Draw(variable+'>>'+tmp_hist_name_LNC, 'DV_weight*(DV_cosmic_sep > 0.05)'+ extra_cuts) 
		ttree_LNV.Draw(variable+'>>'+tmp_hist_name_LNV, 'DV_weight*(DV_cosmic_sep > 0.05)'+extra_cuts) 
		
		#make histogram using 50% LNC and 50% LNV
		ntup_hist_LNC.Scale(0.5)
		ntup_hist_LNV.Scale(0.5)
		ntup_hist = ntup_hist_LNC + ntup_hist_LNV

		return ntup_hist

	def mixLNCLNV_hist_2d(self, ttree_LNC,ttree_LNV,tmp_hist_name_LNC,tmp_hist_name_LNV,variable,label,variable_y="DV_mass",extra_cuts=""):
		ntup_hist_LNC = TH2D(tmp_hist_name_LNC,tmp_hist_name_LNC, self.ntup_nbins, self.x_min, self.x_max,self.ntup_nbins_y ,self.y_min,self.y_max)  # create empty histogram
		ntup_hist_LNV = TH2D(tmp_hist_name_LNV,tmp_hist_name_LNV, self.ntup_nbins, self.x_min, self.x_max,self.ntup_nbins_y ,self.y_min,self.y_max)  # create empty histogram
	
		ttree_LNC.Draw(f'{variable_y}:{variable}'+'>>'+tmp_hist_name_LNC, 'DV_weight*(DV_cosmic_sep > 0.05)'+extra_cuts) 
		ttree_LNV.Draw(f'{variable_y}:{variable}'+'>>'+tmp_hist_name_LNV, 'DV_weight*(DV_cosmic_sep > 0.05)'+extra_cuts) 
		
		#make histogram using 50% LNC and 50% LNV
		ntup_hist_LNC.Scale(0.5)
		ntup_hist_LNV.Scale(0.5)
		ntup_hist = ntup_hist_LNC.Clone("ntup_hist")
		ntup_hist.Add(ntup_hist_LNV)

		return ntup_hist

	def hist_1d(self, ttree,hname,variable,label,extra_cuts=""):
		ntup_hist = TH1D(hname, hname, self.ntup_nbins, self.x_min, self.x_max)  # create empty histogram
		ntup_hist.Sumw2()
		ttree.Draw(variable+'>>'+hname, 'DV_weight*(DV_cosmic_sep > 0.05)'+extra_cuts)  # fill histogram with data from ttree.

		return ntup_hist

	def hist_2d(self, ttree,hname,variable,label,variable_y="DV_mass",extra_cuts=""):
		ntup_hist = TH2D(hname, hname, self.ntup_nbins, self.x_min, self.x_max,self.ntup_nbins_y ,self.y_min,self.y_max)  # create empty histogram
		ntup_hist.Sumw2()
		ttree.Draw(f'{variable_y}:{variable}'+'>>'+hname, 'DV_weight*(DV_cosmic_sep > 0.05)'+extra_cuts)  # fill histogram with data from ttree. 

		return ntup_hist




