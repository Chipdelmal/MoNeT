(* ::Package:: *)

(* Mathematica Package *)
(* Programmed by: Hector Manuel Sanchez Castellanos [chipdelmal]*)
(* Contact: sanchez.hmsc@itesm.mx*)
(* Created by the Wolfram Workbench Feb 4, 2014 *)
 
BeginPackage["PajaroLocoPublic`"]
EdgesStyleList::usage = ""
CreateEdges::usage = ""
RemoveEdgesWithZeroTransitionProbability::usage = ""
VertexNumberToVertexSyllable::usage = ""
EdgesStyleList2::usage = ""
GetPackageVersion::usage ="In[] Out[versionNumber] ::Returns a string with the number of the installed PajaroLoco version. Created for error debugging purposes."
DeletePhraseIfLonger::usage ="In[song,phraseMaxSize] Out[song] ::Deletes a phrase if it is longer than the allowed number of characters. Used to remove researchers' notes."
SplitSongWherePhraseCountIsLower::usage ="In[song,threshold] Out:[songList] ::Splits a song where there are phrases that occur less times than those allowed by a threshold value. This function is to be used to remove phrases that repeat seldomly and need to be removed for analysis."
ImportSongFromTextGrid::usage ="In[filePath,birdNameInUpperCase] Out[song] ::Imports a song from a textgrid where the name value corresponds to the bird tag supplied in TextGrid. The TextGrid should include the tag: name = birdName."
ExtractTimedSyllablesFromTextGrid::usage ="In[filePath,birdNameInUpperCase] Out[timedSong] ::Imports a text grid file with the timing information. A list containing the phrases names with their starting and enging times is returned for analysis."
GetPhrasesFrequencies::usage ="In[song] Out[phrasesCount] ::Receives a song and returns the number of times each phrase present is repeated."
GetPhrasesFrequenciesWithPattern::usage ="In[song,patternList] Out[phrasesCount] ::Receives a song with a pattern list and returns the number of times each phrase from the pattern list is repeated in a specific order."
GetPhrasesCumulativeFrequencies::usage ="In[song] Out[phrasesCount] ::Receives a song and returns the cumulative number of times each phrase is repeated. Each phrase is counted and added to the total of phrases which is accumulated on the following phrases."
GetPhrasesCumulativeFrequenciesWithPattern::usage ="In[song,patternList] Out[phrasesCount] ::Receives a song with a pattern list and returns the cumulative number of times each phrase in the pattern list is repeated in the song in an specific order."
BarChartPhrasesFrequencies::usage ="In[phrasesCount] Out[barChart] ::Creates a bar chart of the frequencies of the phrases of a song."
BarChartPhrasesCumulativeFrequencies::usage ="In[phrasesCount] Out[barChart] ::Creates a bar chart of the cummulative frequencies of the phrases of a song."
ListPlotSong::usage ="*In[song,phrasesLabels] Out[listPlot] ::Creates a list plot with the phrases of a given song."
PlotScaledSongWithFrequency::usage ="In[song,baseSize] Out[plot] ::Creates a visulization in which the song is presented with the phrases scaled to their frequencies values"
LogLogPlotPhrasesFrequencies::usage ="In[phrasesCount] Out[LogLogPlot] ::Creates a Zipf plot from a list of phrases frequencies. To be used for the analysis of scale-free properties of songs."
GetZipfModelFromPhrasesFrequencies::usage ="In[phrasesCount,independentVariable] Out[zipfModel] ::Creates a Zipf model from a list of phrases frequencies and an independent variable. To be used for analysis of scale-free properties of songs."
GetCumulativeNumberOfDifferentPhrases::usage ="In[song] Out[cumulativeCount] ::Gets the number of different phrases used in every step of the sample. Used to measure the linguistic diversity of the sample."
PlotCumulativeNumberOfDifferentPhrases::usage ="In[song] Out[cumulativePlot] ::Creates a plot of the number of different phrases used in every tick of the sample"
GetRepertoire::usage ="In[song] Out[repertoire] ::Returns the different phrases used in a song. Can be used as pattern for network functions."
GetRepertoireSize::usage ="In[song] Out[repertoireSize] ::Returns the number of different phrases used in a song."
GetWindowedRepertoire::usage ="In[song,windowSize] Out[repertoireInWindows] ::Returns the list of repertoires with a preset window around each syllable."
GetWindowedRepertoireSize::usage ="In[song,windowSize] Out[reprtoireSizeInWindows] ::Returns the size of the repertoire with a preset window around each syllable."
PlotWindowedRepertoireSize::usage ="In[song,windowSize] Out[listPlot] ::Creates a plot of the size of the repertoire size in every tick of the sample."
GetCumulativeRepertoire::usage ="In[song] Out[cumulativeRepertoire] ::Returns the cumulative repertoire found in a song. This measures the accumulated number of different phrases used in a song."
GetPairwiseRepertoireSimilarity::usage ="*In[songA,songB] Out[similarity] ::Calculates the repertoire similarity between two songs."
GetTransitionsMarkov::usage ="In[song] Out[networkMatrixMarkov] ::Returns the first order Markov transition matrix from a song."
GetTransitionsMarkovWithPattern::usage ="In[song,pattern] Out[networkMatrixMarkov] ::Returns the Markov transition matrix from a song according to a pattern of phrases that is used as input. This pattern is the one that decides in which order the phrases are set in the matrix."
GetTransitionsFrequencies::usage ="In[song] Out[networkMatrixFrequencies] ::Returns the Frequencies transition matrix from a song."
GetTransitionsFrequenciesWithPattern::usage ="In[song,pattern] Out[networkMatrixFrequencies] ::Returns the Frequency transition matrix from a song according to a pattern of phrases used as input. This pattern is the one that decides in which order the phrases are set in the matrix."
TableFormTransitions::usage ="In[networkMatrix] Out[transitionsTable] ::Creates a table display from a Markov output. This is intended to be a more friendly approach to show the matrix as an alternative to TableForm or Grid."
GraphTransitionsMarkov::usage ="In[networkMatrixMarkov] Out[networkGraphMarkov] ::Generates a graph with the edges corresponding to probabilites of transitions between phrases and the vertices to the phrases. The graph's edges width and color change by default to show how probable a transition is."
GraphTransitionsFrequencies::usage ="In[networkMatrixFrequencies] Out[networkGraphFrequencies] ::Generates a graph with the edges corresponding to transition frequencies between phrases and the vertices to the phrases. The graph's edges width and color change by default to show how frequent a transition is."
GraphTransitionsFrequenciesWithMax::usage ="In[networkMatrixFrequencies,maxValue] Out[networkGraph] ::Generates a transitions graph which colors are scaled to the value entered as MAX. Mostly used to compare several networks with a same frequency scale."
GraphCommunitiesForPublication::usage ="In[networkMatrix] Out[networkGraph] ::Creates a communities graph representation that could be used for publication purposes. The graphs are intended to be readable and customizable to fit publication requirements."
GraphForPublication::usage ="In[networkMatrix] Out[networkGraph] ::Creates a frequencies graph representation that could be used for publication purposes. The graphs are intended to be readable and customizable to fit publication requirements."
GridColorScaleMarkov::usage ="In[numberOfFrames,diskSize] Out[gridColorScale] ::Creates a grid of disks in which the hue of each disk corresponds to the probability of a transition. This should be used as a complement to the graph generation function."
GridColorScaleFrequency::usage ="In[numberOfFrames,diskSize,frequencyOutput] Out[gridColorScale] ::Creates a grid of disks in which the hue of each disk corresponds to the frequency of a transition. This should be used as a complement to the graph generation function."
ConvertAdjacencyMatrixToEdgesList::usage ="In[networkMatrix] Out[edgesList] ::Converts an adjacency matrix into an edges list. Edges lists can be used in R's iGraph software."
GraphCentrality::usage ="In[function,graph] Out[networkGraph] ::Creates a centrality graph from a regular graph by highlighting the centrality values with the sizes of the vertices."
GraphCommunities::usage ="In[networkGraph,communities] Out[networkGraph] ::Creates a communities graph by highlighting the communities with different colors."
PlotDegreeDistribution::usage ="In[networkGraph] Out[degreeDistributionPlots] ::Creates the degree distribution, cummulative probability and probability distribution plots of a given graph."
GetBottlenecks::usage ="In[networkGraphFrequencies,inDegreeThreshold,outDegreeThreshold] Out[listOfPhrases] ::Returns the list of phrases with large in-degree and low out-degree. Used for network motifs analysis (generally using the mean number of degrees as threshold)."
GetBranches::usage ="In[networkGraphFrequencies,inDegreeThreshold,outDegreeThreshold] Out[listOfPhrases] ::Returns the list of phrases with large out-degree and low in-degree. Used for network motifs analysis (generally using the mean number of degrees as threshold)."
GetOneWays::usage ="In[networkGraphFrequencies,inDegreeThreshold,outDegreeThreshold] Out[listOfPhrases] ::Returns the list of phrases with similar out-degree and low in-degree. Used for network motifs analysis (generally using the mean number of degrees as threshold)."
GetHourglasses::usage ="In[networkGraphFrequencies,inDegreeThreshold,outDegreeThreshold] Out[listOfPhrases] ::Returns the list of phrases with large out-degree and large in-degree. Used for network motifs analysis (generally using the mean number of degrees as threshold)."
GetSmallWorldCoefficient::usage ="In[networkGraph,randomGraphsNumber] Out[] ::Calculates the small-world coefficient of a graph by comparing it to a certain amount of randomly generated graphs. The more random graphs number used the more precise the SW value obtained."
TableFormCommunities::usage ="In[networkMatrix,communities] Out[] ::Creates a table display with the communities of each row highlighted in green. This is intended to be a more friendly approach to show the matrix as an alternative to TableForm or Grid."
GetCommunitiesInOutTransitionsFrequencies::usage ="In[networkMatrix,communities] Out[] ::Returns a list of pairs that contain the frequencies of transitions within the community and outside the community."
GetCommunitiesInOutTransitionsRatios::usage ="*In[networkMatrix,communities] Out[] ::Returns a list of pairs that contain the ratios of transitions within the community and outside the community. These frequencies are returned in the order the communities are provided."
GetCommunitiesInOutTransitionsGlobalRatio::usage ="*In[networkMatrix,communities] Out[] ::Returns the total IN/OUT community transitions ratio for the whole community. These frequencies are returned in the order the communities are provided."
ListPlotSongWithCommunities::usage ="In[song,communities] Out[listPlot] ::Creates a list plot of the song with the communities highlighted with rectangles. This is a good complement to the network communities representation."
TestScripts::usage ="In[] Out[verificationList] ::Runs a test on python scripts used on the package (each script should return 0 if running correctly). If the function returns any number other than zero it is probable that some library is missing. Please check the documentation."
RunCollocationsScript::usage ="In[song] Out[] ::Runs the external python collocations script and returns {flag, frequencies, scores}. This function requires Python's package NLTK."
RunNewmanScript::usage ="In[networkMatrix] Out[newmanCommunitiesList] ::Runs the external python Newman communities script and returns {flag, communities, modularity} (depreciated as Mathematica v10 has the fuinction built-in)."
RunAlignmentScript::usage ="In[songs,validCharacters] Out[alignedSongs] ::Runs the external python alignment script from LingPy. The aligned samples are returned as lists that match length."
GridAlignment::usage ="In[alignedSongs] Out[gridAlignedSongs] ::Creates a grid representation of a set of aligned sequences."
ConvertEdgesListToAdjacencyMatrix::usage ="In[edgesList,weightsList] Out[networkMatrix] ::Converts an edges list to an adjacency matrix representation. Used to import iGraph's networks to Mathematica."
ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix::usage ="In[collocationsFrequencies] Out[networkMatrix] ::Transforms a collocation frequencies list into a co-occurrences adjacency matrix"
ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrixWithPattern::usage ="In[collocationsFrequencies,pattern] Out[networkMatrix] ::Transforms a collocation frequencies list into a co-occurrences adjacency matrix according to a given pattern"
ConvertAdjacencyMatrixToiGraphEdgeList::usage ="In[networkMatrix] Out[edgesList] ::Transforms an adjacency matrix to an iGraph edges list format"
ExportAdjacencyMatrixToNCol::usage ="In[networkMatrix] Out[exportPathString] ::Exports an adjacency matrix to an NCOL format file."
ImportGraphFromNColFile::usage ="In[file] Out[networkMatrix] ::Imports a graph from an NCol formatted file preserving the input labels."
ImportGraphFromNColWithPhrasesLabels::usage ="In[file,labels] Out[networkMatrix] ::Imports a graph from an NCol file transforming numeric input labels to their corresponding phrases labels."
MatrixPlotSong::usage ="*In[song,labels,windowSize] Out[matrixPlot] ::Creates a matrix plot visualization with the given sample"
GetTransitionsGraph::usage ="In[song] Out[networkGraph] ::Generates the transitions graph of a song. Use whenever only the graph representation is required, not the adjacency matrix."
GetColocationsGraph::usage ="In[song] Out[networkGraph] ::Generates the colocations graph of a song. Use whenever only the graph representation is required, not the adjacency matrix."
GetTransitionsGraphWithPattern::usage ="In[song,pattern] Out[networkGraph] ::Generates the transitions graph given a pattern of phrases (repertoire)."
GetColocationsGraphWithPattern::usage ="In[song,pattern] Out[networkGraph] ::Generates the colocations graph given a pattern of phrases (repertoire)."
GetIndividualTransitionsGraph::usage ="In[songsList] Out[networkMatrixAndGraph] ::Generates the transitions graph of a group of songs (by performing the sum of the different matrices). This function takes a list of several different songs and obtains the total transitions graph."
GetIndividualColocationsGraph::usage ="In[songsList] Out[networkMatrixAndGraph] ::Generates the colocations graph of a group of songs (by performing the sum of the different matrices). This function takes a list of several different songs and obtains the total transitions graph."
GetIndividualTransitionsGraphWithPattern::usage ="In[songsList,pattern] Out[networkMatrixAndGraph] ::Generates the transitions graph of a group of songs (by performing the sum of the different matrices) given a pattern of phrases. This function takes a list of several different songs and obtains the total transitions graph."
GetIndividualColocationsGraphWithPattern::usage ="In[songsList,pattern] Out[networkMatrixAndGraph] ::Generates the colocations graph of a group of songs (by performing the sum of the different matrices) given a pattern of phrases. This function takes a list of several different songs and obtains the total transitions graph."
CreateFrequenciesGraphAnimationFrames::usage ="In[sample] Out[listWithFrames] ::Generates the frames for the animation of the generation of a frequencies graph (with no time information). Oriented towards brief demonstrations for people who already know about the project."
LaunchVisualizerInterface::usage ="In[] Out ::Currently unused."
GenerateGraphAnimation::usage ="In[songWithTime,fps] Out[listWithFrames] ::Creates the frames for the animation of the network representation of a textgrid file to be synched with an audio file. The frames are intended to be exported so that another software (preferably ffmpeg) generate a video from them."

