///@file
///

/// This file contains a C++-ROOT macro to perform tests of the basic plots
/// using the CMSStyle using the C++-based implementation.
///

/// To run it just execute:
///         $ source scripts/setup_cmstyle   # From the CMSStyle-package top directory
///         $ root -q test_cmsCanvas.C
///
/// It will produce the file test_cmsCanvas.png file.
///
/// <PRE>
/// Written by O. Gonzalez (2024_11_26)
/// </PRE>

#include "cmsstyle.C"

void test_cmsCanvas ()
{
  // Producing the histograms to plot

  TH1F h1("test","test",60,0.0,10.0);
  TH1F h2("test","test",60,0.0,10.0);

  for (int i=1;i<=60;++i) {
    h1.SetBinContent(i,10*exp(-i/5.0));
    h2.SetBinContent(i,8*exp(-i/15.0));
  }
  h1.Add(&h2);

  // Plotting the histogram!

  cmsstyle::setCMSStyle();  // Setting the style

  TCanvas *c = cmsstyle::cmsCanvas("Testing",0.0,10.0,0.08,cmsstyle::cmsReturnMaxY({&h1,&h2}),
                                   "X var [test]","Y var");

  gPad->SetLogy();

  cmsstyle::cmsObjectDraw(&h1,"",{ {"LineColor", cmsstyle::p6::kGray},
                                   {"FillColor", cmsstyle::p6::kGray},
                                   {"FillStyle", 1001},
    } );

  cmsstyle::cmsObjectDraw(&h2,"",{ {"LineColor", cmsstyle::p6::kGrape},
                                   {"FillColor", cmsstyle::p6::kGrape},
                                   {"FillStyle", 1001},
    } );



  cmsstyle::UpdatePad(c);

  c->SaveAs("test_cmsCanvas.png");
}

// //////////////////////////////////////////////////////////////////////
