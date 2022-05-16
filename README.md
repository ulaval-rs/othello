# Othello
Tools that allow you to link M-MACBETH files and GIS data (in the form of a GDB file).

## Usage
Othello has 2 tools.
The first, `Criteria`, allows to transform the values of a criterion thanks to a scale present in a macbeth file.
The second, `Aggregate`, allows you to aggregate all these values in order to calculate an optimization score.


## User guide
Please see the user guide for more detailed information:

# Download from releases
Downloading Othello from its releases is by far the easiest way to use it.
1. Download `othello.zip` from the last version here: https://github.com/ulaval-rs/othello/releases.
2. Unzip `othello.zip`
3. Execute `app.exe`


## Run Othello from source
This project only works on Windows machines due to the FileGDB support.
While it is possible to run it from source, it has a complex setup, and many part can break.
The FileGDB support needs many specific libraries versions (which why the wheels of some of them are in the repo (`.\dependecies`)).

Following these steps may work on your machine:
1. Clone the project 
```shell
git clone https://github.com/ulaval-rs/othello
cd othello
```
2. Setup an Python 3.9 environment (you may use other methods such as conda)
```shell
python3.9 -m venv .\env
```
3. Install the GDAL and Fiona dependencies
```shell
.\env\Scripts\python.exe -m pip install .\dependencies\GDAL-3.3.2-cp39-cp39-win_amd64.whl
.\env\Scripts\python.exe -m pip install .\dependencies\Fiona-1.8.20-cp39-cp39-win_amd64.whl
```
3. Then install the other dependencies
```shell
.\env\Scripts\python.exe -m pip install -r requirements.txt
```
4. Since this application can write GDB files, you must add the FileGDB driver 
   (You can do these steps manually rather than use the following command lines).
```shell
copy .\env\lib\site-packages\osgeo\gdalplugins\disabled\ogr_FileGDB.dll .\env\lib\site-packages\osgeo\gdalplugins\ogr_FileGDB.dll
curl https://raw.githubusercontent.com/Esri/file-geodatabase-api/master/FileGDB_API_1.5.1/FileGDB_API_1_5_1-VS2017.zip -o FileGDB_API.zip
mkdir filegdb_api
tar.exe -xf FileGDB_API.zip -C filegdb_api
copy .\filegdb_api\bin64\FileGDBAPI.dll .\env\lib\site-packages\osgeo\FileGDBAPI.dll
```
5. Finally, run this to start Othello
```shell
.\env\Scripts\python.exe app.py
```


# Contributors
Contributors are welcome!

Follow these steps to contribute to the project.

1. Fork the project from the GitHub web page.
2. Clone your fork and enter the project directory.
```shell
git clone https://github.com/<your-username>/othello
cd othello
```
3. Make a new branch where you will add your changes.
```shell
git checkout -b your-branch-name
```
4. Now make your changes to code.
5. Add, commit and push your changes.
```shell
git add .
git commit -m "message about the changes"
git push origin your-branch-name
```
6. Make a Pull request from GitHub (`https://github.com/<your-username>/othello/pulls`)
from your branch to the main branch.
