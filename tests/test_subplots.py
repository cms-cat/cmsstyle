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
    ncolumns = 2
    nrows = 6

    cvm = cmsstyle.subplots(
        ncolumns=ncolumns,
        nrows=nrows,
        height_ratios=[2, 1] * (nrows // 2),
        canvas_top_margin=0.1,
        canvas_bottom_margin=0.03,
        axis_label_size = 40
        )

    data, hs, h_err, ratio, yerr_root, ref_line, bkg, signal = _create_drawables()

    cvm.plot_common_legend(
        cvm.top_pad,
        cmsstyle.LegendItem(data, "Uncertainty", "pe"),
        cmsstyle.LegendItem(bkg, "MC1", "f"),
        cmsstyle.LegendItem(signal, "MC2", "f"),
        cmsstyle.LegendItem(ratio, "Ratio", "pe"),
        cmsstyle.LegendItem(ratio, "Ratio", "pe"),
        cmsstyle.LegendItem(signal, "Testing", "f"),
        cmsstyle.LegendItem(data, "Data", "pe"),
        cmsstyle.LegendItem(bkg, "MC1", "f"),
        cmsstyle.LegendItem(signal, "MC2", "f"),
        cmsstyle.LegendItem(data, "Hello", "pe"),
        cmsstyle.LegendItem(ratio, "BigTitle", "pe"),
        textalign=12,
        ipos = 11
    )
    cvm.plot_text(
        cvm.top_pad,
        "Run 2, 138 fb^{#minus1}",
        )
    cvm.plot_text(
        cvm.bottom_pad,
        "m^{ll} (GeV)",
        textsize=50,
        )
    cvm.ylabel(labels={0:"Test0", 2:"", 4:"Test4", 6:"", 8:"Test8", 10:""})

    row_index = -1
    for i, pad in enumerate(cvm.pads):
        if i % ncolumns == 0:
            row_index += 1
        if row_index % 2 == 0:
            pad.plot(hs)
            pad.plot(h_err, "E2SAME0", FillColor=ROOT.kBlack, LineWidth=1, LineColor=355, FillStyle=3004)
            pad.plot(data, "E1X0", FillColor=kBlue)
        else:
            pad.plot(yerr_root, "E2SAME0", LineWidth=100, MarkerSize=0, FillColor=ROOT.kBlack, FillStyle=3004)
            pad.plot(ratio, "E1X0")
            pad.plot(ref_line, LineColor=ROOT.kBlack, LineStyle=ROOT.kDotted)

    cvm.save_figure("cmsstyle_subplots.png")


if __name__ == "__main__":
    test_subplots()