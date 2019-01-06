# HelmChangeAnalyzer

This tool analyzes a Repository containing Helm charts. This too automaticially unpacks the tgz
files and runs a diff on it. Based in the different fields a Helm-chart contains, 
it counts the additions, deletions, and changes of these fields. This tool can be applied to a single 
file or the whole repository.

## Prerequisites

Make sure that you are in possesion of a repository with heml charts. Also make sure that you are running a Lunix machine 
otherwise some of the scrips might not work

## Run the Analysis

These instructions will explain how our results can be replicated. It will explain how you can
run the process and where the results are saved.

### How to Run

Run the `tgzComparison.py`

If the whole repository should be analysed run the script with these arguments:
```bash
python tgzComparison.py repo <all|content|count> <outputPath> <trackingdir> <tempStoragePath>
```

If the only one file should be analysed run the script with these arguments:
```bash
python tgzComparison.py file <all|content|count> <outputPath> <trackingdir> <tempStoragePath> <filename>
```
### The arguments

#### < all|content|count >
Defines what output should be generated:	
##### content
Generates a json for each file where for each key all the changes are listed.
Like thisa hostory for each key's entry can be seen.

##### count
Generates a json ove the whole repo/file that stores the numbers of additions, deletions and changes
together with the date and some additional information.

##### all
Does both of the above

#### < outputPath >
Path to where the output Json should be stored

#### < trackingdir >
Path to the directory in the repo where the charts are stored at.

#### < tempStoragePath >
Path to where the tgz should be temporarely be extracted to.

#### < filename >
Filename of the file to be analysed. should en with tgz. only the name not the whole path.
  
## Run the Plottong  

### How to Run

Run the `analyzer.py`

with the path to the `resultjson.json` and the path the where the output should be stored at as arguments

### Example

```bash
python analyzer.py ./resultjson.json ./output
```

  
## Content

```bash
├── Results
│   ├── VersionUpdateHistograms
│   │   ├── histogram_apiVersionUpdates.png
│   │   ├── histogram_appVersionUpdates.png
│   │   ├── histogram_versionUpdates.png
│   ├── datecurve
│   │   ├── datecurve_apiVersion.png
│   │   ├── datecurve_appVersion.png
│   │   ├── datecurve_description.png
│   │   ├── datecurve_email.png
│   │   ├── datecurve_engine.png
│   │   ├── datecurve_home.png
│   │   ├── datecurve_icon.png
│   │   ├── datecurve_maintainers.png
│   │   ├── datecurve_name.png
│   │   ├── datecurve_sources.png
│   │   ├── datecurve_version.png
│   ├── histogram
│   │   ├── histogram_apiVersion.png
│   │   ├── histogram_appVersion.png
│   │   ├── histogram_description.png
│   │   ├── histogram_email.png
│   │   ├── histogram_engine.png
│   │   ├── histogram_home.png
│   │   ├── histogram_icon.png
│   │   ├── histogram_maintainers.png
│   │   ├── histogram_name.png
│   │   ├── histogram_sources.png
│   │   ├── histogram_version.png
│   ├── CountPerKey.txt
│   ├── CountPerModul.txt
│   ├── Timeseries.png
│   ├── histogram_weekdays.png
├── depricated
│   ├── HelmContent.py
│   ├── helm.py
├── output
│   ├── ...
├── README.md
├── analyzer.py
└── tgzComparison.py
```
  
