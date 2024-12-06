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

#include "TCmsCanvas.H"

#include <RtypesCore.h>
//OLD #include <TColor.h>
#include <TH1.h>

#include <TStyle.h>

#include <string>


namespace cmsstyle {

// Some global variables (do not access directly, use the corresponding methods
// to access them or change them!

std::string cms_lumi = "Run 2, 138 fb^{#minus1}";
std::string cms_energy = "13 TeV";

std::string cmsText = "CMS";
std::string extraText = "Preliminary";

TStyle *cmsStyle = nullptr;

std::vector<Int_t> usingPalette2D; // To define a color palette for 2-D histograms

Float_t lumiTextSize = 0.6; // text sizes and text offsets with respect to the top frame in unit of the top margin size
Float_t lumiTextOffset = 0.2;
Float_t cmsTextSize = 0.75;
Float_t cmsTextOffset = 0.1;

std::string useCmsLogo = "";  // To draw the CMS Logo (filename with path must be provided, may be relative to $CMSSTYLE_DIR)

//OLD Bool_t writeExtraText = kTRUE;  // For the extra and addtional text

Font_t cmsTextFont = 61;  // default is helvetic-bold
Font_t extraTextFont = 52;  // default is helvetica-italics
Font_t additionalInfoFont = 42;

std::vector<std::string> additionalInfo;  ///< For extra info, text set under the extra text, for in-frame descriptor.

Float_t extraOverCmsTextSize = 0.76; // ratio of 'CMS' and extra text size

/// Method to setup the style for the ROOT session!
/// Arguments:
///    force; allows to force the style within the ROOT seassion.
void setCMSStyle (bool force=kTRUE);

/// Method to access the CMSStyle variable. It should be easier to access the
/// gROOT->gStyle pointer after setting the CMSStyle, but in case.
TStyle *getCMSStyle (void) {return cmsStyle;}


// ///////////////////////////////////////////////
// Configuration methods
// ///////////////////////////////////////////////

/// This method allows to reset all the values for the CMS-related dataset
/// descriptors to the default.
///
void ResetCmsDescriptors (void);

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


/// This allows to set the location of the file with the CMS Logo in case we
/// want to use that instead of the "CMS" text.
/// When not set (default), the text version is written.
///
/// Arguments:
///    filename: path and filename of the file to be drawn. It can be relative to
///              the CMSSTYLE_DIR path (when set).
void SetCmsLogoFilename (const std::string &filename);

/// This allows to set the extra text. If set to an empty string, nothing
/// extra is written.
///
/// Arguments:
///    text: string to be used as extra text. Empty string means "no extra text",
///          "p" is shortcut for Preliminary (default),
///          "s" is shortcut for Simulation
///          "su" is shortcut for Supplementary
///          "wip" is shortcut for "Work in progress"
///          "pw" is shortcut for "Private work (CMS data)"
///
/// The shortcuts are provided to the recommended values explained in
///     https://cms-analysis.docs.cern.ch/guidelines/plotting/general/#cms-label-requirements
///
/// Note that combinations are possibles, but not with the shortcuts! i.e. to
/// write "Simulation Preliminary" the only text value is the full expression.
///
/// Furthermore, when "Private" is included in the text, the CMS logo is not DRAWN/WRITTEN!
///
void SetExtraText (const std::string &text);

/// This methods allows to append additional information to be displayed,
/// e.g. a string identifying a region, or selection cuts in an automatic way
/// below the CMS-logo-related information (ExtraText, if any) when that is
/// drawn/written inside the frame.
///
/// Arguments:
///    text: string to be appended as a new line of information.
///
void AppendAdditionalInfo(const std::string &text) {additionalInfo.push_back(text);}

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

/// This method defines and returns the TCmsCanvas (a wrapper for TCanvas) for
/// a normal/basic plot.
///
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
///    scaleLumi (optional): Scaling factor for the luminosity text size. Defaults to 1 (see CMS_lumi method for further details).
///    yTitOffset (optional): Set the value for the Y-axis title offset in case default is not good. Defaults to -999 (ignored)
///
/// Returns:
///    The produced TCmsCanvas. It is created with a new command... calling
///    method takes responsability of its deletion.
///
TCmsCanvas *cmsCanvas (const char *canvName,
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
                       Float_t scaleLumi = 1.0,
                       Float_t yTitOffset = -999);

/// This is the method to draw the "CMS" seal (logo and text) and put the
/// luminosity value.
///
/// Arguments:
///    ppad: The pad where to draw the "CMS" seal
///    iPos (optional): Position of the "CMS" seal. Defaults to 11 (top-left, left-aligned).
///                         Alternatives are 33 (top-right, right-aligned), 22 (center, centered)
///                         and 0x (out of frame, in exceptional cases).
///                     Position is calculated as 10*(alignment 1/2/3) + position (1/2/3 = l/c/r).
///    scaleLumi (optional): Scaling factor for the luminosity text size. Defaults to 1.0
///
void CMS_lumi (TPad *ppad, Int_t iPosX=11, Float_t scaleLumi=1.0);

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

/// This is the method to setup a legend according to the style!
///
/// Arguments:
///    x1: The left position of the legend in NDC (0-1).
///    y1:  The bottom position of the legend in NDC (0-1).
///    x2: The right position of the legend in NDC (0-1).
///    y2: The top position of the legend in NDC (0-1).
///    textSize (optional): The text size of the legend entries. Defaults to 0.04.
///    textFont (optional): The font of the legend entries. Defaults to 42 (helvetica).
///    textColor (optional): The color of the legend entries. Defaults to kBlack.
///    columns (optional): The number of columns in the legend.
///
/// Note that parameters may be override later on.
///
/// Returns:
///    A pointer to the defined TLegend. It is created with a new command, so
///    the calling routine must take care of the deletion.
TLegend *cmsLeg(Float_t x1, Float_t y1, Float_t x2, Float_t y2,
                Float_t textSize=0.04,
                Style_t textFont=42,
                Color_t textColor=kBlack,
                Int_t columns=0);

/// This is a method to write a Text in a simplified and straightforward
/// (i.e. user-friendly) way.
///
/// Arguments:
///    text: Text to be written on the plot.
///    posX: Position in X dimension of the text (in NDC coordinates [0,1]
///    posY: Position in Y dimension of the text (in NDC coordinates [0,1]
///    font: Font to be used for the text
///    align: Code for the alignment of the text with respect to the position
///    size: Size of the font
///
void drawText(const char *text, Float_t posX, Float_t posY, Font_t font, Short_t align, Float_t size);

/// This is a method to draw the CMS logo (that should be set using the
/// corresponding method or on the fly) in a TPad set at the indicated location
/// of the currently used TPad.
///
/// Arguments:
///    canv: CMSCanvas that needs to be used to plot the CMSLogo.
///    x0: X position (in relative dimensions) of the lower-left corner of the logo
///    y0: Y position (in relative dimensions) of the lower-left corner of the logo.
///    x1: X position (in relative dimensions) of the upper-left corner of the logo.
///    y1: Y position (in relative dimensions) of the upper-left corner of the logo.
///    logofile (optional): filename (with path) for the logo picture (see SetCmsLogoFilename for details)
///
void addCmsLogo (TCmsCanvas *canv,Float_t x0, Float_t y0, Float_t x1, Float_t y1, const char *logofile=nullptr);

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
