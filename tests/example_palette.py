import os, ROOT
import cmsstyle as CMS

CMS.SetExtraText("Simulation")

class Plotter:
    def __init__(self):
        self.outputPath = "./pdfs_palette"
        os.makedirs(self.outputPath, exist_ok=True)
        self.CreateHistograms()

    def CreateHistograms(self):
        self.bkgs = []
        f_gaus51 = ROOT.TF1("gaus51","gaus", 0, 10)
        f_gaus51.SetParameters(1, 5, 1)
        for i in range(0,6):
            h = ROOT.TH1F("bkg{}".format(i), "bkg{}".format(i), 100, 0, 10)
            h.FillRandom("gaus51", 16666)
            self.bkgs.append(h)

        f_gaus2 = ROOT.TF2("gaus2", "xygaus", 0, 5, 0, 5)
        f_gaus2.SetParameters(1, 2.5, 1, 2.5, 1)
        self.hist2d = ROOT.TH2F("hist2d", "2D Histogram", 25, 0, 5, 25, 0, 5)
        self.hist2d.FillRandom("gaus2", 200000)
        self.hist2d.Scale(10.0 / self.hist2d.Integral())

    def Plot(self, square, iPos):
        canv_name = f'example_{"square" if square else "rectangle"}_pos{iPos}'
        CMS.SetLumi("")
        CMS.SetEnergy("13")
        CMS.ResetAdditionalInfo()

        stack = ROOT.THStack("stack", "Stacked")

        canv = CMS.cmsCanvas(
            canv_name,
            0,
            10,
            1e-3,
            4300,
            "X",
            "",
            square=square,
            extraSpace=0.01,
            iPos=iPos,
        )
        leg = CMS.cmsLeg(0.81, 0.89 - 0.05 * 7, 0.99, 0.89, textSize=0.04)

        # Put samples together and draw them stacked
        hist_dict = {}
        names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
        for n, hist in enumerate(self.bkgs):
            hist_dict[names[n]] =  hist
        CMS.cmsDrawStack(stack, leg, hist_dict)

        # Takes care of fixing overlay and closing object
        CMS.SaveCanvas(canv, os.path.join(self.outputPath, canv_name + ".pdf"))

    def Plot2D(self, square, iPos):
        canv_name = f'example_2D_{"square" if square else "rectangle"}_pos{iPos}'
        # Allow to reduce the size of the lumi info
        scaleLumi = 0.80 if square else None
        canv = CMS.cmsCanvas(
            canv_name,
            0,
            5,
            0,
            5,
            "X",
            "Y",
            square=square,
            extraSpace=0.01,
            iPos=iPos,
            with_z_axis=True,
            scaleLumi=scaleLumi,
        )

        self.hist2d.GetZaxis().SetTitle("Events normalised")
        self.hist2d.GetZaxis().SetTitleOffset(1.4 if square else 1.2)
        self.hist2d.Draw("same colz")
        
        # Set the CMS official palette
        CMS.SetCMSPalette()

        # Allow to adjust palette position
        CMS.UpdatePalettePosition(self.hist2d, canv)

        CMS.SaveCanvas(canv, os.path.join(self.outputPath, canv_name + ".pdf"))

def main():
    plotter = Plotter()
    plotter.Plot(square=CMS.kSquare, iPos=0)
    plotter.Plot(square=CMS.kRectangular, iPos=0)
    plotter.Plot(square=CMS.kSquare, iPos=11)
    plotter.Plot(square=CMS.kRectangular, iPos=11)
    plotter.Plot2D(square=CMS.kSquare, iPos=0)
    plotter.Plot2D(square=CMS.kRectangular, iPos=0)

if __name__ == "__main__":
    main()
