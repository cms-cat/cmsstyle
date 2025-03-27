#
# This python macro plots a THStack
#
# Written by O. Gonzalez (2024_12_07)
#                         2024_12_16  changed to
#

import math

import ROOT

import cmsstyle

# # # #
def test_THStack ():
    """Make the plot with the histograms on the fly.

    """

    cmsstyle.setCMSStyle()  # Setting the style

    # Producing the histograms to plot
    h1 = ROOT.TH1F("test1","test1",60,0.0,10.0)
    h2 = ROOT.TH1F("test2","test2",60,0.0,10.0)

    for i in range(1,61):
        h1.SetBinContent(i,10*math.exp(-i/5.0))
        h2.SetBinContent(i,8*math.exp(-i/15.0))

    tg = ROOT.TF1("fb","gaus(0)",0.0,10.0)
    tg.SetParameter(0,5.0)
    tg.SetParameter(1,3.0)
    tg.SetParameter(2,1.0)
    tg.SetNpx(60)
    hg = tg.CreateHistogram().Clone()
    hg.SetLineColor(ROOT.kBlack)  # By default from functions is kRed(?)

    # Building the "data" histogram:

    hdata = h1.Clone("data")
    for i in range(1,61):
        yval = h1.GetBinContent(i) + h2.GetBinContent(i) + hg.GetBinContent(i)

        hdata.SetBinError(i,0.12*yval)
        hdata.SetBinContent(i, yval*(1+0.1*math.cos(6.28*i/20.)))

    # Now we have the histograms to plot, so setting up the plot!
    # Building the THStack: built and drawn using the corresponding methods in CMSStyle

    if True:   # Recommended for clarity...

        hs = cmsstyle.buildTHStack([h1,h2,hg],[cmsstyle.p10.kBrown,cmsstyle.p10.kBlue,cmsstyle.p10.kOrange])
        #hs = cmsstyle.buildTHStack([h1,h2,hg],[cmsstyle.p10.kBrown,cmsstyle.p10.kBlue,cmsstyle.p10.kOrange],"STACK",FillStyle=3005,FillColor=-1,LineColor=-1)

        # Now we have the histograms to plot, so setting up the plot!

        c = cmsstyle.cmsCanvas("Testing",0.0,10.0,0.08,1.3*cmsstyle.cmsReturnMaxY(hdata),
                               "X var [test]","Y var");

        plotlegend = cmsstyle.cmsLeg(0.55,0.65,0.9,0.9)  # The legend!

        cmsstyle.addToLegend(plotlegend,
                             (hdata,"Data",'p'),
                             (hg,"Sample G",'f'),
                             (h2,"Sample 2",'f'),
                             (h1,"Sample 1",'f')
                             )

        cmsstyle.cmsObjectDraw(hs,"")

    else:  # Shorter version! (but note the canvas dows not use the stack for the canvas height)
        c = cmsstyle.cmsCanvas("Testing",0.0,10.0,0.08,1.3*cmsstyle.cmsReturnMaxY(hdata),
                               "X var [test]","Y var");

        plotlegend = cmsstyle.cmsLeg(0.55,0.65,0.9,0.9)  # The legend!

        cmsstyle.addToLegend(plotlegend,(hdata,"Data",'p'))

        hs = cmsstyle.buildAndDrawTHStack([(h1,"Sample 1",'f'),
                                           (h2,"Sample 2",'f'),
                                           (hg,"Sample G",'f')],
                                          plotlegend,True,[cmsstyle.p10.kBrown,cmsstyle.p10.kBlue,cmsstyle.p10.kOrange],"STACK")

    # Plotting the data and proccedding!
    cmsstyle.cmsObjectDraw(hdata,"E",MarkerStyle=ROOT.kFullCircle)
    plotlegend.Draw()

    # Saving the result!
    cmsstyle.UpdatePad(c)

    c.SaveAs("test_THStack.png")

# # # #
# This is the older code
def test_THStack_OLDER ():
    """Make the plot
    """

    cmsstyle.setCMSStyle()  # Setting the style

    # Producing the histograms to plot
    h1 = ROOT.TH1F("test1","test1",60,0.0,10.0)
    h2 = ROOT.TH1F("test2","test2",60,0.0,10.0)

    for i in range(1,61):
        h1.SetBinContent(i,10*math.exp(-i/5.0))
        h2.SetBinContent(i,8*math.exp(-i/15.0))

    tg = ROOT.TF1("fb","gaus(0)",0.0,10.0)
    tg.SetParameter(0,5.0)
    tg.SetParameter(1,3.0)
    tg.SetParameter(2,1.0)
    tg.SetNpx(60)
    hg = tg.CreateHistogram().Clone()

    h2.SetFillColor(cmsstyle.p10.kBrown)
    h1.SetFillColor(cmsstyle.p10.kBlue)
    hg.SetFillColor(cmsstyle.p10.kOrange)
    hg.SetFillStyle(1001)
    hg.SetLineColor(ROOT.kBlack)  # By default from functions is kRed(?)

    # Building the "data" histogram:

    hdata = h1.Clone("data")
    for i in range(1,61):
        yval = h1.GetBinContent(i) + h2.GetBinContent(i) + hg.GetBinContent(i)

        hdata.SetBinError(i,0.12*yval)
        hdata.SetBinContent(i, yval*(1+0.1*math.cos(6.28*i/20.)))

    # Now we have the histograms to plot, so setting up the plot!

    plotlegend = cmsstyle.cmsLeg(0.5,0.5,0.8,0.8)  # The legend!

    # Building the THStack and plotting it from the background histograms

    if True:   # Set it to True for building the THStack explicitly.
        hs = ROOT.THStack("hs","STACK")
        hs.Add(h2)
        hs.Add(h1)
        hs.Add(hg)

        c = cmsstyle.cmsCanvas("Testing",0.0,10.0,0.08,1.3*cmsstyle.cmsReturnMaxY(hs),
                               "X var [test]","Y var");

        plotlegend.AddEntry(hdata,"Data","p")
        plotlegend.AddEntry(h2,"Sample 1","f")
        plotlegend.AddEntry(h1,"Sample 2","f")
        plotlegend.AddEntry(hg,"Signal","f")

        cmsstyle.cmsObjectDraw(hs,"")
        cmsstyle.cmsObjectDraw(hdata,"E",MarkerStyle=ROOT.kFullCircle)

    else:  # Using the old (very involved) way...
        c = cmsstyle.cmsCanvas("Testing",0.0,10.0,0.08,1.3*cmsstyle.cmsReturnMaxY(hs),
                               "X var [test]","Y var");

        x = ROOT.THStack("hs","STACK")
        cmsstyle.cmsDrawStack(x,plotlegend,{'Sample 1':h2,'Sample 2':h1,'Signal':hg},hdata,[cmsstyle.p10.kBrown,cmsstyle.p10.kBlue,cmsstyle.p10.kOrange])

    plotlegend.Draw()

    # Saving the result!
    cmsstyle.UpdatePad(c)

    c.SaveAs("test_THStack.png")

#    input()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# For running as a shell command to get the list of files (comma-separated)
if __name__ == '__main__':
#    test_THStack_OLDER()
    test_THStack()

# #######################################################################
