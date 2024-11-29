/// @file
///
/// This is the main file loading the CMSStyle parameters and methods to be
/// used in ROOT.
///
/// <PRE>
/// Written by O. Gonzalez (2024_11_19)
/// </PRE>

#ifndef CMSSTYLE_CMSSTYLE__H_
#define CMSSTYLE_CMSSTYLE__H_


#include <RtypesCore.h>
#include <TColor.h>
#include <TCanvas.h>
#include <TH1.h>

#include <TStyle.h>

#include <string>


namespace cmsstyle {

// Some global variables:

std::string cms_lumi = "Run 2, 138 fb^{#minus1}";
std::string cms_energy = "13 TeV";

TStyle *cmsStyle = nullptr;

/// Method to setup the style for the ROOT session!
/// Arguments:
///    force; allows to force the style within the ROOT seassion.
void setCMSStyle (bool force=kTRUE);



// ///////////////////////////////////////////////
// Configuration methods
// ///////////////////////////////////////////////

/// This method sets the centre-of-mass energy value and unit to be displayed.
/// Arguments:
///    energy: The centre-of-mass energy value. If 0 the "unit part if the used string)
///    unit: The energy unit. Defaults to "TeV".
///
/// NOTE: This method is probably a bad implementation due to the original implementation of CMSStyle. Using
///
///    cms_energy = "13.6 TeV";
///
/// would be the actual way to go!
void SetEnergy (float energy, const std::string &unit="TeV");




/// Returns the maximum value associated to the objects that are going to be
/// plotted.
///
/// Arguments:
///    objs: vector with the pointers to the objects to be drawn (or the ones including to
///          check the maximum)
///
Float_t cmsReturnMaxY (const std::vector<TObject *> objs);


// ///////////////////////////////////////////////
// Plotting and related methods
// ///////////////////////////////////////////////

/// This method defines and returns the TCanvas for a normal/basic plot.
/// Arguments:
///    canvName: Name of the canvas
///    x_max: The minimum value of the x-axis.
///    y_max: The minimum value of the y-axis.
///    y_max: The maximum value of the y-axis.
///    nameXaxis: The label for the x-axis.
///    nameYaxis: The label for the y-axis.
///    square (optional): Whether to create a square canvas. Defaults to True.
///    iPos (optional): The position of the CMS logo. Defaults to 11 (see CMS_lumi method for further details).
///    extraSpace (optional): Additional space to add to the left margin to fit labels. Defaults to 0.
///    with_z_axis (optional): Whether to include a z-axis for 2D histograms. Defaults to False.
///    scaleLumi (optional): Scaling factor for the luminosity text size. Defaults to 0.75 (see CMS_lumi method for further details).
///    yTitOffset (optional): Set the value for the Y-axis title offset in case default is not good. Defaults to -999 (ignored)
///
/// Returns:
///    The produced TCanvas. It is created with a new command... calling
///    method takes responsability of its deletion.
///
TCanvas *cmsCanvas (const char *canvName,
                    Float_t x_min,
                    Float_t x_max,
                    Float_t y_min,
                    Float_t y_max,
                    const char *nameXaxis,
                    const char *nameYaxis,
                    Bool_t square = kTRUE,
                    Int_t iPos = 11,
                    Float_t extraSpace = 0,
                    Bool_t with_z_axis = kFALSE,
                    Float_t scaleLumi = 0.75,
                    Float_t yTitOffset = -999);

/// This is the method to draw the "CMS" seal (logo and text) and put the
/// luminosity value.
///
/// Arguments:
///    ppad: The pad where to draw the "CMS" seal
///    iPos (optional): Position of the "CMS" seal. Defaults to 11 (top-left, left-aligned).
///                         Alternatives are 33 (top-right, right-aligned), 22 (center, centered)
///                         and 0 (out of frame, in exceptional cases).
///                     Position is calculated as 10*(alignment 1/2/3) + position (1/2/3 = l/c/r).
///    scaleLumi (optional): Scaling factor for the luminosity text size. Defaults to 0.75.
///
void CMS_lumi (TPad *ppad, Int_t iPosX=11, Float_t scaleLumi=0.75);

/// This is a (mostly internal) method to setup the parameters of the provided
/// object in a "serialized" way.
///
/// Arguments:
///    obj: Point to TObject to be configured
///    confs: Map with "methods" to be used to configure the object on the fly.
///           Only some methods are actually supported (see code for details)
///
void setRootObjectProperties (TObject *obj,
                              std::map<std::string,Float_t> confs);

/// This is the basic and most general method to plot things on the plot.
///
/// Arguments:
///    obj: Point to TObject to be drawn
///    option: ROOT-style object
///    confs: Map with "methods" to be used to configure the object on the fly. Only some methods are
///           actually supported (see method setRootObjectProperties for details)
///
void cmsObjectDraw (TObject *obj,
                    Option_t *option = "",
                    std::map<std::string,Float_t> confs = std::map<std::string,Float_t>());

// ///////////////////////////////////////////////
// Modifiers and accesors for the Style or Canvas
// ///////////////////////////////////////////////


/// This method updates the provided TPad or TCanvas. If Update the currently
/// active TPad (gPad) if no argument is provided.
/// Arguments:
///    ppad: pointer to the TPad or TCanvas we want to Update
///
void UpdatePad (TPad *ppad = nullptr);

/// This method returns the FRam object used to define the cmsCanvas (but it
/// can be used also for any TPad).
///
/// Arguments:
///    pcanv: A pointer to the cmsCanvas or TPad.
///
/// Returns:
///    The TH1 framne associated to the definition of the TCanvas.
TH1 *GetcmsCanvasHist (TPad *pcanv);



}  // Namespace cmsstyle
#endif
// //////////////////////////////////////////////////////////////////////
