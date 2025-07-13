/// @file
/// <PRE>
/// This file contains the method associated to the CMSStyle package. It is the one to be used
/// when compiling the version using any of the following command:
///
///       root[] .L cmsstyle.C++   (or equivalently with CompileMacro() or LoadMacro())
///
/// or simply from the command line (example to just compile)
///       echo '{gROOT->LoadMacro("cmsstyle.C++");}' > /tmp/temp$$.C ; root -q /tmp/temp$$.C
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
#include <TGraph.h>
#include <TLegend.h>
#include <TLatex.h>

#include <iostream>
#include <sstream>
#include <algorithm>
#include <cstdlib>
#include <iomanip>

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
  cmsStyle->SetTitleXOffset(1.1);
  cmsStyle->SetTitleYOffset(1.35);

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
  cmsStyle->SetHatchesLineWidth(2);
  cmsStyle->SetHatchesSpacing(1.3);

  // Some additional parameters we need to set as "style"

#if (ROOT_VERSION_MAJOR>6 || (ROOT_VERSION_MINOR>=32 && ROOT_VERSION_MAJOR==6)) // Not available before 6.32!
    TColor::DefinedColors(1);
#endif

  // Using the Style.
  cmsStyle->cd();
}

// ----------------------------------------------------------------------
void ResetCmsDescriptors (void)
  // This method allows to reset all the values for the CMS-related dataset                                                                      // descriptors to the default.
{
  cms_lumi = "Run 2, 138 fb^{#minus1}";
  cms_energy = "13 TeV";

  cmsText = "CMS";
  extraText = "Preliminary";

  additionalInfo.clear();
}

// ----------------------------------------------------------------------
void SetEnergy (Double_t energy, const std::string &unit)
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
void SetLumi (Double_t lumi, const std::string &unit, const std::string &run, int round_lumi)
  // This method sets the CMS-luminosity related information for the plot.
{
  cms_lumi = "";

  if (run.length()>0)  // There is an indication about the run period
    cms_lumi += run;

  // The lumi value is the most complicated thing

  if (lumi>=0) {
    if (cms_lumi.length()>0) cms_lumi += ", ";

    std::stringstream stream;
    if (round_lumi>=0 && round_lumi<3) stream << std::fixed << std::setprecision(round_lumi);
    stream << lumi;

    cms_lumi += stream.str();

    cms_lumi += std::string(" ") + unit + std::string("^{#minus1}");
  }
}

// ----------------------------------------------------------------------
void SetCmsText (const std::string &text, const Font_t &font, Double_t size)
  // This method allows to set the CMS text. as needed.
{
  cmsText=text;

  if (font!=0) cmsTextFont = font;
  if (size!=0) cmsTextSize = size;
}

// ----------------------------------------------------------------------
void SetCmsLogoFilename (const std::string &filename)
  // This allows to set the location of the file with the CMS Logo in case we
  // want to use that instead of the "CMS" text.
  // When not set (default), the text version is written.
{
  if (filename.length()==0) useCmsLogo ="";

  // We just check for it!
  else if (FILE *file = fopen(filename.c_str(),"r")) {
    useCmsLogo = filename;
    fclose(file);
  }

  else {  // We may look inside the CMSStyle directory if the variable is defined.
    char *x = std::getenv("CMSSTYLE_DIR");
    useCmsLogo ="";

    if (x!=nullptr) {
      useCmsLogo = std::string(x) + std::string("/") + filename;

      if (FILE *file = fopen(useCmsLogo.c_str(),"r")) {
        fclose(file);
      }
      else useCmsLogo ="";
    }

    if (useCmsLogo.length()==0) {
      std::cerr<<"ERROR: Indicated file for CMS Logo: "<<filename<<" could not be found!"<<std::endl;
    }
  }

}

// ----------------------------------------------------------------------
void SetExtraText (const std::string &text, const Font_t &font)
  // This allows to set the extra text. If set to an empty string, nothing
  // extra is written.
{
  extraText = text;

  if (extraText=="p") extraText="Preliminary";
  else if (extraText=="s") extraText="Simulation";
  else if (extraText=="su") extraText="Supplementary";
  else if (extraText=="wip") extraText="Work in progress";
  else if (extraText=="pw") extraText="Private work (CMS data)";

  // Now, if the extraText does contain the word "Private", the CMS logo is not DRAWN/WRITTEN

  if (extraText.find("Private")!=std::string::npos) {
    cmsText="";
    useCmsLogo="";
  }

  // For the font:
  if (font!=0) extraTextFont = font;
}

