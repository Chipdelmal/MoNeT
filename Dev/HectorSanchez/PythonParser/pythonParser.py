def readExperimentFilenames(experimentPath,sexFilenameIdentifiers={"male":"ADM","female":"AF1"}):
    """
    In: Path to the directory that contains the experiments' CSV files (quantiles over patches).
    Out: Tuple with the sorted lists of male and female lexicographically sorted patches filenames.
    Note: This function assumes that male and female naming conventions keep the same lexicographical sorting
        for processing in further functions on the pipeline.
    """
    filenames=os.listdir(path)
    maleFiles=sorted(glob.glob(path + "/" + sexIdentifiers.get("male") + "*.csv"));
    femaleFiles=sorted(glob.glob(path + "/" + sexIdentifiers.get("female") + "*.csv"));
    return {"Male":maleFiles,"Female":femaleFiles}
