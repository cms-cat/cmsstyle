/// @file
/// <PRE>
/// This file contains the method associated to the CMSStyle package. It is the one to be used
/// when compiling the version using any of the following command:
///
///       root[] .L cmsstyle.C++   (or equivalently with CompileMacro() or LoadMacro())
///
/// but it can also be loaded from an interactive session of ROOT as
///
///       root[] .L cmsstyle.C
///
/// </PRE>

#include "colorsets.H"

#include "cmsstyle.H"

#include <RVersion.h>
#include <TROOT.h>
#include <TColor.h>
#include <TFrame.h>

#include <iostream>
#include <algorithm>

// Globals from ROOT

extern TROOT *gROOT;
#include <TVirtualPad.h>  // Included definition of gPad

namespace cmsstyle {

// ----------------------------------------------------------------------
void setCMSStyle (bool force)
  // Method to setup the style for the ROOT session!
{
  if (cmsStyle!=nullptr) delete cmsStyle;  // Starting from scratch!

  cmsStyle = new TStyle("cmsStyle", "Style for P-CMS");

  gROOT->SetStyle(cmsStyle->GetName());
  gROOT->ForceStyle(force);

  // For the canvas:

  cmsStyle->SetCanvasBorderMode(0);
  cmsStyle->SetCanvasColor(kWhite);
  cmsStyle->SetCanvasDefH(600);  // Height of canvas
  cmsStyle->SetCanvasDefW(600);  // Width of canvas
  cmsStyle->SetCanvasDefX(0);    // Position on screen
  cmsStyle->SetCanvasDefY(0);
  cmsStyle->SetPadBorderMode(0);
  cmsStyle->SetPadColor(kWhite);
  cmsStyle->SetPadGridX(kFALSE);
  cmsStyle->SetPadGridY(kFALSE);
  cmsStyle->SetGridColor(0);
  cmsStyle->SetGridStyle(3);
  cmsStyle->SetGridWidth(1);

  // For the frame:
  cmsStyle->SetFrameBorderMode(0);
  cmsStyle->SetFrameBorderSize(1);
  cmsStyle->SetFrameFillColor(0);
  cmsStyle->SetFrameFillStyle(0);
  cmsStyle->SetFrameLineColor(1);
  cmsStyle->SetFrameLineStyle(1);
  cmsStyle->SetFrameLineWidth(1);

  // For the histo:
  cmsStyle->SetHistLineColor(1);
  cmsStyle->SetHistLineStyle(0);
  cmsStyle->SetHistLineWidth(1);
  cmsStyle->SetEndErrorSize(2);
  cmsStyle->SetMarkerStyle(20);

  // For the fit/function:
  cmsStyle->SetOptFit(1);
  cmsStyle->SetFitFormat("5.4g");
  cmsStyle->SetFuncColor(2);
  cmsStyle->SetFuncStyle(1);
  cmsStyle->SetFuncWidth(1);

  // For the date:
  cmsStyle->SetOptDate(0);

  // For the statistics box:
  cmsStyle->SetOptFile(0);
  cmsStyle->SetOptStat(0);  // To display the mean and RMS:   SetOptStat('mr')
  cmsStyle->SetStatColor(kWhite);
  cmsStyle->SetStatFont(42);
  cmsStyle->SetStatFontSize(0.025);
  cmsStyle->SetStatTextColor(1);
  cmsStyle->SetStatFormat("6.4g");
  cmsStyle->SetStatBorderSize(1);
  cmsStyle->SetStatH(0.1);
  cmsStyle->SetStatW(0.15);

  // Margins:
  cmsStyle->SetPadTopMargin(0.05);
  cmsStyle->SetPadBottomMargin(0.13);
  cmsStyle->SetPadLeftMargin(0.16);
  cmsStyle->SetPadRightMargin(0.02);

  // For the Global title:
  cmsStyle->SetOptTitle(0);
  cmsStyle->SetTitleFont(42);

  cmsStyle->SetTitleColor(1);
  cmsStyle->SetTitleTextColor(1);
  cmsStyle->SetTitleFillColor(10);
  cmsStyle->SetTitleFontSize(0.05);

  // For the axis titles:
  cmsStyle->SetTitleColor(1, "XYZ");
  cmsStyle->SetTitleFont(42, "XYZ");
  cmsStyle->SetTitleSize(0.06, "XYZ");
  cmsStyle->SetTitleXOffset(0.9);
  cmsStyle->SetTitleYOffset(1.25);

  // For the axis labels:
  cmsStyle->SetLabelColor(1, "XYZ");
  cmsStyle->SetLabelFont(42, "XYZ");
  cmsStyle->SetLabelOffset(0.012, "XYZ");
  cmsStyle->SetLabelSize(0.05, "XYZ");

  // For the axis:
  cmsStyle->SetAxisColor(1, "XYZ");
  cmsStyle->SetStripDecimals(kTRUE);
  cmsStyle->SetTickLength(0.03, "XYZ");
  cmsStyle->SetNdivisions(510, "XYZ");
  cmsStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
  cmsStyle->SetPadTickY(1);

  // Change for log plots:
  cmsStyle->SetOptLogx(0);
  cmsStyle->SetOptLogy(0);
  cmsStyle->SetOptLogz(0);

  // Postscript options:
  cmsStyle->SetPaperSize(20.0, 20.0);
  cmsStyle->SetHatchesLineWidth(5);
  cmsStyle->SetHatchesSpacing(0.05);

  // Some additional parameters we need to set as "style"

  if (ROOT_VERSION_MAJOR>6 || (ROOT_VERSION_MINOR>=32 && ROOT_VERSION_MAJOR==6)) {  // Not available before 6.32!
      TColor::DefinedColors(1);
  }

  // Using the Style.
  cmsStyle->cd();
}

// ----------------------------------------------------------------------
void SetEnergy (float energy, const std::string &unit)
  // This methos sets the centre-of-mass energy value and unit to be displayed.
{
  if (energy==0) cms_energy=unit;
  else {
    if (fabs(energy-13)<0.001) cms_energy="13 ";
    else if (fabs(energy-13.6)<0.001) cms_energy="13.6 ";
    else {
      std::cerr<<"ERROR: Unsupported value of the energy... use manual setting of the cms_energy value"<<std::endl;
      cms_energy="???? ";
    }
    cms_energy += unit;
  }
}

// ----------------------------------------------------------------------



// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
Float_t cmsReturnMaxY (const std::vector<TObject *> objs)
  // Returns the maximum value associated to the objects that are going to be
  // plotted.
{
  Float_t maxval=0;

  for (auto xobj : objs) {
    if (xobj->InheritsFrom(TH1::Class())) {   // An Histogram
      Float_t value = ((TH1*) xobj)->GetBinContent(((TH1*) xobj)->GetMaximumBin());
      value += ((TH1*) xobj)->GetBinError(((TH1*) xobj)->GetMaximumBin());

      if (maxval<value) maxval=value;
    }
    else if (xobj->InheritsFrom(TGraph::Class())) {
      // TGraph are special as GetMaximum exists but it is a bug value.
      Float_t value = 0;

      Int_t i = ((TGraph *) xobj)->GetN();
      Double_t *y = ((TGraph *) xobj)->GetY();
      Double_t *ey = ((TGraph *) xobj)->GetEY();

      while (i>0) {
        i -= 1;

        Float_t ivalue = y[i];
        ivalue += std::max(ey[i],((TGraph *) xobj)->GetErrorYhigh(i));
      }

      if (maxval<value) maxval=value;
    }

  }

  return maxval;
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
TCanvas *cmsCanvas (const char *canvName,
                    Float_t x_min,
                    Float_t x_max,
                    Float_t y_min,
                    Float_t y_max,
                    const char *nameXaxis,
                    const char *nameYaxis,
                    Bool_t square,
                    Int_t iPos,
                    Float_t extraSpace,
                    Bool_t with_z_axis,
                    Float_t scaleLumi,
                    Float_t yTitOffset)
  // his method defines and returns the TCanvas for a normal/basic plot.
{
  // Set CMS style if not set already
  if (cmsStyle==nullptr) setCMSStyle();

  // Set canvas dimensions and margins
  Int_t H = 600;

  Float_t W = 800;
  if (square) W = 600;

  Float_t T = 0.07 * H;     // Margin borders in absolute (size) value
  Float_t B = 0.11 * H;
  Float_t L = 0.13 * H;
  Float_t R = 0.03 * H;

  // Setting up the TCanvas
  TCanvas *canv = new TCanvas(canvName, canvName, 50, 50, W, H);
  canv->SetFillColor(0);
  canv->SetBorderMode(0);
  canv->SetFrameFillStyle(0);
  canv->SetFrameBorderMode(0);
  canv->SetLeftMargin(L / W + extraSpace);

  canv->SetRightMargin(R / W);
  if (with_z_axis) canv->SetRightMargin(B / W + 0.03);

  canv->SetTopMargin(T / H);
  canv->SetBottomMargin(B / H + 0.02);

  // Draw the frame for plotting things and set axis labels
  TH1 *h = canv->DrawFrame(x_min, y_min, x_max, y_max);

  Float_t y_offset = 0.78;
  if (yTitOffset<-998) {
    y_offset = 0.78;
    if (square) y_offset = 1.0;
  }
  else y_offset = yTitOffset;

  h->GetYaxis()->SetTitleOffset(y_offset);
  h->GetXaxis()->SetTitleOffset(0.9);
  h->GetXaxis()->SetTitle(nameXaxis);
  h->GetYaxis()->SetTitle(nameYaxis);
  h->Draw("AXIS");

  // Draw CMS logo and update canvas
  CMS_lumi(canv, iPos, scaleLumi);

  UpdatePad(canv);
  canv->GetFrame()->Draw();

  return canv;
}

// ----------------------------------------------------------------------
void CMS_lumi (TPad *ppad, Int_t iPosX, Float_t scaleLumi)
  // This is the method to draw the "CMS" seal (logo and text) and put the
  // luminosity value.
{
  /// This is the key method about forcing the CMSStyle. The original python
  /// implementation was complicated and obscure, so rewritten here with a
  /// cleaner coding.



}


// ----------------------------------------------------------------------
void setRootObjectProperties (TObject *obj,
                              std::map<std::string,Float_t> confs)

{

  for ( auto xcnf : confs ) {
    if (xcnf.first=="SetLineColor" || xcnf.first=="LineColor") dynamic_cast<TAttLine*>(obj)->SetLineColor(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetLineStyle" || xcnf.first=="LineStyle") dynamic_cast<TAttLine*>(obj)->SetLineStyle(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetLineWidth" || xcnf.first=="LineWidth") dynamic_cast<TAttLine*>(obj)->SetLineWidth(xcnf.second);

    else if (xcnf.first=="SetFillColor" || xcnf.first=="FillColor") dynamic_cast<TAttFill*>(obj)->SetFillColor(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetFillStyle" || xcnf.first=="FillStyle") dynamic_cast<TAttFill*>(obj)->SetFillStyle(1001); //Int_t(xcnf.second+0.5));

    else if (xcnf.first=="SetMarkerColor" || xcnf.first=="MarkerColor") dynamic_cast<TAttMarker*>(obj)->SetMarkerColor(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetMarkerSize" || xcnf.first=="MarkerSize") dynamic_cast<TAttMarker*>(obj)->SetMarkerSize(xcnf.second);
    else if (xcnf.first=="SetMarkerStyle" || xcnf.first=="MarkerStyle") dynamic_cast<TAttMarker*>(obj)->SetMarkerStyle(Int_t(xcnf.second+0.5));




  }


}

// ----------------------------------------------------------------------
void cmsObjectDraw(TObject *obj,
                   Option_t *option,
                   std::map<std::string,Float_t> confs)

{
  setRootObjectProperties(obj,confs);

  std::string prefix(option);
  if (prefix.find("SAME")==std::string::npos) prefix=std::string("SAME")+prefix;

  obj->Draw(prefix.c_str());



}
// ----------------------------------------------------------------------
// ----------------------------------------------------------------------



// ----------------------------------------------------------------------
void UpdatePad (TPad *ppad)
  // This method updates the provided TPad or TCanvas.
{
  if (ppad==nullptr) {
    gPad->RedrawAxis();
    gPad->Modified();
    gPad->Update();
  }
  else {
    ppad->RedrawAxis();
    ppad->Modified();
    ppad->Update();
  }
}

// ----------------------------------------------------------------------
TH1 *GetcmsCanvasHist (TPad *pcanv)
  // This method returns the Frame object used to define the cmsCanvas (but it can be used also for any TPad).
{
  return (TH1*) pcanv->GetListOfPrimitives()->FindObject("hframe");
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
// ----------------------------------------------------------------------




}  // Namespace cmsstyle

// //////////////////////////////////////////////////////////////////////
