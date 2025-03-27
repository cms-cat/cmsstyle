///@file
///
/// This file contains a C++-ROOT macro to perform tests of the basic plots
/// using the CMSStyle using the C++-based implementation for 2-D Histograms.
///
/// To run it just execute:
///         $ source scripts/setup_cmstyle   # From the CMSStyle-package top directory
///         $ root -q test_cms2DHisto.C
///
/// It will produce the file test_cms2DHisto_C.png file.
///
/// <PRE>
/// Written by O. Gonzalez (2025_02_21)
/// </PRE>

#include "cmsstyle.C"

#include <cmath>

void test_cms2DHisto ()
{
  cmsstyle::setCMSStyle();  // Setting the style

  TH2F h1("test1","test1",60,0.0,60.0,60,0.0,60.0);
  TH2F h2("test2","test2",60,0.0,60.0,60,0.0,60.0);

  for (Int_t i=0;i<61;++i) {
    for (Int_t j=0;j<61;++j) {
      h1.SetBinContent(i,j,10*exp((30-i)*(30-i)/-25.0)*exp((20-j)*(20-j)/-20.0));
      h2.SetBinContent(i,j,15*exp((45-i)*(45-i)/-45.0)*exp((40-j)*(40-j)/-50.0));
    }
  }

  // We only plot the sum for now!
  h1.Add(&h2);

  // Plotting the histogram!
  cmsstyle::SetEnergy(13.6);
  cmsstyle::SetLumi(45.00,"fb","Run 3",1);

  TCanvas *c = cmsstyle::cmsCanvas("Testing",0.0,60.0,0.0,60.0,
                                   "X var [test]","Y var"
                                   ,kTRUE    // Square?
                                   ,11       // position of the Logo: 0 is out-of-frame, default is 11.
                                   ,0        // EXtra space, default is 0
                                   ,kTRUE    // with_z_axis, dafault is kFALSE
                                   );
  //cmsstyle::SetCMSPalette();
  cmsstyle::SetAlternative2DColor(&h1);

  cmsstyle::cmsObjectDraw(&h1,"COLZ");
  //cmsstyle::cmsObjectDraw(&h1,"LEGO2");  // For this, TCanvas should be defined differently (and Axis should not be redrawn as usual.

  // Saving the result!
  cmsstyle::SaveCanvas(c,"test_cms2DHisto_C.png");
}

// //////////////////////////////////////////////////////////////////////
