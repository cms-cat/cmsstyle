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
  cmsstyle::setCMSStyle();  // Setting the style

  // Producing the histograms to plot
  TH1F h1("test1","test1",60,0.0,10.0);
  TH1F h2("test2","test2",60,0.0,10.0);

  for (int i=1;i<=60;++i) {
    h1.SetBinContent(i,10*exp(-i/5.0));
    h2.SetBinContent(i,8*exp(-i/15.0));
  }
  h1.Add(&h2);

  auto *hdata = (TH1F*) h1.Clone("data");
  for (int i=1;i<=60;++i) {
    hdata->SetBinError(i,0.12*hdata->GetBinContent(i));
    hdata->SetBinContent(i, hdata->GetBinContent(i)*(1+0.1*cos(6.28*i/20.)));
  }

  // Plotting the histogram!

//  cmsstyle::SetCmsLogoFilename("CMS-BW-Label.png");  // e.g.
//  cmsstyle::SetExtraText("Private work (CMS data)");  // e.g.
//  cmsstyle::AppendAdditionalInfo("Doing our job");  // e.g.

  cmsstyle::SetEnergy(13.6);
  cmsstyle::SetLumi(45.00,"fb","Run 3",1);

  TCanvas *c = cmsstyle::cmsCanvas("Testing",0.0,10.0,0.08,3*cmsstyle::cmsReturnMaxY({&h1,&h2,hdata}),
                                   "X var [test]","Y var"
                                   ,kTRUE    // Square?
                                   //,0        // position of the Logo: 0 is out-of-frame, default is 11.
                                   );

  gPad->SetLogy();

  cmsstyle::cmsObjectDraw(&h1,"",{ {"LineColor", cmsstyle::p6::kGray},
                                   {"FillColor", cmsstyle::p6::kGray},
                                   {"FillStyle", 1001},
    } );

  cmsstyle::cmsObjectDraw(&h2,"",{ {"LineColor", cmsstyle::p6::kYellow},
                                   {"FillColor", cmsstyle::p6::kYellow},
                                   {"FillStyle", 1001},
    } );


  if (false) {  // To test the use of the changeStatsBox
    gStyle->SetOptStat("mr");
    cmsstyle::cmsObjectDraw(hdata,"SE",{ {"MarkerStyle", kFullCircle}
      } );
    //cmsstyle::changeStatsBox(c,"tl",1,1,{{"FillColor", cmsstyle::p6::kYellow}});
    //cmsstyle::setRootObjectProperties(cmsstyle::changeStatsBox(c,"tl"),{{"FillColor", cmsstyle::p6::kYellow}});
    cmsstyle::changeStatsBox(c,"tl");
  }
  else cmsstyle::cmsObjectDraw(hdata,"E",{ {"MarkerStyle", kFullCircle}
    } );


  // The legend!

  auto *plotlegend = cmsstyle::cmsLeg (0.55,0.65,0.9,0.9);

  plotlegend->AddEntry(hdata,"Data","p");
  plotlegend->AddEntry(&h1,"Sample Number 1","f");
  plotlegend->AddEntry(&h2,"Sample Number 2","f");
//  cmsstyle::cmsObjectDraw(plotlegend);

  // Saving the result!
  cmsstyle::SaveCanvas(c,"test_cmsCanvas_C.png");
}

// //////////////////////////////////////////////////////////////////////
