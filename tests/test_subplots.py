import ROOT
import cmsstyle
import math

try:
    kBlue = ROOT.kP6Blue
    kYellow = ROOT.kP6Yellow
    
except: 
    kBlue = ROOT.TColor.GetColor("#5790fc")
    kYellow = ROOT.TColor.GetColor("#f89c20")

def _create_drawables():
    """Create some graphics to draw later."""
    _ = ROOT.TF1("fsignal", "TMath::Gaus(x,0,0.5)", -2, 2)
    signal = ROOT.TH1D("signal", "Histogram", 20, -2, 2)
    signal.FillRandom("fsignal", 1000)

    bkg = ROOT.TH1D("bkg", "Histogram", 20, -2, 2)
    bkg.FillRandom("pol0", 1000)

    data = ROOT.TH1D("data", "Histogram", 20, -2, 2)
    data.FillRandom("fsignal", 1000)
    data.FillRandom("pol0", 1000)

    bkg_tot = bkg + signal

    h_err = bkg_tot.Clone("h_err")

    ratio = data.Clone("ratio")
    ratio.Divide(bkg_tot)

    for i in range(1, ratio.GetNbinsX()+1):
        if (ratio.GetBinContent(i)):
            ratio.SetBinError(i, math.sqrt(data.GetBinContent(i))/bkg_tot.GetBinContent(i))
        else:
            ratio.SetBinError(i, 10 ^ (-99))

    yerr_root = ROOT.TGraphAsymmErrors()
    yerr_root.Divide(data, bkg_tot, 'pois')

    for i in range(0, yerr_root.GetN()+1):
        yerr_root.SetPointY(i, 1)
    ref_line = ROOT.TLine(-2, 1, 2, 1)

    hs = ROOT.THStack("hstack", "STACK")
    hs.Add(bkg)
    hs.Add(signal)

    # Some graphical attributes here, usually dealt via cmsstyle functions
    signal.SetFillColor(kBlue)
    bkg.SetFillColor(kYellow)
    data.SetFillColor(kBlue)

    return data, hs, h_err, ratio, yerr_root, ref_line, bkg, signal


def test_subplots():
    """Example of multiple plots in the same canvas, with shared common legend"""
    cmsstyle.setCMSStyle()

    # set the luminosity, the COM energy, the Run period to show in the canvases
    cmsstyle.SetLumi(34.8, run='2022')
    cmsstyle.SetEnergy(13.6)
    # default extra text is "Preliminary", set it to an empty string to remove it
    cmsstyle.SetExtraText('')

    ncolumns = 2
    nrows = 6

    cvm = cmsstyle.cmsMultiCanvas(
        canvName="",
        nColumns=ncolumns,
        nRows=nrows,
        heightRatios=[3, 1] * (nrows // 2),
        Xlimits={
            0: [-2, 2], 1: [-2, 2],
            2: [-2, 2], 3: [-2, 2],
            4: [-2, 2], 5: [-2, 2],
            6: [-2, 2], 7: [-2, 2],
            8: [-2, 2], 9: [-2, 2],
            10: [-2, 2], 11: [-2, 2]
            },
        Ylimits={
            0: [0, 500], 1: [1, 500],
            2: [0.5, 1.5], 3: [0.5, 1.5],
            4: [0, 500], 5: [0, 500],
            6: [0.5, 1.5], 7: [0.5, 1.5],
            8: [0, 500], 9: [0, 500],
            10: [0.5, 1.5], 11: [0.5, 1.5]
            },
        nameXaxis="m^{ll} (GeV)",
        nameYaxis={0:"Test0", 2:"", 4:"Test4", 6:"", 8:"Test8", 10:""},
        labelTextSize=30,
        titleTextSize=40,
        lumiTextSize=50,
        logoTextSize=50 * 0.75 / 0.6,
        legendTextSize=30,
        canvasTopMargin=0.1,
        canvasBottomMargin=0.03,
        canvasHeight=2000,
        iPos=11
        )

    data, hs, h_err, ratio, yerr_root, ref_line, bkg, signal = _create_drawables()

    _ = cmsstyle.cmsMultiCanvasLeg(cvm,
        (data, "Uncertainty", "pe"),
        (bkg, "MC1", "f"),
        (signal, "MC2", "f"),
        (ratio, "Ratio", "pe"),
        (ratio, "Ratio", "pe"),
        (signal, "Testing", "f"),
        (data, "Data", "pe"),
        (bkg, "MC1", "f"),
        (signal, "MC2", "f"),
        (data, "Hello", "pe"),
        (ratio, "BigTitle", "pe"),
    )

    row_index = -1
    for i, pad in enumerate(cvm.pads):
        if i % ncolumns == 0:
            row_index += 1
        if row_index % 2 == 0:
            pad.plot(hs)
            pad.plot(h_err, "E2SAME0", FillColor=ROOT.kBlack, MarkerSize=0, LineWidth=1, LineColor=355, FillStyle=3004)
            pad.plot(data, "E1X0", FillColor=kBlue)
        else:
            pad.plot(yerr_root, "E2SAME0", LineWidth=100, MarkerSize=0, FillColor=ROOT.kBlack, FillStyle=3004)
            pad.plot(ratio, "E1X0")
            pad.plot(ref_line, LineColor=ROOT.kBlack, LineStyle=ROOT.kDotted)

    cvm.save_figure("cmsstyle_subplots.png")


if __name__ == "__main__":
    test_subplots()