Begin["`Private`"]
(*Auxiliary*)
GetPackageVersion[]:=1.6
DeletePhraseIfLonger[song_, phraseMaxSize_] := Delete[song, Transpose[{Drop[Position[song, a_ /; StringLength[a // ToString] != phraseMaxSize] // Flatten, 1]}]]
ReplacePhraseIfCountIsLower[song_,threshold_,replaceCharacter_]:=Module[{repertoire,counts,bools,replace,replacementRules},
	repertoire = song // GetRepertoire;
	counts = Count[song, #] & /@ repertoire;
	bools = If[# < threshold, False, True] & /@ counts;
	replace = If[#[[2]], #[[1]], "-"] & /@ ({repertoire, bools} // Transpose);
	replacementRules = (#[[1]] -> #[[2]]) & /@ ({repertoire, replace} // Transpose);
	{song /. replacementRules,replace}
]
SplitSongWherePhraseCountIsLower[song_, threshold_] := Module[{replaces, replacedRepertoire, segmentedSongs},
  	replaces = ReplacePhraseIfCountIsLower[song, threshold, "-"];
  	replacedRepertoire = replaces[[2]] // DeleteCases[#, "-"] &;
  	segmentedSongs = Split[replaces[[1]], Xnor[#1 == "-", #2 == "-"] &];
  	Table[If[Count[segmentedSongs[[i]], "-"] == 0, segmentedSongs[[i]], ## &[]], {i, 1, segmentedSongs // Length}]
]
(*TextGrid*)
ImportSongFromTextGrid[filePath_, birdNameInUpperCase_] := Module[{fullFile, caviList, caviStart, namesPosition, caviPosition, caviEnd},
  	fullFile = Import[filePath, "Table"];
  	caviList = Position[fullFile, {"name", _, a_} /; (StringPosition[a // ToUpperCase, ToUpperCase[birdNameInUpperCase]] //Length) > 0];
  	If[caviList != {},
   		caviStart = caviList[[1]][[1]];
   		namesPosition = Flatten[Position[fullFile, {"name", _, _}]];
   		caviPosition = Position[namesPosition, caviStart][[1]][[1]];
   		caviEnd = If[Length[namesPosition] > caviPosition, namesPosition[[caviPosition + 1]], Length[fullFile]];
   		{filePath, Cases[fullFile[[caviStart + 1 ;; caviEnd - 1]], {"text", _, _}][[All, 3]]}, 
   		## &[]
   	]
]
ExtractTimedSyllablesFromTextGrid[filePath_, birdNameInUpperCase_] := Module[{a, fullFile, caviList, caviStart, positions, namesPosition, caviPosition, caviEnd, text, xmin, xmax},
  fullFile = Import[filePath, "Table"];
  caviList = Position[fullFile, {"name", _, a_} /; (StringPosition[a // ToUpperCase, birdNameInUpperCase] //Length) > 0];
  If[caviList != {},
   	caviStart = caviList[[1]][[1]];
   	namesPosition = Flatten[Position[fullFile, {"name", _, _}]];
   	caviPosition = Position[namesPosition, caviStart][[1]][[1]];
   	caviEnd = If[Length[namesPosition] > caviPosition, namesPosition[[caviPosition + 1]], Length[fullFile]];
   	positions = Cases[Position[fullFile, "xmin"][[All, 1]], a_ /; (a > caviStart && a <= caviEnd)];
   	,
   	## &[]];
  Table[{If[(fullFile[[i + 2]] // Length) < 3, "-", 
     fullFile[[i + 2]][[3]]], {fullFile[[i]][[3]], 
     fullFile[[i + 1]][[3]]}}, {i, positions[[2 ;; All]]}
  ]
]
(*Frequencies*)
GetPhrasesFrequencies[song_]:={#, Count[song, #]}& /@ (song//DeleteDuplicates)
GetPhrasesFrequenciesWithPattern[song_, pattern_]:={#, Count[song, #]}& /@ pattern
GetPhrasesCumulativeFrequencies[songSyllables_]:=Module[{syllablesFrequenciesList},
	syllablesFrequenciesList = GetPhrasesFrequencies[songSyllables];
	Transpose[{syllablesFrequenciesList[[All, 1]],Accumulate[syllablesFrequenciesList[[All, 2]]]}]
]
GetPhrasesCumulativeFrequenciesWithPattern[songSyllables_, pattern_] := Module[{syllablesFrequenciesList},
	syllablesFrequenciesList = GetPhrasesFrequenciesWithPattern[songSyllables, pattern];
	Transpose[{syllablesFrequenciesList[[All, 1]],Accumulate[syllablesFrequenciesList[[All, 2]]]}]
]
Options[BarChartPhrasesFrequencies]:={OrderedRange->{1,All},ImageSize->Automatic} 
BarChartPhrasesFrequencies[phrasesFrequencies_, OptionsPattern[]]:=BarChart[phrasesFrequencies[[OptionValue[OrderedRange][[1]] ;; OptionValue[OrderedRange][[2]], 2]], ChartLabels -> Placed[(phrasesFrequencies[[OptionValue[OrderedRange][[1]] ;; OptionValue[OrderedRange][[2]], 1]]),Below,Rotate[#,90Degree]&],ChartStyle -> "Pastel", AxesLabel -> {"Frequency", "Syllable"},ImageSize->OptionValue[ImageSize]]
Options[BarChartPhrasesCumulativeFrequencies]:={OrderedRange->{1,All},ImageSize->Automatic} 
BarChartPhrasesCumulativeFrequencies[phrasesCumulativeFrequencies_, OptionsPattern[]]:=BarChart[phrasesCumulativeFrequencies[[OptionValue[OrderedRange][[1]] ;; OptionValue[OrderedRange][[2]], 2]], ChartLabels-> Placed[(phrasesCumulativeFrequencies[[OptionValue[OrderedRange][[1]] ;; OptionValue[OrderedRange][[2]], 1]]),Below,Rotate[#,90Degree]&],ChartStyle -> "Pastel", AxesLabel -> {"CumulativeFrequency", "Syllable"},ImageSize->OptionValue[ImageSize]]
Options[ListPlotSong] := {ImageSize -> Automatic, Labeling -> False, TextSize->10}
ListPlotSong[sample_, syllablesLabels_, OptionsPattern[]] := Module[{texts, g},
  	texts = Graphics[Text[Style[ToString[#[[1]]], OptionValue[TextSize]], {(sample // Length) + 10, #[[2]]}, Automatic], AspectRatio -> 1] & /@ ({syllablesLabels, Range[syllablesLabels // Length]} // Transpose);
  	g = ListPlot[
    	If[OptionValue[Labeling] == True, Labeled[#[[1]], #[[2]]] &, Tooltip[#[[1]], #[[2]]] &] /@ ({ConvertSyllablesToID[sample, syllablesLabels], ToString /@ sample} // Transpose),
    	ImageSize -> OptionValue[ImageSize], PlotStyle -> PointSize[Medium], Filling -> Bottom, AxesLabel -> {"TimeStep", "ID"}, PlotRange -> {0, syllablesLabels // Length}, ImagePadding -> 50, GridLines -> Automatic, GridLinesStyle -> Directive[LightRed, Dashed]
    ];
  	Show[g, texts, PlotRange -> {0, (syllablesLabels // Length) + 1}]
]
PlotScaledSongWithFrequency[song_, baseSize_]:=Module[{freq,data=song},
	freq=GetPhrasesFrequencies[data];
	Text[
		Row[
			Table[Style[data[[i]],baseSize*(Cases[freq,{data[[i]],_}][[1,2]]),RandomColor[]],{i,1,data//Length}]
		]
	]
]
Options[LogLogPlotPhrasesFrequencies]:={ImageSize->Automatic}
LogLogPlotPhrasesFrequencies[syllablesFrequencies_, OptionsPattern[]] := ListLogLogPlot[Sort[syllablesFrequencies[[All, 2]],#2<#1&], Joined -> True, PlotMarkers -> {Automatic,Small}, AxesLabel -> {"Syllable Rank", "Frequency"},ImageSize-> OptionValue[ImageSize]]
GetZipfModelFromPhrasesFrequencies[syllablesFrequencies_, independentVariable_] := Module[{a, readyToFit},
  	a = Sort[syllablesFrequencies, #1[[2]] > #2[[2]] &] // Transpose;
  	readyToFit = ReplacePart[a, 1 -> Range[syllablesFrequencies // Length]] // Transpose;
  	LinearModelFit[Map[Log, readyToFit, {2}], {independentVariable}, {independentVariable}]
]
GetCumulativeNumberOfDifferentPhrases[sample_] := Table[sample[[1 ;; i]] // DeleteDuplicates // Length, {i, 1, sample // Length}]
Options[PlotCumulativeNumberOfDifferentPhrases] := {ImageSize -> Automatic}
PlotCumulativeNumberOfDifferentPhrases[sample_, OptionsPattern[]] := ListPlot[GetCumulativeNumberOfDifferentPhrases[sample], Joined -> True, AxesLabel -> {"Sequence Length", "Cumulative Number of Different Phrases"}, ImageSize -> OptionValue[ImageSize], PlotMarkers -> Automatic]
(*Repertoire*)
GetRepertoire[song_]:=song//DeleteDuplicates
GetRepertoireSize[song_]:=song//DeleteDuplicates//Length
GetWindowedRepertoire[song_, windowSize_]:=Module[{sampleIn = song},
  	Table[
    	sampleIn = RotateLeft[sampleIn, 1];
     	(sampleIn[[1 ;; windowSize]] // DeleteDuplicates)
    ,{sampleIn // Length}]
]
GetWindowedRepertoireSize[song_,windowSize_]:=Length /@ GetWindowedRepertoire[song,windowSize]
GetWindowedRepertoireMeanSize[song_,windowSize_]:=GetWindowedRepertoireSize[song,windowSize]//Mean
Options[PlotWindowedRepertoireSize] := {ImageSize -> Automatic, Joined -> True}
PlotWindowedRepertoireSize[windowSize_, sample_, OptionsPattern[]] := ListPlot[GetWindowedRepertoireSize[windowSize, sample], ImageSize -> OptionValue[ImageSize], Joined -> OptionValue[Joined],AxesLabel->{"Time","WindowedRepertoireSize"}]
GetCumulativeRepertoire[song_]:=Table[song[[1 ;; i]] // DeleteDuplicates // Length, {i, 1, song//Length}]
GetPairwiseRepertoireSimilarity[sampleA_, sampleB_] := Module[{repertoireA, repertoireB, c, a, b},
  	repertoireA = sampleA // GetRepertoire;
  	repertoireB = sampleB // GetRepertoire;
  	c = Intersection[repertoireA, repertoireB] // Length;
  	a = sampleA // GetRepertoireSize;
  	b = sampleB // GetRepertoireSize;
  	c/(Sqrt[a]*Sqrt[b])
]
(*Markov*)
GetTransitionsMarkov[song_] := GetTransitionsMarkovWithPattern[song,song//DeleteDuplicates]
GetTransitionsMarkovWithPattern[song_, pattern_] := Module[{nextSyllablesIndexes, nextSyllables, syllablesRelation, syllablesProbability, markov},
  	markov = Table[nextSyllablesIndexes = Flatten[Position[song, pattern[[i]]]] + 1;
    nextSyllablesIndexes = DeleteCases[nextSyllablesIndexes, x_ /; x > Length[song]];
    nextSyllables = song[[nextSyllablesIndexes]];
    syllablesRelation = Table[Count[nextSyllables, pattern[[j]]], {j, 1, Length[pattern]}];
    syllablesProbability = If[Total[syllablesRelation] != 0, syllablesRelation/Total[syllablesRelation], ReplacePart[ConstantArray[0, Length[pattern]], i -> 1]], {i, 1, Length[pattern]}];
  	{markov, pattern}
]
(*Frequencies*)
GetTransitionsFrequencies[song_]:=GetTransitionsFrequenciesWithPattern[song,song//DeleteDuplicates]
GetTransitionsFrequenciesWithPattern[song_, pattern_] := Module[{nextSyllablesIndexes, nextSyllables, syllablesRelation, markov},
  	markov = Table[
  		nextSyllablesIndexes = Flatten[Position[song, pattern[[i]]]] + 1;
    	nextSyllablesIndexes = DeleteCases[nextSyllablesIndexes, x_ /; x > Length[song]];
    	nextSyllables = song[[nextSyllablesIndexes]];
    	syllablesRelation = Table[Count[nextSyllables, pattern[[j]]], {j, 1, Length[pattern]}]
    ,{i, 1, Length[pattern]}];
  	{markov, pattern}
]
(*GraphsAuxiliary*)
CreateEdges[process_, syllables_] :=  With[{sm = MarkovProcessProperties[process, "TransitionMatrix"]}, Flatten@Table[DirectedEdge[i, j] -> sm[[i, j]], {i, Length[syllables]}, {j, Length[syllables]}]];
RemoveEdgesWithZeroTransitionProbability[rawEdges_] := Table[If[rawEdges[[i]][[2]] == 0, ## &[], rawEdges[[i]]], {i, 1, Length[rawEdges]}]
VertexNumberToVertexSyllable[syllables_, fixedEdgesList_] := Table[ DirectedEdge[syllables[[fixedEdgesList[[index]][[1]][[1]]]], syllables[[fixedEdgesList[[index]][[1]][[2]]]] -> fixedEdgesList[[index]][[2]]] // N, {index, 1, Length[fixedEdgesList]}]
Options[EdgesStyleList] := {LineThickness->.004, VariableStyle->"Both"}
EdgesStyleList[vertexSyllableList_, OptionsPattern[]] := 
	Switch[OptionValue[VariableStyle],
		"LineColor", Table[DirectedEdge[vertexSyllableList[[i]][[1]], vertexSyllableList[[i]][[2]][[1]]] -> {Hue[.85*vertexSyllableList[[i]][[2]][[2]]+.15], Thickness[OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}],
		"LineWidth", Table[DirectedEdge[vertexSyllableList[[i]][[1]], vertexSyllableList[[i]][[2]][[1]]] -> {Thickness[vertexSyllableList[[i]][[2]][[2]] * OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}],
		"Both", Table[DirectedEdge[vertexSyllableList[[i]][[1]], vertexSyllableList[[i]][[2]][[1]]] -> {Hue[.85*vertexSyllableList[[i]][[2]][[2]]+.15], Thickness[vertexSyllableList[[i]][[2]][[2]] * OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}],
		_,Table[DirectedEdge[vertexSyllableList[[i]][[1]], vertexSyllableList[[i]][[2]][[1]]] -> {Thickness[OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}]
	]
Options[EdgesStyleList2] := {LineThickness -> .004, VariableStyle -> "Both"}
EdgesStyleList2[vertexSyllableList_, OptionsPattern[]] := 
 	Switch[OptionValue[VariableStyle],
  		"LineColor", Table[DirectedEdge[vertexSyllableList[[i]][[1]][[1]], vertexSyllableList[[i]][[1]][[2]]] -> {Hue[.85*vertexSyllableList[[i]][[2]] + .15], Thickness[OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}],
  		"LineWidth", Table[DirectedEdge[vertexSyllableList[[i]][[1]][[1]], vertexSyllableList[[i]][[1]][[2]]] -> {Black, Thickness[vertexSyllableList[[i]][[2]]*OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}],
  		"Both", Table[DirectedEdge[vertexSyllableList[[i]][[1]][[1]], vertexSyllableList[[i]][[1]][[2]]] -> {Hue[.85*vertexSyllableList[[i]][[2]] + .15], Thickness[vertexSyllableList[[i]][[2]]*OptionValue[LineThickness]]},{i, 1, Length[vertexSyllableList]}], 
  		_, Table[DirectedEdge[vertexSyllableList[[i]][[1]][[1]], vertexSyllableList[[i]][[1]][[2]]] -> {Thickness[OptionValue[LineThickness]]}, {i, 1, Length[vertexSyllableList]}]
  	]
Options[MarkovSyllablesStyledGraph] := {GraphLayout -> Automatic, ImageSize -> 1000, VertexSize -> .25, EdgeShapeFunction -> edgeshape, VertexLabelStyle -> Automatic, EdgeWeight -> 0}
edgeshape[e_, ___] := {Arrowheads[{{.015, .9}}], Arrow[e]}
MarkovSyllablesStyledGraph[syllables_, process_, edgesStyleList_, OptionsPattern[]] := 
 	Graph[syllables, process, EdgeWeight -> OptionValue[EdgeWeight], 
  		ImageSize -> OptionValue[ImageSize], EdgeStyle -> edgesStyleList, 
  		GraphLayout -> OptionValue[GraphLayout], 
  		EdgeShapeFunction -> OptionValue[EdgeShapeFunction], 
  		VertexSize -> OptionValue[VertexSize], 
  		VertexLabelStyle -> OptionValue[VertexLabelStyle]
  	]
(*Graphs*)
TableFormTransitions[markovOutput_] := TableForm[markovOutput[[1]], TableHeadings -> {markovOutput[[2]], markovOutput[[2]]}, TableAlignments -> Center, TableSpacing -> {.75, .75}]
Options[GraphTransitionsMarkov] := {LineThickness -> .004, VariableStyle -> "Both", GraphLayout -> Automatic, ImageSize -> Automatic, VertexSize -> .5, EdgeShapeFunction -> edgeshape, VertexLabelStyle -> {Italic}}
GraphTransitionsMarkov[markovOutput_, OptionsPattern[]] := Module[{rawEdgesList, fixedEdgesList, vertexSyllableList, edgesStyleList}, 
  	rawEdgesList = CreateEdges[DiscreteMarkovProcess[1, markovOutput[[1]]], markovOutput[[2]]];
  	fixedEdgesList = RemoveEdgesWithZeroTransitionProbability[rawEdgesList];
  	vertexSyllableList = VertexNumberToVertexSyllable[markovOutput[[2]], fixedEdgesList];
  	edgesStyleList = EdgesStyleList[vertexSyllableList, LineThickness -> OptionValue[LineThickness], VariableStyle -> OptionValue[VariableStyle]];
  	MarkovSyllablesStyledGraph[markovOutput[[2]], 
   		DiscreteMarkovProcess[1, markovOutput[[1]]], edgesStyleList,
   		EdgeWeight -> vertexSyllableList[[All, 2, 2]],
   		ImageSize -> OptionValue[ImageSize],
   		GraphLayout -> OptionValue[GraphLayout],
   		EdgeShapeFunction -> OptionValue[EdgeShapeFunction],
   		VertexSize -> OptionValue[VertexSize],
   		VertexLabelStyle -> OptionValue[VertexLabelStyle]
   	]
 ]
Options[GraphTransitionsFrequencies] := {VertexStyle->Automatic, EdgeStyle->Automatic, LineThickness -> .0075, VariableStyle -> "Both", GraphLayout -> Automatic, ImageSize -> Automatic, VertexSize -> .5, EdgeShapeFunction -> edgeshape, VertexLabelStyle -> {Italic}}
GraphTransitionsFrequencies[frequenciesOutput_, OptionsPattern[]] := Module[{frequencies, syllables, max, edges, fixedEdgesList, vertexSyllableList, normalizedVertexSyllableList,edgesStyleList, links},
  	frequencies = frequenciesOutput[[1]];
  	syllables = frequenciesOutput[[2]];
  	max = frequencies // Flatten // Max;
  	edges = Table[DirectedEdge[i, j] -> frequencies[[i, j]], {i, Length[syllables]}, {j, Length[syllables]}] // Flatten;
  	fixedEdgesList = DeleteCases[edges, DirectedEdge[_, _] -> 0];
  	vertexSyllableList = VertexNumberToVertexSyllable[frequenciesOutput[[2]], fixedEdgesList];
	normalizedVertexSyllableList = (DirectedEdge[#[[1]], #[[2]][[1]]] -> #[[2]][[2]]/max &) /@ vertexSyllableList;
  	edgesStyleList = EdgesStyleList2[normalizedVertexSyllableList, LineThickness -> OptionValue[LineThickness], VariableStyle -> OptionValue[VariableStyle]];
  	links = DirectedEdge[#[[1]], #[[2, 1]]] & /@ vertexSyllableList;
  	Graph[syllables, links, EdgeWeight -> vertexSyllableList[[All, 2, 2]], VertexStyle->OptionValue[VertexStyle], EdgeStyle -> edgesStyleList, ImageSize -> OptionValue[ImageSize], GraphLayout -> OptionValue[GraphLayout], EdgeShapeFunction -> OptionValue[EdgeShapeFunction], VertexSize -> OptionValue[VertexSize], VertexLabelStyle -> OptionValue[VertexLabelStyle], VertexLabels -> Placed["Name", Center],EdgeLabels -> Table[links[[i]] -> Placed[fixedEdgesList[[All, 2]][[i]], Tooltip], {i, Length[links]}]]
]
Options[GraphTransitionsFrequenciesWithMax] := {VertexStyle->Automatic, VertexCoordinates-> Automatic, LineThickness -> .0075, VariableStyle -> "Both", GraphLayout -> Automatic, ImageSize -> Automatic, VertexSize -> .5, EdgeShapeFunction -> edgeshape, VertexLabelStyle -> {Italic}}
GraphTransitionsFrequenciesWithMax[frequenciesOutput_, max_, OptionsPattern[]] := Module[{frequencies, syllables, edges, fixedEdgesList, vertexSyllableList, normalizedVertexSyllableList,edgesStyleList, links},
  	frequencies = frequenciesOutput[[1]];
  	syllables = frequenciesOutput[[2]];
   	edges = Table[DirectedEdge[i, j] -> frequencies[[i, j]], {i, Length[syllables]}, {j, Length[syllables]}] // Flatten;
  	fixedEdgesList = DeleteCases[edges, DirectedEdge[_, _] -> 0];
  	vertexSyllableList = VertexNumberToVertexSyllable[frequenciesOutput[[2]], fixedEdgesList];
	normalizedVertexSyllableList = (DirectedEdge[#[[1]], #[[2]][[1]]] -> #[[2]][[2]]/max &) /@ vertexSyllableList;
  	edgesStyleList = EdgesStyleList2[normalizedVertexSyllableList, LineThickness -> OptionValue[LineThickness], VariableStyle -> OptionValue[VariableStyle]];
  	links = DirectedEdge[#[[1]], #[[2, 1]]] & /@ vertexSyllableList;
  	Graph[syllables, links, EdgeWeight -> vertexSyllableList[[All, 2, 2]], VertexStyle->OptionValue[VertexStyle], EdgeStyle -> edgesStyleList, VertexCoordinates-> OptionValue[VertexCoordinates], ImageSize -> OptionValue[ImageSize], GraphLayout -> OptionValue[GraphLayout], EdgeShapeFunction -> OptionValue[EdgeShapeFunction], VertexSize -> OptionValue[VertexSize], VertexLabelStyle -> OptionValue[VertexLabelStyle], VertexLabels -> Placed["Name", Center],EdgeLabels -> Table[links[[i]] -> Placed[fixedEdgesList[[All, 2]][[i]], Tooltip], {i, Length[links]}]]
]
GridColorScaleMarkov[numberOfFrames_, diskSize_] := Grid[{Prepend[N[Range[0, 1, 1/numberOfFrames], 2], "Probability"], Prepend[Table[Graphics[{Hue[i], Disk[{0, 0}, 1]}, ImageSize -> diskSize], {i, .15, 1, (1 - .15)/numberOfFrames}], "Color"]}, Frame -> All]
GridColorScaleFrequency[numberOfFrames_, diskSize_, frequencyOutput_] :=Grid[{Prepend[N[Range[Min[frequencyOutput[[1]] // Flatten],Max[frequencyOutput[[1]] // Flatten],(Max[frequencyOutput[[1]] // Flatten] - Min[frequencyOutput[[1]] // Flatten])/10], 2],"Frequency"],Prepend[Table[Graphics[{Hue[i], Disk[{0, 0}, 1]}, ImageSize -> diskSize], {i, .15, 1, (1 - .15)/numberOfFrames}], "Color"]}, Frame -> All]
Options[ConvertAdjacencyMatrixToEdgesList]:={AllowLoops->True}
ConvertAdjacencyMatrixToEdgesList[adjacencyMatrix_,OptionsPattern[]] := Module[{a,tuples, subsets, pairedMatrix, readyMatrix},
  	tuples = adjacencyMatrix[[2]] // Tuples[#, 2] & // Partition[#, adjacencyMatrix[[1]] // Length] &;
  	subsets = adjacencyMatrix[[2]] // Subsets[#, {2}] &;
	pairedMatrix = Table[{tuples[[i]], adjacencyMatrix[[1]][[i]]} // Transpose, {i, 1, adjacencyMatrix[[1]] // Length}] // Flatten[#, 1] &;
  	readyMatrix = {#[[1]][[1]], #[[1]][[2]], #[[2]]} & /@ pairedMatrix //N;
  	If[OptionValue[AllowLoops],readyMatrix,DeleteCases[readyMatrix, {a_, a_, _}]]
]
GraphCentrality[function_, graph_] := HighlightGraph[graph, VertexList[graph], VertexSize -> Thread[VertexList[graph] -> (Rescale[function @@ {graph}] + .25)]]
GraphCommunities[graph_,communities_]:= HighlightGraph[graph, Map[Subgraph[graph, #] &, communities], GraphHighlightStyle -> "Thick"]
Options[PlotDegreeDistribution]:={PlotStyle->{Thickness[.005]}}
PlotDegreeDistribution[graph_,OptionsPattern[]] := Module[{b, plotA, c, plotB, plotC, d},
  	d = graph // VertexDegree // Tally // Sort[#, #1[[1]] < #2[[1]] &] &;
  	b = {d[[All, 1]], d[[All, 2]]/(d[[All, 2]] // Total)} // Transpose;
  	plotA = ListLogLogPlot[d, Joined -> False, AxesLabel -> {"Degree", "Frequency"}, PlotStyle -> {OptionValue[PlotStyle]}];
  	c = {b[[All, 1]], Accumulate[b[[All, 2]]]} // Transpose;
  	plotB = ListPlot[Prepend[c,{0,0}], Joined -> True, PlotRange -> {0, 1.15}, AxesLabel -> {"Degree", "CumulativeProbability"},InterpolationOrder->2,PlotStyle->{OptionValue[PlotStyle]}];
  	plotC = SmoothHistogram[graph // VertexDegree, AxesLabel -> {"Degree", "Probability"},PlotRange->All,PlotStyle->{OptionValue[PlotStyle]}];
  	{plotA, plotB, plotC}//Quiet
]
(*SmallWorlds*)
MedianGraphDistance[graph_] := Median[If[# > 0, #, ## &[]] & /@ (graph // GraphDistanceMatrix // UpperTriangularize // Flatten)]
GenerateConnectedRandomGraphs[{vertexNumber_, edgesNumber_}, numberOfGraphs_] := Module[{connected, randomGraph},
  	connected = {};
	While[
   		Length[connected] < numberOfGraphs,
   		randomGraph = RandomGraph[{vertexNumber, edgesNumber}];
   		If[ConnectedGraphQ[randomGraph], connected = Append[connected, randomGraph]]
   	];
  	connected
]
Options[GetSmallWorldCoefficient] := {Method -> "Mean"}
GetSmallWorldCoefficient[graph_, randomGraphsNumber_, OptionsPattern[]] := Module[{studyGraph, edgesNumber, vertexNumber, lRand, cRand, l, c, connected},
  	studyGraph = SimpleGraph[UndirectedGraph[graph]];
  	edgesNumber = studyGraph // EdgeCount;
  	vertexNumber = studyGraph // VertexCount;
  	connected = GenerateConnectedRandomGraphs[{vertexNumber, edgesNumber}, randomGraphsNumber];
  	If[OptionValue[Method] == "Median", 
  		lRand = Map[MedianGraphDistance, connected] // Mean;
   		cRand = Map[MeanClusteringCoefficient, connected] // Mean;
   		l = MedianGraphDistance[studyGraph];
   		c = MeanClusteringCoefficient[studyGraph];
   		,
   		lRand = Map[MeanGraphDistance, connected] // Mean;
   		cRand = Map[MeanClusteringCoefficient, connected] // Mean;
   		l = MeanGraphDistance[studyGraph];
   		c = MeanClusteringCoefficient[studyGraph];
   	]; 
  	If[cRand != 0 && lRand != 0, (c/cRand)/(l/lRand), 0]
]
SyllableToID[a_, labels_] := Position[labels, a]
ConvertSyllablesToID[sample_, syllablesLabels_] := Table[SyllableToID[sample[[i]], syllablesLabels], {i, 1, Length[sample]}] // Flatten
InTuples[communitiesList_, syllablesLabels_] := Module[{communitiesIndexes},
  	communitiesIndexes = Map[(Map[Position[syllablesLabels, #] &, #] // Flatten) &, communitiesList];
  	Tuples[#, 2] & /@ communitiesIndexes
]
OutTuples[communitiesList_, syllablesLabels_] := Module[{outCommunity, communitiesIndexes},
  	communitiesIndexes = Map[(Map[Position[syllablesLabels, #] &, #] // Flatten) &,communitiesList];
  	outCommunity = Delete[Range[syllablesLabels // Length], #] & /@ Map[{#} & /@ # &, communitiesIndexes];
  	Tuples[{#[[1]], #[[2]]}] & /@ ({communitiesIndexes, outCommunity} //Transpose)
]
TableFormCommunities[frequency_, communities_] := Module[{repertoire, inTuples, outTuples, colorArray, colorArray2},
  	repertoire = frequency[[2]];
  	inTuples = InTuples[communities, repertoire];
  	outTuples = OutTuples[communities, repertoire];
  	colorArray = ((# + 1) -> LightGreen) & /@ Flatten[inTuples, 1];
  	colorArray2 = ((# + 1) -> LightYellow) & /@ ({Range[repertoire // Length], Range[repertoire // Length]} // Transpose);
  	Grid[MapThread[Prepend, {Prepend[frequency[[1]], frequency[[2]]], {"", frequency[[2]]} // Flatten}], Background -> {{LightRed}, {LightRed}, {colorArray, colorArray2} //Flatten}, Frame -> All,ItemSize->Full]
]
TransitionsValues[inputMatrix_, tuples_] := Map[Map[inputMatrix[[#[[1]], #[[2]]]] &, #] &, tuples] // N;
CalculateInOutRatio[inOutList_] := (inOutList[[1]]/(inOutList[[1]] + inOutList[[2]]))
Options[GetCommunitiesInOutTransitionsFrequencies] := {CountLoops -> True}
GetCommunitiesInOutTransitionsFrequencies[frequencyOutput_, communities_, OptionsPattern[]] := Module[{frequencyMatrix, labels, inTuples, inTransitions, outTuples, outTransitions, inTotals, outTotals},
  	frequencyMatrix = frequencyOutput[[1]];
  	labels = frequencyOutput[[2]];
  	inTuples = If[OptionValue[CountLoops],InTuples[communities, labels],DeleteCases[#,{a_,a_}]&/@InTuples[communities, labels]];
  	outTuples = OutTuples[communities, labels];
  	inTransitions = TransitionsValues[frequencyMatrix, inTuples];
  	outTransitions = TransitionsValues[frequencyMatrix, outTuples];
  	inTotals = Total /@ inTransitions;
  	outTotals = Total /@ outTransitions;
  	{inTotals, outTotals}
]
Options[GetCommunitiesInOutTransitionsRatios] := {CountLoops -> True}
GetCommunitiesInOutTransitionsRatios[frequencyOutput_,communities_, OptionsPattern[]]:=Module[{inOutTotals},
	inOutTotals = GetCommunitiesInOutTransitionsFrequencies[frequencyOutput,communities,CountLoops->OptionValue[CountLoops]];
	CalculateInOutRatio[#] & /@ (inOutTotals // Transpose)
]
Options[GetCommunitiesInOutTransitionsGlobalRatio] := {CountLoops -> True}
GetCommunitiesInOutTransitionsGlobalRatio[frequencyOutput_,communities_, OptionsPattern[]]:=Module[{communitiesInOutTotals},
	communitiesInOutTotals = Total /@ GetCommunitiesInOutTransitionsFrequencies[frequencyOutput, communities,CountLoops->OptionValue[CountLoops]];
	CalculateInOutRatio[communitiesInOutTotals]
]
Options[ListPlotSongWithCommunities] := {ImageSize -> Automatic, Labeling -> False, CountLoops->True, TextSize->10}
ListPlotSongWithCommunities[sample_, communities_, OptionsPattern[]] := Module[{frequencyOutput,inOutTotals,labels2,individualCommunitiesInOutRatios, texts, connectionsRules, connectionsWithLabels, rect, rectangles, listPlot, sortedCommunities, wrappers, communitiesIDs, wrappersID},
   	(*labels=communities//Flatten//DeleteDuplicates;*)
   	frequencyOutput=GetTransitionsFrequencies[sample];
   	inOutTotals=GetCommunitiesInOutTransitionsFrequencies[frequencyOutput,communities,CountLoops->OptionValue[CountLoops]];
   	labels2=communities//Flatten//DeleteDuplicates;
   	sortedCommunities = Table[SortBy[i, Position[labels2, #] &], {i, communities}];
  	wrappers = {(# // First) & /@ sortedCommunities, (# // Last) & /@ sortedCommunities} // Transpose;
  	communitiesIDs = Table[Position[labels2, #] & /@ i // Flatten, {i, sortedCommunities}];
  	wrappersID = {(# // First) & /@ communitiesIDs, (# // Last) & /@ communitiesIDs} // Transpose;
  	connectionsRules = wrappersID;
  	connectionsWithLabels = (UndirectedEdge[labels2[[#[[1]]]], labels2[[#[[2]]]]]) & /@ connectionsRules;
  	rect = Rectangle[{0.5, #[[1]]}, {(sample // Length) + .5, #[[2]]}, RoundingRadius -> 0] & /@ connectionsRules;
 	rectangles = Graphics[{EdgeForm[Directive[Dashing[RandomReal[{0, 0}]], Thickness[RandomReal[{.00175, .00175}]], Opacity[.5], Hue[#[[2]] + RandomReal[.05]]]], Opacity[0], Hue[#[[2]]], #[[1]]}, ImagePadding -> 500] & /@ ({rect, Table[i[[1]]/(labels2 // Length), {i, wrappersID}]} // Transpose);
  	individualCommunitiesInOutRatios = CalculateInOutRatio[#] & /@ (inOutTotals // Transpose);
  	texts = Graphics[Text[Style[ToString[#[[1]]], OptionValue[TextSize]], {(sample // Length)/2, #[[2]] - .35}, Automatic], AspectRatio -> 1] & /@ ({individualCommunitiesInOutRatios, connectionsRules[[All, 1]]} // Transpose);
  	listPlot = ListPlotSong[sample, labels2, ImageSize -> OptionValue[ImageSize], Labeling -> OptionValue[Labeling], TextSize->OptionValue[TextSize]];
  	Show[{listPlot,rectangles, texts} // Flatten]
]
(*PythonScripts*)
TestScripts[]:=Module[{alignmentReturn,collocationReturn,newmanReturn},
	alignmentReturn = Run["python alignSequences.py"];
	collocationReturn = Run["python collocation.py"];
	newmanReturn = Run["python newman.py newmanIn.dat"];
	{{"SequenceAlignment_LingPy",alignmentReturn},{"Collocations_NLTK",collocationReturn},{"Newman",newmanReturn}}
]
ReplaceArrayCharacters[triplet_] := {ToExpression[StringReplace[triplet[[1]], {"'" -> "\"", "(" -> "{", ")" -> "}"}]], triplet[[2]]}
RunCollocationsScript[song_]:=Module[{flag,frequency,score},
	Export["collocationsIn.csv", song];
	flag=Run["python collocation.py"];
	frequency=ReplaceArrayCharacters/@Import["outputFrequencycollocationsOut.csv"];
	score=ReplaceArrayCharacters/@Import["outputScoredcollocationsOut.csv"];
	{flag,frequency,score}
]
SyllableToID[a_, labels_] := Position[labels, a]
IDToSyllable[a_, labels_] := labels[[a]]
ConvertPhrasesToNumbers[song_, phrasesLabels_] := (SyllableToID[#, phrasesLabels]&/@song)//Flatten
ConvertNumbersToPhrases[song_, phrasesLabels_] := (IDToSyllable[#, phrasesLabels]&/@song)//Flatten
GetCommunitiesFromNewmanPython[rawFile_] := Module[{string, pythonOut, IDs},
  	string = StringReplacePart[rawFile, "", {(rawFile // StringLength) - 1, (rawFile // StringLength) - 1}];
  	pythonOut = string // StringReplace[#, {"[" -> "{", "]" -> "}"}] & // ToExpression;
  	IDs = pythonOut + 1
]
RunNewmanScript[frequencyOutput_]:=Module[{edgesList,communitiesRaw,modularityRaw,flag},
	edgesList = ConvertAdjacencyMatrixToEdgesList[{frequencyOutput[[1]],ConvertPhrasesToNumbers[frequencyOutput[[2]],frequencyOutput[[2]]]-1},AllowLoops->False];
	Export["newmanIn.dat",FixNumericIDToInteger[edgesList], FieldSeparators -> ","];
	flag = Run["python newman.py newmanIn.dat"];
	communitiesRaw = GetCommunitiesFromNewmanPython[Import["newmanOut1.txt", "Text"]];
	modularityRaw = Import["newmanOut2.txt","Text"];
	{flag,ConvertNumbersToPhrases[#,frequencyOutput[[2]]]&/@communitiesRaw,modularityRaw}
]
SampleToEncodingList[sample_, repertoire_, characters_] := characters[[ConvertPhrasesToNumbers[sample, repertoire]]]
FixCharacters[stringSample_] := FromCharacterCode /@ (ToCharacterCode /@ stringSample)[[All, -2]]
GetPositions[data_, validCharacters_] := Position[validCharacters, #] & /@ data // Flatten
IndexesToPhrasesAlignment[indexes_, repertoire_, validCharacters_] := Table[If[i != (validCharacters // Length), repertoire[[i]], "-"], {i,indexes}]
RunAlignmentScript[songs_, validCharacters_]:=Module[{repertoire,flag,encodedLists,encodedStrings,import,data,indexes},
	repertoire = songs // Flatten // GetRepertoire;
	encodedLists = SampleToEncodingList[#, repertoire, validCharacters] & /@ songs;
	encodedStrings = StringJoin@ #& /@ encodedLists;
	Export["alignmentIn.txt", encodedStrings];
	flag=Run["python alignSequences.py"];
	import = Import["alignmentOut.txt", "Table"];
	data = FixCharacters[#] & /@ import;
	indexes = GetPositions[#, validCharacters] & /@ data;
	{flag,IndexesToPhrasesAlignment[#, repertoire, validCharacters] & /@ indexes}
]
CheckEqual[tuple_] := If[(tuple // DeleteDuplicates // Length) == 1, True, False]
CheckSpace[tuple_] := If[(Cases[tuple, "-"] // Length) > 0, True, False]
StyleList[tuple_] := If[CheckSpace[tuple], LightBlue, If[CheckEqual[tuple], LightGreen, LightRed]]
GridAlignment[import_] := Module[{tuples},
  	tuples = import // Transpose;
  	Grid[import, Background -> {StyleList[#] & /@ tuples}, Frame -> All,ItemSize->Full]
]
(*Co-occurrences*)
ConvertEdgesListToAdjacencyMatrix[edgesList_, weightsList_] := Module[{matrix, labels},
  	matrix = Graph[edgesList, EdgeWeight -> weightsList] // WeightedAdjacencyMatrix // Normal;
  	labels = {#[[1]], #[[2]]} & /@ edgesList // Flatten // DeleteDuplicates;
  	{matrix, labels}
]
ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[collocationsFrequencies_] := Module[{edges, weights},
  	edges = DirectedEdge[#[[1]][[1]], #[[1]][[2]]] & /@ collocationsFrequencies;
  	weights = collocationsFrequencies[[All, 2]];
  	ConvertEdgesListToAdjacencyMatrix[edges, weights]
]
ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrixWithPattern[frequencies_, pattern_] := Module[{edgesList},
  	edgesList = Table[If[MemberQ[frequencies, {pattern[[i]], _}], frequencies[[Position[frequencies, {pattern[[i]], _}][[1, 1]]]], {pattern[[i]], 0}], {i, 1, pattern // Length}];
  	ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[edgesList]
]
(*iGraph*)
FixNumericIDToInteger[edgesList_]:={#[[1]]//IntegerPart,#[[2]]//IntegerPart,#[[3]]}&/@edgesList
ConvertAdjacencyMatrixToiGraphEdgeList[frequencyMatrix_]:=Module[{numericLabels},
	numericLabels=ConvertPhrasesToNumbers[frequencyMatrix[[2]],frequencyMatrix[[2]]]-1;
	ConvertAdjacencyMatrixToEdgesList[{frequencyMatrix[[1]],numericLabels}]//FixNumericIDToInteger
]
ExportAdjacencyMatrixToNCol[matrixOutput_,filePath_]:=Module[{edgesList},
	edgesList = ConvertAdjacencyMatrixToEdgesList[{matrixOutput[[1]], ConvertPhrasesToNumbers[matrixOutput[[2]], matrixOutput[[2]]] - 1}, AllowLoops -> True];
	Export[filePath, FixNumericIDToInteger[edgesList], "TSV"]
]
ImportUndirectedGraph[file_] := {UndirectedEdge[#[[1]], #[[2]]] & /@ Import[file, "Table"], ConstantArray[1, Import[file, "Table"] // Length]}
ImportDirectedGraph[file_] := {DirectedEdge[#[[1]], #[[2]]] & /@ Import[file, "Table"], ConstantArray[1, Import[file, "Table"] // Length]}
ImportUndirectedWeightedGraph[file_] := Module[{fileData},
 	fileData = Import[file, "Table"];
  	{UndirectedEdge[#[[1]], #[[2]]] & /@ fileData, fileData[[All, 3]]}
]
ImportDirectedWeightedGraph[file_] := Module[{fileData},
  	fileData = Import[file, "Table"];
  	{DirectedEdge[#[[1]], #[[2]]] & /@ fileData, fileData[[All, 3]]}
]
Options[ImportGraphFromNColFile] := {DirectedEdges -> True, WeightedEdges -> True}
ImportGraphFromNColFile[file_, OptionsPattern[]] := Module[{edgesList},
 	edgesList=If[OptionValue[WeightedEdges] == False,
  		If[OptionValue[DirectedEdges] == False, ImportUndirectedGraph[file],ImportDirectedGraph[file]],
  		If[OptionValue[DirectedEdges] == False, ImportUndirectedWeightedGraph[file], ImportDirectedWeightedGraph[file]]
  	];
  	ConvertEdgesListToAdjacencyMatrix[edgesList[[1]],edgesList[[2]]]
]
ConvertNumericEdgesListToPhrasesEdgesList[edgesList_,labels_] := Module[{fixed},
	fixed = ({#[[1]], #[[2]]} & /@ edgesList) + 1;
	DirectedEdge[labels[[#[[1]]]], labels[[#[[2]]]]] & /@ fixed	
]
Options[ImportGraphFromNColWithPhrasesLabels] := {DirectedEdges -> True, WeightedEdges -> True}
ImportGraphFromNColWithPhrasesLabels[file_,phrasesLabels_,OptionsPattern[]]:= Module[{edgesList,edgesListLabels},
 	edgesList=If[OptionValue[WeightedEdges] == False,
  		If[OptionValue[DirectedEdges] == False, ImportUndirectedGraph[file],ImportDirectedGraph[file]],
  		If[OptionValue[DirectedEdges] == False, ImportUndirectedWeightedGraph[file], ImportDirectedWeightedGraph[file]]
  	];
  	edgesListLabels=ConvertNumericEdgesListToPhrasesEdgesList[edgesList[[1]],phrasesLabels];
  	ConvertEdgesListToAdjacencyMatrix[edgesListLabels, edgesList[[2]]]
]
(*Other*)
MatrixPlotSong[sample_, syllablesLabels_, windowSize_] := Partition[ConvertSyllablesToID[sample, sample // GetRepertoire], windowSize, windowSize, {1, 1}] // MatrixPlot[#, ColorFunction -> "Pastel"] &
ConvertEdgesListToAdjacencyMatrix[edgesList_, weightsList_] := Module[{matrix, labels},
  	matrix = Graph[edgesList, EdgeWeight -> weightsList] // WeightedAdjacencyMatrix // Normal;
  	labels = {#[[1]], #[[2]]} & /@ edgesList // Flatten // DeleteDuplicates;
  	{matrix, labels}
]
ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[collocationsFrequencies_] := Module[{edges, weights},
  	edges = DirectedEdge[#[[1]][[1]], #[[1]][[2]]] & /@ collocationsFrequencies;
  	weights = collocationsFrequencies[[All, 2]];
  	ConvertEdgesListToAdjacencyMatrix[edges, weights]
]
ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrixWithPattern[frequencies_, pattern_] := Module[{edgesList},
  	edgesList = Table[If[MemberQ[frequencies, {pattern[[i]], _}], frequencies[[Position[frequencies, {pattern[[i]], _}][[1, 1]]]], {pattern[[i]], 0}], {i, 1, pattern // Length}];
  	ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[edgesList]
]
(*iGraph*)
FixNumericIDToInteger[edgesList_]:={#[[1]]//IntegerPart,#[[2]]//IntegerPart,#[[3]]}&/@edgesList
ConvertAdjacencyMatrixToiGraphEdgeList[frequencyMatrix_]:=Module[{numericLabels},
	numericLabels=ConvertPhrasesToNumbers[frequencyMatrix[[2]],frequencyMatrix[[2]]]-1;
	ConvertAdjacencyMatrixToEdgesList[{frequencyMatrix[[1]],numericLabels}]//FixNumericIDToInteger
]
ExportAdjacencyMatrixToNCol[matrixOutput_,filePath_]:=Module[{edgesList},
	edgesList = ConvertAdjacencyMatrixToEdgesList[{matrixOutput[[1]], ConvertPhrasesToNumbers[matrixOutput[[2]], matrixOutput[[2]]] - 1}, AllowLoops -> True];
	Export[filePath, FixNumericIDToInteger[edgesList], "TSV"];
]
ImportUndirectedGraph[file_] := {UndirectedEdge[#[[1]], #[[2]]] & /@ Import[file, "Table"], ConstantArray[1, Import[file, "Table"] // Length]}
ImportDirectedGraph[file_] := {DirectedEdge[#[[1]], #[[2]]] & /@ Import[file, "Table"], ConstantArray[1, Import[file, "Table"] // Length]}
ImportUndirectedWeightedGraph[file_] := Module[{fileData},
 	fileData = Import[file, "Table"];
  	{UndirectedEdge[#[[1]], #[[2]]] & /@ fileData, fileData[[All, 3]]}
]
ImportDirectedWeightedGraph[file_] := Module[{fileData},
  	fileData = Import[file, "Table"];
  	{DirectedEdge[#[[1]], #[[2]]] & /@ fileData, fileData[[All, 3]]}
]
ConvertNumericEdgesListToPhrasesEdgesList[edgesList_,labels_] := Module[{fixed},
	fixed = ({#[[1]], #[[2]]} & /@ edgesList) + 1;
	DirectedEdge[labels[[#[[1]]]], labels[[#[[2]]]]] & /@ fixed	
]
(*Other*)
MatrixPlotSong[sample_, syllablesLabels_, windowSize_] := Partition[ConvertSyllablesToID[sample, sample // GetRepertoire], windowSize, windowSize, {1, 1}] // MatrixPlot[#, ColorFunction -> "Pastel"] &
(*Mathematica10Update*)
CollageSong[song_, rasterSize_, imageSize_] := Module[{sampledData = song, data, images},
  	data = GetPhrasesFrequencies[sampledData];
  	images = #2 -> Rasterize[Style[#1, RandomColor[LCHColor[_, 1, _]]], "Image", RasterSize -> rasterSize] & @@@ data;
  	ImageCollage[images, "Fit", imageSize, ImagePadding -> 4, Background -> White]
]
ConvertTransitionFrequenciesMatrixToWeightedAdjacencyGraph[transitionFrequencies_] := WeightedAdjacencyGraph[transitionFrequencies[[1]], VertexLabels -> Table[i -> transitionFrequencies[[2, i]], {i, 1, transitionFrequencies[[2]] // Length}]]
Options[FindGraphCommunitiesFromTransitionFrequenciesMatrix] := {Method -> "Modularity"}
FindGraphCommunitiesFromTransitionFrequenciesMatrix[transitionFrequencies_, OptionsPattern[]] := Module[{graph},
  	graph = ConvertTransitionFrequenciesMatrixToWeightedAdjacencyGraph[transitionFrequencies];
  	transitionFrequencies[[2]][[#]] & /@ FindGraphCommunities[graph, Method -> OptionValue[Method]]
]
GetTransitionFrequenciesTotalFromSamples[songs_] := Module[{repertoire, frequencies},
  	repertoire = songs // Flatten // GetRepertoire // Sort;
  	frequencies = GetTransitionsFrequenciesWithPattern[#, repertoire] & /@ songs;
  	{frequencies[[All, 1]] // Total, frequencies[[1, 2]]}
]
GetTransitionFrequenciesTotalFromSamplesWithPattern[songs_,pattern_] := Module[{frequencies},
  	frequencies = GetTransitionsFrequenciesWithPattern[#, pattern] & /@ songs;
  	{frequencies[[All, 1]] // Total, frequencies[[1, 2]]}
]
GetIndividualGraphMeasures[individualData_, measuresList_] := Module[{transitionFrequencies, transitionFrequenciesGraph, colocations, fullRepertoire, tuples, collocationMatrices, collocationsGraphs, analysisGraphs1, analysisGraphs2, transitionFrequenciesGraphMeasures, colocationsFrequenciesGraphMeasures},
  	(*TransitionFrequenciesGraph*)
  	transitionFrequencies = GetTransitionFrequenciesTotalFromSamples[individualData];
  	transitionFrequenciesGraph = GraphTransitionsFrequencies[transitionFrequencies];
  	(*ColocationsFrequenciesGraph*)
  	colocations = RunCollocationsScript[individualData // Flatten];
  	fullRepertoire = individualData // Flatten // GetRepertoire // Sort;
  	tuples = Tuples[fullRepertoire, 2];
  	collocationMatrices = ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[colocations[[2]]];
  	collocationsGraphs = GraphTransitionsFrequencies[collocationMatrices];
  	(*Measures*)
    analysisGraphs1 = {{transitionFrequenciesGraph}, {transitionFrequenciesGraph // UndirectedGraph}} // Transpose;
  	analysisGraphs2 = {{collocationsGraphs}, {collocationsGraphs // UndirectedGraph}} // Transpose;
  	transitionFrequenciesGraphMeasures = Flatten /@ (((Map[#, analysisGraphs1, {2}] // N)) & /@ measuresList);
  	colocationsFrequenciesGraphMeasures = Flatten /@ (((Map[#, analysisGraphs2, {2}] // N)) & /@ measuresList);
  	(*Output*)
  	{ToString /@ measuresList, transitionFrequenciesGraphMeasures, colocationsFrequenciesGraphMeasures}
]
BootstrapSamples[samples_, lengthOfBootstrap_, repetitions_] := Table[RandomChoice[samples, lengthOfBootstrap], {i, 1, repetitions}]
GetThemesSimilarity[themes1_, themes2_] := Module[{best, obtained},
  	best = themes1 // Flatten // Length;
  	obtained = (Max /@ Table[NeedlemanWunschSimilarity[i // Sort, # // Sort] & /@ themes2, {i, themes1}]) // Total;
  	{obtained/best, {obtained, best}}
]  
(**)
GetTransitionsGraph[song_] := Module[{frequenciesMatrix, frequenciesGraph},
  	frequenciesMatrix = GetTransitionsFrequencies[song];
  	frequenciesGraph = GraphTransitionsFrequencies[frequenciesMatrix];
  	{frequenciesMatrix, frequenciesGraph}
]
GetColocationsGraph[song_] := Module[{colocations, fullRepertoire, tuples, collocationMatrices, collocationsGraphs},
  	colocations = RunCollocationsScript[song];
  	fullRepertoire = song // GetRepertoire // Sort;
  	tuples = Tuples[fullRepertoire, 2];
  	collocationMatrices = ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[colocations[[2]]];
  	collocationsGraphs = GraphTransitionsFrequencies[collocationMatrices];
  	{collocationMatrices, collocationsGraphs}
]
GetTransitionsGraphWithPattern[song_, pattern_] := Module[{frequenciesMatrix, frequenciesGraph},
  	frequenciesMatrix = GetTransitionsFrequenciesWithPattern[song, pattern];
  	frequenciesGraph = GraphTransitionsFrequencies[frequenciesMatrix];
  	{frequenciesMatrix, frequenciesGraph}
]
GetColocationsGraphWithPattern[song_, pattern_] := Module[{colocations, fullRepertoire, tuples, collocationMatrices, collocationsGraphs},
  	colocations = RunCollocationsScript[song];
  	tuples = Tuples[pattern, 2];
  	collocationMatrices = ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrixWithPattern[colocations[[2]], tuples];
  	collocationsGraphs = GraphTransitionsFrequencies[collocationMatrices];
  	{collocationMatrices, collocationsGraphs}
]
GetIndividualTransitionsGraph[individualSongs_] := Module[{frequenciesMatrix, frequenciesGraph},
  	frequenciesMatrix = GetTransitionFrequenciesTotalFromSamples[individualSongs];
  	frequenciesGraph = GraphTransitionsFrequencies[frequenciesMatrix];
  	{frequenciesMatrix, frequenciesGraph}
]
GetIndividualColocationsGraph[individualSongs_] := Module[{colocations, fullRepertoire, tuples, collocationMatrices, collocationsGraphs},
  	colocations = RunCollocationsScript[individualSongs // Flatten];
  	fullRepertoire = individualSongs // Flatten // GetRepertoire // Sort;
  	tuples = Tuples[fullRepertoire, 2];
  	collocationMatrices = ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrix[colocations[[2]]];
  	collocationsGraphs = GraphTransitionsFrequencies[collocationMatrices];
  	{collocationMatrices, collocationsGraphs}
]
GetIndividualTransitionsGraphWithPattern[individualSongs_, pattern_] :=Module[{frequenciesMatrix, frequenciesGraph},
  	frequenciesMatrix = GetTransitionFrequenciesTotalFromSamplesWithPattern[individualSongs, pattern];
  	frequenciesGraph = GraphTransitionsFrequencies[frequenciesMatrix];
  	{frequenciesMatrix, frequenciesGraph}
]
GetIndividualColocationsGraphWithPattern[individualSongs_, pattern_] :=Module[{colocations, fullRepertoire, tuples, collocationMatrices, collocationsGraphs},
  	colocations = RunCollocationsScript[individualSongs // Flatten];
  	tuples = Tuples[pattern, 2];
  	collocationMatrices = ConvertCollocationsFrequenciesToCoOccurrencesAdjacencyMatrixWithPattern[colocations[[2]], tuples];
  	collocationsGraphs = GraphTransitionsFrequencies[collocationMatrices];
  	{collocationMatrices, collocationsGraphs}
]
edgesShape[e_, ___] := {Arrowheads[{{.01, .75}}], Arrow[e]};
Options[CreateFrequenciesGraphAnimationFrames] := {LineThickness -> .0075, VariableStyle -> "Both", GraphLayout -> Automatic, ImageSize -> Automatic, VertexSize -> .5, EdgeShapeFunction -> edgesShape, VertexLabelStyle -> {Italic}}
CreateFrequenciesGraphAnimationFrames[sample_, OptionsPattern[]] := Module[{appendedData = sample, fullTransitionFrequencies, graphForm, vertexCoordinates, data, partialTransitionFrequencies, graph, highGraph},
  	fullTransitionFrequencies = GetTransitionsFrequencies[appendedData];
  	graphForm = GraphTransitionsFrequencies[fullTransitionFrequencies, ImageSize -> OptionValue[ImageSize], GraphLayout -> OptionValue[GraphLayout], EdgeShapeFunction -> OptionValue[EdgeShapeFunction], VertexSize -> OptionValue[VertexSize], VertexLabelStyle -> OptionValue[VertexLabelStyle]];
  	vertexCoordinates = GraphEmbedding[graphForm];
  	data = Table[
    	partialTransitionFrequencies = GetTransitionsFrequenciesWithPattern[appendedData[[1 ;; i]], fullTransitionFrequencies[[2]]];
    	graph = GraphTransitionsFrequenciesWithMax[partialTransitionFrequencies, fullTransitionFrequencies[[1]] // Flatten // Max,ImageSize -> OptionValue[ImageSize], GraphLayout -> OptionValue[GraphLayout], EdgeShapeFunction -> OptionValue[EdgeShapeFunction], VertexSize -> OptionValue[VertexSize], VertexLabelStyle -> OptionValue[VertexLabelStyle], VertexCoordinates -> vertexCoordinates];
    	highGraph = HighlightGraph[graph, {Style[appendedData[[1 ;; i]] // Last, LightYellow]}]
    ,{i, 2, appendedData // Length}]
]
(*Motifs*)
GetBottlenecks[frequenciesGraph_, inDegreeThreshold_, outDegreeThreshold_] := Module[{triplets},
  triplets = {frequenciesGraph // SimpleGraph // VertexInDegree, frequenciesGraph // SimpleGraph // VertexOutDegree, frequenciesGraph // VertexList} // Transpose;
  Cases[triplets, {a_, b_, c_} /; (a >= inDegreeThreshold && b <= outDegreeThreshold) -> {c, {a, b}}]
]
GetBranches[frequenciesGraph_, inDegreeThreshold_, outDegreeThreshold_] := Module[{triplets},
  triplets = {frequenciesGraph // SimpleGraph // VertexInDegree, frequenciesGraph // SimpleGraph // VertexOutDegree, frequenciesGraph // VertexList} // Transpose;
  Cases[triplets, {a_, b_, c_} /; (a <= inDegreeThreshold && b >= outDegreeThreshold) -> {c, {a, b}}]
]
GetOneWays[frequenciesGraph_, inDegreeThreshold_, outDegreeThreshold_] := Module[{triplets},
  triplets = {frequenciesGraph // SimpleGraph // VertexInDegree, frequenciesGraph // SimpleGraph // VertexOutDegree, frequenciesGraph // VertexList} // Transpose;
  Cases[triplets, {a_, b_, c_} /; (a == inDegreeThreshold && b == outDegreeThreshold) -> {c, {a, b}}]
]
GetHourglasses[frequenciesGraph_, inDegreeThreshold_, outDegreeThreshold_] := Module[{triplets},
  triplets = {frequenciesGraph // SimpleGraph // VertexInDegree, frequenciesGraph // SimpleGraph // VertexOutDegree, frequenciesGraph // VertexList} // Transpose;
  Cases[triplets, {a_, b_, c_} /; (a >= inDegreeThreshold && b >= outDegreeThreshold) -> {c, {a, b}}]
]
(*Publication Graphs*)
edgeshape[e_, ___] := {Arrowheads[{{.015, .9}}], Arrow[e]}
Options[GraphCommunitiesForPublication] := {ClusteringMethod-> "Modularity",LinesNumber->10, GridLineThickness -> .01, CommunityThickness -> .005, PlotSize -> 500, VertexLabelStyle -> {{Bold, FontSize -> 12, FontColor -> Black}},EdgeShapeFunction -> edgeshape, VertexSize -> .75, LinesPatternSize -> 25, CommunityColors -> {Red, Green, Blue, Cyan, Magenta, Yellow, Brown, 
    Orange, Pink, Purple, LightRed, LightGreen, LightBlue, LightMagenta, LightYellow, LightBrown, LightOrange, LightPink, LightPurple}}
GraphCommunitiesForPublication[transitionFrequencies_, OptionsPattern[]] := Module[{communities,steps= OptionValue[LinesNumber], lineThickness = OptionValue[GridLineThickness], plotsSize = OptionValue[PlotSize], min, max, widths, linesPattern, scaleGrid, communitiesFrequenciesPlot, colors, array, frequenciesGraph, communitiesPlot},
	(*Constants*)
  	colors = OptionValue[CommunityColors];
  	array = ConstantArray[Thickness[OptionValue[CommunityThickness]], colors // Length];
  	(*LinesPattern*)
  	{max, min} = Apply[#, Flatten[transitionFrequencies[[1]]]] & /@ {Max, Min};
  	widths = Range[min, max, (max - min)/steps] // N;
  	linesPattern = Graphics[{Thickness[#], Line[{{0, 0}, {0, .025}}]}, PlotRange -> {{-Max[(lineThickness*widths)]*.05, .05*Max[(lineThickness*widths)]}, {0, .025}}, PlotRangeClipping -> True, ImageSize -> OptionValue[LinesPatternSize]] & /@ (lineThickness*widths*2);
  	scaleGrid = Grid[{
     	Prepend[Round /@ widths[[2 ;; (widths // Length)]], "Frequency"],
     	Prepend[linesPattern[[2 ;; (widths // Length)]], "Width"]
     	}, Frame -> All];
  	(*FrequencyGraph*)  
  	frequenciesGraph = GraphTransitionsFrequencies[transitionFrequencies,
    	VertexLabelStyle -> OptionValue[VertexLabelStyle],
    	ImageSize -> plotsSize,
    	EdgeShapeFunction -> OptionValue[EdgeShapeFunction],
    	LineThickness -> lineThickness,
    	VertexSize -> OptionValue[VertexSize],
    	VariableStyle -> "LineWidth"
    ];
    communities = FindGraphCommunities[frequenciesGraph, Method -> OptionValue[ClusteringMethod]];
  	(*CommunityGraph*)
  	communitiesFrequenciesPlot = CommunityGraphPlot[frequenciesGraph, communities,
    	ImageSize -> plotsSize,
    	VertexStyle -> {White},
    	EdgeStyle -> Black,
    	CommunityBoundaryStyle -> ({colors, array} // Transpose)
    ];
  	(*Output*)
  	Grid[{{communitiesFrequenciesPlot}, {scaleGrid}}]
]
Options[GraphForPublication] := {ClusteringMethod -> "Modularity", LinesNumber -> 10, GridLineThickness -> .01, CommunityThickness -> .005, PlotSize -> 500, VertexLabelStyle -> {{Bold, FontSize -> 12, FontColor -> Black}}, EdgeShapeFunction -> edgeshape, VertexSize -> .75, LinesPatternSize -> 25, CommunityColors -> {Red, Green, Blue, Cyan, Magenta, Yellow, Brown, Orange, Pink, Purple, LightRed, LightGreen, LightBlue, LightMagenta, LightYellow, LightBrown, LightOrange, LightPink, LightPurple}}
GraphForPublication[transitionFrequencies_,OptionsPattern[]] := Module[{steps = OptionValue[LinesNumber], lineThickness = OptionValue[GridLineThickness], 
   plotsSize = OptionValue[PlotSize], min, max, widths, linesPattern, scaleGrid, communitiesFrequenciesPlot, colors, array, frequenciesGraph, communitiesPlot},(*Constants*)
  	colors = OptionValue[CommunityColors];
  	array = ConstantArray[Thickness[OptionValue[CommunityThickness]], colors // Length];
  	(*LinesPattern*)
  	{max, min} = Apply[#, Flatten[transitionFrequencies[[1]]]] & /@ {Max, Min};
  	widths = Range[min, max, (max - min)/steps] // N;
	linesPattern = Graphics[{Thickness[#], Line[{{0, 0}, {0, .025}}]}, PlotRange -> {{-Max[(lineThickness*widths)]*.05, .05*Max[(lineThickness*widths)]}, {0, .025}}, PlotRangeClipping -> True, ImageSize -> OptionValue[LinesPatternSize]] & /@ (lineThickness*widths*2);
  	scaleGrid = Grid[{Prepend[Round /@ widths[[2 ;; (widths // Length)]], "Frequency"], Prepend[linesPattern[[2 ;; (widths // Length)]], "Width"]}, Frame -> All];
  	(*FrequencyGraph*)
  	frequenciesGraph = GraphTransitionsFrequencies[transitionFrequencies, 
    	VertexLabelStyle -> OptionValue[VertexLabelStyle], 
    	ImageSize -> plotsSize, 
    	EdgeShapeFunction -> OptionValue[EdgeShapeFunction], 
    	LineThickness -> lineThickness, 
    	VertexSize -> OptionValue[VertexSize], 
    	VariableStyle -> "LineWidth",
    	VertexStyle->White
    ];
  	(*Output*)
  	Grid[{{frequenciesGraph}, {scaleGrid}}]
]
Options[GenerateGraphAnimation] := {BaseStyle -> {}, GraphLayout-> Automatic, CommunityColors -> {Red, Green, Blue, Cyan, Magenta, Yellow, Brown, Orange, Pink, Purple, LightGreen, LightBlue, LightMagenta, LightYellow, LightBrown, LightOrange, LightPink, LightPurple}, VertexStyle -> Automatic, LineThickness -> .0075, VariableStyle -> "Both", GraphLayout -> Automatic, ImageSize -> Automatic, VertexSize -> .5, EdgeShapeFunction -> edgesShape, VertexLabelStyle -> {Italic}}
GenerateGraphAnimation[songWithTime_, frameScale_, OptionsPattern[]] :=Module[{timedSong, song, communities, time, songPure, testData = songWithTime, fullTransitionFrequencies, graphForm, vertexCoordinates, j, graphs, partialTransitionFrequencies, graph, highGraph, trans, anim, colors = OptionValue[CommunityColors], constants, vStyles},
  	(*PreProcessing*)
  	timedSong = {#[[1]], (#[[2, 2]] - #[[2, 1]])*frameScale} & /@ testData;
  	{song, time, songPure} = {timedSong[[All, 1]], Round /@ timedSong[[All, 2]], Cases[timedSong[[All, 1]], a_ /; a != "-"]};
  	(*VerticesPositions*)
	fullTransitionFrequencies = GetTransitionsFrequencies[songPure];
  	graphForm = GraphTransitionsFrequencies[fullTransitionFrequencies,GraphLayout-> OptionValue[GraphLayout]];
  	vertexCoordinates = GraphEmbedding[graphForm];
  	communities = FindGraphCommunities[graphForm];
  	constants = Table[ConstantArray[colors[[i]], communities[[i]] // Length], {i, 1, communities // Length}];
  	vStyles = {#[[1]], #[[2]]} & /@ Flatten[(Transpose /@ ({communities, constants} // Transpose)), 1];
  	(*Frames*)
  	j = 0;
  	graphs = Table[
    	If[song[[i]] == "-",
     		(*True*)
     		partialTransitionFrequencies = GetTransitionsFrequenciesWithPattern[songPure[[1 ;; j]], fullTransitionFrequencies[[2]]];
     		graph = GraphTransitionsFrequenciesWithMax[partialTransitionFrequencies,
        		fullTransitionFrequencies[[1]] // Flatten // Max,
       			VertexStyle -> OptionValue[VertexStyle], 
       			VertexCoordinates -> vertexCoordinates, 
       			ImageSize -> OptionValue[ImageSize], 
       			EdgeShapeFunction -> OptionValue[EdgeShapeFunction], 
       			VertexSize -> OptionValue[VertexSize], 
       			VertexLabelStyle -> OptionValue[VertexLabelStyle]];
     			HighlightGraph[graph, Style[#[[1]], #[[2]]] & /@ vStyles]
     		,
     		(*False*)
     		j = j + 1;
     		partialTransitionFrequencies = GetTransitionsFrequenciesWithPattern[songPure[[1 ;; j]], fullTransitionFrequencies[[2]]];
     		graph = GraphTransitionsFrequenciesWithMax[partialTransitionFrequencies,
        		fullTransitionFrequencies[[1]] // Flatten // Max,
       			VertexStyle -> OptionValue[VertexStyle], 
       			VertexCoordinates -> vertexCoordinates, 
       			ImageSize -> OptionValue[ImageSize],
       			EdgeShapeFunction -> OptionValue[EdgeShapeFunction], 
       			VertexSize -> OptionValue[VertexSize], 
       			VertexLabelStyle -> OptionValue[VertexLabelStyle]];
     		graph = HighlightGraph[graph, Style[#[[1]], #[[2]]] & /@ vStyles];
     		highGraph = HighlightGraph[graph, {Style[songPure[[1 ;; j]] // Last, LightYellow]}]
    	]
    ,{i, 1, song // Length}];
  	trans = {graphs, time} // Transpose;
  	anim = Flatten[ConstantArray[#[[1]], #[[2]]] & /@ trans]
]
        
End[]
EndPackage[]



