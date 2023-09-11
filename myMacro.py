import ROOT as rt
import CMS_lumi, tdrstyle
import array

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

# 
# Simple example of macro: plot with CMS name and lumi text
#  (this script does not pretend to work in all configurations)
# iPeriod = 1*(0/1 7 TeV) + 2*(0/1 8 TeV)  + 4*(0/1 13 TeV) 
# For instance: 
#               iPeriod = 3 means: 7 TeV + 8 TeV
#               iPeriod = 7 means: 7 TeV + 8 TeV + 13 TeV 
#               iPeriod = 0 means: free form (uses lumi_sqrtS)
# Initiated by: Gautier Hamel de Monchenault (Saclay)
# Translated in Python by: Joshua Hardenbrook (Princeton)
# Updated by:   Dinko Ferencek (Rutgers)
#

iPeriod = 3

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

canvas = rt.TCanvas("c2","c2",50,50,W,H)
canvas.SetFillColor(0)
canvas.SetBorderMode(0)
canvas.SetFrameFillStyle(0)
canvas.SetFrameBorderMode(0)
canvas.SetLeftMargin( L/W )
canvas.SetRightMargin( R/W )
canvas.SetTopMargin( T/H )
canvas.SetBottomMargin( B/H )
canvas.SetTickx(0)
canvas.SetTicky(0)

h =  rt.TH1F("h","h; m_{e^{+}e^{-}} (GeV); Events / 0.5 GeV",80,70,110)

h.SetMaximum(260)

xAxis = h.GetXaxis()
xAxis.SetNdivisions(6,5,0)

yAxis = h.GetYaxis()
yAxis.SetNdivisions(6,5,0)
yAxis.SetTitleOffset(1)

h.Draw()

file = rt.TFile("histo.root","READ")
data = file.Get("data")
MC   = file.Get("MC")

MC.Draw("histsame")
data.Draw("esamex0")

#draw the lumi text on the canvas
CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

canvas.cd()
canvas.Update()
canvas.RedrawAxis()
frame = canvas.GetFrame()
frame.Draw()


#set the colors and size for the legend
histLineColor = rt.kOrange+7
histFillColor = rt.kOrange-2
markerSize  = 1.0

latex = rt.TLatex()
n_ = 2

x1_l = 0.92
y1_l = 0.60

dx_l = 0.30
dy_l = 0.18
x0_l = x1_l-dx_l
y0_l = y1_l-dy_l

legend =  rt.TPad("legend_0","legend_0",x0_l,y0_l,x1_l, y1_l )
#legend.SetFillColor( rt.kGray )
legend.Draw()
legend.cd()

ar_l = dy_l/dx_l
#gap_ = 0.09/ar_l
gap_ = 1./(n_+1)
bwx_ = 0.12
bwy_ = gap_/1.5

x_l = [1.2*bwx_]
#y_l = [1-(1-0.10)/ar_l]
y_l = [1-gap_]
ex_l = [0]
ey_l = [0.04/ar_l]

#array must be converted 
x_l = array.array("f",x_l)
ex_l = array.array("f",ex_l)
y_l = array.array("f",y_l)
ey_l = array.array("f",ey_l)

gr_l =  rt.TGraphErrors(1, x_l, y_l, ex_l, ey_l)

rt.gStyle.SetEndErrorSize(0)
gr_l.SetMarkerSize(0.9)
gr_l.Draw("0P")

latex.SetTextFont(42)
latex.SetTextAngle(0)
latex.SetTextColor(rt.kBlack)    
latex.SetTextSize(0.25)    
latex.SetTextAlign(12) 

box_ = rt.TBox()
xx_ = x_l[0]
yy_ = y_l[0]
latex.DrawLatex(xx_+1.*bwx_,yy_,"Data")

yy_ -= gap_
box_.SetLineStyle( rt.kSolid )
box_.SetLineWidth( 1 )
# box_.SetLineColor( kBlack )
box_.SetLineColor( histLineColor )
box_.SetFillColor( histFillColor )
box_.DrawBox( xx_-bwx_/2, yy_-bwy_/2, xx_+bwx_/2, yy_+bwy_/2 )
box_.SetFillStyle(0)
box_.DrawBox( xx_-bwx_/2, yy_-bwy_/2, xx_+bwx_/2, yy_+bwy_/2 )
#Draw Z->ee text
latex.DrawLatex(xx_+1.*bwx_,yy_,"Z #rightarrow e^{+}e^{-} (MC)")

#update the canvas to draw the legend
canvas.Update()

raw_input("Press Enter to end")
