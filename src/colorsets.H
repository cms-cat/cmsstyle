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

#include <TColor.h>

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
  const int p6::kViolet = kP6Violet;  // It should be fine!
#else
  const int p6::kBlue = TColor::GetColor("#5790fc");
  const int p6::kYellow = TColor::GetColor("#f89c20");
  const int p6::kRed = TColor::GetColor("#e42536");
  const int p6::kGrape = TColor::GetColor("#964a8b");
  const int p6::kGray = TColor::GetColor("#9c9ca1");
  const int p6::kViolet = TColor::GetColor("#7a21dd");
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
  const int p10::kCyan = kP10Cyan;
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

/// ///////////////////
/// Some tools to handle the sets or use them efficiently
/// ///////////////////

/// This method returns the object (EColor) associated to a given color in the
/// previous sets from a given string to identify it.
///
/// Arguments:
///    color: Name of the color given as a string, e.g. 'p8::kBlue' or 'p8.kBlue'
///           Note: If the color name does not contain a "dot" or "semicolon it
///           is assumed to be a ROOT color by name!
///
/// Returns:
///    EColor/Int_t: color associated to the requested color name.
Int_t getPettroffColor (const std::string &color) {
  size_t ic = color.find("::");
  size_t ic2=-1;
  if (ic!=std::string::npos) {
    ic2=ic+2;
  }
  else {
    ic = color.find(".");
    ic2=ic+1;
  }

  if (ic2>0) {  // A Pettroff color in the package
    std::string v = color.substr(ic2);
    std::string p = color.substr(0,ic);

    if (p=="p6") {
      if (v=="kBlue") {return p6::kBlue;} else if (v=="kYellow") {return p6::kYellow;} else if (v=="kRed") {return p6::kRed;}
      else if (v=="kGrape") {return p6::kGrape;} else if (v=="kGray") {return p6::kGray;} else if (v=="kViolet") {return p6::kViolet;}
    }
    else if (p=="p8") {
      if (v=="kBlue") {return p8::kBlue;} else if (v=="kOrange") {return p8::kOrange;} else if (v=="kRed") {return p8::kRed;} else if (v=="kPink") {return p8::kPink;}
      else if (v=="kGreen") {return p8::kGreen;} else if (v=="kCyan") {return p8::kCyan;}  else if (v=="kAzure") {return p8::kAzure;} else if (v=="kGray") {return p8::kGray;}
    }
    else if (p=="p10") {
      if (v=="kBlue") {return p10::kBlue;} else if (v=="kYellow") {return p10::kYellow;} else if (v=="kRed") {return p10::kRed;} else if (v=="kGray") {return p10::kGray;}
      else if (v=="kViolet") {return p10::kViolet;} else if (v=="kBrown") {return p10::kBrown;} else if (v=="kOrange") {return p10::kOrange;}
      else if (v=="kGreen") {return p10::kGreen;} else if (v=="kAsh") {return p10::kAsh;} else if (v=="kCyan") {return p10::kCyan;}
    }
    return kBlack;  // In case the provided color was not identified!
  }
#if (ROOT_VERSION_MAJOR>6 || (ROOT_VERSION_MINOR>=32 && ROOT_VERSION_MAJOR==6)) // Not available before 6.32!
  return TColor::GetColorByName(color.c_str());
#else
  // For other versions we use a hardcoded way of using the basic colors.
  if (color=="kWhite") {return kWhite;}
  else if (color=="kGray") {return kGray;}
  else if (color=="kRed") {return kRed;}
  else if (color=="kGreen") {return kGreen;}
  else if (color=="kBlue") {return kBlue;}
  else if (color=="kYellow") {return kYellow;}
  else if (color=="kMagenta") {return kMagenta;}
  else if (color=="kCyan") {return kCyan;}
  else if (color=="kOrange") {return kOrange;}
  else if (color=="kSpring") {return kSpring;}
  else if (color=="kTeal") {return kTeal;}
  else if (color=="kAzure") {return kAzure;}
  else if (color=="kViolet") {return kViolet;}
  else if (color=="kPink") {return kPink;}

  return kBlack;
#endif
}

/// This method returns a list of colors for the given number of colors based on
/// the previous sets.
///
/// Arguments:
///    ncolors: number of colors that are needed for the list.
///             If larger than 10, the list would repeat itself as needed.
/// Returns:
///    A pointer to the build vector of integers containing the colors.
std::vector<Int_t> *getPettroffColorSet (unsigned int ncolors) {
  std::vector<Int_t> *dev;// = new std::vector<int>;

  if (ncolors<7) { // Using the collection of P6.
    dev = new std::vector<Int_t>({p6::kBlue,p6::kYellow,p6::kRed,p6::kGrape,p6::kGray,p6::kViolet});
  }
  else if (ncolors<9) { // Using the collection of P8.
    dev = new std::vector<Int_t>({p8::kBlue,p8::kOrange,p8::kRed,p8::kPink,p8::kGreen,p8::kCyan,p8::kAzure,p8::kGray});
  }
  else { // Using the collection of P10... repeating as needed
    dev = new std::vector<Int_t>({p10::kBlue,p10::kYellow,p10::kRed,p10::kGray,p10::kViolet,p10::kBrown,p10::kOrange,p10::kGreen,p10::kAsh,p10::kCyan});

    for (unsigned int i = 10; i<ncolors ; ++i) dev->push_back(dev->at(i%10));
  }

  return dev;
}

}  // Namespace cmsstyle
#endif
/////////////////////////////////////////////////////////////////////////
