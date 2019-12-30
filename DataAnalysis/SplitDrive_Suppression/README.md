# Split Drive: Two-Node Suppression

These routines were coded to do the comparison between different suppression drives in two-node landscapes. Same as for the *pgSIT*, we are interested in health, and ecology outcomes. The metric taken into account for now is the time the non-drive alleles appear in the population (assuming the *H* is dominant).


##  Files

* Main sim file: https://github.com/Chipdelmal/MGDrivE/blob/master/Main/SplitDrive/Main_Suppression.R
* Main analysis file: https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/SplitDrive_Suppression/main.py
* Drives selection/definition routines: https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/SplitDrive_Suppression/drive.py
* Other functions definitions: https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/SplitDrive_Suppression/aux.py


##  Notes

* *WARNING:* Special care had to be taken for the autosomal shredder, which has two _locii_.
* Revert [main.py](https://github.com/Chipdelmal/MoNeT/blob/master/DataAnalysis/SplitDrive_Suppression/main.py) to this [commit](https://github.com/Chipdelmal/MoNeT/commit/8c60a18a445bad83b89cdd76ab2c46b5df3cafb0) for the ecology metric (days of the wild below a threshold)
