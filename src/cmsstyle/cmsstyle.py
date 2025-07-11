########################################
# CMS Style                            #
# Authors: CMS, Andrea Malara          #
#          Modified by O. Gonzalez to improve features
#                                  when adding C++ version.
########################################
"""This python module contains the core methods for the usage of the CMSStyle tools.

The cmsstyle library provides a pyROOT-based implementation of the figure
guidelines of the CMS Collaboration.
"""

from __future__ import annotations
import sys

import ROOT as rt
from array import array

import re
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterable
import os

# This global variables for the module should not be accessed directy! Use the utilities below.
cms_lumi = "Run 2, 138 fb^{#minus1}"
cms_energy = "13 TeV"

cmsText = "CMS"
extraText = "Preliminary"

cmsStyle = None

usingPalette2D = None  # To define a color palette for 2-D histograms

lumiTextSize = 0.6  # text sizes and text offsets with respect to the top frame in unit of the top margin size
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffsetX = 0

writeExtraText = True  # For the extra and addtional text

useCmsLogo = ""  # To draw the CMS Logo (filename with path must be provided, may be relative to $CMSSTYLE_DIR)

cmsTextFont = 61  # default is helvetic-bold
extraTextFont = 52  # default is helvetica-italics
additionalInfoFont = 42
additionalInfo = []  # For extra info

# ratio of 'CMS' and extra text size
extraOverCmsTextSize = 0.76

drawLogo = False

# This should be consider CONSTANT! (i.e. do not modify them)
# --------------------------------

# Plots for limits and statistical bands
kLimit68 = rt.TColor.GetColor("#607641")  # Internal band, default set
kLimit95 = rt.TColor.GetColor("#F5BB54")  # External band, default set

kLimit68cms = rt.TColor.GetColor("#85D1FBff")  # Internal band, CMS-logo set
kLimit95cms = rt.TColor.GetColor("#FFDF7Fff")  # External band, CMS-logo set

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def SetEnergy(energy, unit="TeV"):
    """
    Set the centre-of-mass energy value and unit to be displayed.

    Args:
        energy (float): The centre-of-mass energy value. If it is 0, the
                        string for the energy is set to the value of unit.

        unit (str, optional): The energy unit. Defaults to "TeV".
    """
    global cms_energy
    if energy is None or energy == 0:
        cms_energy = unit
    else:
        if abs(energy - 13) < 0.001:
            cms_energy = "13 "
        elif abs(energy - 13.6) < 0.001:
            cms_energy = "13.6 "
        else:
            print("ERROR: Provided energy is not recognized! {}".format(energy))
            cms_energy = "??? "
        cms_energy += unit


# # # #
def SetLumi(lumi, unit="fb", run="Run 2", round_lumi=-1):
    """
    Set the integrated luminosity value and unit to be displayed.

    Args:
        lumi (float): The integrated luminosity value. May be skipped if set to None.
        unit (str, optional): The integrated luminosity unit. Defaults to "fb".
        run (str, optional): The LHC run to which the sample refers to.
        round_lumi (int, optional): Number of decimal digits to present the number. If no 0, 1 nor 2, no rounding is done.
    """
    global cms_lumi

    cms_lumi = ""
    if run is not None and len(run) > 0:  # There is an indication about the run period
        cms_lumi += run

    # The lumi value is the most complicated thing

    if lumi is not None and lumi >= 0:
        if len(cms_lumi) > 0:
            cms_lumi += ", "

        if round_lumi == 0:
            cms_lumi += "{:.0f}".format(lumi)
        elif round_lumi == 1:
            cms_lumi += "{:.1f}".format(lumi)
        elif round_lumi == 2:
            cms_lumi += "{:.2f}".format(lumi)
        else:
            cms_lumi += "{}".format(lumi)

        cms_lumi += " {unit}^{{#minus1}}".format(unit=unit)


# # # #
def SetCmsText(text, font=None, size=None):
    """
    Function that allows to edit the default
    "CMS" string

    Args:
        text (str): The CMS text.
        font (ROOT.Font_t, optional): Font of the CMS Text. If None or 0, it is not changed.
        size (float, optional): Size of the CMS Text. If None or 0, it is not changed.
    """
    global cmsText
    global cmsTextFont
    global cmsTextSize
    cmsText = text

    if font is not None and font != 0:
        cmsTextFont = font

    if size is not None and size != 0:
        cmsTextSize = size


def SetCmsLogoFilename(filename: str):
    global useCmsLogo

    if len(filename) == 0:
        useCmsLogo = ""
        return

    if os.path.isfile(filename):
        useCmsLogo = filename
        return

    cmsstyle_dir = os.getenv("CMSSTYLE_DIR")
    useCmsLogo = ""

    if cmsstyle_dir:
        full_path = os.path.join(cmsstyle_dir, filename)
        if os.path.isfile(full_path):
            useCmsLogo = full_path
            return

    print(
        f"ERROR: Indicated file for CMS Logo: {filename} could not be found!",
        file=sys.stderr,
    )


# # # #
def SetExtraText(text, font=None):
    """
    Set extra text to be displayed next to "CMS", e.g. "Preliminary". If set to an empty string, nothing
    extra is written.

    Args:
        text (str): The extra text. It should be noted that some special nicknames
                    are allowed.
        font (ROOT.Font_t, optional): Font of the extra text. If None or 0, it is not changed.

    The nicknames that could be used take info account the most relevant case (as seen in
    https://cms-analysis.docs.cern.ch/guidelines/plotting/general/#cms-label-requirements
        "p"   -> "Preliminary"
        "s"   -> "Simulation"
        "su"  -> "Supplementary"
        "wip" -> "Work in progress
        "pw"  -> "Private work (CMS data)"
    """
    global extraText
    extraText = text

    if extraText == "p":
        extraText = "Preliminary"
    elif extraText == "s":
        extraText = "Simulation"
    elif extraText == "su":
        extraText = "Supplementary"
    elif extraText == "wip":
        extraText = "Work in progress"
    elif extraText == "pw":
        extraText = "Private work (CMS data)"

    # Now, if the extraText does contain the word "Private", the CMS logo is not DRAWN/WRITTEN

    if "Private" in extraText:
        global cmsText
        global useCmsLogo

        cmsText = ""
        useCmsLogo = ""

    # For the font:
    global extraTextFont
    if font is not None and font != 0:
        extraTextFont = font


# # # #
def ResetAdditionalInfo():
    """
    Reset the additional information to be displayed.
    """
    global additionalInfo
    additionalInfo = []


def AppendAdditionalInfo(text):
    """
    Append additional information to be displayed, e.g. a string identifying a region, or selection cuts.

    Args:
        text (str): The additional information text.
    """
    global additionalInfo
    additionalInfo.append(text)


# # # #
class p6:
    """
    A class to represent the Petroff color scheme with 6 colors.

    Attributes:
    kBlue (int): The color blue.
    kYellow (int): The color yellow.
    kRed (int): The color red.
    kGrape (int): The color grape.
    kGray (int): The color gray.
    kViolet (int): The color violet.
    """

    # ROOT may have defined the colors:
    try:
        kBlue = rt.kP6Blue
        kYellow = rt.kP6Yellow
        kRed = rt.kP6Red
        kGrape = rt.kP6Grape
        kGray = rt.kP6Gray
        if (
            rt.gROOT.GetColor(rt.kP6Violet).GetTitle == "#7a21dd"
        ):  # There was a bug in the first implementation in ROOT
            # (I think no "released" version is affected. 6.34.00 is already OK)
            kViolet = rt.kP6Violet
        else:
            kViolet = rt.TColor.GetColor("#7a21dd")
    except Exception:  # Defining the color scheme by hand
        kBlue = rt.TColor.GetColor("#5790fc")
        kYellow = rt.TColor.GetColor("#f89c20")
        kRed = rt.TColor.GetColor("#e42536")
        kGrape = rt.TColor.GetColor("#964a8b")
        kGray = rt.TColor.GetColor("#9c9ca1")
        kViolet = rt.TColor.GetColor("#7a21dd")


# # # #
class p8:
    """
    A class to represent the Petroff color scheme with 8 colors.

    Attributes:
    kBlue (int): The color blue.
    kOrange (int): The color orange.
    kRed (int): The color red.
    kPink (int): The color pink.
    kGreen (int): The color green.
    kCyan (int): The color cyan.
    kAzure (int): The color azure.
    kGray (int): The color gray.
    """

    # ROOT may have defined the colors:
    try:
        kBlue = rt.kP8Blue
        kOrange = rt.kP8Orange
        kRed = rt.kP8Red
        kPink = rt.kP8Pink
        kGreen = rt.kP8Green
        kCyan = rt.kP8Cyan
        kAzure = rt.kP8Azure
        kGray = rt.kP8Gray
    except Exception:  # Defining the color scheme by hand
        kBlue = rt.TColor.GetColor("#1845fb")
        kOrange = rt.TColor.GetColor("#ff5e02")
        kRed = rt.TColor.GetColor("#c91f16")
        kPink = rt.TColor.GetColor("#c849a9")
        kGreen = rt.TColor.GetColor("#adad7d")
        kCyan = rt.TColor.GetColor("#86c8dd")
        kAzure = rt.TColor.GetColor("#578dff")
        kGray = rt.TColor.GetColor("#656364")


class p10:
    """
    A class to represent the Petroff color scheme with 10 colors.

    Attributes:
    kBlue (int): The color blue.
    kYellow (int): The color yellow.
    kRed (int): The color red.
    kGray (int): The color gray.
    kViolet (int): The color violet.
    kBrown (int): The color brown.
    kOrange (int): The color orange.
    kGreen (int): The color green.
    """

    # ROOT may have defined the colors:
    try:
        kBlue = rt.kP10Blue
        kYellow = rt.kP10Yellow
        kRed = rt.kP10Red
        kGray = rt.kP10Gray
        kViolet = rt.kP10Violet
        kBrown = rt.kP10Brown
        kOrange = rt.kP10Orange
        kGreen = rt.kP10Green
        kAsh = rt.kP10Ash
        kCyan = rt.kP10Cyan
    except Exception:
        kBlue = rt.TColor.GetColor("#3f90da")
        kYellow = rt.TColor.GetColor("#ffa90e")
        kRed = rt.TColor.GetColor("#bd1f01")
        kGray = rt.TColor.GetColor("#94a4a2")
        kViolet = rt.TColor.GetColor("#832db6")
        kBrown = rt.TColor.GetColor("#a96b59")
        kOrange = rt.TColor.GetColor("#e76300")
        kGreen = rt.TColor.GetColor("#b9ac70")
        kAsh = rt.TColor.GetColor("#717581")
        kCyan = rt.TColor.GetColor("#92dadd")


