#
# This python macro produces a plot with 2-D histograms.
#
# Written by O. Gonzalez (2024_12_02)
#

import math

import ROOT

import cmsstyle

# # # #
def test_cms2dHisto ():
    """Make the plot with the histograms on the fly.

    """

    cmsstyle.setCMSStyle()  # Setting the style

    # Producing the histograms to plot
    h1 = ROOT.TH2F("test1","test1",60,0.0,60.0,60,0.0,60.0)
    h2 = ROOT.TH2F("test2","test2",60,0.0,60.0,60,0.0,60.0)

    for i in range(1,61):
        for j in range(1,61):
            h1.SetBinContent(i,j,10*math.exp((30-i)**2/-25.0)*math.exp((20-j)**2/-20.0))
            h2.SetBinContent(i,j,15*math.exp((45-i)**2/-45.0)*math.exp((40-j)**2/-50.0))

    # We only plot the sum for now!

    h1.Add(h2)

    # Plotting the histogram!
    cmsstyle.SetEnergy(13.6)
    cmsstyle.SetLumi(45.00,"fb","Run 3",1)
    cmsstyle.SetExtraText("")

    c = cmsstyle.cmsCanvas("Testing",0.0,60.0,0.0,60.0,
                           "X var [test]","Y var",square=True,
                           with_z_axis=True,
                           iPos=0
                           )

#    cmsstyle.SetCMSPalette()
    cmsstyle.SetAlternative2DColor(h1)

    cmsstyle.cmsObjectDraw(h1,"COLZ")
#    cmsstyle.cmsObjectDraw(h1,"LEGO2")

    # Saving the result!
    cmsstyle.SaveCanvas(c,"test_cms2DHisto.png")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# For running as a shell command to get the list of files (comma-separated)
if __name__ == '__main__':
    test_cms2dHisto()

# #######################################################################
