///@file
///
/// This code contains the declaration and definition of the class TCmsCanvas
/// that inherits from a normal TCanvas en ROOT but keep track of created
/// objects that are not visible to the user, for its proper deletion as the
/// TCanvas is destroyed.
///
/// <PRE>
/// Written by O. Gonzalez (2024_11_12)
/// </PRE>
///

#ifndef CMSSTYLE_TCMSCANVAS__H_
#define CMSSTYLE_TCMSCANVAS__H_

#include <TCanvas.h>
#include <TASImage.h>

#include <vector>

namespace cmsstyle {


/// This is the class that CMSStyle (in the C++ version) uses to handle the
/// TCanvases that are defined to be plotted, but one has to keep in mind that
/// externally

class TCmsCanvas : public TCanvas {

  // Internal variables (pointers to keep track)

  TASImage *CMS_logo;  ///< CMS Logo when used in the TCanvas.
  TPad *pad_logo;  ///< TPad containing the CMS logo, when used.

  // Internal methods

  /// Initialization of the internal variables...
  void Initialize (void) {
    CMS_logo=nullptr;
    pad_logo=nullptr;
  }

public:

  /// Normal constructor: It just creates the Canvas using the arguments and
  /// the corresponding constructor method ot eh TCanvas. It also initializes
  /// the values to keep track of when needed.
  ///
  /// Arguments:
  ///    name: Name of the created object
  ///    title: Title for the TCanvas
  ///    wtopx: X position of the top left corner of the canvas in pixels.
  ///    wtopy: Y position of the top left corner of the canvas in pixels
  ///    ww: the window size in pixels along X.
  ///    wh: the window size in pixels along Y.
  ///
  TCmsCanvas (const char *name,
              const char *title,
              Int_t wtopx,
              Int_t wtopy,
              Int_t ww,
              Int_t wh) : TCanvas(name,title,wtopx,wtopy,ww,wh) {
    Initialize();
  }

  /// Destructor of the class, as the most important object since it handles
  /// the deletion of objects defined
  ~TCmsCanvas () {
    if (CMS_logo!=nullptr) delete CMS_logo;
    if (pad_logo!=nullptr) delete pad_logo;
  }


  /// Method to draw the CMS Logo in the defined TCanvas in a TPad set at the indicated location
  /// of the currently used TPad.
  void AddCmsLogo (Float_t x0, Float_t y0, Float_t x1, Float_t y1, const char *logofile)
  {
    if (CMS_logo!=nullptr) delete CMS_logo;
    CMS_logo = new TASImage(logofile);

    auto oldpad = gPad;

    if (pad_logo!=nullptr) delete pad_logo;
    pad_logo = new TPad("logo", "logo", x0, y0, x1, y1);
    pad_logo->Draw();
    pad_logo->cd();
    CMS_logo->Draw("X");
    pad_logo->Modified();

    oldpad->cd();
  }




};

}  // Namespace cmsstyle
#endif
///----------------------------------------------------------------------
