# cmsstyle
Holding repo for CMS plotting style ROOT macros
guidelines available at https://cms-analysis.docs.cern.ch/guidelines/plotting/general/

Both python and C++ implementations available.

## Installation
Python:
```python
pip install cmsstyle
```
Once this is done, the ``import cmsstyle`` should work from any location.

C++:
```bash
git clone https://github.com/cms-cat/cmsstyle.git
cd cmsstyle
source scripts/setup_cmstyle
```

For the C++ to work from inside ROOT (and any location), it is recommended to
add something like the following to the rootlogon.C macro (or equivalent):
```if (gSystem->Getenv("CMSSTYLE_DIR")!=nullptr) {
  std::string var = string(gROOT->GetMacroPath())+":"+gSystem->Getenv("CMSSTYLE_DIR")+"/src";
  gROOT->SetMacroPath(var.c_str());
  std::cout<<"Adding the ${CMSSTYLE_DIR}/src to the macro path"<<std::endl;
}
```
In fact a similar configuration may be achieved by modifying the ``${HOME}/.rootrc`` instead.

## Documentation

Documentation for the Python implementation is available at [cmsstyle.readthedocs.io](https://cmsstyle.readthedocs.io/). C++ implementation is analogous.