# # # #
def getPettroffColor(color):  # -> EColor
    """This method returns the object (EColor) associated to a given color in the
    previous sets from a given string to identify it.

    Args:
        color (str): Name of the color given as a string, e.g. 'p8.kBlue'
                     Note: If the color name does not contain a "dot" it is assumed to
                     be a ROOT color by name!

    Returns:
        EColor: color associated to the requested color name.
    """
    if "." in color:
        x = color.split(".")
        return getattr(getattr(sys.modules[__name__], x[0]), x[1])

    # We try to identify a ROOT color...
    try:  # Some versions don't identify GetColorByName as a valid method (still used in CMSSW)
        return rt.TColor.GetColorByName(color)
    except Exception:  # We keep for others some basic/common color names
        pass

    if color in (
        "kWhite",
        "kBlack",
        "kGray",
        "kRed",
        "kGreen",
        "kBlue",
        "kYellow",
        "kMagenta",
        "kCyan",
        "kOrange",
        "kSpring",
        "kTeal",
        "kAzure",
        "kViolet",
        "kPink",
    ):
        return getattr(rt, color)
    return None  # Not valid color!


# # # #
def getPettroffColorSet(ncolors):
    """This method returns a list of colors for the given number of colors based on
    the previous sets.

    Args:
        ncolors (int): Number of colors to be set for the list of colors (as a minimum!)

    Returns:
        list: list of colors (using the keywords above!)
    """

    print(ncolors)

    if ncolors < 7:  # Using the collection of P6.
        return [p6.kBlue, p6.kYellow, p6.kRed, p6.kGrape, p6.kGray, p6.kViolet]
    elif ncolors < 9:  # Using the collection of P8.
        return [
            p8.kBlue,
            p8.kOrange,
            p8.kRed,
            p8.kPink,
            p8.kGreen,
            p8.kCyan,
            p8.kAzure,
            p8.kGray,
        ]

    # Using the collection of P10... repeating as needed

    dev = [
        p10.kBlue,
        p10.kYellow,
        p10.kRed,
        p10.kGray,
        p10.kViolet,
        p10.kBrown,
        p10.kOrange,
        p10.kGreen,
        p10.kAsh,
        p10.kCyan,
    ]

    i = 10
    while i < ncolors:
        dev.append(dev[i % 10])
        i += 1
    return dev


# # # #
def CreateAlternativePalette(alpha=1):
    """
    Create an alternative color palette for 2D histograms.

    Args:
        alpha (float, optional): The transparency value for the palette colors. Defaults to 1 (opaque).
    """
    red_values = array("d", [0.00, 0.00, 1.00, 0.70])
    green_values = array("d", [0.30, 0.50, 0.70, 0.00])
    blue_values = array("d", [0.50, 0.40, 0.20, 0.15])
    length_values = array("d", [0.00, 0.15, 0.70, 1.00])
    num_colors = 200
    color_table = rt.TColor.CreateGradientColorTable(
        len(length_values),
        length_values,
        red_values,
        green_values,
        blue_values,
        num_colors,
        alpha,
    )
    global usingPalette2D
    usingPalette2D = [color_table + i for i in range(num_colors)]


# # # #
def SetAlternative2DColor(hist=None, style=None, alpha=1):
    """
    Set an alternative colour palette for a 2D histogram.

    Args:
        hist (ROOT.TH2, optional): The 2D histogram to set the colour palette for.
        style (ROOT.TStyle, optional): The style object to use for setting the palette.
        alpha (float, optional): The transparency value for the palette colours. Defaults to 1 (opaque).
    """
    global usingPalette2D
    if usingPalette2D is None:
        CreateAlternativePalette(alpha=alpha)
    if style is None:  # Using the cmsStyle or, if not set the current style.
        global cmsStyle
        if cmsStyle is not None:
            style = cmsStyle
        else:
            style = rt.gStyle

    style.SetPalette(len(usingPalette2D), array("i", usingPalette2D))

    if hist is not None:
        hist.SetContour(len(usingPalette2D))


# # # #
def SetCMSPalette():
    """
    Set the official CMS colour palette for 2D histograms directly.
    """
    cmsStyle.SetPalette(rt.kViridis)
    # cmsStyle.SetPalette(rt.kCividis)


# # # #
def GetPalette(hist):
    """
    Get the colour palette object associated with a histogram.

    Args:
        hist (ROOT.TH1 or ROOT.TH2): The histogram to get the palette from.

    Returns:
        ROOT.TPaletteAxis: The colour palette object.
    """
    UpdatePad()  # Must update the pad to access the palette
    palette = hist.GetListOfFunctions().FindObject("palette")
    return palette


# # # #
def UpdatePalettePosition(
    hist, canv=None, X1=None, X2=None, Y1=None, Y2=None, isNDC=True
):
    """
    Adjust the position of the color palette for a 2D histogram.

    Args:
        hist (ROOT.TH2): The 2D histogram to adjust the palette for.
        canv (ROOT.TCanvas, optional): The canvas containing the histogram. If provided, the palette position will be adjusted based on the canvas margins.
        X1 (float, optional): The left position of the palette in NDC (0-1) or absolute coordinates.
        X2 (float, optional): The right position of the palette in NDC (0-1) or absolute coordinates.
        Y1 (float, optional): The bottom position of the palette in NDC (0-1) or absolute coordinates.
        Y2 (float, optional): The top position of the palette in NDC (0-1) or absolute coordinates.
        isNDC (bool, optional): Whether the provided coordinates are in NDC (True) or absolute coordinates (False). Defaults to True.
    """
    palette = GetPalette(hist)
    if canv is not None and isNDC:  # Ignoring the provided camvas if units are not NDC!
        # If we provide a TPad/Canvas we use the values for it, EXCEPT if explicit
        # values are provided!
        _ = GetCmsCanvasHist(canv)

        if X1 is None:
            X1 = 1 - canv.GetRightMargin() * 0.95
        if X2 is None:
            X2 = 1 - canv.GetRightMargin() * 0.70
        if Y1 is None:
            Y1 = canv.GetBottomMargin()
        if Y2 is None:
            Y2 = 1 - canv.GetTopMargin()

    suffix = ""
    if isNDC:
        suffix = "NDC"

    if X1 is not None:
        getattr(palette, "SetX1" + suffix)(X1)
    if X2 is not None:
        getattr(palette, "SetX2" + suffix)(X2)
    if Y1 is not None:
        getattr(palette, "SetY1" + suffix)(Y1)
    if Y2 is not None:
        getattr(palette, "SetY2" + suffix)(Y2)


# ######## ########  ########        ######  ######## ##    ## ##       ########
#    ##    ##     ## ##     ##      ##    ##    ##     ##  ##  ##       ##
#    ##    ##     ## ##     ##      ##          ##      ####   ##       ##
#    ##    ##     ## ########        ######     ##       ##    ##       ######
#    ##    ##     ## ##   ##              ##    ##       ##    ##       ##
#    ##    ##     ## ##    ##       ##    ##    ##       ##    ##       ##
#    ##    ########  ##     ##       ######     ##       ##    ######## ########


# Turns the grid lines on (true) or off (false)
def cmsGrid(gridOn):
    """
    Enable or disable the grid mode in the CMSStyle. It could also be done by
    calling the corresponding methods for ROOT.gStyle after setting the style.

    Args:
        gridOn (bool): To indicate whether to sets or unset the Grid on the CMSStyle.
    """

    if cmsStyle is not None:
        cmsStyle.SetPadGridX(gridOn)
        cmsStyle.SetPadGridY(gridOn)
    else:
        print("ERROR: You should set the CMS Style before calling cmsGrid")


# # # #
def UpdatePad(pad=None):
    """Update the indicated pad. If none is provided, update the currently active Pad.

    Args:
        pad (TPad or TCanvas, optional): Pad or Canvas to be updated (gPad if none provided)
    """
    if pad is not None:
        pad.RedrawAxis()
        pad.Modified()
        pad.Update()
    else:
        rt.gPad.RedrawAxis()
        rt.gPad.Modified()
        rt.gPad.Update()


