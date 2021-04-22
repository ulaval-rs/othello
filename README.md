# Othello
Tools that allow you to read and manipulate M-MACBETH files and transform GIS data accordingly.

__Project status : in development__

## Usage

### Evaluate criteria
<img src="https://raw.githubusercontent.com/ulaval-rs/othello/main/docs/diagrams/criteria_workflow.png" alt="criteria workflow" width="100%">


### Aggregate values
<img src="https://raw.githubusercontent.com/ulaval-rs/othello/main/docs/diagrams/aggregate_workflow.png" alt="aggregate workflow" width="100%">


## Installation (*only working on Windows*)
### Install from release (preferred)
1. Find the most recent release here : [https://github.com/ulaval-rs/othello/releases](https://github.com/ulaval-rs/othello/releases)
2. In the assets, download the othello zip file
3. Unzip the zip file at the path where you want the application
4. Run `app.exe` to start the application

### Install from source
Clone the repo:
```bash
git clone https://github.com/ulaval-rs/othello.git
cd othello
```

Make a virtual environment:
```bash
virtualenv venv
venv\Scripts\pip install -r requirements.txt
```

Re-install the `GDAL`, `Shapely`, `pyproj`, `Rtree` and `Fiona` from
https://www.lfd.uci.edu/~gohlke/pythonlibs with the following command (tested with python 3.8).
```bash
venv\Scripts\pip install --force-reinstall GDAL-3.2.2-cp38-cp38-win_amd64.whl
venv\Scripts\pip install --force-reinstall Shapely-1.7.1-cp38-cp38-win_amd64.whl
venv\Scripts\pip install --force-reinstall pyproj-3.0.1-cp38-cp38-win_amd64.whl
venv\Scripts\pip install --force-reinstall Rtree-0.9.7-cp38-cp38-win_amd64.whl
venv\Scripts\pip install --force-reinstall Fiona-1.8.18-cp38-cp38-win_amd64.whl
```

#### (OPTIONAL) Setup the ESRI geodatabase (.gdb) driver support
You need 2 files for this: `ogr_FileGDB.dll` and `FileGDBAPI.dll`.

gohlke's GDAL library comes with the `ogr_FileGDB` driver as a plugin.
`ogr_FileGDB.dll` is found at in `venv\Lib\site-packages\osgeo\gdalplugins\disable\ogr_FileGDB.dll`.
Simply copy and paste the file outside the _disable_ directory: `venv\Lib\site-packages\osgeo\gdalplugins\ogr_FileGDB.dll`.

The `FileGDBAPI.dll` is the proprietary SDK from ESRI.
It can be found on the following repository: https://github.com/Esri/file-geodatabase-api/blob/master/FileGDB_API_1.5.1/FileGDB_API_1_5_1-VS2017.zip .
Unpack the zip file and copy-paste the `bin64\FileGDPAPI.dll` to `venv\Lib\site-packages\osgeo\FileGDPAPI.dll`.
The ESRI geodatabase driver support should then be enabled.

#### Build Othello
Build the application to the `build` directory with the following command.
```bash
venv\Scripts\python3.8 setup.py build
```

