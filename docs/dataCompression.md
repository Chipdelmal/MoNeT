# Experiments Compression and Serialization

To decide which Compression algorithm would be best for our use, we ran a benchmark to compare them.
We want a compression algorithm that is lossless and is easily utilized in Python.
This criteria led us to the following compression algorithms: zip, lzma, gzip and bz2.

Here are the steps to the following experiment:
1. Load in the data from the appropriate directory
2. Clean the data to ensure data is consistent & usable
3. Convert cleaned data into a dictionary where it follows this format: {header : array of column values}
4. For each compression algorithm we will complete the following steps
  - Start a timer
  - Pickle and compress the data.  Note: For the Zip compression algorithm, we skipped this step
  - Record the time
  - Open output directory & write compressed data into the appropriate (.zip, .xz, .gz, .gz2)
  - Record the time

After collecting this data, we generated the following plots to assist us with our analysis.

Plots:

<center>

<img src="./media/CompressionAlg_06.png" width="65%" align="middle">

<img src="./media/CompressionAlg_07.png" width="65%" align="middle">

<img src="./media/CompressionAlg_08.png" width="65%" align="middle">

<img src="./media/CompressionAlg_09.png" width="65%" align="middle">

<img src="./media/CompressionAlg_10.png" width="65%" align="middle">


</center>




## Authors

Priscilla Zhang, Héctor M. Sánchez C.
