# Split Drive

These routines test Omar's Split Drive construct for protection and invasiveness in two neighboring populations.

* **CRISPR** in both variants 'replacement' and 'suppression'.
* **Inundative Releases** a Mendelian cube to benchmark suppression.
* **Split Drive** _Cas9_ and _gRNA_ are separated, so the drive tends to be more confined.

##  Scripts

* [splitDrive_Main](./splitDrive_Main.py): Generates the traces plots in batch from the shared drive directory for all drives.
* [splitDrive_Select](./splitDrive_Select.py): Sets up the genotypes and paths for the drives-specific parameters.
* [SplitDriveFactorialsFinals02](./SplitDriveFactorialsFinals02.nb): Does the response surfaces for the paper **[NEED TO VERIFY]**

##  Metrics

* **Health**: Counts the genotypes that have at least one **H**, assuming the drive is dominant for pathogen-blocking properties.
* **Ecology**: Counts the frequency of **W** against all of the other genotypes.

##  Latest Changes

* Inundative releases is now Mendelian with only two genotypes.
