import uproot
import uproot_methods
import numpy as np
import pandas as pd
import sys

if len(sys.argv) < 3:
    print('usage: python kshort_selection.py <input files with wildcard> <output .pkl file>')
    exit(1)

inputs = str(sys.argv[1])
output = str(sys.argv[2])
print('in:', inputs)
print('out:', output)

# # Control Region
# This is a mehod that calculates whether or not there is a prompt lepton in the event. This is the definition of our control region so we are not accidentally plotting potential signal regions.
def calc_pass_cr(row):
    '''To be used with df.apply()'''
    # Check muons
    for loose, medium, tight, d0, z0sintheta in zip(row['muon_isLoose'], 
                                                    row['muon_isMedium'], 
                                                    row['muon_isTight'],
                                                    row['muon_trkd0'],
                                                    row['muon_trkz0sintheta'],
                                   ):
        if loose or medium or tight:
            if abs(d0) < 3.0 or abs(z0sintheta) < 0.5: #mm
                return 0 # Found a prompt muon. Does not pass CR.
    # Check electrons
    for loose, medium, tight, d0, z0sintheta in zip(row['el_LHLoose'], 
                                                    row['el_LHMedium'], 
                                                    row['el_LHTight'],
                                                    row['el_trkd0'],
                                                    row['el_trkz0sintheta'],
                                   ):
        if loose or medium or tight:
            if abs(d0) < 3.0 or abs(z0sintheta) < 0.5: #mm
                return 0 # Found a prompt electron. Does not pass CR.
    return 1


# # Alpha
# This is the calculation of the parameter alpha, which is used to reduce the background when selecting k-short vertices.
def calc_alpha(row):
    '''To be used with df.apply()'''
    alphas = []
    
    if len(row['secVtx_VSI_LRTR3_1p0_x']) == 0:
        return alphas
    
    # primary vertex position vector
    pv_vector = uproot_methods.TVector3(row['vertex_x'],
                                        row['vertex_y'],
                                        row['vertex_z'])    

    for dv_x, dv_y, dv_z, dv_phi in zip(row['secVtx_VSI_LRTR3_1p0_x'], 
                                        row['secVtx_VSI_LRTR3_1p0_y'], 
                                        row['secVtx_VSI_LRTR3_1p0_z'],
                                        row['secVtx_VSI_LRTR3_1p0_phi'],
                                       ):

        # secondary vertex position vector
        sv_vector = uproot_methods.TVector3(dv_x,
                                            dv_y,
                                            dv_z)

        # vector from pv to sv
        pv_sv_vector = sv_vector - pv_vector

        # vector difference between momentum vector and position vector
        alpha = pv_sv_vector.phi - dv_phi
        # put in -pi to pi range
        alpha = (alpha + np.pi/2) % np.pi*2 - np.pi
        alphas.append(alpha)
    return alphas


vertex_branches = ['secVtx_VSI_LRTR3_1p0_mass',
                'secVtx_VSI_LRTR3_1p0_ntrk',
                'secVtx_VSI_LRTR3_1p0_ntrk_lrt',
                'secVtx_VSI_LRTR3_1p0_trk_isLRT',
                'secVtx_VSI_LRTR3_1p0_r',
                'secVtx_VSI_LRTR3_1p0_pt',
                'secVtx_VSI_LRTR3_1p0_eta',
                'secVtx_VSI_LRTR3_1p0_x',
                'secVtx_VSI_LRTR3_1p0_y',
                'secVtx_VSI_LRTR3_1p0_z',
                'secVtx_VSI_LRTR3_1p0_phi',]

lepton_branches = ['muon_isTight',
                'muon_isMedium',
                'muon_isLoose',
                'muon_trkd0',
                'muon_trkz0sintheta',
                'el_LHTight',
                'el_LHMedium',
                'el_LHLoose',
                'el_trkd0',
                'el_trkz0sintheta',]

pv_branches = ['vertex_x',
            'vertex_y',
            'vertex_z',]

branches = vertex_branches + lepton_branches + pv_branches

# remove duplicates
branches = list(dict.fromkeys(branches))


full_df = None
# # Iterating over a set of files
# Using this method, we will iterate over several trees chained together across files. Uproot has some good documentation on how this works. https://uproot.readthedocs.io/en/latest/opening-files.html#uproot-iterate
for it in uproot.tree.iterate(inputs, 
                              'outTree',
                              branches=branches,
                             ):    

    # load chunk into dataframe
    df = pd.DataFrame(it)
    # remove bytesteam flag from columns
    df.columns = branches

    # calculate variables needed in selection

    # cut on control region
    df['pass_cr'] = df.apply(calc_pass_cr, axis=1)
    df = df.query('pass_cr > 0')

    # cut on number of DVs
    df = df[df['secVtx_VSI_LRTR3_1p0_mass'].str.len() > 1]
    
    # calculate alpha
    df['alpha'] = df.apply(calc_alpha, axis=1)

    # explode into a dataframe of just vertex quantities
    vtx_df = df[vertex_branches+['alpha']].apply(pd.Series.explode)

    # only use 2-trk vertices
    vtx_df = vtx_df.query('secVtx_VSI_LRTR3_1p0_ntrk == 2')

    # cut on alpha
    vtx_df = vtx_df[abs(vtx_df['alpha']) < 0.01]

    # append to the full dataframe
    if full_df is None:
        full_df = vtx_df
    else:
        full_df = full_df.append(vtx_df)
    print("Total vertices loaded:", len(full_df))

print('writing')
full_df.to_pickle(output)

print("Finished")