// ----------------------------------------------------------------------


// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
Double_t cmsReturnMaxY (const std::vector<TObject *> objs)
  // Returns the maximum value associated to the objects that are going to be
  // plotted.
{
  Double_t maxval=0;

  for (auto xobj : objs) {
    if (xobj->InheritsFrom(TH1::Class())) {   // An Histogram
      Double_t value = ((TH1*) xobj)->GetBinContent(((TH1*) xobj)->GetMaximumBin());
      value += ((TH1*) xobj)->GetBinError(((TH1*) xobj)->GetMaximumBin());

      if (maxval<value) maxval=value;
    }
    else if (xobj->InheritsFrom(THStack::Class())) {  // A THStack!
      Double_t value = ((THStack*) xobj)->GetMaximum();

      if (maxval<value) maxval=value;
    }
    else if (xobj->InheritsFrom(TGraph::Class())) {
      // TGraph are special as GetMaximum exists but it is a bug value.
      Int_t i = ((TGraph *) xobj)->GetN();
      Double_t *y = ((TGraph *) xobj)->GetY();
      Double_t *ey = ((TGraph *) xobj)->GetEY();

      while (i>0) {
        i -= 1;

        Double_t ivalue = y[i];
        ivalue += std::max(ey[i],((TGraph *) xobj)->GetErrorYhigh(i));

        if (maxval<ivalue) maxval=ivalue;
      }
    }

    else {
      std::cerr<<"ERROR: Trying to get a maximum or an unsupported type on cmsstyle::cmsReturnMaxY"<<std::endl;
    }
  }

  return maxval;
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------
TCmsCanvas *cmsCanvas (const char *canvName,
                       Double_t x_min,
                       Double_t x_max,
                       Double_t y_min,
                       Double_t y_max,
                       const char *nameXaxis,
                       const char *nameYaxis,
                       Bool_t square,
                       Int_t iPos,
                       Double_t extraSpace,
                       Bool_t with_z_axis,
                       Double_t scaleLumi,
                       Double_t yTitOffset)
  // This method defines and returns the TCmsCanvas (a wrapper for TCanvas) for
  // a normal/basic plot.
{
  // Set CMS style if not set already
  if (cmsStyle==nullptr) setCMSStyle();

  // Set canvas dimensions and margins
  Int_t H = 600;

  Double_t W = 800;
  if (square) W = 600;

  Double_t T = 0.07 * H;
  Double_t B = 0.125 * H;   // Changing this to allow more space in X-title (i.e. subscripts)
  Double_t L = 0.145 * H;    // Changing this to leave more space
  Double_t R = 0.05 * H;  // Changing this to leave more space

  // The position of the y-axis title may also change a bit the plot:
  Double_t y_offset = 0.78;
  if (yTitOffset<-998) {
    y_offset = 0.78;
    if (square) y_offset = 1.2;  // Changed to fitting larger font
  }
  else y_offset = yTitOffset;

  if (y_offset<1.5) L += y_offset*50-60;     // Some adjustment
  else if (y_offset<1.8) L += (y_offset-1.4)*35+25;

  // Setting up the TCanvas
  TCmsCanvas *canv = new TCmsCanvas(canvName, canvName, 50, 50, W, H);
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

  h->GetYaxis()->SetTitleOffset(y_offset);
  h->GetXaxis()->SetTitleOffset(1.05);  // Changed to fitting larger font
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
void CMS_lumi (TPad *ppad, Int_t iPosX, Double_t scaleLumi)
  // This is the method to draw the "CMS" seal (logo and text) and put the
  // luminosity value.
{
  /// This is the key method about forcing the CMSStyle. The original python
  /// implementation was complicated and obscure, so rewritten here with a
  /// cleaner coding.

  Double_t relPosX = 0.035;
  Double_t relPosY = 0.035;
  Double_t relExtraDY = 1.2;

  Bool_t outOfFrame = (int(iPosX / 10) == 0);
  Int_t alignX_ = max(int(iPosX / 10), 1);
  Int_t alignY_ = (iPosX==0)?1:3;
  Int_t align_ = 10 * alignX_ + alignY_;

  Double_t H = ppad->GetWh() * ppad->GetHNDC();
  Double_t W = ppad->GetWw() * ppad->GetWNDC();
  Double_t l = ppad->GetLeftMargin();
  Double_t t = ppad->GetTopMargin();
  Double_t r = ppad->GetRightMargin();
  Double_t b = ppad->GetBottomMargin();
  Double_t outOfFrame_posY = 1 - t + lumiTextOffset * t;

  ppad->cd();

  std::string lumiText(cms_lumi);
  if (cms_energy != "") lumiText += " (" + cms_energy + ")";

  //OLD if (scaleLumi) lumiText = ScaleText(lumiText, scaleLumi);

  drawText(lumiText.c_str(),1-r,outOfFrame_posY,42,31,lumiTextSize * t * scaleLumi);

  // Now we go to the CMS message:

  Double_t posX_ = 0;
  if (iPosX % 10 <= 1) posX_ = l + relPosX * (1 - l - r);
  else if (iPosX % 10 == 2) posX_ = l + 0.5 * (1 - l - r);
  else if (iPosX % 10 == 3) posX_ = 1 - r - relPosX * (1 - l - r);

  Double_t posY_ = 1 - t - relPosY * (1 - t - b);

  if (outOfFrame) {  // CMS logo and extra text out of the frame
    if (useCmsLogo.length()>0)  {   // Using CMS Logo instead of the text label (uncommon!)
      std::cerr<<"WARNING: Usage of (graphical) CMS-logo outside the frame is not currently supported!"<<std::endl;
    }
//    else {
    if (cmsText.length()!=0) {
      drawText(cmsText.c_str(),l,outOfFrame_posY,cmsTextFont,11,cmsTextSize * t);
      // Checking position of the extraText after the CMS logo text.
      Double_t scale=1;
      if (W > H) scale = H/ Double_t(W);  // For a rectangle;
      l += 0.043 * (extraTextFont * t * cmsTextSize) * scale;
    }

    if (extraText.length()!=0) {  // Only if something to write
      drawText(extraText.c_str(),l,outOfFrame_posY,extraTextFont,align_,extraOverCmsTextSize * cmsTextSize * t);
    }
    if (additionalInfo.size()!=0) {  // We do not support this!
      std::cerr<<"WARNING: Additional Info for the CMS-info part outside the frame is not currently supported!"<<std::endl;
    }
//    }
  }
  else {  // In the frame!
    if (useCmsLogo.length()>0)  {   // Using CMS Logo instead of the text label
      posX_ = l + 0.045 * (1 - l - r) * W / H;
      posY_ = 1 - t - 0.045 * (1 - t - b);
      // This is only for TCanvas!
      addCmsLogo((TCmsCanvas*) ppad, posX_,posY_ - 0.15,posX_ + 0.15 * H / W,posY_);
    }
    else {
      if (cmsText.length()!=0) {
        drawText(cmsText.c_str(),posX_,posY_,cmsTextFont,align_,cmsTextSize * t);
        // Checking position of the extraText after the CMS logo text.
        posY_ -= relExtraDY * cmsTextSize * t;
      }
      if (extraText.length()!=0) {  // Only if something to write
        drawText(extraText.c_str(),posX_,posY_,extraTextFont,align_,extraOverCmsTextSize * cmsTextSize * t);
      }
      else posY_ += relExtraDY * cmsTextSize * t;  // Preparing for additional text!
    }

    for (UInt_t i=0; i<additionalInfo.size(); ++i) {
      drawText(additionalInfo[i].c_str(),posX_,posY_ - 0.004 - (relExtraDY * extraOverCmsTextSize * cmsTextSize * t / 2 + 0.02) * (i + 1),
               additionalInfoFont,align_,extraOverCmsTextSize * cmsTextSize * t);
    }
  }

  UpdatePad(ppad);  // To be sure, although cmsCanvas and similar also calls it!
}


// ----------------------------------------------------------------------
void setRootObjectProperties (TObject *obj,
                              std::map<std::string,Double_t> confs)
  // This is a (mostly internal) method to setup the parameters of the provided
  // object in a "serialized" way.
{
  for ( auto xcnf : confs ) {
    if (xcnf.first=="SetLineColor" || xcnf.first=="LineColor") dynamic_cast<TAttLine*>(obj)->SetLineColor(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetLineStyle" || xcnf.first=="LineStyle") dynamic_cast<TAttLine*>(obj)->SetLineStyle(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetLineWidth" || xcnf.first=="LineWidth") dynamic_cast<TAttLine*>(obj)->SetLineWidth(xcnf.second);

    else if (xcnf.first=="SetFillColor" || xcnf.first=="FillColor") dynamic_cast<TAttFill*>(obj)->SetFillColor(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetFillStyle" || xcnf.first=="FillStyle") dynamic_cast<TAttFill*>(obj)->SetFillStyle(Int_t(xcnf.second+0.5));

    else if (xcnf.first=="SetMarkerColor" || xcnf.first=="MarkerColor") dynamic_cast<TAttMarker*>(obj)->SetMarkerColor(Int_t(xcnf.second+0.5));
    else if (xcnf.first=="SetMarkerSize" || xcnf.first=="MarkerSize") dynamic_cast<TAttMarker*>(obj)->SetMarkerSize(xcnf.second);
    else if (xcnf.first=="SetMarkerStyle" || xcnf.first=="MarkerStyle") dynamic_cast<TAttMarker*>(obj)->SetMarkerStyle(Int_t(xcnf.second+0.5));
  }
}

// ----------------------------------------------------------------------
void copyRootObjectProperties (TObject *obj,
                               TObject *srcobj,
                               std::vector<std::string> proplist,
                               std::map<std::string,Double_t> confs)
  // This is an internal method to coordinate the parameters and configuration
  // of objects that should have the same.
{
  // Looping over the properties and copy them:
  for ( auto xcnf : proplist ) {
    if (xcnf=="LineColor") dynamic_cast<TAttLine*>(obj)->SetLineColor(dynamic_cast<TAttLine*>(srcobj)->GetLineColor());
    else if (xcnf=="LineStyle") dynamic_cast<TAttLine*>(obj)->SetLineStyle(dynamic_cast<TAttLine*>(srcobj)->GetLineStyle());
    else if (xcnf=="LineWidth") dynamic_cast<TAttLine*>(obj)->SetLineWidth(dynamic_cast<TAttLine*>(srcobj)->GetLineWidth());

    else if (xcnf=="FillColor") dynamic_cast<TAttFill*>(obj)->SetFillColor(dynamic_cast<TAttFill*>(srcobj)->GetFillColor());
    else if (xcnf=="FillStyle") dynamic_cast<TAttFill*>(obj)->SetFillStyle(dynamic_cast<TAttFill*>(srcobj)->GetFillStyle());

    else if (xcnf=="MarkerColor") dynamic_cast<TAttMarker*>(obj)->SetMarkerColor(dynamic_cast<TAttMarker*>(srcobj)->GetMarkerColor());
    else if (xcnf=="MarkerSize") dynamic_cast<TAttMarker*>(obj)->SetMarkerSize(dynamic_cast<TAttMarker*>(srcobj)->GetMarkerSize());
    else if (xcnf=="MarkerStyle") dynamic_cast<TAttMarker*>(obj)->SetMarkerStyle(dynamic_cast<TAttMarker*>(srcobj)->GetMarkerStyle());
  }

  // If we indicated some additional arguments, we use them to further
  // configure the object.
  if (confs.size()>0)
    setRootObjectProperties(obj,confs);
}

// ----------------------------------------------------------------------
void cmsObjectDraw(TObject *obj,
                   Option_t *option,
                   std::map<std::string,Double_t> confs)

{
  setRootObjectProperties(obj,confs);

  std::string prefix(option);
  if (prefix.find("SAME")==std::string::npos) prefix=std::string("SAME")+prefix;

  obj->Draw(prefix.c_str());



}

// ----------------------------------------------------------------------
TLegend *cmsLeg(Double_t x1, Double_t y1, Double_t x2, Double_t y2,
                Double_t textSize,
                Style_t textFont,
                Color_t textColor,
                Int_t columns)
  // This is the method to setup a legend according to the style!
{
  TLegend *leg = new TLegend(x1, y1, x2, y2, "", "brNDC");

  leg->SetTextSize(textSize);
  leg->SetTextFont(textFont);
  leg->SetTextColor(textColor);
  leg->SetBorderSize(0);
  leg->SetFillStyle(0);
  leg->SetFillColor(0);

  if (columns!=0) leg->SetNColumns(columns);
  leg->Draw();

  return leg;
}

// ----------------------------------------------------------------------
void addToLegend (TLegend *leg,
                  const std::vector<std::pair<const TObject *,std::pair<const std::string,const std::string>>> &objs)
  // This is an auxiliar method to help the addition of elements to the TLegend,
  // that could be more efficient in some cases.
{
  // We just loop over the objects to add to the legend in the given order.

  for (auto xobj : objs) {
    leg->AddEntry(xobj.first,xobj.second.first.c_str(),xobj.second.second.c_str());
  }
}

// ----------------------------------------------------------------------
void cmsGrid (bool gridon)
  // Enable or disable the grid mode in the CMSStyle.
{
  // CMSStyle should be set:
  if (cmsStyle==nullptr) {
    std::cerr<<"ERROR: You should set the CMS Style before calling cmsGrid"<<std::endl;
  }
  else {
    cmsStyle->SetPadGridX(gridon);
    cmsStyle->SetPadGridY(gridon);
  }
}

// ----------------------------------------------------------------------
void drawText(const char *text, Double_t posX, Double_t posY,
              Font_t font, Short_t align, Double_t size)
  // This is a method to write a Text in a simplified and straightforward                                                                                                                        // (i.e. user-friendly) way.
{
  TLatex latex;
  latex.SetNDC();
  latex.SetTextAngle(0);
  latex.SetTextColor(kBlack);

  latex.SetTextFont(font);
  latex.SetTextAlign(align);
  latex.SetTextSize(size);

  latex.DrawLatex(posX, posY, text);
}

// ----------------------------------------------------------------------
void addCmsLogo (TCmsCanvas *canv,Double_t x0, Double_t y0, Double_t x1, Double_t y1, const char *logofile)
  // This is a method to draw the CMS logo (that should be set using the
  // corresponding method or on the fly) in a TPad set at the indicated location
  // of the currently used TPad.
{
  if (logofile!=nullptr) {
    SetCmsLogoFilename(logofile);   // Trying to load the file)
  }

  if (useCmsLogo.length()==0) {
    std::cerr<<"ERROR: Not possible to add the CMS Logo as the file is not properly defined (not found?)"<<std::endl;
    return;
  }

  canv->AddCmsLogo(x0,y0,x1,y1,useCmsLogo.c_str());
  UpdatePad();  // For gPad
}

// ----------------------------------------------------------------------
TPaveStats *changeStatsBox (TPad *pcanv,
                            Double_t x1pos,
                            Double_t y1pos,
                            Double_t x2pos,
                            Double_t y2pos,
                            const std::map<std::string,Double_t> &confs)
/// This method allows to modify the properties and similar of the Stats Box in
/// the plot.
{
  UpdatePad(pcanv);
  TPaveStats *stbox = (TPaveStats *) pcanv->GetPrimitive("stats");

  if (stbox==nullptr) {
    std::cerr<<"ERROR: Trying to change the StatsBox when it has not been enabled... activate it with SetOptStat (and use \"SAMES\" or equivalent)"<<std::endl;
    return nullptr;
  }

  changeStatsBox(stbox,x1pos,y1pos,x2pos,y2pos,confs);  // Calling the method for the TPaveStats!

  UpdatePad(pcanv);

  return stbox;
}

// ----------------------------------------------------------------------
void changeStatsBox (TPaveStats *pstats, Double_t x1pos, Double_t y1pos, Double_t x2pos, Double_t y2pos,
                     const std::map<std::string,Double_t> &confs)
  // This method allows to modify the properties and similar of the provided Stats Box.
{
  setRootObjectProperties(pstats,confs);

  // Changing the new positions (if not -999)

  if (x1pos>-998) pstats->SetX1NDC(x1pos);
  if (y1pos>-998) pstats->SetY1NDC(y1pos);
  if (x2pos>-998) pstats->SetX2NDC(x2pos);
  if (y2pos>-998) pstats->SetY2NDC(y2pos);
}

// ----------------------------------------------------------------------
TPaveStats *changeStatsBox (TPad *pcanv,
                            const std::string &ipos_x1,
                            Double_t xscale,
                            Double_t yscale,
                            const std::map<std::string,Double_t> &confs)
  // This method allows to modify the properties and similar of the Stats Box in
  // the plot. Similar to the one with the same name but we use ipos_x0 as a
  // predefined position identified by using a string.
{
  UpdatePad(pcanv);
  TPaveStats *stbox = (TPaveStats *) pcanv->GetPrimitive("stats");

  if (stbox==nullptr) {
    std::cerr<<"ERROR: Trying to change the StatsBox when it has not been enabled... activate it with SetOptStat (and use \"SAMES\" or equivalent)"<<std::endl;
    return nullptr;
  }

  // The idea is to use the predefined positions:

  std::string a = ipos_x1;
  std::transform(a.begin(),a.end(),a.begin(),::tolower);

  // The size may be modified depending on the text size. Note that the text
  // size is 0, it is adapted to the box size (I think)
  Double_t textsize = 6*(stbox->GetTextSize()-0.025);
  if (stbox->GetTextSize()==0) textsize = 0;

  Double_t xsize = (1-pcanv->GetRightMargin()-pcanv->GetLeftMargin())*xscale;  // Note these parameters looses their "x"-"y" nature.
  Double_t ysize = (1-pcanv->GetBottomMargin()-pcanv->GetTopMargin())*yscale;

  Double_t yfactor = 0.05+0.05*stbox->GetListOfLines()->GetEntries();

  Double_t x1=0;
  Double_t y1=0;
  Double_t x2=0;
  Double_t y2=0;

  // For "tr":
  if (a=="tr") {
    x1 = 1-pcanv->GetRightMargin()-xsize*0.33-textsize;
    y1 = 1-pcanv->GetTopMargin()-ysize*yfactor-textsize;
    x2 = 1-pcanv->GetRightMargin()-xsize*0.03;
    y2 = 1-pcanv->GetTopMargin()-ysize*0.03;
  }
  else if (a=="tl") {
    x1 = pcanv->GetLeftMargin()+xsize*0.03;
    y1 = 1-pcanv->GetTopMargin()-ysize*yfactor-textsize;
    x2 = pcanv->GetLeftMargin()+xsize*0.33+textsize;
    y2 = 1-pcanv->GetTopMargin()-ysize*0.03;
  }
  else if (a=="bl") {
    x1 = pcanv->GetLeftMargin()+xsize*0.03;
    y1 = pcanv->GetBottomMargin()+ysize*0.03;
    x2 = pcanv->GetLeftMargin()+xsize*0.33+textsize;
    y2 = pcanv->GetBottomMargin()+ysize*yfactor+textsize;
  }
  else if (a=="br") {
    x1 = 1-pcanv->GetRightMargin()-xsize*0.33-textsize;
    y1 = pcanv->GetBottomMargin()+ysize*0.03;
    x2 = 1-pcanv->GetRightMargin()-xsize*0.03;
    y2 = pcanv->GetBottomMargin()+ysize*yfactor+textsize;
  }
  else {
    std::cerr<<"ERROR: Invalid code provided to position the statistics box: "<<ipos_x1<<std::endl;
    return stbox;
  }

  changeStatsBox(stbox,x1,y1,x2,y2,confs);  // Using the main method for the action.

  UpdatePad(pcanv);
  return stbox;
}

// ----------------------------------------------------------------------
void SetCMSPalette (void)
  // Set the official CMS colour palette for 2D histograms directly.
{
  if (cmsStyle!=nullptr) {
    cmsStyle->SetPalette(EColorPalette::kViridis);
    //cmsStyle->SetPalette(EColorPalette::kCividis);
  }
  else std::cerr<<"ERROR: Not possible to set the CMS Palette if the CMS Style is not set!"<<std::endl;
}

// ----------------------------------------------------------------------
TPaletteAxis *GetPalette (TH1 *hist)
  // Get the colour palette object associated with a histogram.
{
  UpdatePad();  // Must update the pad to access the palette
  return (TPaletteAxis*) hist->GetListOfFunctions()->FindObject("palette");
}

// ----------------------------------------------------------------------
void CreateAlternativePalette(Double_t alpha)
  // Create an alternative color palette for 2D histograms.
{
  Double_t red_values[4] = {0.00, 0.00, 1.00, 0.70};
  Double_t green_values[4] = {0.30, 0.50, 0.70, 0.00};
  Double_t blue_values[4] = {0.50, 0.40, 0.20, 0.15};

  Double_t length_values[4] = {0.00, 0.15, 0.70, 1.00};

  Int_t num_colors = 200;
  Int_t color_table = TColor::CreateGradientColorTable(
                                                       4,  // Size of the arrays above!
                                                       length_values,
                                                       red_values,
                                                       green_values,
                                                       blue_values,
                                                       num_colors,
                                                       alpha
                                                       );

  // Once the palette has been built, we process it a color list:

  usingPalette2D.clear();

  for (int i=0;i<num_colors;++i) usingPalette2D.push_back(color_table+i);
}

// ----------------------------------------------------------------------
void SetAlternative2DColor (TH2 *hist, TStyle *style, Double_t alpha)
  // Set an alternative colour palette for a 2D histogram.
{
  // Creating the alternative palette
  if (usingPalette2D.size()==0) CreateAlternativePalette(alpha);

  if (style==nullptr) {   // By default we use the cmsStyle... or the current style:
    if (cmsStyle==nullptr) style=gStyle;
    else style = cmsStyle;
  }

  style->SetPalette(usingPalette2D.size(), (Int_t*) usingPalette2D.data());

  if (hist!=nullptr) hist->SetContour(usingPalette2D.size());
}

// ----------------------------------------------------------------------
void UpdatePalettePosition (TH2 *hist,
                            TPad *canv,
                            Double_t X1,
                            Double_t X2,
                            Double_t Y1,
                            Double_t Y2,
                            Bool_t isNDC)
  // Adjust the position of the color palette for a 2D histogram.
{
  TPaletteAxis *palette = GetPalette(hist);

  if (canv!=nullptr && isNDC) {  // Note it is ignored if we do not give NDC!

    // If we provide a TPad/Canvas we use the values for it, EXCEPT if explicit
    // values are provided!
    TH1 *hframe = GetCmsCanvasHist(canv);

    if (isnan(X1)) X1 = 1 - canv->GetRightMargin() * 0.95;
    if (isnan(X2)) X2 = 1 - canv->GetRightMargin() * 0.70;
    if (isnan(Y1)) Y1 = canv->GetBottomMargin();
    if (isnan(Y2)) Y2 = 1 - canv->GetTopMargin();
  }

  std::vector<void (TPave::*)(Double_t)> vars({&TPave::SetX1,&TPave::SetX2,&TPave::SetY1,&TPave::SetY2});
  if (isNDC) vars = {&TPave::SetX1NDC,&TPave::SetX2NDC,&TPave::SetY1NDC,&TPave::SetY2NDC};

  // Changing the coordinates!
  if (isnan(X1)) (palette->*vars[0])(X1);
  if (isnan(X2)) (palette->*vars[1])(X2);
  if (isnan(Y1)) (palette->*vars[2])(Y1);
  if (isnan(Y2)) (palette->*vars[3])(Y2);
}

// ----------------------------------------------------------------------
THStack *buildTHStack (const std::vector<TH1*> &histos,
                       const std::vector<int> &colors,
                       const std::string &stackopt,
                       const std::map<std::string,Double_t> &confs)
  // This method allows to build a THStack that is returned to the caller so it
  // may be used for later processing.
{
  // We create the THStack to be created... it may be an empty one if no
  // histogram is provided...

  std::string x(stackopt);
  if (x.size()==0) x="STACK";  // The default for using ""
  auto *hstack = new THStack("hstack",x.c_str());

  // If the provided color list is not useful, we get one from Pettroff's sets
  auto *colorset = &colors;
  UInt_t ncolors = colorset->size();
  if (ncolors==0 && histos.size()>0) {
    // Need to build a set of colors from Petroff's sets!
    ncolors = histos.size();
    colorset = getPettroffColorSet(ncolors);
  }

  // Looping over the histograms to generate the THStack

  unsigned int ihst = 0;
  for (auto xhst : histos) {

    //std::cout<<"Information: "<<xhst->GetFillStyle()<<" "<<xhst->GetFillColor()<<std::endl;

    // We may modify the histogram... indeed it should be given! When no
    // argument is given, we use FillColor by default for stack histograms (see default!)

    for ( auto xcnf : confs ) {
      if (xcnf.first=="SetLineColor" || xcnf.first=="LineColor") xhst->SetLineColor(colors[ihst]);    // NOTE: FOR THE COLOR WE USE THE VECTOR!
      else if (xcnf.first=="SetFillColor" || xcnf.first=="FillColor") xhst->SetFillColor(colors[ihst]);
      else if (xcnf.first=="SetMarkerColor" || xcnf.first=="MarkerColor") xhst->SetMarkerColor(colors[ihst]);

      else if (xcnf.first=="SetLineStyle" || xcnf.first=="LineStyle") xhst->SetLineStyle(Int_t(xcnf.second+0.5));
      else if (xcnf.first=="SetLineWidth" || xcnf.first=="LineWidth") xhst->SetLineWidth(xcnf.second);

      else if (xcnf.first=="SetFillStyle" || xcnf.first=="FillStyle") xhst->SetFillStyle(Int_t(xcnf.second+0.5));
      else if (xcnf.first=="SetMarkerSize" || xcnf.first=="MarkerSize") xhst->SetMarkerSize(xcnf.second);
      else if (xcnf.first=="SetMarkerStyle" || xcnf.first=="MarkerStyle") xhst->SetMarkerSize(xcnf.second);
    }

    // Adding it!
    hstack->Add(xhst);
    ++ihst;
  }

//  if (colorset!=&colors) delete colorset;  // It means it was created!

  return hstack;
}

// ----------------------------------------------------------------------
THStack *buildAndDrawTHStack (const std::vector<std::pair<TH1 *,std::pair<const std::string,const std::string>>> &objs,
                              TLegend *leg,
                              Bool_t reverseleg,
                              const std::vector<int> &colors,
                              const std::string &stackopt,
                              const std::map<std::string,Double_t> &confs)
  // This method allows to build and draw a THStack with a single command.
{
  // We get a vector with the histogram pointers!
  std::vector<TH1*> histos;
  histos.reserve(objs.size());

  for (auto xhst : objs) histos.push_back(xhst.first);

  THStack *hs = buildTHStack(histos,colors,stackopt,confs);

  // We add the histograms to the legend... perhaps looping in reverse order!
  if (reverseleg) {
    for (auto xobj = objs.rbegin(); xobj != objs.rend(); ++xobj) leg->AddEntry(xobj->first,xobj->second.first.c_str(),xobj->second.second.c_str());
  }
  else for (auto xobj : objs) leg->AddEntry(xobj.first,xobj.second.first.c_str(),xobj.second.second.c_str());

  cmsObjectDraw(hs,"");  // Also drawing it!

  return hs;
}

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
TH1 *GetCmsCanvasHist (TPad *pcanv)
  // This method returns the Frame object used to define the cmsCanvas (but it can be used also for any TPad).
{
  return (TH1*) pcanv->GetListOfPrimitives()->FindObject("hframe");
}

// ----------------------------------------------------------------------
void SaveCanvas (TPad *pcanv,const std::string &path,bool close)
  // This method allows to save the canvas with the proper update.
{
  UpdatePad();
  pcanv->SaveAs(path.c_str());

  if (close) pcanv->Close();
}

// ----------------------------------------------------------------------
// ----------------------------------------------------------------------




}  // Namespace cmsstyle

// //////////////////////////////////////////////////////////////////////