# # # #
def setCMSStyle(force=rt.kTRUE):
    """This method allows to define the CMSStyle defaults.

    Args:
        force (ROOT boolean): boolean passed to the application of the Style in ROOT to force to objects loaded after setting the style.
    """
    global cmsStyle
    if cmsStyle is not None:
        del cmsStyle
    cmsStyle = rt.TStyle("cmsStyle", "Style for P-CMS")
    rt.gROOT.SetStyle(cmsStyle.GetName())
    rt.gROOT.ForceStyle(force)
    # for the canvas:
    cmsStyle.SetCanvasBorderMode(0)
    cmsStyle.SetCanvasColor(rt.kWhite)
    cmsStyle.SetCanvasDefH(600)  # Height of canvas
    cmsStyle.SetCanvasDefW(600)  # Width of canvas
    cmsStyle.SetCanvasDefX(0)  # Position on screen
    cmsStyle.SetCanvasDefY(0)
    cmsStyle.SetPadBorderMode(0)
    cmsStyle.SetPadColor(rt.kWhite)
    cmsStyle.SetPadGridX(False)
    cmsStyle.SetPadGridY(False)
    cmsStyle.SetGridColor(0)
    cmsStyle.SetGridStyle(3)
    cmsStyle.SetGridWidth(1)
    # For the frame:
    cmsStyle.SetFrameBorderMode(0)
    cmsStyle.SetFrameBorderSize(1)
    cmsStyle.SetFrameFillColor(0)
    cmsStyle.SetFrameFillStyle(0)
    cmsStyle.SetFrameLineColor(1)
    cmsStyle.SetFrameLineStyle(1)
    cmsStyle.SetFrameLineWidth(1)
    # For the histo:
    cmsStyle.SetHistLineColor(1)
    cmsStyle.SetHistLineStyle(0)
    cmsStyle.SetHistLineWidth(1)
    cmsStyle.SetEndErrorSize(2)
    cmsStyle.SetMarkerStyle(20)
    cmsStyle.SetMarkerSize(
        1
    )  # Not actually set by the TDR Style, but useful to fix default!
    # For the fit/function:
    cmsStyle.SetOptFit(1)
    cmsStyle.SetFitFormat("5.4g")
    cmsStyle.SetFuncColor(2)
    cmsStyle.SetFuncStyle(1)
    cmsStyle.SetFuncWidth(1)
    # For the date:
    cmsStyle.SetOptDate(0)
    # For the TLegend (added by O. Gonzalez, in case people do not/cannot use cmsLeg)
    cmsStyle.SetLegendTextSize(0.04)
    cmsStyle.SetLegendFont(42)
    # Not avaiable    cmsStyle.SetLegendTextColor(rt.kBlack)
    # Not available for now   cmsStyle.SetLegendFillStyle(0)
    cmsStyle.SetLegendBorderSize(0)
    cmsStyle.SetLegendFillColor(0)
    # For the statistics box:
    cmsStyle.SetOptFile(0)
    cmsStyle.SetOptStat(0)  # To display the mean and RMS:   SetOptStat('mr')
    cmsStyle.SetStatColor(rt.kWhite)
    cmsStyle.SetStatFont(42)
    cmsStyle.SetStatFontSize(0.025)
    cmsStyle.SetStatTextColor(1)
    cmsStyle.SetStatFormat("6.4g")
    cmsStyle.SetStatBorderSize(1)
    cmsStyle.SetStatH(0.1)
    cmsStyle.SetStatW(0.15)
    # Margins:
    cmsStyle.SetPadTopMargin(0.05)
    cmsStyle.SetPadBottomMargin(0.13)
    cmsStyle.SetPadLeftMargin(0.16)
    cmsStyle.SetPadRightMargin(0.02)
    # For the Global title:
    cmsStyle.SetOptTitle(0)
    cmsStyle.SetTitleFont(42)
    cmsStyle.SetTitleColor(1)
    cmsStyle.SetTitleTextColor(1)
    cmsStyle.SetTitleFillColor(10)
    cmsStyle.SetTitleFontSize(0.05)
    # For the axis titles:
    cmsStyle.SetTitleColor(1, "XYZ")
    cmsStyle.SetTitleFont(42, "XYZ")
    cmsStyle.SetTitleSize(0.06, "XYZ")
    cmsStyle.SetTitleXOffset(1.1)  # Changed to fitting larger font
    cmsStyle.SetTitleYOffset(1.35)  # Changed to fitting larger font
    # For the axis labels:
    cmsStyle.SetLabelColor(1, "XYZ")
    cmsStyle.SetLabelFont(42, "XYZ")
    cmsStyle.SetLabelOffset(0.012, "XYZ")
    cmsStyle.SetLabelSize(0.05, "XYZ")
    # For the axis:
    cmsStyle.SetAxisColor(1, "XYZ")
    cmsStyle.SetStripDecimals(True)
    cmsStyle.SetTickLength(0.03, "XYZ")
    cmsStyle.SetNdivisions(510, "XYZ")
    cmsStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    cmsStyle.SetPadTickY(1)
    # Change for log plots:
    cmsStyle.SetOptLogx(0)
    cmsStyle.SetOptLogy(0)
    cmsStyle.SetOptLogz(0)
    # Postscript options:
    cmsStyle.SetPaperSize(20.0, 20.0)
    cmsStyle.SetHatchesLineWidth(2)  # These numbers were preventing hatched histograms!
    cmsStyle.SetHatchesSpacing(1.3)

    # Some additional parameters we need to set as "style"

    if (
        float(".".join(re.split("\\.|/", rt.__version__)[0:2])) >= 6.32
    ):  # Not available before!
        # This change by O. Gonzalez allows to save inside the canvas the
        # informnation about the defined colours.
        rt.TColor.DefinedColors(1)

    # Using the Style.
    cmsStyle.cd()


# # # #
def getCMSStyle():
    """This returns the CMSStyle variable, in case it is required externally,
    although usually it should be accessed via ROOT.gStyle after setting it.
    """
    return cmsStyle


#  ######  ##     ##  ######       ##       ##     ## ##     ## ####
# ##    ## ###   ### ##    ##      ##       ##     ## ###   ###  ##
# ##       #### #### ##            ##       ##     ## #### ####  ##
# ##       ## ### ##  ######       ##       ##     ## ## ### ##  ##
# ##       ##     ##       ##      ##       ##     ## ##     ##  ##
# ##    ## ##     ## ##    ##      ##       ##     ## ##     ##  ##
#  ######  ##     ##  ######       ########  #######  ##     ## ####


def CMS_lumi(pad, iPosX=11, scaleLumi=1):
    """
    Draw the CMS text and luminosity information on the specified pad.

    Args:
        pad (ROOT.TPad): The pad to draw on.
        iPosX (int, optional): The position of the CMS logo. Defaults to 11 (top-left, left-aligned).
                               Set it to 0 to put it outside the box (top left)
        scaleLumi (float, optional): Scale factor for the luminosity text size (default is 1, no scaling).
    """
    relPosX = 0.035
    relPosY = 0.035
    relExtraDY = 1.2
    outOfFrame = int(iPosX / 10) == 0
    alignX_ = max(int(iPosX / 10), 1)
    alignY_ = 1 if iPosX == 0 else 3
    align_ = 10 * alignX_ + alignY_
    H = pad.GetWh() * pad.GetHNDC()
    W = pad.GetWw() * pad.GetWNDC()
    L = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    outOfFrame_posY = 1 - t + lumiTextOffset * t
    pad.cd()

    lumiText = cms_lumi
    if cms_energy != "":
        lumiText += " (" + cms_energy + ")"

    drawText(
        text=lumiText,
        posX=1 - r,
        posY=outOfFrame_posY,
        font=42,
        align=31,
        size=lumiTextSize * t * scaleLumi,
    )

    # Now we go to the CMS message:

    posX_ = 0
    if iPosX % 10 <= 1:
        posX_ = L + relPosX * (1 - L - r)
    elif iPosX % 10 == 2:
        posX_ = L + 0.5 * (1 - L - r)
    elif iPosX % 10 == 3:
        posX_ = 1 - r - relPosX * (1 - L - r)

    posY_ = 1 - t - relPosY * (1 - t - b)

    if outOfFrame:  #  CMS logo and extra text out of the frame
        if (
            len(useCmsLogo) > 0
        ):  # Using CMS Logo instead of the text label (uncommon and discouraged!)
            print(
                "WARNING: Usage of (graphical) CMS-logo outside the frame is not currently supported!"
            )
        #        else {
        if len(cmsText) > 0:
            drawText(cmsText, L, outOfFrame_posY, cmsTextFont, 11, cmsTextSize * t)

            # Checking position of the extraText after the CMS logo text.
            scale = 1
            if W > H:
                scale = H / float(W)  # For a rectangle
            L += 0.043 * (extraTextFont * t * cmsTextSize) * scale

        if len(extraText) > 0:  # Only if something to write
            drawText(
                extraText,
                L,
                outOfFrame_posY,
                extraTextFont,
                align_,
                extraOverCmsTextSize * cmsTextSize * t,
            )

        if len(additionalInfo) > 0:  # This is currently not supported!
            print(
                "WARNING: Additional Info for the CMS-info part outside the frame is not currently supported!"
            )

    else:  # In the frame!
        if len(useCmsLogo) > 0:  # Using CMS Logo instead of the text label
            posX_ = L + 0.045 * (1 - L - r) * W / H
            posY_ = 1 - t - 0.045 * (1 - t - b)
            # Note this is only for TCanvas!
            addCmsLogo(pad, posX_, posY_ - 0.15, posX_ + 0.15 * H / W, posY_)

        else:
            if len(cmsText) > 0:
                drawText(cmsText, posX_, posY_, cmsTextFont, align_, cmsTextSize * t)
                # Checking position of the extraText after the CMS logo text.
                posY_ -= relExtraDY * cmsTextSize * t

            if len(extraText) > 0:  # Only if something to write
                drawText(
                    extraText,
                    posX_,
                    posY_,
                    extraTextFont,
                    align_,
                    extraOverCmsTextSize * cmsTextSize * t,
                )
            else:
                posY_ += relExtraDY * cmsTextSize * t  # Preparing for additional text!

            for ind, tt in enumerate(additionalInfo):
                drawText(
                    tt,
                    posX_,
                    posY_
                    - 0.004
                    - (relExtraDY * extraOverCmsTextSize * cmsTextSize * t / 2 + 0.02)
                    * (ind + 1),
                    additionalInfoFont,
                    align_,
                    extraOverCmsTextSize * cmsTextSize * t,
                )

    UpdatePad(pad)


# # # #
def drawText(text, posX, posY, font, align, size):
    """This method allows to draw a given text with all the provided characteristics.

    Args:
        text (str): text to be written in the Current TPad/TCanvas.
        posX (float): position in X (using NDC) where to place the text.
        posY (float): poisition in Y (using NDC) where to place the text.
        font (Font_t): Font to be used.
        align (int): Alignment code for the text.
        size (float): Size of the text.
    """
    latex = rt.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(rt.kBlack)

    latex.SetTextFont(font)
    latex.SetTextAlign(align)
    latex.SetTextSize(size)
    latex.DrawLatex(posX, posY, text)


# # # #
def addCmsLogo(canv, x0, y0, x1, y1, logofile=None):
    """This is a method to draw the CMS logo (that should be set using the
    corresponding method or on the fly) in a TPad set at the indicated location
    of the currently used TPad.

    Args:
        canv (TCanvas): CMSCanvas that needs to be used to plot the CMSLogo.
        x0 (float): X position (in relative dimensions) of the lower-left corner of the logo
        y0 (float): Y position (in relative dimensions) of the lower-left corner of the logo.
        x1 (float): X position (in relative dimensions) of the upper-left corner of the logo.
        y1 (floar): Y position (in relative dimensions) of the upper-left corner of the logo.
        logofile (str,optional): filename (with path) for the logo picture (see SetCmsLogoFilename for details)
    """

    if logofile is not None:
        SetCmsLogoFilename(logofile)  # Trying to load the picture file!

    if len(useCmsLogo) == 0:
        print(
            "ERROR: Not possible to add the CMS Logo as the file is not properly defined (not found?)"
        )
        return

    # Checking we actually have a TCanvas:

    if canv.Class().GetName() != "TCanvas":  # For now reporting an error!
        print(
            "ERROR: You cannot use a picture for the CMS logo if you do not provide a TCanvas for the plot"
        )
        return

    # Addint a TPad with the picture!

    CMS_logo = rt.TASImage(useCmsLogo)

    oldpad = rt.gPad

    pad_logo = rt.TPad("logo", "logo", x0, y0, x1, y1)
    pad_logo.Draw()
    pad_logo.cd()
    CMS_logo.Draw("X")
    pad_logo.Modified()

    oldpad.cd()
    UpdatePad()  # For gPad


