///@file
///

/// This file contains a C++-ROOT macro to perform tests of the THStack plots
/// using the CMSStyle using the C++-based implementation.
///

/// To run it just execute:
///         $ source scripts/setup_cmstyle   # From the CMSStyle-package top directory
///         $ root -q test_THStack.C
///
/// It will produce the file test_cmsCanvas.png file.
///
/// <PRE>
/// Written by O. Gonzalez (2025_01_15)
/// </PRE>

#include "cmsstyle.C"

#include <TF1.h>

void test_THStack ()
{
  cmsstyle::setCMSStyle();  // Setting the style

  // Producing the histograms to plot

  TH1F *h1 = new TH1F("test","test",60,0.0,10.0);
  TH1F *h2 = new TH1F("test","test",60,0.0,10.0);

  for (unsigned int i=0;i<61;++i) {
    h1->SetBinContent(i,10*exp(-float(i)/5.0));
    h2->SetBinContent(i,8*exp(-float(i)/15.0));
  }

  auto tg = new TF1("fb","gaus(0)",0.0,10.0);
  tg->SetParameter(0,5.0);
  tg->SetParameter(1,3.0);
  tg->SetParameter(2,1.0);
  tg->SetNpx(60);
  TH1 *hg = (TH1*) tg->CreateHistogram()->Clone();
  hg->SetLineColor(kBlack);  // By default from functions is kRed(?)

  // Building the "data" histogram:

  TH1 *hdata = (TH1*) h1->Clone("data");
  for (unsigned int i=0;i<61;++i) {
    auto yval = h1->GetBinContent(i) + h2->GetBinContent(i) + hg->GetBinContent(i);

    hdata->SetBinError(i,0.12*yval);
    hdata->SetBinContent(i, yval*(1+0.1*cos(6.28*i/20.)));
  }

  // Now we have the histograms to plot, so setting up the plot!

  cmsstyle::TCmsCanvas *c;

  TLegend *leg;

  // Building the THStack

  THStack *hs;
  if (true) {
    hs = cmsstyle::buildTHStack(std::vector<TH1*>({h1,h2,hg}),
                                         {cmsstyle::p10::kBrown,cmsstyle::p10::kBlue,cmsstyle::p10::kOrange},
                                         "STACK");


    c = cmsstyle::cmsCanvas("Testing",0.0,10.0,0.08,1.3*cmsstyle::cmsReturnMaxY({hdata,hs}),
                            "X var [test]","Y var");

    leg = cmsstyle::cmsLeg(0.55,0.65,0.9,0.9);

    cmsstyle::addToLegend(leg,{ {hdata,{"Data","p"}},
                                {hg,{"Sample G","f"}},
                                {h2,{"Sample 2","f"}},
                                {h1,{"Sample 1","f"}} });

    cmsstyle::cmsObjectDraw(hs,"");
  }
  else {  // Shorter version! (but note the canvas dows not use the stack for the canvas height)
    c = cmsstyle::cmsCanvas("Testing",0.0,10.0,0.08,1.3*cmsstyle::cmsReturnMaxY({hdata}),
                            "X var [test]","Y var");

    leg = cmsstyle::cmsLeg(0.55,0.65,0.9,0.9);

    cmsstyle::addToLegend(leg,{ {hdata,{"Data","p"}} });

    hs = cmsstyle::buildAndDrawTHStack(//std::vector<std::pair<TH1*,std::pair<const std::string,const std::string>>>(
                                       { {h1,{"Sample 1","f"}},
                                         {h2,{"Sample 2","f"}},
                                         {hg,{"Sample G","f"}} }
                                                                                                      //)
                                       ,leg,true,{cmsstyle::p10::kBrown,cmsstyle::p10::kBlue,cmsstyle::p10::kOrange},
                                       "STACK");
  }

  cmsstyle::cmsObjectDraw(hdata,"E",{ {"MarkerStyle",kFullCircle} });
  leg->Draw();

  // Saving the result!
  cmsstyle::UpdatePad(c);

  c->SaveAs("test_THStack_C.png");
  delete hs;
}

// //////////////////////////////////////////////////////////////////////
