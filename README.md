##APRICOT
A tool to explore functional classes of proteins.

**APRICOT** is a computational pipeline for the identification of specific functional classes of interest in large protein sets. The pipeline uses efficient sequence-based algorithms and predictive models like signature motifs of protein families for the characterization of user-provided query proteins with specific functional features. The dynamic framework of APRICOT allows the identification of unexplored functional classes of interest in the large protein sets or the entire proteome.

###Introduction

The initial focus of this project was to identify functional domains in bacterial proteins that have the potential to interact with RNA and understand their regulatory roles and mechanisms, therefore it was named as **APRICOT** (stands for **A**nalysing **P**rotein **R**NA **I**nteractions by **Co**mbined-scoring **T**echniques). RNA-binding proteins (RBPs) have been widely investigated for their properties as post-transcriptional regulators. Several studies have been carried out using experimental techniques such as cross-linking and co-immunoprecipitation experiments, which have enabled the characterization of RNA-binding domains (RBDs) and their regulatory roles. Such large-scale screening studies are technically challenging and costly, and so far performed only on the human and yeast data. Here we introduce APRICOT, a computational pipeline for the large-scale sequence-based identification and characterization of RBPs using RNA-binding signature motifs and RBD models obtained from experimental studies. The pipeline includes tools that are built upon RPS-BLAST and HMMER3 to predict functional domains in protein sequences by querying Position Specific Scoring Matrices and Hidden Markov Models of the functional domains. It carries out an extensive annotation of the predicted motifs by a series of sequence-based features and statistically scores them. Subsequently, the RBPs are identified if the predicted domains share significant similarities with their corresponding references. The efficiency and adaptability of the APRICOT analysis pipeline is demonstrated by achieving an average sensitivity of 0.92 and average accuracy of 0.91 on various benchmark and large-scale datasets, including full proteome sets of human and Escherichia coli.

Due to the flexible choice of reference predictive models, several proteins of known classes are being tested by this computational pipeline. We are also carrying out experimental validations in collaboration with the biologists in our lab, which can contribute significantly to the improved functional characterization of the query proteins by APRICOT.  

###Authors and Contributors

The tool is designed and developed by Malvika Sharan @malvikasharan in the lab of Prof. Dr. Jörg Vogel in the Institute for Molecular Infection Biology at the University of Würzburg. Dr. Konrad Förstner @konrad contributed to the project by providing important technical supervision and discussions. The authors are grateful to Prof. Thomas dandekar, Dr. Ana Eulalio, Dr. Charlotte Michaux and Caroline Taouk for critical discussions and feedback.

###Documentation

The documentation is under preparation.


