# HelmChangeAnalyzer

This tool analyzes a Repository containing Helm charts. This too automaticially unpacks the tgz
files and runs a diff on it. Based in the different fields a Helm-chart contains, 
it counts the additions, deletions, and changes of these fields. This tool can be applied to a single 
file or the whole repository.

# How to Run

Run the `tgzComparison.py`

If the whole repository should be analysed run the script with these arguments:
`repo <all|content|count> <outputPath> <trackingdir> <tempStoragePath>`

If the only one file should be analysed run the script with these arguments:
`file <all|content|count> <outputPath> <trackingdir> <tempStoragePath> <filename>`

# The arguments

## <all|content|count>
Defines what output should be generated:	
### content
Generates a json for each file where for each key all the changes are listed.
Like thisa hostory for each key's entry can be seen.

### count
Generates a json ove the whole repo/file that stores the numbers of additions, deletions and changes
together with the date and some additional information.

### all
Does both of the above

## <outputPath>
Path to where the output Json should be stored

## <trackingdir>
Path to the directory in the repo where the charts are stored at.

## <tempStoragePath>
Path to where the tgz should be temporarely be extracted to.

## <filename>
Filename of the file to be analysed. should en with tgz. only the name not the whole path.
