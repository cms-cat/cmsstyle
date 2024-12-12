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

## Installation inside the CMSSW

If you use a CMSSW that supports the _scram-venv_ you may use that to achieve
the installation of the python package with pip already locally, as described
in [this page](http://cms-sw.github.io/venv.html) using the following instructions:
```scram-venv
cmsenv

pip install cmstyle
```

It should be remarked that after installation of the _venv_ (done by
_scram-venv_) that step is no longer needed, but the working directory should
be used always in the virtual enviroment (that should be already setup when
doing the commonly required _cmsenv_ command.

Remark that if you have a local installacion of cmsstyle, it may collide with
the virtual environment, so you may want to do
```export PYTHONNOUSERSITE=True
```
to prevent the conflicts.

In the case of the C++ code, it is possible to add the code as source code but
downloading the packages as mentioned above. Keep in mind that the repository
does not follows the required structure for CMSSW packages, so you may
encounter difficulties to integrate. _Do not hesitate to contact us for the use
case_.

## Documentation

Documentation for the Python implementation is available at [cmsstyle.readthedocs.io](https://cmsstyle.readthedocs.io/). C++ implementation is analogous.
