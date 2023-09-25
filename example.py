import os, ROOT
import numpy as np
import tdrstyle as TDR
TDR.extraText  = 'Simulation Preliminary'

class Plotter():
    def __init__(self):
        self.outputPath = './pdfs'
        os.makedirs(self.outputPath, exist_ok=True)
        self.CreateHistograms()
    
    def CreateHistograms(self):
        self.data = ROOT.TH1F('data', 'data', 50, 0,100)
        self.bkg = ROOT.TH1F('bkg', 'bkg', 50, 0,100)
        self.signal = ROOT.TH1F('signal', 'signal', 50, 0,100)
        
        for _ in range(10000):
            self.bkg.Fill(np.random.exponential(30))
            self.data.Fill(np.random.exponential(30))
        for _ in range(1000):
            self.signal.Fill(np.random.normal(30,5))
            self.data.Fill(np.random.normal(30,5))
        self.signal.Scale(0.1/self.signal.Integral())
        self.bkg.Scale(1./self.bkg.Integral())
        self.bkg_tot = self.bkg.Clone('bkg_tot')
        self.bkg_tot.Add(self.signal)
        
        self.data.Scale(self.bkg_tot.Integral()/self.data.Integral())
        self.ratio = self.data.Clone('ratio')
        self.ratio_nosignal = self.data.Clone('ratio_nosignal')
        
        self.ratio.Divide(self.bkg_tot)
        self.ratio_nosignal.Divide(self.bkg)

        self.hist2d = ROOT.TH2F("hist2d", "2D Histogram", 25, 0, 5, 25, 0, 5)
        for i in range(200000):
            x = np.random.normal(2.5,1)
            y = np.random.normal(2.5,1)
            self.hist2d.Fill(x, y)
        self.hist2d.Scale(10./self.hist2d.Integral())
        
    def Plot(self, square, iPos):
        canv_name = f'example_{"square" if square else "rectangle"}_pos{iPos}'
        TDR.SetLumi('138')
        TDR.SetEnergy('13')
        # Write extra lines below the extra text (usuful to define regions/channels)
        TDR.additionalInfoFont = 42
        TDR.additionalInfo = []
        TDR.additionalInfo.append('Signal region')
        TDR.additionalInfo.append('#mu-channel')
        
        canv = TDR.tdrCanvas(canv_name, 0, 90, 1e-3, 2, 'X', 'A.U.', square=square, extraSpace=0.01, iPos=iPos)
        canv.SetLogy(True)
        leg = TDR.tdrLeg(0.60,0.89-0.04*4,0.89,0.89, textSize=0.04)
        
        # Draw objects in one line
        TDR.tdrDraw(self.bkg, 'hist', fcolor=ROOT.kAzure+2, alpha=0.5)
        TDR.tdrDraw(self.signal, 'hist', fcolor=ROOT.kRed+1, alpha=0.5)
        TDR.tdrDraw(self.data, 'P', mcolor=ROOT.kBlack)

        leg.AddEntry(self.data, 'Data', 'lp')
        leg.AddEntry(self.bkg, 'Background', 'f')
        leg.AddEntry(self.signal, 'Signal', 'f')
        
        # Takes care of fixing overlay and closing object
        TDR.SaveCanvas(canv, os.path.join(self.outputPath, canv_name+'.pdf'))
        
        canv_name += '_ratio'
        dicanv = TDR.tdrDiCanvas(canv_name, 10, 90, 0, 0.2, 0.0, 2.0, 'X', 'A.U.', 'Data/Pred.', square=square, extraSpace=0.1, iPos=iPos)
        dicanv.cd(1)
        
        leg = TDR.tdrLeg(0.60,0.89-0.05*5,0.89,0.89, textSize=0.05)
        leg.AddEntry(self.data, 'Data', 'lp')
        leg.AddEntry(self.bkg, 'Background', 'f')
        leg.AddEntry(self.signal, 'Signal', 'f')
        
        TDR.tdrHeader(leg, 'With title', textSize=0.05)
        
        TDR.tdrDraw(self.bkg_tot, 'hist', fcolor=ROOT.kRed+1, alpha=0.5)
        TDR.tdrDraw(self.bkg, 'hist', fcolor=ROOT.kAzure+2, alpha=0.9)
        TDR.tdrDraw(self.data, 'P', mcolor=ROOT.kBlack)
        
        TDR.fixOverlay()

        dicanv.cd(2)
        leg_ratio = TDR.tdrLeg(0.15,0.98-0.05*5,0.40,0.98, textSize=0.05, columns=2)
        #how alternative way to pass style options
        style = {'style':'hist', 'lcolor':ROOT.kAzure+2, 'lwidth':2, 'fstyle':0 }
        TDR.tdrDraw(self.ratio_nosignal, **style)
        TDR.tdrDraw(self.ratio, 'P', mcolor=ROOT.kBlack)
        
        leg_ratio.AddEntry(self.ratio, 'Bkg', 'lp')
        leg_ratio.AddEntry(self.ratio_nosignal, 'Bkg+Signal', 'l')

        ref_line = ROOT.TLine(10, 1, 90, 1)
        TDR.tdrDrawLine(ref_line, lcolor=ROOT.kBlack, lstyle=ROOT.kDotted)
        
        TDR.SaveCanvas(dicanv, os.path.join(self.outputPath, canv_name+'.pdf'))
    
    def Plot2D(self, square, iPos):
        canv_name = f'example_2D_{"square" if square else "rectangle"}_pos{iPos}'
        # Allow to reduce the size of the lumi info 
        scaleLumi = (0.80 if square else None)
        canv = TDR.tdrCanvas(canv_name, 0, 5, 0, 5, 'X', 'Y', square=square, extraSpace = 0.01, iPos=iPos, with_z_axis=True, scaleLumi=scaleLumi)

        self.hist2d.GetZaxis().SetTitle('Events normalised')
        self.hist2d.GetZaxis().SetTitleOffset(1.4 if square else 1.2)
        self.hist2d.Draw('same colz')
        # Set a new palette
        TDR.SetAlternative2DColor(self.hist2d, TDR.tdrStyle)
        
        # Allow to adjust palette position
        X1 =TDR.GettdrCanvasHist(canv).GetXaxis().GetXmax()+ 0.1
        X2 =TDR.GettdrCanvasHist(canv).GetXaxis().GetXmax()+ (0.3 if square else 0.5)
        Y1 =TDR.GettdrCanvasHist(canv).GetYaxis().GetXmin()
        Y2 =TDR.GettdrCanvasHist(canv).GetYaxis().GetXmax()
        TDR.UpdatePalettePosition(self.hist2d, X1=None, X2=None, Y1=None, Y2=None)
        
        TDR.SaveCanvas(canv, os.path.join(self.outputPath, canv_name+'.pdf'))


def main():
    plotter = Plotter()
    plotter.Plot(square = TDR.kSquare, iPos=0)
    plotter.Plot(square = TDR.kRectangular, iPos=0)
    plotter.Plot(square = TDR.kSquare, iPos=11)
    plotter.Plot(square = TDR.kRectangular, iPos=11)
    plotter.Plot2D(square = TDR.kSquare, iPos=0)
    plotter.Plot2D(square = TDR.kRectangular, iPos=0)

if __name__ == '__main__':
    main()
