///@file
///
/// This code contains the definition of the colors to be used in CMSStyle,
/// as they can be loaded to use in other projects.
///
/// Contains the definitions of Petroff color schemes used in CMSStyle.
///
/// <PRE>
/// Written by O. Gonzalez (2024_11_12)
/// </PRE>
///

#ifndef CMSSTYLE_COLORSETS__H_
#define CMSSTYLE_COLORSETS__H_

#include "TColor.h"

namespace cmsstyle {

/// ///////////////////
/// This is the Petroff color scheme with 6 colors.
/// ///////////////////
struct p6 {
  static const int kBlue;    //= TColor::GetColor("#5790fc");
  static const int kYellow;  //= TColor::GetColor("#f89c20");
  static const int kRed;     //= TColor::GetColor("#e42536");
  static const int kGrape;   //= TColor::GetColor("#964a8b");
  static const int kGray;    //= TColor::GetColor("#9c9ca1");
  static const int kViolet;  //= TColor::GetColor("#7a21dd");
};

// Initialize! Depending on version as ROOT added
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,34,0)
  const int p6::kBlue = kP6Blue;
  const int p6::kYellow = kP6Yellow;
  const int p6::kRed = kP6Red;
  const int p6::kGrape = kP6Grape;
  const int p6::kGray = kP6Gray;
//SEE BELOW  const int p6::kViolet = kP6Violet;
#else
  const int p6::kBlue = TColor::GetColor("#5790fc");
  const int p6::kYellow = TColor::GetColor("#f89c20");
  const int p6::kRed = TColor::GetColor("#e42536");
  const int p6::kGrape = TColor::GetColor("#964a8b");
  const int p6::kGray = TColor::GetColor("#9c9ca1");
// SEE BELOW  const int p6::kViolet = TColor::GetColor("#7a21dd");
#endif

// kP6Violet is wrong in some versions...
#if ROOT_VERSION_CODE < ROOT_VERSION(6,35,0)
  const int p6::kViolet = TColor::GetColor("#7a21dd");
#else
  const int p6::kViolet = kP6Violet;
#endif

/// ///////////////////
/// This is the Petroff color scheme with 8 colors.
/// ///////////////////
struct p8 {
    static const int kBlue;   //= rt.TColor.GetColor("#1845fb")
    static const int kOrange; //= rt.TColor.GetColor("#ff5e02")
    static const int kRed;    //= rt.TColor.GetColor("#c91f16")
    static const int kPink;   //= rt.TColor.GetColor("#c849a9")
    static const int kGreen;  //= rt.TColor.GetColor("#adad7d")
    static const int kCyan;   //= rt.TColor.GetColor("#86c8dd")
    static const int kAzure;  //= rt.TColor.GetColor("#578dff")
    static const int kGray;   //= TColor::GetColor("#656364")
};

// Initialize! Depending on version as ROOT added
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,34,0)
  const int p8::kBlue = kP8Blue;
  const int p8::kOrange = kP8Orange;
  const int p8::kRed = kP8Red;
  const int p8::kPink = kP8Pink;
  const int p8::kGreen = kP8Green;
  const int p8::kCyan = kP8Cyan;
  const int p8::kAzure = kP8Azure;
  const int p8::kGray = kP8Gray;
#else
  const int p8::kBlue = TColor::GetColor("#1845fb");
  const int p8::kOrange = TColor::GetColor("#ff5e02");
  const int p8::kRed = TColor::GetColor("#c91f16");
  const int p8::kPink = TColor::GetColor("#c849a9");
  const int p8::kGreen = TColor::GetColor("#adad7d");
  const int p8::kCyan = TColor::GetColor("#86c8dd");
  const int p8::kAzure = TColor::GetColor("#578dff");
  const int p8::kGray = TColor::GetColor("#656364");
#endif

/// ///////////////////
/// This is the Petroff color scheme with 10 colors.
/// ///////////////////
struct p10 {
     static const int kBlue;     //= TColor::GetColor("#3f90da")
     static const int kYellow;   //= TColor::GetColor("#ffa90e")
     static const int kRed;      //= TColor::GetColor("#bd1f01")
     static const int kGray;     //= TColor::GetColor("#94a4a2")
     static const int kViolet;   //= TColor::GetColor("#832db6")
     static const int kBrown;    //= TColor::GetColor("#a96b59")
     static const int kOrange;   //= TColor::GetColor("#e76300")
     static const int kGreen;    //= TColor::GetColor("#b9ac70")
     static const int kAsh;      //= TColor::GetColor("#717581")
     static const int kCyan;     //= TColor::GetColor("#92dadd")
};

// Initialize! Depending on version as ROOT added
#if ROOT_VERSION_CODE >= ROOT_VERSION(6,34,0)
  const int p10::kBlue = kP10Blue;
  const int p10::kYellow = kP10Yellow;
  const int p10::kRed = kP10Red;
  const int p10::kGray = kP10Gray;
  const int p10::kViolet = kP10Violet;
  const int p10::kBrown = kP10Brown;
  const int p10::kOrange = kP10Orange;
  const int p10::kGreen = kP10Green;
  const int p10::kAsh = kP10Ash;
  const int p10::kCyan = KP10Cyan;
#else
  const int p10::kBlue = TColor::GetColor("#3f90da");
  const int p10::kYellow = TColor::GetColor("#ffa90e");
  const int p10::kRed = TColor::GetColor("#bd1f01");
  const int p10::kGray = TColor::GetColor("#94a4a2");
  const int p10::kViolet = TColor::GetColor("#832db6");
  const int p10::kBrown = TColor::GetColor("#a96b59");
  const int p10::kOrange = TColor::GetColor("#e76300");
  const int p10::kGreen = TColor::GetColor("#b9ac70");
  const int p10::kAsh = TColor::GetColor("#717581");
  const int p10::kCyan = TColor::GetColor("#92dadd");
#endif

/// ///////////////////
/// Pair-sets of colors for the limit plots ("Brazilian flag plots")
/// From https://cms-analysis.docs.cern.ch/guidelines/plotting/colors/#brazilian-flag-limit-plots
/// ///////////////////
const int kLimit68 = TColor::GetColor("#607641");   // Internal band, default set
const int kLimit95 = TColor::GetColor("#F5BB54");   // External band, default set

const int kLimit68cms = TColor::GetColor("#85D1FBff");  // Internal band, CMS-logo set
const int kLimit95cms = TColor::GetColor("#FFDF7Fff");  // External band, CMS-logo set

}  // Namespace cmsstyle
#endif
///----------------------------------------------------------------------
