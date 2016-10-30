
###Summary of the pipeline
  
The functionality of APRICOT can be explained in 3 parts: program input, analysis modules and program output. 
 
####Program inputs
 
1) Query proteins that are subjected to characterization by domains and associated functional properties
2) Set of terms indicating protein domains of functional relevance. 
 
Based on these inputs, APRICOT can be executed for the analysis of the proteins of interest using the analysis modules as explained later.

####Analysis modules of APRICOT
The functionalities involved in the primary analysis are retrieval of sequences and known annotations of query proteins, collection of domains of interest from domain databases, and identification of all the functional domains in a given query.

The data obtained from the primary analysis is used as a resource for the secondary analysis, which mainly involves the selection of proteins based on the predicted domains, the calculation of the statistical and biological significance of the selected proteins to possess the function of interest by means of sequence-based features, and biological characterization of these proteins by additional annotations like subcellular localization and secondary structures. 

####Program output

For each analysis step, APRICOT generates results in tablular manner, in addition with an overview of the analysis and graphics associated with the resulting information.


###Trivia
The initial focus of this project was to identify functional domains in bacterial proteins that have the potential to interact with RNA (RNA-binding proteins or RBPs) and understand their regulatory roles and mechanisms. Hence, the tool is named **APRICOT** that stands for **A**nalysing **P**rotein **R**NA **I**nteractions by **C**ombined **O**utput **T**echnique. However, due to the adaptability of the pipeline to different sets of reference domains, APRICOT is not limited to RBP identification. The *combined output* referes to the combined scoring method of the software that uses a series of sequence based features to score the proteins predicted with the domains of interest. The pipeline has been tested successfully on the several functional classes. We are carrying out the experimental validations of few RBPs identified by APRICOT in collaboration with the biologists in our lab, which can provide a high confidence dataset and contribute significantly to the improvement of this computational approach.
 
