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
import ROOT as rt
from array import array

import re

# This global variables for the module should not be accessed directy! Use the utilities below.
cms_lumi = "Run 2, 138 fb^{#minus1}"
cms_energy = "13 TeV"

cmsText = "CMS"
extraText = "Preliminary"

cmsStyle = None

usingPalette2D = None # To define a color palette for 2-D histograms

lumiTextSize = 0.6   # text sizes and text offsets with respect to the top frame in unit of the top margin size
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1

writeExtraText = True  # For the extra and addtional text

cmsTextFont = 61  # default is helvetic-bold
extraTextFont = 52  # default is helvetica-italics
additionalInfoFont = 42
additionalInfo = []  # For extra info

# ratio of 'CMS' and extra text size
extraOverCmsTextSize = 0.76

drawLogo = False
kSquare = True
kRectangular = False

# Petroff color schemes for 6, 8 and 10 colors, respectively. See classes below. Avoid using this... better use the names.
petroff_6 = ["#5790fc", "#f89c20", "#e42536", "#964a8b", "#9c9ca1", "#7a21dd"]
petroff_8 = ["#1845fb", "#ff5e02", "#c91f16", "#c849a9", "#adad7d", "#86c8dd", "#578dff", "#656364"]
petroff_10 = ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#832db6", "#a96b59", "#e76300", "#b9ac70", "#717581", "#92dadd"]

# This should be consider CONSTANT! (i.e. do not modify them)
# --------------------------------

# Plots for limits and statistical bands
kLimit68 = rt.TColor.GetColor("#607641")  # Internal band, default set
kLimit95 = rt.TColor.GetColor("#F5BB54")    # External band, default set

kLimit68cms = rt.TColor.GetColor("#85D1FBff")  # Internal band, CMS-logo set
kLimit95cms = rt.TColor.GetColor("#FFDF7Fff")  # External band, CMS-logo set

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def SetEnergy (energy, unit = "TeV"):
    """
    Set the centre-of-mass energy value and unit to be displayed.

    Args:
        energy (float): The centre-of-mass energy value.
        unit (str, optional): The energy unit. Defaults to "TeV".
    """
    global cms_energy
    cms_energy = str(energy) + " " + unit if energy != "" else ""


def SetLumi (lumi, unit="fb", round_lumi=False):
    """
    Set the integrated luminosity value and unit to be displayed.

    Args:
        lumi (float): The integrated luminosity value.
        unit (str, optional): The integrated luminosity unit. Defaults to "fb".
        round_lumi (bool, optional): Whether to round the luminosity value to the nearest integer. Defaults to False.
    """
    global cms_lumi
    if lumi != "":
        cms_lumi = "{:.0f}".format(lumi) if round_lumi else "{}".format(lumi)
        cms_lumi += " {unit}^{{#minus1}}".format(unit=unit)
    else:
        cms_lumi = lumi

def SetCmsText(text):
    """
    Function that allows to edit the default
    "CMS" string

    Args:
        text (str): The CMS text.
    """
    global cmsText
    cmsText = text

def SetExtraText(text):
    """
    Set extra text to be displayed next to "CMS", e.g. "Preliminary".

    Args:
        text (str): The extra text.
    """
    global extraText
    extraText = text

# # # #
def SetCmsTextFont(font):
    """
    Function that allows to edit the default font of the
    "CMS" string

    Args:
        font (int): The CMS text font code.
    """
    global cmsTextFont
    cmsTextFont = font

def SetExtraTextFont(font):
    """
    Function that allows to edit the default font
    of extra text string (printed after "CMS" by default)

    Args:
        font (int): The extra text font code.
    """
    global extraTextFont
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
def SetCmsTextSize(size):
    """
    Function that allows to edit the default fontsize of the
    "CMS" string

    Args:
        size (int): The CMS text font size.
    """
    global cmsTextSize
    cmsTextSize = size

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
        if (rt.GetColor(rt.kP6Violet).GetTitle=='#7a21dd'):  # There was a bug in the first implementation in ROOT
                                                             # (I think no "released" version is affected. 6.34.00 is already OK)
            kViolet = rt.kP6Violet
        else:
            kViolet = rt.TColor.GetColor("#7a21dd")
    except: # Defining the color scheme by hand
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
    except: # Defining the color scheme by hand
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
    except:
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
        if cmStyle is not None: style = cmsStyle
        else: style = rt.gStyle

    style.SetPalette(len(usingPalette2D), array("i", usingPalette2D))

    if hist is not None:
        hist.SetContour(len(usingPalette2D))