# ########  ##        #######  ######## ######## #### ##    ##  ######         ##     ##    ###     ######  ########   #######   ######
# ##     ## ##       ##     ##    ##       ##     ##  ###   ## ##    ##        ###   ###   ## ##   ##    ## ##     ## ##     ## ##    ##
# ##     ## ##       ##     ##    ##       ##     ##  ####  ## ##              #### ####  ##   ##  ##       ##     ## ##     ## ##
# ########  ##       ##     ##    ##       ##     ##  ## ## ## ##   ####       ## ### ## ##     ## ##       ########  ##     ##  ######
# ##        ##       ##     ##    ##       ##     ##  ##  #### ##    ##        ##     ## ######### ##       ##   ##   ##     ##       ##
# ##        ##       ##     ##    ##       ##     ##  ##   ### ##    ##        ##     ## ##     ## ##    ## ##    ##  ##     ## ##    ##
# ##        ########  #######     ##       ##    #### ##    ##  ######         ##     ## ##     ##  ######  ##     ##  #######   ######


# Create canvas with predefined axix and CMS logo
def cmsCanvas(
    canvName,
    x_min,
    x_max,
    y_min,
    y_max,
    nameXaxis,
    nameYaxis,
    square=True,
    iPos=11,
    extraSpace=0,
    with_z_axis=False,
    scaleLumi=1,
    yTitOffset=None,
):
    """
    Create a canvas with CMS style and predefined axis labels.

    Args:
        canvName (str): The name of the canvas.
        x_min (float): The minimum value of the x-axis.
        x_max (float): The maximum value of the x-axis.
        y_min (float): The minimum value of the y-axis.
        y_max (float): The maximum value of the y-axis.
        nameXaxis (str): The label for the x-axis.
        nameYaxis (str): The label for the y-axis.
        square (bool, optional): Whether to create a square canvas. Defaults to True.
        iPos (int, optional): The position of the CMS logo. Defaults to 11 (top-left, left-aligned). Alternatives are 33 (top-right, right-aligned), 22 (center, centered) and 0 (out of frame, in exceptional cases). Position is calculated as 10*(alignment 1/2/3) + position (1/2/3 = l/c/r).
        extraSpace (float, optional): Additional space to add to the left margin to fit labels. Defaults to 0.
        with_z_axis (bool, optional): Whether to include a z-axis for 2D histograms. Defaults to False.
        scaleLumi (float, optional): Scale factor for the luminosity text size. Default is 1.0 indicating no scale
        yTitOffset (float, optional): Set the value for the Y-axis title offset in case default is not good. [Added by O. Gonzalez]

    Returns:
        ROOT.TCanvas (ROOT.TCanvas): The created canvas.
    """

    # Set CMS style if not set already.
    if cmsStyle is None:
        setCMSStyle()

    # Set canvas dimensions and margins
    W_ref = 600 if square else 800
    H_ref = 600 if square else 600

    W = W_ref
    H = H_ref
    T = 0.07 * H_ref
    B = 0.125 * H_ref  # Changing this to allow more space in X-title (i.e. subscripts)
    L = 0.14 * H_ref  # Changing these to leave more space
    R = 0.04 * H_ref

    canv = rt.TCanvas(canvName, canvName, 50, 50, W, H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetLeftMargin(L / W + extraSpace)
    canv.SetRightMargin(R / W)
    if with_z_axis:
        canv.SetRightMargin(B / W + 0.03)
    canv.SetTopMargin(T / H)
    canv.SetBottomMargin(B / H + 0.02)

    # Draw frame and set axis labels
    h = canv.DrawFrame(x_min, y_min, x_max, y_max)

    if yTitOffset is None:
        y_offset = 1.15 if square else 0.78  # Changed to fitting larger font
    else:
        y_offset = yTitOffset

    h.GetYaxis().SetTitleOffset(y_offset)
    h.GetXaxis().SetTitleOffset(1.05)  # Changed to fitting larger font
    h.GetXaxis().SetTitle(nameXaxis)
    h.GetYaxis().SetTitle(nameYaxis)
    h.Draw("AXIS")

    # Draw CMS logo and update canvas
    CMS_lumi(canv, iPos, scaleLumi=scaleLumi)
    UpdatePad(canv)
    canv.RedrawAxis()
    canv.GetFrame().Draw()
    return canv


# # # #
def GetCmsCanvasHist(canv):
    """
    Get the histogram frame object from a canvas created with cmsCanvas (or any TPad).

    Args:
        canv (ROOT.TCanvas): The canvas to get the histogram frame from (that can be any TPad).

    Returns:
        ROOT.TH1: The histogram frame object.
    """
    return canv.GetListOfPrimitives().FindObject("hframe")


# # # #
def cmsCanvasResetAxes(canv, x_min, x_max, y_min, y_max):
    """
    Reset the axis ranges of a canvas created with cmsCanvas.

    Args:
        canv (ROOT.TCanvas): The canvas to reset the axis ranges for.
        x_min (float): The minimum value of the x-axis.
        x_max (float): The maximum value of the x-axis.
        y_min (float): The minimum value of the y-axis.
        y_max (float): The maximum value of the y-axis.
    """
    GetCmsCanvasHist(canv).GetXaxis().SetRangeUser(x_min, x_max)
    GetCmsCanvasHist(canv).GetYaxis().SetRangeUser(y_min, y_max)


def cmsDiCanvas(
    canvName,
    x_min,
    x_max,
    y_min,
    y_max,
    r_min,
    r_max,
    nameXaxis,
    nameYaxis,
    nameRatio,
    square=True,
    iPos=11,
    extraSpace=0,
    scaleLumi=1,
):
    """
    Create a canvas with CMS style and predefined axis labels, with a ratio pad.

    Args:
        canvName (str): The name of the canvas.
        x_min (float): The minimum value of the x-axis.
        x_max (float): The maximum value of the x-axis.
        y_min (float): The minimum value of the y-axis.
        y_max (float): The maximum value of the y-axis.
        r_min (float): The minimum value of the ratio axis.
        r_max (float): The maximum value of the ratio axis.
        nameXaxis (str): The label for the x-axis.
        nameYaxis (str): The label for the y-axis.
        nameRatio (str): The label for the ratio axis.
        square (bool, optional): Whether to create a square canvas. Defaults to True.
        iPos (int, optional): The position of the CMS text. Defaults to 11 (top-left, left-aligned).
        extraSpace (float, optional): Additional space to add to the left margin to fit labels. Defaults to 0.
        scaleLumi (float, optional): Scale factor for the luminosity text size. Default is 1 that means no scaling.

    Returns:
        ROOT.TCanvas: The created canvas.
    """

    # Set CMS style if not set
    if cmsStyle is None:
        setCMSStyle()

    # Set canvas dimensions and margins
    W_ref = 700 if square else 800
    H_ref = 600 if square else 500
    # Set bottom pad relative height and relative margin
    F_ref = 1.0 / 3.0
    M_ref = 0.03
    # Set reference margins
    T_ref = 0.07
    B_ref = 0.13
    L = 0.15 if square else 0.12
    R = 0.05
    # Calculate total canvas size and pad heights
    W = W_ref
    H = int(H_ref * (1 + (1 - T_ref - B_ref) * F_ref + M_ref))
    Hup = H_ref * (1 - B_ref)
    Hdw = H - Hup
    # references for T, B, L, R
    Tup = T_ref * H_ref / Hup
    Tdw = M_ref * H_ref / Hdw
    Bup = 0.022
    Bdw = B_ref * H_ref / Hdw

    canv = rt.TCanvas(canvName, canvName, 50, 50, W, H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetFrameLineColor(0)
    canv.SetFrameLineWidth(0)
    canv.Divide(1, 2)

    canv.cd(1)
    rt.gPad.SetPad(0, Hdw / H, 1, 1)
    rt.gPad.SetLeftMargin(L)
    rt.gPad.SetRightMargin(R)
    rt.gPad.SetTopMargin(Tup)
    rt.gPad.SetBottomMargin(Bup)

    hup = canv.cd(1).DrawFrame(x_min, y_min, x_max, y_max)
    hup.GetYaxis().SetTitleOffset(extraSpace + (1.1 if square else 0.9) * Hup / H_ref)
    hup.GetXaxis().SetTitleOffset(999)
    hup.GetXaxis().SetLabelOffset(999)
    hup.SetTitleSize(hup.GetTitleSize("Y") * H_ref / Hup, "Y")
    hup.SetLabelSize(hup.GetLabelSize("Y") * H_ref / Hup, "Y")
    hup.GetYaxis().SetTitle(nameYaxis)

    CMS_lumi(rt.gPad, iPos, scaleLumi=scaleLumi)

    canv.cd(2)
    rt.gPad.SetPad(0, 0, 1, Hdw / H)
    rt.gPad.SetLeftMargin(L)
    rt.gPad.SetRightMargin(R)
    rt.gPad.SetTopMargin(Tdw)
    rt.gPad.SetBottomMargin(Bdw)

    hdw = canv.cd(2).DrawFrame(x_min, r_min, x_max, r_max)
    # Scale text sizes and margins to match normal size
    hdw.GetYaxis().SetTitleOffset(extraSpace + (1.0 if square else 0.8) * Hdw / H_ref)
    hdw.GetXaxis().SetTitleOffset(0.9)
    hdw.SetTitleSize(hdw.GetTitleSize("Y") * H_ref / Hdw, "Y")
    hdw.SetLabelSize(hdw.GetLabelSize("Y") * H_ref / Hdw, "Y")
    hdw.SetTitleSize(hdw.GetTitleSize("X") * H_ref / Hdw, "X")
    hdw.SetLabelSize(hdw.GetLabelSize("X") * H_ref / Hdw, "X")
    hdw.SetLabelOffset(hdw.GetLabelOffset("X") * H_ref / Hdw, "X")
    hdw.GetXaxis().SetTitle(nameXaxis)
    hdw.GetYaxis().SetTitle(nameRatio)

    # Set tick lengths to match original (these are fractions of axis length)
    hdw.SetTickLength(hdw.GetTickLength("Y") * H_ref / Hup, "Y")  # ?? ok if 1/3
    hdw.SetTickLength(hdw.GetTickLength("X") * H_ref / Hdw, "X")

    # Reduce divisions to match smaller height (default n=510, optim=kTRUE)
    hdw.GetYaxis().SetNdivisions(505)
    hdw.Draw("AXIS")
    canv.cd(1)
    UpdatePad(canv.cd(1))
    canv.cd(1).RedrawAxis()
    canv.cd(1).GetFrame().Draw()
    return canv


def cmsLeg(
    x1, y1, x2, y2, textSize=0.04, textFont=42, textColor=rt.kBlack, columns=None
):
    """
    Create a legend with CMS style.

    Args:
        x1 (float): The left position of the legend in NDC (0-1).
        y1 (float): The bottom position of the legend in NDC (0-1).
        x2 (float): The right position of the legend in NDC (0-1).
        y2 (float): The top position of the legend in NDC (0-1).
        textSize (float, optional): The text size of the legend entries. Defaults to 0.04.
        textFont (int, optional): The font of the legend entries. Defaults to 42 (helvetica).
        textColor (int, optional): The color of the legend entries. Defaults to kBlack.
        columns (int, optional): The number of columns in the legend.

    Returns:
        ROOT.TLegend: The created legend.
    """
    leg = rt.TLegend(x1, y1, x2, y2, "", "brNDC")
    leg.SetTextSize(textSize)
    leg.SetTextFont(textFont)
    leg.SetTextColor(textColor)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    if columns:
        leg.SetNColumns(columns)
    leg.Draw()
    return leg


# # # #
def addToLegend(leg, *objs):
    """
    Add to the given TLegend the indicated elements (tuples or lists with references to ROOT
    TObjects and the information required by the TLegend).

    Written by O. Gonzalez.
    Args:
        leg (ROOT.TLegend): The legend to add the elements to.
        *objs: any number of arguments with a tuple or list with three elements each,
               being (ROOT.TObject,str,str) where the first is the TObject to add,
               the second the label for the TLegend and the third the identifier for the legend.
    """

    # We simply loop over the elements to

    for xobj in objs:
        leg.AddEntry(*xobj)  # Same as leg.AddEntry(xobj[0],xobj[1],xobj[2])


# # # #
def cmsHeader(
    leg,
    legTitle,
    textAlign=12,
    textSize=0.04,
    textFont=42,
    textColor=rt.kBlack,
    isToRemove=True,
):
    """
    Add a header to a legend with CMS style.

    Args:
        leg (ROOT.TLegend): The legend to add the header to.
        legTitle (str): The title of the header.
        textAlign (int, optional): The alignment of the header text. Defaults to 12 (centered).
        textSize (float, optional): The text size of the header. Defaults to 0.04.
        textFont (int, optional): The font of the header. Defaults to 42 (helvetica).
        textColor (int, optional): The color of the header. Defaults to kBlack.
        isToRemove (bool, optional): Whether to remove the default header and replace it with the new one. Defaults to True.
    """
    header = rt.TLegendEntry(0, legTitle, "h")
    header.SetTextFont(textFont)
    header.SetTextSize(textSize)
    header.SetTextAlign(textAlign)
    header.SetTextColor(textColor)
    if isToRemove:
        leg.SetHeader(legTitle, "C")
        leg.GetListOfPrimitives().Remove(leg.GetListOfPrimitives().At(0))
        leg.GetListOfPrimitives().AddAt(header, 0)
    else:
        leg.GetListOfPrimitives().AddLast(header)


# ########  ########     ###    ##      ##
# ##     ## ##     ##   ## ##   ##  ##  ##
# ##     ## ##     ##  ##   ##  ##  ##  ##
# ##     ## ########  ##     ## ##  ##  ##
# ##     ## ##   ##   ######### ##  ##  ##
# ##     ## ##    ##  ##     ## ##  ##  ##
# ########  ##     ## ##     ##  ###  ###


def cmsDraw(
    h,
    style,
    marker=rt.kFullCircle,
    msize=1.0,
    mcolor=rt.kBlack,
    lstyle=rt.kSolid,
    lwidth=1,
    lcolor=-1,
    fstyle=1001,
    fcolor=rt.kYellow + 1,
    alpha=-1,
):
    """
    Draw a histogram with CMS style.

    Args:
        h (ROOT.TH1 or ROOT.TH2): The histogram to draw.
        style (str): The drawing style (e.g., "HIST", "P", etc.).
        marker (int, optional): The marker style. Defaults to kFullCircle.
        msize (float, optional): The marker size. Defaults to 1.0.
        mcolor (int, optional): The marker color. Defaults to kBlack.
        lstyle (int, optional): The line style. Defaults to kSolid.
        lwidth (int, optional): The line width. Defaults to 1.
        lcolor (int, optional): The line color. If -1, uses the marker color. Defaults to -1.
        fstyle (int, optional): The fill style. Defaults to 1001 (solid).
        fcolor (int, optional): The fill color. Defaults to kYellow+1.
        alpha (float, optional): The transparency value for the fill color (0-1). If -1, uses the default transparency. Defaults to -1.
    """
    h.SetMarkerStyle(marker)
    h.SetMarkerSize(msize)
    h.SetMarkerColor(mcolor)
    h.SetLineStyle(lstyle)
    h.SetLineWidth(lwidth)
    h.SetLineColor(mcolor if lcolor == -1 else lcolor)
    h.SetFillStyle(fstyle)
    h.SetFillColor(fcolor)
    if alpha > 0:
        h.SetFillColorAlpha(fcolor, alpha)

    # We expect this command to be used with an alreasdy-defined canvas.
    prefix = "SAME"
    if "SAME" in style:
        prefix = ""

    h.Draw(prefix + style)
    # This change (by O. Gonzalez) is to put the "SAME" at the beginning so
    # style may override it if needed. It also allows to use "SAMES" just by
    # starting the style with a single S.


def cmsDrawLine(line, lcolor=rt.kRed, lstyle=rt.kSolid, lwidth=2):
    """
    Draw a line with CMS style.

    Args:
        line (ROOT.TLine): The line to draw.
        lcolor (int, optional): The line color. Defaults to kRed.
        lstyle (int, optional): The line style. Defaults to kSolid.
        lwidth (int, optional): The line width. Defaults to 2.
    """
    line.SetLineStyle(lstyle)
    line.SetLineColor(lcolor)
    line.SetLineWidth(lwidth)
    line.Draw("SAME")


# # # #
def cmsObjectDraw(obj, opt="", **kwargs):
    """This method allows to plot the indicated object by modifying optionally the
    configuration of the object itself using named parameters referring to the
    methods to call.

    Examples of use:

            cmsstyle.cmsObjectDraw(hist,'HISTSAME',LineColor=ROOT.kRed,FillColor=ROOT.kRed,FillStyle=3555)
            cmsstyle.cmsObjectDraw(hist,'E',SetLineColor=ROOT.kRed,MarkerStyle=ROOT.kFullCircle)
            cmsstyle.cmsObjectDraw(hist,'SE',SetLineColor=cmsstyle.p6.kBlue,MarkerStyle=ROOT.kFullCircle)

    Written by O. Gonzalez.

    Args:
        obj (ROOT object): Any drawable ROOT object.
        opt (str, optional): The plotting option. It does not need to include SAME as it is prefixed to it. Starting that opt with "S" converts that "SAME" in "SAMES" (e.g. to include the stats box). Using "SAMES" or "SAME" in opt makes the prefix not being used.
        **kwargs (ROOT styling object, optional): Parameter names correspond to object styling method and arguments correspond to stilying ROOT objects: e.g. `SetLineColor=ROOT.kRed`. A method starting with "Set" may omite the "Set" part: i.e. `LineColor=ROOT.kRed`.
    """

    setRootObjectProperties(obj, **kwargs)

    prefix = "SAME"
    if "SAME" in opt:
        prefix = ""
    obj.Draw(prefix + opt)


# # # #
def buildTHStack(histlist, colorlist=None, opt="STACK", **kwargs):
    """This method allows to build a THStack out of a list of histograms and
    configure at the same time the colors to be used with each histogram and
    some possible general configurations.

    Examples of use:

        hs = cmsstyle.buildTHStack([h1,h2,hg])

        hs = cmsstyle.buildTHStack([h1,h2,hg],[cmsstyle.p10.kBrown,cmsstyle.p10.kBlue,cmsstyle.p10.kOrange],"STACK",FillStyle=3005,FillColor=-1,LineColor=-1)

    Written by O. Gonzalez.

    Args:
        histlist (list/tuple): list of histograms to add in order to the THStack to be built!
        colorlist (list/tuple, optional): list of colors to be used as the color for each histogram
        opt (str,optional): option to be used to create the THStack.

        **kwargs (ROOT styling object, optional): Parameter names correspond to
                  object styling method and arguments correspond to stilying ROOT objects:
                  e.g. `SetLineColor=ROOT.kRed`. A method starting with "Set" may omite the
                  "Set" part: i.e. `LineColor=ROOT.kRed`.
                  Note that any color style that is to be changed is adapted in a "per-histogram"
                  mode. Also check the default below! (to avois the default, use NoDefault=None)

    Returns:
        ROOT.THStack: the created THStack.
    """

    if opt is None or len(opt) == 0:
        opt = "STACK"  # The default for using "" or None!

    hstack = rt.THStack("hstack", opt)

    if len(kwargs) == 0:  # If no configuration arguments, we use a default!
        kwargs["FillColor"] = -1  # The colors list is used!
        kwargs["FillStyle"] = 1001

    elif "NoDefault" in kwargs:
        kwargs.clear()  # Nothing is used!

    # If the provided color list is not useful, we get one from Pettroff's sets
    ncolors = 0 if colorlist is None else len(colorlist)
    if ncolors == 0 and len(histlist) > 0:
        # Need to build a set of colors from Petroff's sets!
        ncolors = len(histlist)
        colorlist = getPettroffColorSet(ncolors)

    # Looping over the histograms to generate the THStack

    ihst = 0
    for xhst in histlist:
        # We may modify the histogram... indeed it should be given! When no
        # argument is given, we use FillColor by default for stack histograms
        # (see values for default above inb the code!)

        for xcnf in kwargs.items():
            if xcnf[0] == "SetLineColor" or xcnf[0] == "LineColor":
                xhst.SetLineColor(
                    colorlist[ihst]
                )  # NOTE: FOR THE COLOR WE USE THE VECTOR!
            elif xcnf[0] == "SetFillColor" or xcnf[0] == "FillColor":
                xhst.SetFillColor(colorlist[ihst])
            elif xcnf[0] == "SetMarkerColor" or xcnf[0] == "MarkerColor":
                xhst.SetMarkerColor(colorlist[ihst])

            else:
                setRootObjectProperties(xhst, **{xcnf[0]: xcnf[1]})

        # Adding it!
        hstack.Add(xhst)
        ihst += 1

    return hstack


# # #
def buildAndDrawTHStack(
    objs, leg, reverseleg=True, colorlist=None, stackopt="STACK", **kwargs
):
    """This method allows to build and draw a THStack with a single command.

    Basically it reduces to a single command the calls to buildTHStack, to
    addToLegend and to cmsObjectDraw for the most common case.

    Examples of use:

        hs = cmsstyle.buildAndDrawTHStack([(h2,"Sample 2",'f'),
                                            (h1,"Sample 1",'f'),
                                           (hg,"Sample G",'f')],
                                          plotlegend,True,[cmsstyle.p10.kBrown,cmsstyle.p10.kBlue,cmsstyle.p10.kOrange],"STACK")


    Written by O. Gonzalez.

    Args:
        objs (list/tuple of (ROOT.TH1,str,str) tuples): list of objects, organized as
             tuples containing each of histograms to be added to the THStack with its
             label and option for the legend.
        leg (ROOT.TLegend): legend to which the THStack members may be added.
        reverseleg (bool, optional): whether elements should be added to the legend in reverse order.
        colorlist (list/tuple, optional): list of colors to be used as the color for each histogram.
        stackopt (str,optional): option to define the THStack.
        **kwargs (ROOT styling object, optional): Parameter names correspond to
                  object styling method and arguments correspond to stilying ROOT objects:
                  e.g. `SetLineColor=ROOT.kRed`. A method starting with "Set" may omite the
                  "Set" part: i.e. `LineColor=ROOT.kRed`.

    Returns:
        ROOT.THStack: the created THStack.
    """

    # We get a list with the histogram!
    histlist = [x[0] for x in objs]

    hs = buildTHStack(histlist, colorlist, stackopt, **kwargs)

    # We add the histograms to the legend... perhaps looping in reverse order!
    if reverseleg:
        for xobj in reversed(objs):
            leg.AddEntry(*xobj)
    else:
        for xobj in objs:
            leg.AddEntry(*xobj)

    cmsObjectDraw(hs, "")  # Also drawing it!

    return hs


# # # #
def changeStatsBox(canv, ipos_x1=None, y1pos=None, x2pos=None, y2pos=None, **kwargs):
    """This method allows to obtain the StatsBox from the given Canvas and modify
    its position and, additionally, modify its properties using named keywords
    arguments.

    Written by O. Gonzalez.

    The ipos_x0 may be set to a numeric value in NDC coordinates OR a
    predefined position using a string of the following:

            'tr' -> Drawn in the Top-Right part of the frame including the plot.
            'tl' -> Drawn in the Top-Left part of the frame including the plot.
            'br' -> Drawn in the Bottom-Right part of the frame including the plot.
            'bl' -> Drawn in the Bottom-Left part of the frame including the plot.

    In this case the second coordinate may be used to scale the x-dimension
    (for readability), and the third may be used to scale the y-dimension (usually not needed)

    Examples of use:

            cmsstyle.changeStatsBox(canv,'tr',FillColor=ROOT.kRed,FillStyle=3555)
            cmsstyle.changeStatsBox(canv,'tl',SetTextColor=ROOT.kRed,SetFontSize=0.03)
            cmsstyle.changeStatsBox(canv,'tl',1.2,SetTextColor=ROOT.kRed,SetFontSize=0.03)

    (A method starting with "Set" may omite the "Set" part)

    Args:
        canv (ROOT.TCanvas or ROOT.TPaveStats): canvas to which we modify the stats box (or directly the TPaveStats to change)
        ipos_x1 (str or float): position for the stats box. Use a predefined string of a location or an NDC x coordinate number
        y1pos (float): NDC y coordinate number or a factor to scale the width of the box when using a predefined location.
        x2pos (float): NDC x coordinate number or a factor to scale the height of the box when using a predefined location.
        y2pos (float): NDC y coordinate number or ignored value.
        **kwargs: Arbitrary keyword arguments for mofifying the properties of the stats box using Set methods or similar.

    Returns:
        The Stats Box so it may be access externally.
    """

    stbox = canv
    if canv.Class().GetName() != "TPaveStats":  # Very likely a TPad or TCanvas
        canv.Update()  # To be sure we have created the statistic box
        stbox = canv.GetPrimitive("stats")

        if stbox.Class().GetName() != "TPaveStats":
            raise ReferenceError(
                'ERROR: Trying to change the StatsBox when it has not been enabled... activate it with SetOptStat (and use "SAMES" or equivalent)'
            )

    setRootObjectProperties(stbox, **kwargs)

    # We may change the position... first chosing how:
    if isinstance(ipos_x1, str):
        # When we deal with a TPaveStats directly we should have real coordinates, not the predefined strings.
        if canv.Class().GetName() == "TPaveStats":
            raise TypeError(
                "ERROR: When proving a TPaveStats to changeStatsBox the coordinates should be numbers"
            )

        a = ipos_x1.lower()
        x = None
        # The size may be modified depending on the text size. Note that the text
        # size is 0, it is adapted to the box size (I think)
        textsize = (
            0 if (stbox.GetTextSize() == 0) else 6 * (stbox.GetTextSize() - 0.025)
        )
        xsize = (1 - canv.GetRightMargin() - canv.GetLeftMargin()) * (
            1 if y1pos is None else y1pos
        )  # Note these parameters looses their "x"-"y" nature.
        ysize = (1 - canv.GetBottomMargin() - canv.GetTopMargin()) * (
            1 if x2pos is None else x2pos
        )

        yfactor = 0.05 + 0.05 * stbox.GetListOfLines().GetEntries()

        if a == "tr":
            x = {
                "SetX1NDC": 1 - canv.GetRightMargin() - xsize * 0.33 - textsize,
                "SetY1NDC": 1 - canv.GetTopMargin() - ysize * yfactor - textsize,
                "SetX2NDC": 1 - canv.GetRightMargin() - xsize * 0.03,
                "SetY2NDC": 1 - canv.GetTopMargin() - ysize * 0.03,
            }
        elif a == "tl":
            x = {
                "SetX1NDC": canv.GetLeftMargin() + xsize * 0.03,
                "SetY1NDC": 1 - canv.GetTopMargin() - ysize * yfactor - textsize,
                "SetX2NDC": canv.GetLeftMargin() + xsize * 0.33 + textsize,
                "SetY2NDC": 1 - canv.GetTopMargin() - ysize * 0.03,
            }
        elif a == "bl":
            x = {
                "SetX1NDC": canv.GetLeftMargin() + xsize * 0.03,
                "SetY1NDC": canv.GetBottomMargin() + ysize * 0.03,
                "SetX2NDC": canv.GetLeftMargin() + xsize * 0.33 + textsize,
                "SetY2NDC": canv.GetBottomMargin() + ysize * yfactor + textsize,
            }
        elif a == "br":
            x = {
                "SetX1NDC": 1 - canv.GetRightMargin() - xsize * 0.33 - textsize,
                "SetY1NDC": canv.GetBottomMargin() + ysize * 0.03,
                "SetX2NDC": 1 - canv.GetRightMargin() - xsize * 0.03,
                "SetY2NDC": canv.GetBottomMargin() + ysize * yfactor + textsize,
            }

        if x is None:
            print(
                "ERROR: Invalid code provided to position the statistics box: {ipos_x1}".format(
                    ipos_x1=ipos_x1
                )
            )
        else:
            for xkey, xval in x.items():
                getattr(stbox, xkey)(xval)

    else:  # We change the values that are not None
        for xkey, xval in {
            "ipos_x1": "SetX1NDC",
            "y1pos": "SetY1NDC",
            "x2pos": "SetX2NDC",
            "y2pos": "SetY2NDC",
        }.items():
            x = locals()[xkey]
            if x is not None:
                getattr(stbox, xval)(x)

    UpdatePad(canv)  # To update the TCanvas or TPad.

    return stbox


# # # #
def setRootObjectProperties(obj, **kwargs):
    """This method allows to modify the properties of a ROOT object using a list of
    named keyword arguments to call the associated methods.

    Written by O. Gonzalez.

    Mostly intended to be called from other routines within the project, but it
    can be used externally with a call like e.g.

    cmsstyle.setRootObjectProperties(hist,FillColor=ROOT.kRed,FillStyle=3555,SetLineColor=cmsstyle.p6.kBlue)

    (A method starting with "Set" may omite the "Set" part)

    Args:
        obj (ROOT TObject): ROOT object to which we want to change the properties
        **kwargs: Arbitrary keyword arguments for mofifying the properties of the object using Set methods or similar.
    """

    for xkey, xval in kwargs.items():
        if hasattr(obj, "Set" + xkey):  # Note!
            method = "Set" + xkey
        elif hasattr(obj, xkey):
            method = xkey
        else:
            print(
                "Indicated argument for configuration is invalid: {} {} {}".format(
                    xkey, xval, type(obj)
                )
            )
            raise AttributeError("Invalid argument " + str(xkey) + " " + str(xval))

        if xval is None:
            getattr(obj, method)()
        elif xval is tuple:
            getattr(obj, method)(*xval)
        else:
            getattr(obj, method)(xval)


def is_valid_hex_color(hexcolor):
    """
    Check if a string represents a valid hexadecimal color code. It also allows other

    Args:
        hex_color (str/int/ROOT.TColor): The hexadecimal color code to check... or a TColor or intenger value

    Returns:
        bool: True if the string is a valid hexadecimal color code, False otherwise.
    """

    if isinstance(hexcolor, str):
        hex_color_pattern = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")
        return bool(hex_color_pattern.match(hexcolor))

    if isinstance(hexcolor, int):  # Identifying the color by the index (probably)
        if rt.gROOT.GetColor(hexcolor) is None:
            return False  # nullptr...
        return True

    try:
        if hexcolor.Class().GetName() == "TColor":
            if rt.gROOT.GetColor(hexcolor) is None:
                return False  # nullptr...
            return True
    except Exception:
        pass

    return False  # Not clear what format was provided


# # # #
def cmsReturnMaxY(*args):
    """This routine returns the recommended value for the maximum of the Y axis
    given a set of ROOT Object.

    Args:
      *args: list of ROOT objects for which we need the maximum value on Y axis.

    Returns:
      float: recommended value to be used in a Y axis for plotting those objects.
    """

    maxval = 0

    for xobj in args:
        if (
            xobj.Class().GetName() == "THStack"
        ):  # For the THStack it is assumed that we will print the sum!
            maxval = xobj.GetMaximum()

        elif hasattr(xobj, "GetMaximumBin"):  # Probably an histogram!
            value = xobj.GetBinContent(xobj.GetMaximumBin())
            value += xobj.GetBinError(xobj.GetMaximumBin())

            if maxval < value:
                maxval = value

        elif hasattr(
            xobj, "GetErrorYhigh"
        ):  # TGraph are special as GetMaximum exists but it is a bug value.
            value = 0

            i = xobj.GetN()
            y = xobj.GetY()
            ey = xobj.GetEY()

            while i > 0:
                i -= 1  # Fortrans convention -> C convention

                ivalue = y[i]
                try:
                    ivalue += max(ey[i], xobj.GetErrorYhigh(i))
                except ReferenceError:
                    pass

                if value < ivalue:
                    value = ivalue

            if maxval < value:
                maxval = value

        elif hasattr(
            xobj, "GetMaximum"
        ):  # Note that histograms may also have a "maximum" set.
            if maxval < xobj.GetMaximum():
                maxval = xobj.GetMaximum()

        # Other classes are for now ignored.

    return maxval


# # # #
def SaveCanvas(canv, path, close=True):
    """
    Save a canvas to a file and optionally close it. Takes care of fixing overlay and closing objects.

    Args:
        canv (ROOT.TCanvas): The canvas to save.
        path (str): The path to save the canvas to.
        close (bool, optional): Whether to close the canvas after saving. Defaults to True.
    """
    UpdatePad(canv)
    canv.SaveAs(path)
    if close:
        canv.Close()


# Multipad utilities


@contextmanager
def _managed_tpad_context(tpad):
    """
    Creates a context manager around a TVirtualPad.TContext.

    This allows to move to a different part of a canvas (pad) inside of the
    context, and restore the gPad variable to the previous value at its end.
    """
    ctxt = rt.TVirtualPad.TContext(tpad)
    try:
        yield ctxt
    finally:
        ctxt.__destruct__()


class CMSPad:
    """A pad, part of a canvas."""

    def __init__(
        self, manager: CMSCanvasManager, pad: rt.TPad, has_frame: bool = False
    ):
        self._manager = manager
        self._pad = pad
        # The frame is a ROOT histogram (TH1F), only used in the pad to define
        # define the axis ranges and be able to modify them consistently
        self._has_frame = has_frame

        # Throughout the lifetime of this pad, many drawables might be drawn
        # onto it. Make sure to keep lifelines around to avoid early object
        # destruction
        self._drawables = []

    def plot(self, obj: Any, opt: str = "", **kwargs):
        # If a frame has been created for this pad, its axis must be respected.
        # Make sure of it by plotting every object on top of the existing frame.
        if self._has_frame and "same" not in opt.lower():
            opt += " SAME"

        with _managed_tpad_context(self._manager._canvas):
            self._pad.cd()
            setRootObjectProperties(obj, **kwargs)
            obj.Draw(opt)
            self._drawables.append(obj)


@dataclass
class GridMetaData:
    """
    Metadata related to the grid layout of a cmsstyle canvas.

    (ncolumns,nrows) is the grid disposition. Horizontal and vertical margins
    indicate the margin to use for a proper alignment of the graphical elements
    and they are used throughout different utilities in CMSCanvasManager.
    """

    ncolumns: int
    nrows: int
    pad_horizontal_margin: int
    pad_vertical_margin: int


@dataclass
class LegendItem:
    """An item to be added to a legend, together with its name and drawing option."""

    obj: Any
    name: str
    opt: str


class CMSCanvasManager:
    """A manager of the different graphical parts of a canvas."""

    def __init__(
        self,
        canvas: rt.TCanvas,
        pads: Iterable[rt.TPad] | None = None,
        frames: Iterable[rt.TH1F] | None = None,
        bottom_pad: rt.TPad | None = None,
        top_pad: rt.TPad | None = None,
        grid_metadata: GridMetaData | None = None,
    ):
        """
        At minimum, a canvas manager needs a canvas to plot on. Optionally, it
        can manage different sub-components of a canvas:
        - A list of pads that will display subplots
        - A list of frames, one per subplot. The frame is an empty rt.TH1F which
          is only used to manage the graphical attributes of axes (range, labels, etc.)
        - A separate pad for the top part of the canvas. If this is not None, then
          the subplots will be contained below this pad.
        - A separate pad for the bottom part of the canvas. If this is not None,
          then the subplots will be contained above this pad.
        """
        self._canvas = canvas
        self._frames = frames
        if self._frames is not None:
            if pads is None:
                raise RuntimeError(
                    "Received an input list of pad frames, but no pads associated with them."
                )
            if len(self._frames) != len(pads):
                raise RuntimeError(
                    f"Received an input list of pad frames with wrong length: {len(self._frames)} != {len(pads)}"
                )
            self._pads = (
                [CMSPad(self, pad, True) for pad in pads] if pads is not None else None
            )
        else:
            self._pads = (
                [CMSPad(self, pad) for pad in pads] if pads is not None else None
            )

        self._grid_metadata = grid_metadata
        if self._pads is not None:
            if self._grid_metadata is None:
                raise RuntimeError("Missing grid metadata in canvas manager.")
            npads = self._grid_metadata.ncolumns * self._grid_metadata.nrows
            if len(self._pads) != npads:
                raise RuntimeError(
                    f"Number of pads passed to canvas manager ({len(self._pads)}) "
                    f"is different from the expected number ({npads})."
                )
        self._bottom_pad = CMSPad(self, bottom_pad) if bottom_pad is not None else None
        self._top_pad = CMSPad(self, top_pad) if top_pad is not None else None

    @property
    def top_pad(self):
        if self._top_pad is None:
            raise RuntimeError(
                "Trying to retrive top pad, but it is not present. Make sure you created it."
            )

        return self._top_pad

    @property
    def bottom_pad(self):
        if self._bottom_pad is None:
            raise RuntimeError(
                "Trying to retrive bottom pad, but it is not present. Make sure you created it."
            )
        return self._bottom_pad

    @property
    def pads(self):
        if self._pads is None:
            raise RuntimeError(
                "Trying to retrieve subplots of the canvas, but they are not present. Make sure you created them first."
            )
        return self._pads

    def plot_common_legend(
        self,
        pad: CMSPad,
        *args: LegendItem,
        xleft: int | None = None,
        xright: int | None = None,
        ydown: int | None = None,
        yup: int | None = None,
        title: str = "CMS",
        titleFont: int = 62,
        titleSize: float = 50 * 0.75 / 0.6,
        subtitle: str = "Preliminary",
        subtitleFont: str = 52,
        textalign: int = 13,
        ipos: int = 0,
    ):
        pad._pad.cd()
        horizontal_margin = (
            self._grid_metadata.pad_horizontal_margin / self._grid_metadata.ncolumns
        )
        xleft = xleft if xleft is not None else horizontal_margin
        xright = xright if xright is not None else 1 - horizontal_margin
        ydown = ydown if ydown is not None else 0
        yup = yup if yup is not None else 0.7

        leg = rt.TLegend(xleft, ydown, xright, yup)
        leg.SetTextAlign(textalign)
        
        leg.SetBorderSize(1)
        leg.SetMargin(0.5)     

        # Have at most 4 items on the same row
        ndrawables = len(args)
        ncolumns = (ndrawables + 1) if (ndrawables + 1) < 6 else 5
        leg.SetNColumns(ncolumns)
        if ipos != 0:
            n = 0
            for arg in args:
                if n % ncolumns == 0:
                    leg.AddEntry(0, "      ", "  ")
                    n += 1
                leg.AddEntry(arg.obj, arg.name, arg.opt)
                n += 1
        else:
            for arg in args:
                leg.AddEntry(arg.obj, arg.name, arg.opt)

        pad.plot(leg)

        latex = rt.TLatex()
        latex.SetNDC()
        latex.SetTextFont(titleFont)

        canvas_height = pad._pad.GetWh()
        ymin = pad._pad.GetYlowNDC()
        ymax = pad._pad.GetYlowNDC() + pad._pad.GetHNDC()
        pad_ndc_height = ymax - ymin
        pad_pixel_height = canvas_height * pad_ndc_height
        titleSize =  titleSize / pad_pixel_height
        subtitleSize = titleSize * 0.76

        latex.SetTextSize(titleSize) 
        latex.SetTextAlign(13)    
        if ipos != 0:
            latex.DrawLatex(0.11, 0.60, title)
        else:
            latex.DrawLatex(0.10, 0.97, title)
        latex.SetTextFont(subtitleFont)
        latex.SetTextSize(subtitleSize)
        if ipos != 0:
            latex.DrawLatex(0.11, 0.30, subtitle)
        else:
            latex.DrawLatex(0.17, 0.94, subtitle)


    def plot_text(
        self,
        pad: CMSPad,
        text,
        textsize=50,
        textfont=42,
        textalign=33,
        xcoord: int | None = None,
        ycoord: int | None = None,
    ):
        # Plotting text is special, we need to be already inside the right pad
        # (i.e. `cd()` must have been called before the creation of the text)
        with _managed_tpad_context(self._canvas):
            pad._pad.cd()
            horizontal_margin = (
                self._grid_metadata.pad_horizontal_margin / self._grid_metadata.ncolumns
            )
            xcoord = xcoord if xcoord is not None else 1 - horizontal_margin
            ycoord = ycoord if ycoord is not None else 1

            latex = rt.TLatex()
            latex.SetNDC()
            latex.SetTextAngle(0)
            latex.SetTextColor(rt.kBlack)

            latex.SetTextFont(textfont)
            latex.SetTextAlign(textalign)
            
            canvas_height = pad._pad.GetWh()
            ymin = pad._pad.GetYlowNDC()
            ymax = pad._pad.GetYlowNDC() + pad._pad.GetHNDC()
            pad_ndc_height = ymax - ymin
            pad_pixel_height = canvas_height * pad_ndc_height
            textsize = textsize / pad_pixel_height
            latex.SetTextSize(textsize)

            latex.DrawLatex(xcoord, ycoord, text)
            latex.Draw()

            pad._drawables.append(latex)

    def ylabel(self, label: str | None = None, labels: dict | None = None):
        # Cannot have both one title for all axes and a dictionary of axis titles
        if label is not None and labels is not None:
            raise RuntimeError(
                "Cannot set both the same title for all axes and also different titles for different axes."
            )

        if label is not None:
            for frame in self._frames:
                frame.GetYaxis().SetTitle(label)
        # If the dictionary is passed it must be of the form dict[int, str] where
        # the keys are the indexes of the pads in the canvas with the usual
        # convention left-right,top-bottom starting from 1.
        elif labels is not None:
            for nframe in labels:
                self._frames[nframe].GetYaxis().SetTitle(labels[nframe])
    
    def ylimits(self, limits: dict | None = None):
        for nframe in limits:
            self._frames[nframe].SetMinimum(limits[nframe][0])
            self._frames[nframe].SetMaximum(limits[nframe][1])
            #self._frames[nframe].GetYaxis().SetLimits(limits[nframe][0], limits[nframe][1])
    
    def xlimits(self, limits: dict | None = None):
        for nframe in limits:
            self._frames[nframe].GetXaxis().SetLimits(limits[nframe][0], limits[nframe][1])

    def save_figure(self, filename: str):
        self._canvas.SaveAs(filename)


def _subplots_coordinates(
    ncolumns,
    nrows,
    height_ratios=None,
    width_ratios=None,
    canvas_top_margin=None,
    canvas_bottom_margin=None,
):
    """
    Computes the coordinates of each sub-component (pad) of the canvas in the case of multiple subplots.
    Args:
    - ncolumns: number of columns
    - nrows: number of rows
    - height_ratios: list of weights for the relative heights of the pads along the columns. Length must be equal to nrows
    - width_ratios: list of weights for the relative widths of the pads along the rows. Length must be equal to ncolumns
    - canvas_top_margin: margin to remove starting from the top of the canvas to make space for the top pad
    - canvas_bottom_margin: margin to remove starting from the bottom of the canvas to make space for the bottom pad
    """
    if height_ratios is None:
        height_ratios = [1 / nrows] * nrows
    if width_ratios is None:
        width_ratios = [1 / ncolumns] * ncolumns

    assert len(height_ratios) == nrows, (
        f"Length of parameter height_ratios ({len(height_ratios)}) should be equal to the number of rows ({nrows})"
    )

    assert len(width_ratios) == ncolumns, (
        f"Length of parameter width_ratios ({len(width_ratios)}) should be equal to the number of columns ({ncolumns})"
    )

    # Compute coordinates for top and bottom pads. The remaining size of the canvas is used to compute the coordinates
    # for the actual subplots
    top_pad_coords = (
        (0, (1 - canvas_top_margin), 1, 1) if canvas_top_margin is not None else None
    )
    bottom_pad_coords = (
        (0, 0, 1, canvas_bottom_margin) if canvas_bottom_margin is not None else None
    )

    if canvas_top_margin is None:
        canvas_top_margin = 0
    if canvas_bottom_margin is None:
        canvas_bottom_margin = 0

    # The main part of the computation, here is the overall logic:
    # - width and height of each pad are normalised to the sum of respectively all width and height ratios
    # - adjust with top and bottom margins if present
    # - compute xlow, ylow, xup, yup of the current pad
    # - continue on each pad of the same row
    # - when moving to next row, decrease the starting height by the height of pads in the previous row
    first_pad_h = (height_ratios[0] / sum(height_ratios)) * (
        1 - canvas_top_margin - canvas_bottom_margin
    )
    xlow = 0
    ylow = 1 - first_pad_h - canvas_top_margin
    first_pad_w = width_ratios[0] / sum(width_ratios)
    xup = 0 + first_pad_w
    yup = 1 - canvas_top_margin
    npad = 0
    previous_h_offset = first_pad_h
    coordinates = []

    for height_ratio in height_ratios:
        for width_ratio in width_ratios:
            pad_h = (height_ratio / sum(height_ratios)) * (
                1 - canvas_top_margin - canvas_bottom_margin
            )
            pad_w = width_ratio / sum(width_ratios)
            # We skip the first pad as its coordinates are computed already before the for loop
            if npad != 0 and npad % ncolumns == 0:
                # This branch is for the start of a new row
                ylow -= pad_h
                yup -= previous_h_offset
                xlow = 0
                first_pad_w = width_ratios[0] / sum(width_ratios)
                xup = 0 + first_pad_w

                previous_h_offset = pad_h
            elif npad != 0:
                # Here we just move to the next pad in the same row
                xlow = xlow + pad_w
                xup = xup + pad_w

            # Finally, round coordinates to avoid graphical artifacts
            newcoords = []
            for coord in (xlow, ylow, xup, yup):
                newcoords.append(abs(round(coord, 5)))

            coordinates.append(newcoords)
            npad += 1

    return coordinates, top_pad_coords, bottom_pad_coords


def subplots(
    ncolumns: int,
    nrows: int,
    height_ratios: Iterable[float] | None = None,
    width_ratios: Iterable[float] | None = None,
    canvas_top_margin: float | None = None,
    canvas_bottom_margin: float | None = None,
    shared_x_axis: bool = True,
    shared_y_axis: bool = True,
    canvas_width: int = 2000,
    canvas_height: int = 2000,
    axis_title_size: float = 50,
    axis_label_size: float = 50 * 0.8
) -> CMSCanvasManager:
    """
    Creates multiple pads in a canvas according to the input configuration, then
    returns an object to help manage the canvas and all its graphical parts.

    Args:
    - ncolumns: number of columns in the grid
    - nrows: number of rows in the grid
    - height_ratios: list of weights for the relative heights of the pads along the columns. Length must be equal to nrows
    - width_ratios: list of weights for the relative widths of the pads along the rows. Length must be equal to ncolumns
    - canvas_top_margin: margin to remove starting from the top of the canvas to make space for the top pad
    - canvas_bottom_margin: margin to remove starting from the bottom of the canvas to make space for the bottom pad
    - shared_x_axis: whether the x axis of all columns should be shared
    - shared_y_axis: whether the y axis of all columns should be shared
    - canvas_width: total width of the canvas
    - canvas_height: total height of the canvas
    - axis_title_size: reference absolute size for axis titles
    - axis_label_size: reference absolute size for axis labels
    """

    top_pad = None
    bottom_pad = None
    canvas = rt.TCanvas("CMS_canvas", "CMS_canvas", canvas_width, canvas_height)
    with _managed_tpad_context(canvas):
        # Gather the raw coordinates for all the pads
        pads_coords, top_pad_coords, bottom_pad_coords = _subplots_coordinates(
            ncolumns,
            nrows,
            height_ratios=height_ratios,
            width_ratios=width_ratios,
            canvas_top_margin=canvas_top_margin,
            canvas_bottom_margin=canvas_bottom_margin,
        )

        # Create the pads manually using the coordinates from above, and some adjustments
        listofpads = []
        pad_horizontal_margin = 0.2
        pad_vertical_margin = 0.4
        epsilon_height = 0.07
        epsilon_width = 0.01
        row_index = -1
        for i, (xleft, ylow, xright, yup) in enumerate(pads_coords):
            pad = rt.TPad(f"pad_{i + 1}", f"pad_{i + 1}", xleft, ylow, xright, yup)

            # The next lines adjust the relative margins (vertically and horizontally)
            # of the pads so that the final plots will always be consistent
            if i % ncolumns == 0:
                row_index += 1
                pad.SetLeftMargin(pad_horizontal_margin)
                pad.SetRightMargin(epsilon_width)
            elif i % ncolumns == (ncolumns - 1):
                pad.SetRightMargin(pad_horizontal_margin)
                pad.SetLeftMargin(epsilon_width)
            else:
                pad.SetRightMargin(pad_horizontal_margin / 2)
                pad.SetLeftMargin(pad_horizontal_margin / 2)

            if row_index == 0:
                pad.SetTopMargin(
                    pad_vertical_margin * (1 / height_ratios[i // ncolumns])
                    - epsilon_height
                )
                pad.SetBottomMargin(epsilon_height)
            elif row_index == nrows - 1:
                margin = pad_vertical_margin * (1 / height_ratios[i // ncolumns]) / 2
                pad.SetTopMargin(margin)
                pad.SetBottomMargin(margin)
            else:
                pad.SetTopMargin(
                    pad_vertical_margin / 2 * (1 / height_ratios[i // ncolumns])
                )
                pad.SetBottomMargin(
                    pad_vertical_margin / 2 * (1 / height_ratios[i // ncolumns])
                )

            # The pad *must* be drawn once before being used for any other plotting
            pad.Draw()
            listofpads.append(pad)

        if top_pad_coords is not None:
            xleft, ylow, xright, yup = top_pad_coords
            pad = rt.TPad("top_pad", "top_pad", xleft, ylow, xright, yup)
            pad.Draw()
            top_pad = pad

        if bottom_pad_coords is not None:
            xleft, ylow, xright, yup = bottom_pad_coords
            pad = rt.TPad("bottom_pad", "bottom_pad", xleft, ylow, xright, yup)
            pad.Draw()
            bottom_pad = pad

        canvas.Modified()

    # After creating the pads, we create one frame per pad. These will be used
    # to manage the axis range, labels etc.
    listofframes = []
    row_index = -1
    for i, pad in enumerate(listofpads):
        with _managed_tpad_context(canvas):
            pad.cd()
            if i % ncolumns == 0:
                row_index += 1

            # This part here is still custom, needs an abstract definition in
            # the function signature to provide the ranges of all the axes
            if row_index % 2 == 0:
                ymin = 0
                ymax = 400
            else:
                ymin = 0
                ymax = 2

            frame = pad.DrawFrame(-2, ymin, 2, ymax)
            xaxis = frame.GetXaxis()
            yaxis = frame.GetYaxis()
            yaxis.SetNdivisions(3, 5, 0, True)
            xaxis.SetLabelSize(0)
            yaxis.SetLabelSize(0)
            xaxis.SetTitleSize(0)
            yaxis.SetTitleSize(0)
            listofframes.append(frame)

    if shared_x_axis:
        for frame, pad in zip(listofframes[-ncolumns:], listofpads[-ncolumns:]):
            with _managed_tpad_context(canvas):
                pad.cd()
                
                canvas_height = listofpads[i].GetWh()
                ymin = listofpads[i].GetYlowNDC()
                ymax = listofpads[i].GetYlowNDC() + listofpads[i].GetHNDC()
                pad_ndc_height = ymax - ymin
                pad_pixel_height = canvas_height * pad_ndc_height
                labeltextsize = axis_label_size / pad_pixel_height
                frame.GetXaxis().SetLabelSize(labeltextsize)
                frame.GetXaxis().SetNdivisions(5, 5, 0, True)

    if shared_y_axis:
        for i in range(0, len(listofframes), ncolumns):
            with _managed_tpad_context(canvas):
                listofpads[i].cd()

                canvas_height = listofpads[i].GetWh()
                ymin = listofpads[i].GetYlowNDC()
                ymax = listofpads[i].GetYlowNDC() + listofpads[i].GetHNDC()
                pad_ndc_height = ymax - ymin
                pad_pixel_height = canvas_height * pad_ndc_height
                labeltextsize = axis_label_size / pad_pixel_height
                
                listofframes[i].GetYaxis().SetLabelSize(labeltextsize)
                listofframes[i].GetYaxis().SetNdivisions(3, 5, 0, True)
                
                titletextsize = axis_title_size / pad_pixel_height
                listofframes[i].GetYaxis().SetTitleSize(titletextsize)

               
                listofframes[i].GetYaxis().SetTitleOffset(
                    3 * (height_ratios[i // ncolumns] / sum(height_ratios))
                )

    return CMSCanvasManager(
        canvas,
        pads=listofpads,
        frames=listofframes,
        bottom_pad=bottom_pad,
        top_pad=top_pad,
        grid_metadata=GridMetaData(
            ncolumns, nrows, pad_horizontal_margin, pad_vertical_margin
        ),
    )


# #######################################################################
