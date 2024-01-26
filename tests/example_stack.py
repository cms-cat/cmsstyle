import os, ROOT
import numpy as np
import cmsstyle as CMS

CMS.SetExtraText("Simulation")


class Plotter:
    def __init__(self):
        self.outputPath = "./pdfs_stack"
        os.makedirs(self.outputPath, exist_ok=True)
        self.CreateHistograms()

    def CreateHistograms(self):
        self.bkgs = []
        for i in range(0,6):
            h = ROOT.TH1F("bkg{}".format(i), "bkg{}".format(i), 100, 0, 10)
            for _ in range(16666):
                h.Fill(np.random.normal(5, 1))
                #h.Scale(1.0 / h.Integral())
            self.bkgs.append(h)

    def Plot(self, square, iPos):
        canv_name = f'example_{"square" if square else "rectangle"}_pos{iPos}'
        CMS.SetLumi("")
        CMS.SetEnergy("13")
        # Write extra lines below the extra text (usuful to define regions/channels)
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
        #canv.SetLogy(True)
        leg = CMS.cmsLeg(0.81, 0.89 - 0.05 * 7, 0.99, 0.89, textSize=0.04)

        # Draw objects in one line
        hist_dict = {}
        names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
        for n, hist in enumerate(self.bkgs):
            hist_dict[names[n]] =  hist
        print(hist_dict)
        CMS.cmsDrawStack(hist_dict, stack,  leg)
        #CMS.cmsDrawStack({"background new": self.bkg, "signal new": self.signal,}, leg)

        # Takes care of fixing overlay and closing object
        CMS.SaveCanvas(canv, os.path.join(self.outputPath, canv_name + ".pdf"))

def main():
    plotter = Plotter()
    plotter.Plot(square=CMS.kSquare, iPos=0)
    plotter.Plot(square=CMS.kRectangular, iPos=0)
    plotter.Plot(square=CMS.kSquare, iPos=11)
    plotter.Plot(square=CMS.kRectangular, iPos=11)


if __name__ == "__main__":
    main()