# # # #
def SetCMSPalette():
    """
    Set the official CMS colour palette for 2D histograms directly.
    """
    cmsStyle.SetPalette(rt.kViridis)
    #cmsStyle.SetPalette(rt.kCividis)

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
    hist, canv=None, X1=None, X2=None, Y1=None, Y2=None, isNDC=True):
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
    if canv != None:
        hframe = GetcmsCanvasHist(canv)
        X1 = 1 - canv.GetRightMargin() * 0.95
        X2 = 1 - canv.GetRightMargin() * 0.70
        Y1 = canv.GetBottomMargin()
        Y2 = 1 - canv.GetTopMargin()
    if isNDC:
        if X1 != None:
            palette.SetX1NDC(X1)
        if X2 != None:
            palette.SetX2NDC(X2)
        if Y1 != None:
            palette.SetY1NDC(Y1)
        if Y2 != None:
            palette.SetY2NDC(Y2)
    else:
        if X1 != None:
            palette.SetX1(X1)
        if X2 != None:
            palette.SetX2(X2)
        if Y1 != None:
            palette.SetY1(Y1)
        if Y2 != None:
            palette.SetY2(Y2)


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
    Enable or disable the grid mode in the CMSStyle.

    Args:
        gridOn (bool): To indicate whether to sets or unset the Grid on the CMSStyle.
    """
    cmsStyle.SetPadGridX(gridOn)
    cmsStyle.SetPadGridY(gridOn)

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
    if cmsStyle != None:
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
    cmsStyle.SetMarkerSize(1) # Not actually set by the TDR Style, but useful to fix default!
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
    cmsStyle.SetTitleXOffset(0.9)
    cmsStyle.SetTitleYOffset(1.25)
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
    cmsStyle.SetHatchesLineWidth(5)
    cmsStyle.SetHatchesSpacing(0.05)

    # Some additional parameters we need to set as "style"

    if (float('.'.join(re.split('\.|/',rt.__version__)[0:2])) >= 6.32):  # Not available before!
        # This change by O. Gonzalez allows to save inside the canvas the
        # informnation about the defined colours.
        rt.TColor.DefinedColors(1)

    # Using the Style.
    cmsStyle.cd()

# # # #
def getCMSStyle ():
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


def CMS_lumi(pad, iPosX=11, scaleLumi=None):

    """
    Draw the CMS text and luminosity information on the specified pad.

    Args:
        pad (ROOT.TPad): The pad to draw on.
        iPosX (int, optional): The position of the CMS logo. Defaults to 11 (top-left, left-aligned).
        scaleLumi (float, optional): Scale factor for the luminosity text size.
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
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    outOfFrame_posY = 1 - t + lumiTextOffset * t
    pad.cd()
    lumiText = ""
    lumiText += cms_lumi
    if cms_energy != "":
        lumiText += " (" + cms_energy + ")"
    if scaleLumi:
        lumiText = ScaleText(lumiText, scale=scaleLumi)

    def drawText(text, posX, posY, font, align, size):
        latex.SetTextFont(font)
        latex.SetTextAlign(align)
        latex.SetTextSize(size)
        latex.DrawLatex(posX, posY, text)

    latex = rt.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(rt.kBlack)
    extraTextSize = extraOverCmsTextSize * cmsTextSize
    drawText(
        text=lumiText,
        posX=1 - r,
        posY=outOfFrame_posY,
        font=42,
        align=31,
        size=lumiTextSize * t,
    )
    if outOfFrame:
        drawText(
            text=cmsText,
            posX=l,
            posY=outOfFrame_posY,
            font=cmsTextFont,
            align=11,
            size=cmsTextSize * t,
        )
    posX_ = 0
    if iPosX % 10 <= 1:
        posX_ = l + relPosX * (1 - l - r)
    elif iPosX % 10 == 2:
        posX_ = l + 0.5 * (1 - l - r)
    elif iPosX % 10 == 3:
        posX_ = 1 - r - relPosX * (1 - l - r)
    posY_ = 1 - t - relPosY * (1 - t - b)
    if not outOfFrame:
        if drawLogo:
            posX_ = l + 0.045 * (1 - l - r) * W / H
            posY_ = 1 - t - 0.045 * (1 - t - b)
            xl_0 = posX_
            yl_0 = posY_ - 0.15
            xl_1 = posX_ + 0.15 * H / W
            yl_1 = posY_
            CMS_logo = rt.TASImage("CMS-BW-label.png")
            pad_logo = rt.TPad("logo", "logo", xl_0, yl_0, xl_1, yl_1)
            pad_logo.Draw()
            pad_logo.cd()
            CMS_logo.Draw("X")
            pad_logo.Modified()
            pad.cd()
        else:
            drawText(
                text=cmsText,
                posX=posX_,
                posY=posY_,
                font=cmsTextFont,
                align=align_,
                size=cmsTextSize * t,
            )
            if writeExtraText:
                posY_ -= relExtraDY * cmsTextSize * t
                drawText(
                    text=extraText,
                    posX=posX_,
                    posY=posY_,
                    font=extraTextFont,
                    align=align_,
                    size=extraTextSize * t,
                )
                if len(additionalInfo) != 0:
                    latex.SetTextSize(extraTextSize * t)
                    latex.SetTextFont(additionalInfoFont)
                    for ind, tt in enumerate(additionalInfo):
                        latex.DrawLatex(
                            posX_,
                            posY_
                            - 0.004
                            - (relExtraDY * extraTextSize * t / 2 + 0.02) * (ind + 1),
                            tt,
                        )
    elif writeExtraText:
        if outOfFrame:
            scale = float(H) / W if W > H else 1
            posX_ = l + 0.043 * (extraTextFont * t * cmsTextSize) * scale
            posY_ = outOfFrame_posY
        drawText(
            text=extraText,
            posX=posX_,
            posY=posY_,
            font=extraTextFont,
            align=align_,
            size=extraTextSize * t,
        )
    UpdatePad(pad)


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
    square=kSquare,
    iPos=11,
    extraSpace=0,
    with_z_axis=False,
    scaleLumi=None,
    yTitOffset=None
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
        scaleLumi (float, optional): Scale factor for the luminosity text size.
        yTitOffset (float, optional): Set the value for the Y-axis title offset in case default is not good. [Added by O. Gonzalez]

    Returns:
        ROOT.TCanvas (ROOT.TCanvas): The created canvas.
    """

    # Set CMS style if not set already.
    if cmsStyle is None: setCMSStyle()

    # Set canvas dimensions and margins
    W_ref = 600 if square else 800
    H_ref = 600 if square else 600

    W = W_ref
    H = H_ref
    T = 0.07 * H_ref
    B = 0.11 * H_ref
    L = 0.13 * H_ref
    R = 0.03 * H_ref

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
        y_offset = 1.0 if square else 0.78
    else:
        y_offset = yTitOffset

    h.GetYaxis().SetTitleOffset(y_offset)
    h.GetXaxis().SetTitleOffset(0.9)
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
def GetcmsCanvasHist(canv):
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
    GetcmsCanvasHist(canv).GetXaxis().SetRangeUser(x_min, x_max)
    GetcmsCanvasHist(canv).GetYaxis().SetRangeUser(y_min, y_max)


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
    square=kSquare,
    iPos=11,
    extraSpace=0,
    scaleLumi=None,
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
        scaleLumi (float, optional): Scale factor for the luminosity text size.

    Returns:
        ROOT.TCanvas: The created canvas.
    """

    # Set CMS style if not set
    if cmsStyle is None: setCMSStyle()

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
    prefix='SAME'
    if ('SAME' in style): prefix=''

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
def cmsObjectDraw (obj,opt='',**kwargs):
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

    setRootObjectProperties(obj,**kwargs)

    prefix='SAME'
    if ('SAME' in opt): prefix=''
    obj.Draw(prefix+opt)

