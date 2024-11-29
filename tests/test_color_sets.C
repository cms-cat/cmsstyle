///@file
///
/// This file contains an example to show how is the aspect of the color sets
/// that are defined in the style.
///
/// To run it we need:
///        $ source scripts/setup_cmstyle   # From the CMSStyle-package top directory
///        $ root -q tests/test_color_sets.C   # Can be run from any location (or from inside ROOT directly!).
///
/// It will produce the file test_color_sets.png file.
///
/// <PRE>
/// Written by O. Gonzalez (2024_11_19)
/// </PRE>

#include "colorsets.H"

void test_color_sets (void) {

  // Vectors of pair values to access the

  std::vector<std::pair<std::string,const int *>> colorset_p6({{"p6::kBlue",&cmsstyle::p6::kBlue},
                                                               {"p6::kYellow",&cmsstyle::p6::kYellow},
                                                               {"p6::kRed",&cmsstyle::p6::kRed},
                                                               {"p6::kGrape",&cmsstyle::p6::kGrape},
                                                               {"p6::kGray",&cmsstyle::p6::kGray},
                                                               {"p6::kViolet",&cmsstyle::p6::kViolet}});

  std::vector<std::pair<std::string,const int *>> colorset_p8({{"p8::kBlue",&cmsstyle::p8::kBlue},
                                                               {"p8::kOrange",&cmsstyle::p8::kOrange},
                                                               {"p8::kRed",&cmsstyle::p8::kRed},
                                                               {"p8::kPink",&cmsstyle::p8::kPink},
                                                               {"p8::kGreen",&cmsstyle::p8::kGreen},
                                                               {"p8::kCyan",&cmsstyle::p8::kCyan},
                                                               {"p8::kAzure",&cmsstyle::p8::kAzure},
                                                               {"p8::kGray",&cmsstyle::p8::kGray}});

  std::vector<std::pair<std::string,const int *>> colorset_p10({{"p10::kBlue",&cmsstyle::p10::kBlue},
                                                                {"p10::kYellow",&cmsstyle::p10::kYellow},
                                                                {"p10::kRed",&cmsstyle::p10::kRed},
                                                                {"p10::kGray",&cmsstyle::p10::kGray},
                                                                {"p10::kViolet",&cmsstyle::p10::kViolet},
                                                                {"p10::kBrown",&cmsstyle::p10::kBrown},
                                                                {"p10::kOrange",&cmsstyle::p10::kOrange},
                                                                {"p10::kGreen",&cmsstyle::p10::kGreen},
                                                                {"p10::kAsh",&cmsstyle::p10::kAsh},
                                                                {"p10::kCyan",&cmsstyle::p10::kCyan}});



  // Create the TCanvas
  auto *c = new TCanvas("colors","Color sets in CMSStyle",800,400);

  unsigned int jdx=-1;
  for (auto xset : {&colorset_p10,&colorset_p8,&colorset_p6}) {
    ++jdx;

    unsigned int idx=-1;
    for (auto xcol : *xset) {
      ++idx;
      auto *tt = new TPaveLabel(0.02+idx*0.097,0.07+jdx*0.2,0.01+0.097*(1+idx),0.12+jdx*0.2,xcol.first.c_str());
      tt->SetTextColor(kWhite);

      tt->SetBorderSize(1);
      tt->SetLineColor(*xcol.second);
      tt->SetFillColor(*xcol.second);

      tt->Draw();

      tt = new TPaveLabel(0.02+idx*0.097,0.15+jdx*0.2,0.01+0.097*(idx+1),0.2+jdx*0.2,xcol.first.c_str());
      tt->SetTextColor(*xcol.second);

      tt->SetBorderSize(1);
      tt->SetLineColor(kWhite);
      tt->SetFillColor(kWhite);

      tt->Draw();
    }
  }

  // Also plots for the limit plots:

  auto *tt = new TPaveLabel(0,0.7,0.25,0.8,"Stats/Limit Bands:");

  tt->SetBorderSize(1);
  tt->SetLineColor(kWhite);
  tt->SetFillColor(kWhite);

  tt->Draw();

  auto *tb = new TBox(0.3,0.75,0.6,0.95);
  tb->SetLineColor(cmsstyle::kLimit95);
  tb->SetFillColor(cmsstyle::kLimit95);
  tb->Draw();

  tb = new TBox(0.3,0.8,0.6,0.9);
  tb->SetLineColor(cmsstyle::kLimit68);
  tb->SetFillColor(cmsstyle::kLimit68);
  tb->Draw();

  auto *tl = new TLine(0.3,0.85,0.6,0.85);
  tl->Draw();

  tt = new TPaveLabel(0.35,0.63,0.55,0.73,"Usual/Default");

  tt->SetBorderSize(1);
  tt->SetLineColor(kWhite);
  tt->SetFillColor(kWhite);

  tt->Draw();


  tb = new TBox(0.65,0.75,0.95,0.95);
  tb->SetLineColor(cmsstyle::kLimit95cms);
  tb->SetFillColor(cmsstyle::kLimit95cms);
  tb->Draw();

  tb = new TBox(0.65,0.8,0.95,0.9);
  tb->SetLineColor(cmsstyle::kLimit68cms);
  tb->SetFillColor(cmsstyle::kLimit68cms);
  tb->Draw();

  tl = new TLine(0.65,0.85,0.95,0.85);
  tl->Draw();

  tt = new TPaveLabel(0.7,0.63,0.9,0.73,"CMS-logo colors");

  tt->SetBorderSize(1);
  tt->SetLineColor(kWhite);
  tt->SetFillColor(kWhite);

  tt->Draw();

  c->SaveAs("test_color_sets.png");

  std::cout<<"Finished: produced file test_color_sets.png"<<std::endl;
}

// //////////////////////////////////////////////////////////////////////
