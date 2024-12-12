#
# This python macro
#
# Written by O. Gonzalez (2024_12_02)
#

import math

import ROOT

import cmsstyle

# # # #
def test_cmsCanvas ():
    """Make the plot with the histograms on the fly.

    """

    # Producing the histograms to plot
    h1 = ROOT.TH1F("test1","test1",60,0.0,10.0)
    h2 = ROOT.TH1F("test2","test2",60,0.0,10.0)

    for i in range(1,61):
        h1.SetBinContent(i,10*math.exp(-i/5.0))
        h2.SetBinContent(i,8*math.exp(-i/15.0))

    h1.Add(h2)

    hdata = h1.Clone("data")
    for i in range(1,61):
        hdata.SetBinError(i,0.12*hdata.GetBinContent(i))
        hdata.SetBinContent(i, hdata.GetBinContent(i)*(1+0.1*math.cos(6.28*i/20.)))

    # Plotting the histogram!

    cmsstyle.setCMSStyle()  # Setting the style

    cmsstyle.SetEnergy(13.6)
    cmsstyle.SetLumi(45.00,"fb","Run 3",-1)

    c = cmsstyle.cmsCanvas("Testing",0.0,10.0,0.08,3*cmsstyle.cmsReturnMaxY(h1,h2,hdata),
                           "X var [test]","Y var",square=True,
                           #iPos=0
                           )

    ROOT.gPad.SetLogy()

    cmsstyle.cmsObjectDraw(h1,"",LineColor=cmsstyle.p6.kGray,
                           FillColor=cmsstyle.p6.kGray,
                           FillStyle=1001)

    cmsstyle.cmsObjectDraw(h2,"",LineColor=cmsstyle.p6.kYellow,
                           FillColor=cmsstyle.p6.kYellow,
                           FillStyle=1001)

    if False:  # To test the use of the changeStatsBox
        ROOT.gStyle.SetOptStat('mr')
        cmsstyle.cmsObjectDraw(hdata,"SE",MarkerStyle=ROOT.kFullCircle)
        cmsstyle.changeStatsBox(c,'tl')

    else:
        cmsstyle.cmsObjectDraw(hdata,"E",MarkerStyle=ROOT.kFullCircle)

    # The legend!

    plotlegend = cmsstyle.cmsLeg(0.55,0.65,0.9,0.9)

    plotlegend.AddEntry(hdata,"Data","p")
    plotlegend.AddEntry(h1,"Sample Number 1","f")
    plotlegend.AddEntry(h2,"Sample Number 2","f")

    # Saving the result!
    cmsstyle.SaveCanvas(c,"test_cmsCanvas.png")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# For running as a shell command to get the list of files (comma-separated)
if __name__ == '__main__':
    test_cmsCanvas()

# #######################################################################