# # # #
def changeStatsBox (canv,ipos_x1=None,y1pos=None,x2pos=None,y2pos=None,**kwargs):
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
        canv (ROOT.TCanvas): canvas to which we modify the stats box
        ipos_x1 (str or float): position for the stats box. Use a predefined string of a location or an NDC x coordinate number
        y1pos (float): NDC y coordinate number or a factor to scale the width of the box when using a predefined location.
        x2pos (float): NDC x coordinate number or a factor to scale the height of the box when using a predefined location.
        y2pos (float): NDC y coordinate number or ignored value.
        **kwargs: Arbitrary keyword arguments for mofifying the properties of the stats box using Set methods or similar.
    """

    canv.Update()  # To be sure we have created the statistic box
    stbox = canv.GetPrimitive('stats')

    if (stbox.Class().GetName()!='TPaveStats'):
        raise ReferenceError("ERROR: Trying to change the StatsBox when it has not been enabled... activate it with SetOptStat (and use \"SAMES\" or equivalent)")

    setRootObjectProperties(stbox,**kwargs)
    canv.Update()

    # We may change the position... first chosing how:
    if isinstance(ipos_x1,str):
        a = ipos_x1.lower()
        x = None
        # The size may be modified depending on the text size. Note that the text
        # size is 0, it is adapted to the box size (I think)
        textsize = 0 if (stbox.GetTextSize()==0) else 6*(stbox.GetTextSize()-0.025)
        xsize = (1-canv.GetRightMargin()-canv.GetLeftMargin())*(1 if y1pos is None else y1pos)  # Note these parameters looses their "x"-"y" nature.
        ysize = (1-canv.GetBottomMargin()-canv.GetTopMargin())*(1 if x2pos is None else x2pos)

        yfactor = 0.05+0.05*stbox.GetListOfLines().GetEntries()

        if (a=='tr'):
            x = {'SetX1NDC':1-canv.GetRightMargin()-xsize*0.33-textsize,'SetY1NDC':1-canv.GetTopMargin()-ysize*yfactor-textsize,'SetX2NDC':1-canv.GetRightMargin()-xsize*0.03,'SetY2NDC':1-canv.GetTopMargin()-ysize*0.03}
        elif (a=='tl'):
            x = {'SetX1NDC':canv.GetLeftMargin()+xsize*0.03,'SetY1NDC':1-canv.GetTopMargin()-ysize*yfactor-textsize,'SetX2NDC':canv.GetLeftMargin()+xsize*0.33+textsize,'SetY2NDC':1-canv.GetTopMargin()-ysize*0.03}
        elif (a=='bl'):
            x = {'SetX1NDC':canv.GetLeftMargin()+xsize*0.03,'SetY1NDC':canv.GetBottomMargin()+ysize*0.03,'SetX2NDC':canv.GetLeftMargin()+xsize*0.33+textsize,'SetY2NDC':canv.GetBottomMargin()+ysize*yfactor+textsize}
        elif (a=='br'):
            x = { 'SetX1NDC':1-canv.GetRightMargin()-xsize*0.33-textsize,'SetY1NDC':canv.GetBottomMargin()+ysize*0.03,'SetX2NDC':1-canv.GetRightMargin()-xsize*0.03,'SetY2NDC':canv.GetBottomMargin()+ysize*yfactor+textsize}

        if x is None:
            print("ERROR: Invalid code provided to position the statistics box: {ipos_x1}".format(ipos_x1=ipos_x1))
        else:
            for xkey,xval in x.items():
                getattr(stbox,xkey)(xval)

    else: # We change the values that are not None
        for xkey,xval in {'ipos_x1':'SetX1NDC','y1pos':'SetY1NDC','x2pos':'SetX2NDC','y2pos':'SetY2NDC'}.items():
            x = locals()[xkey]
            if x is not None: getattr(stbox,xval)(x)

    UpdatePad(canv)   # To update the TCanvas or TPad.

# # # #
def setRootObjectProperties (obj,**kwargs):
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

    for xkey,xval in kwargs.items():
        if hasattr(obj,'Set'+xkey):   # Note!
            method = 'Set'+xkey
        elif hasattr(obj,xkey):
            method = xkey
        else:
            print("Indicated argument for configuration is invalid: {} {} {}".format(xkey, xval, type(obj)))
            raise AttributeError("Invalid argument")

        if xval is None:
            getattr(obj,method)()
        elif xval is tuple:
            getattr(obj,method)(*xval)
        else:
            getattr(obj,method)(xval)

def is_valid_hex_color(hex_color):
    """
    Check if a string represents a valid hexadecimal color code.

    Args:
        hex_color (str): The hexadecimal color code to check.

    Returns:
        bool: True if the string is a valid hexadecimal color code, False otherwise.
    """
    hex_color_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')

    return bool(hex_color_pattern.match(hex_color))

# # # #
def cmsDrawStack(stack, legend, MC, data = None, palette = None, invertLegendEntries = True):
    """
    Draw a stack of histograms on a pre-defined stack plot and optionally a data histogram, with a pre-defined legend, using a user-defined or default list (palette) of hex colors.

    Args:
        stack (ROOT.THStack): The stack to draw the histograms on.
        legend (ROOT.TLegend): The legend to add entries to.
        MC (dict): A dictionary of Monte Carlo histograms, where the keys are the legend entries and the values are the histograms.
        data (ROOT.TH1, optional): The data histogram to draw on top of the stack.
        palette (list, optional): A list of hexadecimal color codes to use for the histograms. If not provided, a default palette will be used.
        invertLegendEntries (bool, optional): Whether to add the legend entries in reverse order. Defaults to True.
    """
    is_user_palette_valid = False

    if palette != None:
        is_user_palette_valid = all(is_valid_hex_color(color) for color in palette)
        if is_user_palette_valid:
            palette_ = palette
            if len(MC.keys()) > len(palette_):
                print("Length of provided palette is smaller than the number of histograms to be drawn, wrap around is enabled")
        else:
            print("Invalid palette elements provided, default palette will be used")

    if palette == None or is_user_palette_valid == False:
        if len(MC.keys()) < 7:
            palette_ = petroff_6
        elif len(MC.keys()) < 9:
            palette_ = petroff_8
        else:
            palette_ = petroff_10
            if len(MC.keys()) > len(palette_):
                print("Length of largest default palette is smaller than the number of histograms to be drawn, wrap around is enabled")

    # Add legend entries in inverse order
    if invertLegendEntries:
        for n, item in reversed(list(enumerate(MC.items()))):
            legend.AddEntry(item[1], item[0], "f")
    for n, item in enumerate(MC.items()):
        item[1].SetLineColor(rt.TColor.GetColor(palette_[n%len(palette_)]))
        item[1].SetFillColor(rt.TColor.GetColor(palette_[n%len(palette_)]))
        stack.Add(item[1])
        if not invertLegendEntries:
            legend.AddEntry(item[1], item[0], "f")
        stack.Draw("HIST SAME")

    if data != None:
        cmsDraw(data, "P", mcolor=rt.kBlack)
        legend.AddEntry(data, "Data", "lp")

# # # #
def ScaleText(name, scale=0.75):
    """
    Scale the size of a text string.

    Args:
        name (str): The text string to scale.
        scale (float, optional): The scale factor. Defaults to 0.75.

    Returns:
        str: The scaled text string.
    """
    return "#scale[" + str(scale) + "]{" + str(name) + "}"

# # # #
def cmsReturnMaxY (*args):
    """This routine returns the recommended value for the maximum of the Y axis
    given a set of ROOT Object.

    Args:
      *args: list of ROOT objects for which we need the maximum value on Y axis.

    Returns:
      float: recommended value to be used in a Y axis for plotting those objects.
    """

    maxval=0

    for xobj in args:
        if hasattr(xobj,'GetMaximumBin'):  # Probably an histogram!
            value = xobj.GetBinContent(xobj.GetMaximumBin())
            value += xobj.GetBinError(xobj.GetMaximumBin())

            if (maxval<value): maxval = value

        elif hasattr(xobj,'GetErrorYhigh'):  # TGraph are special as GetMaximum exists but it is a bug value.
            value = 0

            i = xobj.GetN()
            y = xobj.GetY()
            ey = xobj.GetEY()

            while (i>0):
                i -= 1  # Fortrans convention -> C convention

                ivalue = y[i]
                try:
                    ivalue += max(ey[i],xobj.GetErrorYhigh(i))
                except ReferenceError:
                    pass

                if (value<ivalue): value = ivalue

            if (maxval<value): maxval = value

        elif hasattr(xobj,'GetMaximum'):  # Note that histograms may also have a "maximum" set.
            if (maxval<xobj.GetMaximum()): maxval = xobj.GetMaximum()

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

# #######################################################################
