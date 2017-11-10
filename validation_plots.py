""" Code for creating validation plots from the DR1 tables
"""

import os
import sys
import copy
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import vaex as vx
import decimal

class Bole():
    def __init__(self):
        pass

    def read(self, selcols, group=1):
        """ Read the tables and generate an output dataframe with the selected
        subset of columns. Different groups for different set of tables
        """
        if (group == 1):
            ls_g = ["dr1_band_g_7pcent_20171101_000001.h5",
                    "dr1_band_g_7pcent_20171101_000002.h5"]
            ls_r = ["dr1_band_r_10pcent_20171101_000001.h5",
                    "dr1_band_r_10pcent_20171101_000002.h5",
                    "dr1_band_r_10pcent_20171101_000003.h5"]
            ls_i = ["dr1_band_i_10pcent_20171101_000001.h5",
                    "dr1_band_i_10pcent_20171101_000002.h5",
                    "dr1_band_i_10pcent_20171101_000003.h5"]
            ls_z = ["dr1_band_z_10pcent_20171101_000001.h5",
                    "dr1_band_z_10pcent_20171101_000002.h5",
                    "dr1_band_z_10pcent_20171101_000003.h5"]
            ls_Y = ["dr1_band_Y_7pcent_20171101_000001.h5",
                    "dr1_band_Y_7pcent_20171101_000002.h5"]
            ls_band = ls_g + ls_r + ls_i + ls_z + ls_Y
            # Create a DF to harbor the selection, adding BAND and COADD_OBJECT_ID
            selC = copy.copy(selcols) + ["BAND", "COADD_OBJECT_ID"]
            for idx, l in enumerate(ls_band):
                dfaux = pd.read_hdf(l)
                if False:
                    cols = np.sort(dfaux.columns.values)
                    print(cols)
                    exit() 
                dfaux = dfaux[selC]
                if (idx == 0):
                    sel = dfaux.copy(deep=True)
                else:
                    sel = pd.concat([sel, dfaux])
            # Reset indexing
            sel.reset_index(drop=False, inplace=True) 
        elif (group == 2):
            f = "Y3A2_COADD_OBJECT_SUMMARY_10pcent_WAVG_MAGandFLUX.h5"
            sel = pd.read_hdf(f)
        elif (group == 3):
            f = "bechtol.y3a2_ext_mash_onlyWAVG.h5"
            sel = pd.read_hdf(f)
        return sel

    def comp_flux_mag(self):
        """ Comparison plots among flux and magnitudes
        """
        err_f = ['FLUXERR_APER_1', 'FLUXERR_APER_10', 'FLUXERR_APER_11',
                 'FLUXERR_APER_12', 'FLUXERR_APER_2', 'FLUXERR_APER_3',
                 'FLUXERR_APER_4', 'FLUXERR_APER_5', 'FLUXERR_APER_6',
                 'FLUXERR_APER_7', 'FLUXERR_APER_8', 'FLUXERR_APER_9',
                 'FLUXERR_AUTO', 'FLUXERR_DETMODEL', 'FLUXERR_DISK', 
                 'FLUXERR_HYBRID', 'FLUXERR_MODEL', 'FLUXERR_PETRO',
                 'FLUXERR_PSF']
        f = ['FLUX_APER_1', 'FLUX_APER_10', 'FLUX_APER_11', 'FLUX_APER_12',
             'FLUX_APER_2', 'FLUX_APER_3', 'FLUX_APER_4', 'FLUX_APER_5',
             'FLUX_APER_6', 'FLUX_APER_7', 'FLUX_APER_8', 'FLUX_APER_9', 
             'FLUX_AUTO', 'FLUX_DETMODEL', 'FLUX_DISK', 'FLUX_HYBRID', 
             'FLUX_MAX', 'FLUX_MODEL', 'FLUX_PETRO', 'FLUX_PSF', 
             'FLUX_RADIUS']
        err_m = ['MAGERR_APER_1', 'MAGERR_APER_10', 'MAGERR_APER_11', 
                 'MAGERR_APER_12', 'MAGERR_APER_2', 'MAGERR_APER_3', 
                 'MAGERR_APER_4', 'MAGERR_APER_5', 'MAGERR_APER_6',
                 'MAGERR_APER_7', 'MAGERR_APER_8', 'MAGERR_APER_9', 
                 'MAGERR_AUTO', 'MAGERR_DETMODEL', 'MAGERR_DISK', 
                 'MAGERR_HYBRID', 'MAGERR_ISO', 'MAGERR_MODEL',
                 'MAGERR_PETRO', 'MAGERR_PSF']
        m = ['MAG_APER_1', 'MAG_APER_10', 'MAG_APER_11', 'MAG_APER_12', 
             'MAG_APER_2', 'MAG_APER_3', 'MAG_APER_4', 'MAG_APER_5', 
             'MAG_APER_6', 'MAG_APER_7', 'MAG_APER_8', 'MAG_APER_9',
             'MAG_AUTO', 'MAG_DETMODEL', 'MAG_DISK', 'MAG_HYBRID', 
             'MAG_ISO', 'MAG_MODEL', 'MAG_PETRO', 'MAG_PSF']
        # Create the plots
        
        #
        # MAG {WAVG, AUTO, PETRO} vs FLUX 
        #
        if False:
            plt.close("all")
            fig, ax = plt.subplots(3, 5, figsize=(15, 8))
            kw = {
                "marker":".",
                "s": 10,
                "alpha":0.5,
                "edgecolors":None,
                }
            tab = self.read(m + f)
            tabx2 = self.read(None, group=2)
            # Drop all NaN
            tab.dropna(subset=["FLUX_AUTO", "MAG_AUTO", "FLUX_PSF", 
                        "MAG_PSF", "FLUX_MODEL", "MAG_MODEL", 
                        "FLUX_DETMODEL", "MAG_DETMODEL"], how="any", 
                        inplace=True)
            tabx2.dropna(how="any", inplace=True)
            # Set colors and bands
            color = {"g":"green", "r":"gold", "i":"orange", "z":"red", 
                     "Y":"coral"}
            bands = ["g", "r", "i", "z", "Y"]
            # Select physical fluxes, discard bad magnitude (=99) 
            tab = tab.loc[((tab["FLUX_AUTO"] > 0) & (tab["MAG_AUTO"] <99))]
            tab = tab.loc[((tab["FLUX_PETRO"] > 0) & (tab["MAG_PETRO"] <99))]
            tab.reset_index(drop=False, inplace=True)
            for b in bands:
                tabx2 = tabx2.loc[((tabx2["WAVG_FLUX_PSF_" + b.upper()] > 0) & 
                                  (tabx2["WAVG_MAG_PSF_" + b.upper()] < 99))]
            tabx2.reset_index(drop=False, inplace=True)
            for idx, x in enumerate(bands):
                kw.update({"c": color[x]})
                # *_AUTO
                tmp_f = np.log10(tab.loc[tab["BAND"] == x, "FLUX_AUTO"].values)
                tmp_f *= -2.5
                tmp_f += 30
                aux_d = tmp_f - tab.loc[(tab["BAND"] == x), "MAG_AUTO"].values
                avg_d = np.mean(aux_d) 
                std_d = np.std(aux_d)
                #
                ax[0, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_AUTO"],
                                   tmp_f, label="AUTO", **kw)
                ax[0, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                txt = r"Avg Diff: {0:.2E} $\pm$ {1:.2E}".format(
                    decimal.Decimal(avg_d), decimal.Decimal(std_d))
                ax[0, idx].text(0.01, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[0, idx].transAxes)
                ax[0, idx].grid(alpha=0.5)
                # *_PETRO
                tmp_f = np.log10(tab.loc[tab["BAND"] == x, "FLUX_PETRO"].values)
                tmp_f *= -2.5
                tmp_f += 30
                aux_d = tmp_f - tab.loc[(tab["BAND"] == x), "MAG_PETRO"].values
                avg_d = np.mean(aux_d) 
                std_d = np.std(aux_d)
                ax[1, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_PETRO"],
                                   tmp_f, label="PETRO", **kw)
                ax[1, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                txt = r"Avg Diff: {0:.2E} $\pm$ {1:.2E}".format(
                    decimal.Decimal(avg_d), decimal.Decimal(std_d))
                ax[1, idx].text(0.01, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[1, idx].transAxes)
                ax[1, idx].grid(alpha=0.5)
                # WAVG_* is taken from other table, originated from 
                # Y3A2_COADD_OBJECT
                mag_key, flux_key = "WAVG_MAG_PSF_", "WAVG_FLUX_PSF_" 
                tmp_f = np.log10(tabx2[flux_key + x.upper()].values)
                tmp_f *= -2.5
                tmp_f += 30
                aux_d = tmp_f - tabx2[mag_key + x.upper()].values
                avg_d = np.mean(aux_d) 
                std_d = np.std(aux_d)
                ax[2, idx].scatter(tabx2[mag_key + x.upper()],
                                   tmp_f, label="WAVG_PSF", **kw)
                ax[2, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                txt = r"Avg Diff: {0:.2E} $\pm$ {1:.2E}".format(
                    decimal.Decimal(avg_d), decimal.Decimal(std_d))
                ax[2, idx].text(0.01, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[2, idx].transAxes)
                ax[2, idx].grid(alpha=0.5)
                ax[2, idx].set_xlabel(r"MAG")
            # Set minor ticks
            for ax_row in ax:
                for ax_col_idx in range(ax_row.shape[0]):
                    # Use Auto Minor Locator
                    minorLocator_x = AutoMinorLocator()
                    ax_row[ax_col_idx].xaxis.set_minor_locator(minorLocator_x)
                    minorLocator_y = AutoMinorLocator()
                    ax_row[ax_col_idx].yaxis.set_minor_locator(minorLocator_y)
                    # Invert axis
                    ax_row[ax_col_idx].invert_xaxis()
                    ax_row[ax_col_idx].invert_yaxis()
                    # Rasterize
                    ax_row[ax_col_idx].set_rasterization_zorder(-10)
                    # ax_row[ax_col_idx].tick_params(axis="both", #labelsize=7,
                    #                                bottom="on")
            
            #
            ax[0, 0].set_title("g-band", color="green")
            ax[0, 1].set_title("r-band", color="gold")
            ax[0, 2].set_title("i-band", color="orange")
            ax[0, 3].set_title("z-band", color="red")
            ax[0, 4].set_title("Y-band", color="coral")
            #
            ax[0, 0].set_ylabel(r"-2.5$\,\log_{10}$(FLUX$_{AUTO}$)+30")
            ax[1, 0].set_ylabel(r"-2.5$\,\log_{10}$(FLUX$_{PETRO}$)+30")
            ax[2, 0].set_ylabel(r"-2.5$\,\log_{10}$(FLUX$_{WAVG}$)+30")
            # Title
            supt = "Comparing db MAG vs magnitude from FLUX (zero point=30)"
            supt += ", using a sample of ~4e5 objects"
            plt.suptitle(supt, color="royalblue", weight="medium")
            # Spacing
            plt.subplots_adjust(left=0.05, bottom=0.06, right=0.98, top=0.92,
                                wspace=0.22, hspace=0.2)
            # Save 
            if True:
                outname = "MAG_FLUX_compare_set1.png"
                plt.savefig(outname, dpi=400, facecolor="w", edgecolor="w",
                            orientation="portrait", papertype=None, 
                            format="png", transparent=False, bbox_inches=None, 
                            pad_inches=0.1, frameon=None)
            plt.show()
            #
            #
            #
        #
        # MAG_APER vs FLUX
        #
        if False:
            plt.close("all")
            fig, ax = plt.subplots(3, 5, figsize=(15, 8))
            kw = {
                "marker":".",
                "s": 10,
                "alpha":1.,
                "edgecolors":None,
                }
            tab = self.read(m + f)
            # Drop all NaN
            tab.dropna(subset=['FLUX_APER_1', 'FLUX_APER_10', 'FLUX_APER_11', 
                       'FLUX_APER_12', 'FLUX_APER_2', 'FLUX_APER_3', 
                       'FLUX_APER_4', 'FLUX_APER_5', 'FLUX_APER_6', 
                       'FLUX_APER_7', 'FLUX_APER_8', 'FLUX_APER_9', 
                       'MAG_APER_1', 'MAG_APER_10', 'MAG_APER_11', 
                       'MAG_APER_12', 'MAG_APER_2', 'MAG_APER_3', 
                       'MAG_APER_4', 'MAG_APER_5', 'MAG_APER_6', 
                       'MAG_APER_7', 'MAG_APER_8', 'MAG_APER_9'], 
                       how="any", 
                       inplace=True)
            # Set colors and bands
            color = {"g":["aquamarine", "limegreen", "green", "lime"],
                     "r":["khaki", "goldenrod", "yellow", "gold"], 
                     "i":["orange", "tan", "orangered", "peru"], 
                     "z":["red", "pink", "firebrick", "salmon"], 
                     "Y":["peachpuff", "chocolate", "coral", "darkred"],}
            bands = ["g", "r", "i", "z", "Y"]
            # Select physical fluxes, discard bad magnitude (=99) 
            for A in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", 
                      "12"]:
                f_aper = "FLUX_APER_{0}".format(A)
                m_aper = "MAG_APER_{0}".format(A)
                tab = tab.loc[((tab[f_aper] > 0) & (tab[m_aper] < 99))]
                tab = tab.loc[((tab[f_aper] > 0) & (tab[m_aper] < 99))]
            tab.reset_index(drop=False, inplace=True)
            # As there are 12 apertures, then plot them in groups of 4. Use 
            # different scales of the colors for each group
            for idx, x in enumerate(bands):
                # APER_1 to APER_4
                aux_d = []
                aux_f = []
                for A in ["1", "2", "3", "4"]:
                    f_aper = "FLUX_APER_{0}".format(A)
                    m_aper = "MAG_APER_{0}".format(A)
                    tmp_f = np.log10(tab.loc[tab["BAND"] == x, f_aper].values)
                    tmp_f *= -2.5
                    tmp_f += 30
                    aux_f.append(tmp_f)
                    r = tmp_f - tab.loc[(tab["BAND"] == x), m_aper].values
                    aux_d += list(r)
                avg_d = np.mean(np.array(aux_d))
                std_d = np.std(np.array(aux_d))
                # Apertures 1 to 4
                kw.update({"c": color[x][3]})
                ax[0, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_1"],
                                   aux_f[0], label="APER_1", **kw)
                kw.update({"c": color[x][2]})
                ax[0, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_2"],
                                   aux_f[1], label="APER_2", **kw)
                kw.update({"c": color[x][1]})
                ax[0, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_3"],
                                   aux_f[2], label="APER_3", **kw)
                kw.update({"c": color[x][0]})
                ax[0, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_4"],
                                   aux_f[3], label="APER_4", **kw)
                ax[0, idx].legend(loc="lower right", fancybox=True, fontsize=8,
                                  markerscale=4) 
                txt = r"Avg Diff: {0:.2E} $\pm$ {1:.2E}".format(
                    decimal.Decimal(avg_d), decimal.Decimal(std_d))
                ax[0, idx].text(0.01, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[0, idx].transAxes)
                ax[0, idx].grid(alpha=0.5)
                # APER_5 to APER_8
                del aux_d
                aux_d = []
                aux_f = []
                for A in ["5", "6", "7", "8"]:
                    f_aper = "FLUX_APER_{0}".format(A)
                    m_aper = "MAG_APER_{0}".format(A)
                    tmp_f = np.log10(tab.loc[tab["BAND"] == x, f_aper].values)
                    tmp_f *= -2.5
                    tmp_f += 30
                    aux_f.append(tmp_f)
                    r = tmp_f - tab.loc[(tab["BAND"] == x), m_aper].values
                    aux_d += list(r)
                avg_d = np.mean(np.array(aux_d))
                std_d = np.std(np.array(aux_d))
                # Apertures 5 to 8
                kw.update({"c": color[x][3]})
                ax[1, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_5"],
                                   aux_f[0], label="APER_5", **kw)
                kw.update({"c": color[x][2]})
                ax[1, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_6"],
                                   aux_f[1], label="APER_6", **kw)
                kw.update({"c": color[x][1]})
                ax[1, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_7"],
                                   aux_f[2], label="APER_7", **kw)
                kw.update({"c": color[x][0]})
                ax[1, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_8"],
                                   aux_f[3], label="APER_8", **kw)
                ax[1, idx].legend(loc="lower right", fancybox=True, fontsize=8,
                                  markerscale=4) 
                txt = r"Avg Diff: {0:.2E} $\pm$ {1:.2E}".format(
                    decimal.Decimal(avg_d), decimal.Decimal(std_d))
                ax[1, idx].text(0.01, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[1, idx].transAxes)
                ax[1, idx].grid(alpha=0.5)
                # APER_9 to APER_12
                del aux_d
                aux_d = []
                aux_f = []
                for A in ["9", "10", "11", "12"]:
                    f_aper = "FLUX_APER_{0}".format(A)
                    m_aper = "MAG_APER_{0}".format(A)
                    tmp_f = np.log10(tab.loc[tab["BAND"] == x, f_aper].values)
                    tmp_f *= -2.5
                    tmp_f += 30
                    aux_f.append(tmp_f)
                    r = tmp_f - tab.loc[(tab["BAND"] == x), m_aper].values
                    aux_d += list(r)
                avg_d = np.mean(np.array(aux_d))
                std_d = np.std(np.array(aux_d))
                # Apertures 9 to 12
                kw.update({"c": color[x][3]})
                ax[2, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_9"],
                                   aux_f[0], label="APER_9", **kw)
                kw.update({"c": color[x][2]})
                ax[2, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_10"],
                                   aux_f[1], label="APER_10", **kw)
                kw.update({"c": color[x][1]})
                ax[2, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_11"],
                                   aux_f[2], label="APER_11", **kw)
                kw.update({"c": color[x][0]})
                ax[2, idx].scatter(tab.loc[tab["BAND"] == x, "MAG_APER_12"],
                                   aux_f[3], label="APER_12", **kw)
                ax[2, idx].legend(loc="lower right", fancybox=True, fontsize=8,
                                  markerscale=4) 
                txt = r"Avg Diff: {0:.2E} $\pm$ {1:.2E}".format(
                    decimal.Decimal(avg_d), decimal.Decimal(std_d))
                ax[2, idx].text(0.01, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[2, idx].transAxes)
                ax[2, idx].grid(alpha=0.5)
                ax[2, idx].set_xlabel(r"MAG")
            # Set minor ticks
            for ax_row in ax:
                for ax_col_idx in range(ax_row.shape[0]):
                    # Use Auto Minor Locator
                    minorLocator_x = AutoMinorLocator()
                    ax_row[ax_col_idx].xaxis.set_minor_locator(minorLocator_x)
                    minorLocator_y = AutoMinorLocator()
                    ax_row[ax_col_idx].yaxis.set_minor_locator(minorLocator_y)
                    # Invert axis
                    ax_row[ax_col_idx].invert_xaxis()
                    ax_row[ax_col_idx].invert_yaxis()
                    # Rasterize
                    ax_row[ax_col_idx].set_rasterization_zorder(-10)
                    # ax_row[ax_col_idx].tick_params(axis="both", #labelsize=7,
                    #                                bottom="on")
            
            #
            ax[0, 0].set_title("g-band", color="green")
            ax[0, 1].set_title("r-band", color="gold")
            ax[0, 2].set_title("i-band", color="orange")
            ax[0, 3].set_title("z-band", color="red")
            ax[0, 4].set_title("Y-band", color="coral")
            #
            ax[0, 0].set_ylabel(r"-2.5$\,\log_{10}$(FLUX$_{APER\ 1-4}$)+30")
            ax[1, 0].set_ylabel(r"-2.5$\,\log_{10}$(FLUX$_{APER\ 5-8}$)+30")
            ax[2, 0].set_ylabel(r"-2.5$\,\log_{10}$(FLUX$_{APER\ 9-12}$)+30")
            # Title
            supt = "Comparing db MAG vs magnitude from FLUX (zero point=30)"
            supt += ", using a sample of ~4e5 objects. Set of apertures"
            plt.suptitle(supt, color="royalblue", weight="medium")
            # Spacing
            plt.subplots_adjust(left=0.05, bottom=0.06, right=0.98, top=0.92,
                                wspace=0.22, hspace=0.2)
            # Save 
            if True:
                outname = "MAG_FLUX_compare_set2.png"
                plt.savefig(outname, dpi=400, facecolor="w", edgecolor="w",
                            orientation="portrait", papertype=None, 
                            format="png", transparent=False, bbox_inches=None, 
                            pad_inches=0.1, frameon=None)
            plt.show()
            #
            #
            #
        #
        # Not used: MAG vs MAGERR
        #
        if False:
            plt.close("all")
            fig, ax = plt.subplots(4, 5, figsize=(15, 8))
            # Second set: AUTO, PSF, PETRO, ISO vs its ERRORS
            kw = {
                "marker":".",
                "s": 30,
                "alpha":0.8,
                "edgecolors":"none",
                }
            tab = self.read(m + err_m)
            tab.dropna(subset=["MAG_AUTO", "MAGERR_AUTO", 
                               "MAG_PSF", "MAGERR_PSF",
                               "MAG_MODEL", "MAGERR_MODEL",
                               "MAG_DETMODEL", "MAGERR_DETMODEL"], 
                               how="any", inplace=True)
            # Set colors and bands
            color = {"g":"green", "r":"gold", "i":"orange", "z":"red", 
                     "Y":"coral"}
            bands = ["g", "r", "i", "z", "Y"]
            # Cut the bad magnitudes = 99
            tab = tab.loc[((tab["MAG_AUTO"] < 99) & 
                          (tab["MAG_PSF"] < 99) &
                          (tab["MAG_MODEL"] < 99) &
                          (tab["MAG_DETMODEL"] < 99))]
            tab.reset_index(drop=False, inplace=True)
            for idx, x in enumerate(bands): 
                kw.update({"c": color[x]})
                # *_AUTO
                ax[0, idx].scatter(tab.loc[tab["BAND"] == x, "MAGERR_AUTO"],
                                   tab.loc[tab["BAND"] == x, "MAG_AUTO"],
                                   label="AUTO", **kw)
                ax[0, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                # *_PSF
                ax[1, idx].scatter(tab.loc[tab["BAND"] == x, "MAGERR_PSF"],
                                   tab.loc[tab["BAND"] == x, "MAG_PSF"],
                                   label="PSF", **kw)
                ax[1, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                # *_MODEL
                ax[2, idx].scatter(tab.loc[tab["BAND"] == x, "MAGERR_MODEL"],
                                   tab.loc[tab["BAND"] == x, "MAG_MODEL"],
                                   label="MODEL", **kw)
                ax[2, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                # *_DETMODEL
                ax[3, idx].scatter(tab.loc[tab["BAND"] == x, "MAGERR_DETMODEL"],
                                   tab.loc[tab["BAND"] == x, "MAG_DETMODEL"],
                                   label="DETMODEL", **kw)
                ax[3, idx].legend(loc="lower right", fancybox=True, fontsize=8) 
                # ax[3, idx].set_xlabel(r"$\log_{10}$(MAGERR)")
                ax[3, idx].set_xlabel(r"MAGERR")
            for ax_row in ax:
                for ax_col_idx in range(ax_row.shape[0]):
                    # Use Auto Minor Locator
                    minorLocator_x = AutoMinorLocator()
                    ax_row[ax_col_idx].xaxis.set_minor_locator(minorLocator_x)
                    minorLocator_y = AutoMinorLocator()
                    ax_row[ax_col_idx].yaxis.set_minor_locator(minorLocator_y)
                    # ax_row[ax_col_idx].tick_params(axis="both", #labelsize=7,
                    #                                bottom="on")
            ax[0, 0].set_title("g-band", color="green")
            ax[0, 1].set_title("r-band", color="gold")
            ax[0, 2].set_title("i-band", color="orange")
            ax[0, 3].set_title("z-band", color="red")
            ax[0, 4].set_title("Y-band", color="coral")
            #
            ax[0, 0].set_ylabel(r"MAG")
            ax[1, 0].set_ylabel(r"MAG")
            ax[2, 0].set_ylabel(r"MAG")
            ax[3, 0].set_ylabel(r"MAG")
            # Title
            plt.suptitle("Comparing MAG vs its errors, linear scale",
                         color="royalblue")
            # Spacing
            plt.subplots_adjust(left=0.05, bottom=0.06, right=0.98, top=0.92,
                                wspace=0.22, hspace=0.2)
            # Save 
            if True:
                outname = "mag_err_linear.png"
                plt.savefig(outname, dpi=400, facecolor="w", edgecolor="w",
                            orientation="portrait", papertype=None, format="png",
                            transparent=False, bbox_inches=None, pad_inches=0.1,
                            frameon=None)
            plt.show()
        #df_m = self.read(m)
    
    def magerr_distrib(self):
        err_m = ['MAGERR_APER_1', 'MAGERR_APER_10', 'MAGERR_APER_11', 
                 'MAGERR_APER_12', 'MAGERR_APER_2', 'MAGERR_APER_3', 
                 'MAGERR_APER_4', 'MAGERR_APER_5', 'MAGERR_APER_6',
                 'MAGERR_APER_7', 'MAGERR_APER_8', 'MAGERR_APER_9', 
                 'MAGERR_AUTO', 'MAGERR_PETRO']
        err_m_wavg = ['WAVG_MAGERR_PSF_G', 'WAVG_MAGERR_PSF_I', 
                     'WAVG_MAGERR_PSF_R', 'WAVG_MAGERR_PSF_Y', 
                     'WAVG_MAGERR_PSF_Z']
        # Read tables, for some of them, read only specific columns
        tab = self.read(err_m)
        tabx2 = self.read(None, group=2)
        xcl = self.read(None, group=3)
        # Merge extended classificator table to the MAGERR tables
        xcl_tab = pd.merge(tab, xcl, how="inner", on=["COADD_OBJECT_ID"])
        xcl_tabx2 = pd.merge(tabx2, xcl, how="inner", on=["COADD_OBJECT_ID"])
        print("XMATCH with ExtClass: {0} and {1}".format(len(xcl_tab.index),
              len(xcl_tabx2.index)))
        # Drop all NaN and ERRMAG=99
        max_MAGERR = 2
        tab.dropna(how="any", inplace=True)
        for i in err_m:
            tab = tab.loc[(tab[i] < max_MAGERR)]
        tab.reset_index(drop=False, inplace=True)
        tabx2.dropna(subset=err_m_wavg,
                     how="any", inplace=True)
        for j in err_m_wavg:
            tabx2 = tabx2.loc[(tabx2[j] < max_MAGERR)]
        tabx2.reset_index(drop=False, inplace=True)
        xcl.dropna(how="any", inplace=True)
        xcl.reset_index(drop=False, inplace=True)
        # Set colors and bands
        color = {"g":"green", "r":"gold", "i":"orange", "z":"red", 
                 "Y":"coral"}
        bands = ["g", "r", "i", "z", "Y"]
        plt.close("all")
        fig, ax = plt.subplots(4, 5, figsize=(15, 8))
        kw = {
            "alpha": 0.7,
            "lw": 2,
            }
        #
        # MAGERR_APER
        #
        if False:
            for ind, b in enumerate(bands):
                kw.update({"color": color[b],})
                print(color[b])
                # MAGERR_APER 1-4, 5-8, 9-12
                # for row, a in enumerate(["1", "2", "3", "4"]):
                # for row, a in enumerate(["5", "6", "7", "8"]):
                # for row, a in enumerate(["9", "10", "11", "12"]):
                for row, a in enumerate(["1", "2", "3", "4"]):
                    kap = "MAGERR_APER_{0}".format(a)
                    t1 = tab.loc[tab["BAND"] == b, kap]
                    weights = np.ones_like(t1.values) / t1.values.shape[0]
                    hist, bin_edges = np.histogram(t1, bins="auto")
                    ax[row, ind].hist(t1, bins=hist.size, weights=weights, 
                                    histtype="step", 
                                    label= "APER_{0}".format(a), 
                                    **kw)
                    txt = r"APER_{2} Avg/Std: {0:.2f}/{1:.2f}".format(
                        np.mean(t1), np.std(t1), a)
                    ax[row, ind].legend(loc="lower right", fancybox=True, 
                                      fontsize=8,
                                      markerscale=4) 
                    ax[row, ind].text(0.02, 0.9, txt, fontsize=9, 
                                    fontweight="semibold", 
                                    transform=ax[row, ind].transAxes)
                ax[3, ind].set_xlabel(r"MAGERR")
                # Set axis limits
                ax[0, ind].set_xlim([0, 1.])
                ax[1, ind].set_xlim([0, 1.])
                ax[2, ind].set_xlim([0, 1.])
                ax[3, ind].set_xlim([0, 1.])
                #
            for ax_row in ax:
                for ax_col_idx in range(ax_row.shape[0]):
                    # Use Auto Minor Locator
                    minorLocator_x = AutoMinorLocator()
                    ax_row[ax_col_idx].xaxis.set_minor_locator(minorLocator_x)
                    minorLocator_y = AutoMinorLocator()
                    ax_row[ax_col_idx].yaxis.set_minor_locator(minorLocator_y)
            ax[0, 0].set_title("g-band", color="green")
            ax[0, 1].set_title("r-band", color="gold")
            ax[0, 2].set_title("i-band", color="orange")
            ax[0, 3].set_title("z-band", color="red")
            ax[0, 4].set_title("Y-band", color="coral")
            ax[0, 0].set_ylabel(r"N")
            ax[1, 0].set_ylabel(r"N")
            ax[2, 0].set_ylabel(r"N")
            # Title
            supt = "Selecting: MAGERR < {0}".format(max_MAGERR)
            supt += " (MAGERR >> {0} exists!)".format(max_MAGERR)
            supt += " for a sample of ~4e5 objects"
            plt.suptitle(supt,color="royalblue", weight="medium")

            # Spacing
            plt.subplots_adjust(left=0.05, bottom=0.06, right=0.98, top=0.92,
                                wspace=0.25, hspace=0.2)

            # Save 
            if False:
                outname = "MAGERR_distrib_set2.png"
                plt.savefig(outname, dpi=400, facecolor="w", edgecolor="w",
                            orientation="portrait", papertype=None, 
                            format="png", transparent=False, bbox_inches=None, 
                            pad_inches=0.1, frameon=None)
            plt.show()
            #
            #
            #
        if False:
            for ind, b in enumerate(bands):
                kw.update({"color": color[b],})
                print(color[b])
                # MAGERR_AUTO
                t1 = tab.loc[tab["BAND"] == b, "MAGERR_AUTO"]
                weights = np.ones_like(t1.values) / t1.values.shape[0]
                # normed gives sum=1 if ins width is 1
                hist, bin_edges = np.histogram(t1, bins="auto")
                ax[0, ind].hist(t1, bins=hist.size, weights=weights, 
                                histtype="stepfilled", label= "AUTO", **kw)
                ax[0, ind].legend(loc="lower right", fancybox=True, fontsize=8,
                                  markerscale=4) 
                txt = r"Range/Avg: {0:.2f}/{1:.2f}".format(
                    np.ptp(t1), np.mean(t1))
                ax[0, ind].text(0.02, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[0, ind].transAxes)
                # MAGERR_PETRO
                t1 = tab.loc[tab["BAND"] == b, "MAGERR_PETRO"]
                weights = np.ones_like(t1.values) / t1.values.shape[0]
                # normed gives sum=1 if ins width is 1
                hist, bin_edges = np.histogram(t1, bins="auto")
                ax[1, ind].hist(t1, bins=hist.size, weights=weights, 
                                histtype="stepfilled", **kw)
                ax[1, ind].legend(loc="lower right", fancybox=True, fontsize=8,
                                  markerscale=4) 
                txt = r"Range/Avg: {0:.2f}/{1:.2f}".format(
                    np.ptp(t1), np.mean(t1))
                ax[1, ind].text(0.02, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[1, ind].transAxes)
                # WAVG_MAGERR_PSF
                aux_b = "WAVG_MAGERR_PSF_{0}".format(b.upper())  
                t1 = tabx2[aux_b]
                weights = np.ones_like(t1.values) / t1.values.shape[0]
                hist, bin_edges = np.histogram(t1, bins="auto")
                ax[2, ind].hist(t1, bins=hist.size, weights=weights, 
                                histtype="stepfilled", **kw)
                ax[2, ind].legend(loc="lower right", fancybox=True, fontsize=8,
                                  markerscale=4) 
                txt = r"Range/Avg: {0:.2f}/{1:.2f}".format(
                    np.ptp(t1), np.mean(t1))
                ax[2, ind].text(0.02, 0.9, txt, fontsize=9, 
                                fontweight="semibold", 
                                transform=ax[2, ind].transAxes,
                                multialignment="right")
                ax[2, ind].set_xlabel(r"MAGERR")
                # Set axis limits
                ax[0, ind].set_xlim([0, 1.])
                ax[1, ind].set_xlim([0, 1.])
                ax[2, ind].set_xlim([0, 0.2])
                #
            for ax_row in ax:
                for ax_col_idx in range(ax_row.shape[0]):
                    # Use Auto Minor Locator
                    minorLocator_x = AutoMinorLocator()
                    ax_row[ax_col_idx].xaxis.set_minor_locator(minorLocator_x)
                    minorLocator_y = AutoMinorLocator()
                    ax_row[ax_col_idx].yaxis.set_minor_locator(minorLocator_y)
            ax[0, 0].set_title("g-band", color="green")
            ax[0, 1].set_title("r-band", color="gold")
            ax[0, 2].set_title("i-band", color="orange")
            ax[0, 3].set_title("z-band", color="red")
            ax[0, 4].set_title("Y-band", color="coral")
            ax[0, 0].set_ylabel(r"N")
            ax[1, 0].set_ylabel(r"N")
            ax[2, 0].set_ylabel(r"N")
            # Title
            supt = "Selecting: MAGERR < {0}".format(max_MAGERR)
            supt += " (MAGERR >> {0} exists!)".format(max_MAGERR)
            supt += " for a sample of ~4e5 objects"
            # supt += " The xmatch with WAVG Extended Classificator gets"
            # supt += " just {0} IDs in total".format(len(xcl_tab.index) + 
            #                                   len(xcl_tabx2.index))
            plt.suptitle(supt,color="royalblue", weight="medium")

            # Spacing
            plt.subplots_adjust(left=0.05, bottom=0.06, right=0.98, top=0.92,
                                wspace=0.25, hspace=0.2)

            # Save 
            if True:
                outname = "MAGERR_distrib_set1.png"
                plt.savefig(outname, dpi=400, facecolor="w", edgecolor="w",
                            orientation="portrait", papertype=None, 
                            format="png", transparent=False, bbox_inches=None, 
                            pad_inches=0.1, frameon=None)
            plt.show()
    
    def mag_distrib(self):
        #
        # MAG distributions, cutting on MAG 22 for stars and 23 for galaxies,
        # because og Keith Bechtol Star/Gal classificator
        #
        

    def rad_profile(self):
        """ Create a way to compare profiles and select by classificator
        """
        f = ['FLUX_APER_1', 'FLUX_APER_10', 'FLUX_APER_11', 
             'FLUX_APER_12', 'FLUX_APER_2', 'FLUX_APER_3', 
             'FLUX_APER_4', 'FLUX_APER_5', 'FLUX_APER_6', 
             'FLUX_APER_7', 'FLUX_APER_8', 'FLUX_APER_9',]
        tab = self.read(f)
        #
        plt.close("all")
        fig, ax = plt.subplots(1, 1, figsize=(8, 8))
        kw = {
            "marker":"*",
            "s": 15,
            "alpha":0.5,
            "edgecolors":None,
            }
        # Set colors and bands
        color = {"g":"green", "r":"gold", "i":"orange", "z":"red", 
                 "Y":"coral"}
        bands = ["g", "r", "i", "z", "Y"]
        for idx, b in enumerate(bands):
            kw.update({"c": color[b]})
            N1 = len(tab.loc[tab["BAND"] == b, "FLUX_APER_1"].index)
            r1 = np.ones((N1))
            ax.scatter(r1, tab.loc[tab["BAND"] == b, "FLUX_APER_1"],
                       **kw)
            ax.scatter(r1*2, tab.loc[tab["BAND"] == b, "FLUX_APER_2"],
                       **kw)
            ax.scatter(r1*3, tab.loc[tab["BAND"] == b, "FLUX_APER_3"],
                       **kw)
            ax.scatter(r1*4, tab.loc[tab["BAND"] == b, "FLUX_APER_4"],
                       **kw)
            ax.scatter(r1*5, tab.loc[tab["BAND"] == b, "FLUX_APER_5"],
                       **kw)
            ax.scatter(r1*6, tab.loc[tab["BAND"] == b, "FLUX_APER_6"],
                       **kw)
            ax.scatter(r1*7, tab.loc[tab["BAND"] == b, "FLUX_APER_7"],
                       **kw)
            ax.scatter(r1*8, tab.loc[tab["BAND"] == b, "FLUX_APER_8"],
                       **kw)
            ax.scatter(r1*9, tab.loc[tab["BAND"] == b, "FLUX_APER_9"],
                       **kw)
            ax.scatter(r1*10, tab.loc[tab["BAND"] == b, "FLUX_APER_10"],
                       **kw)
            ax.scatter(r1*11, tab.loc[tab["BAND"] == b, "FLUX_APER_11"],
                       **kw)
            ax.scatter(r1*12, tab.loc[tab["BAND"] == b, "FLUX_APER_12"],
                       **kw)
            # ax.set_ylim([0, 40])
        plt.show()

if __name__ == "__main__":
    print(sys.version)

    B = Bole()
    

    logging.warning("Exiting")
    exit()
    
    B.magerr_distrib()
    B.comp_flux_mag()
    B.rad_profile()

