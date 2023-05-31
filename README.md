# 💻 Entrepreneurial Mindset Concept Map Scoring Tool
## Developers :
- Martha Lucía Cano Morales 
- Eduardo Rodríguez Mejía 
# 📃 Description
The Entrepreneurial Mindset (EM) Concept Map (Cmap) Scoring Tool allows you to score a concept map using either a Traditional or Categorical assessment method. The default root concept is set to Entrepreneurial Mindset, but it can be changed to another root concept. For the Categorical assessment, a list of categories, or [Word Bank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_2/WordBank.csv), with its associated concepts is preinstalled in the software directories to be used when assessing the concepts maps. Additional categories and/or concepts can be added to the Word Bank following the proposed [Word Bank structure](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Structure%20of%20the%20WordBank.md)

For future developers, it may be worth to review the [Naming Protocol](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Naming%20protocol.md) that was used for this project.

This project was divided into 5 phases. The files for each one are located in separated folders within this repository. 
### :file_folder:Phase 1
The objective of [Phase 1](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_1) was to develop the Graphical User Interface (GUI) of the scoring tool. Please refer to [Phase 1](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_1) folder for instructions on how to download and use the EM Cmap Scoring Tool in this first phase.
### :file_folder:Phase 2
The objective of [Phase 2](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_2) was to develop the algorithm for data extraction and the algorithms for identifying the characteristic values for each scoring method (see below [Theoretical Framework](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool#-theoretical-framework)).

The main program (GUI) calls a program file (score_trad or score_cat) according to the scoring method selected by the user. The extracted and classified information is saved in a .csv file that can be read with a spreadsheet software tool (such as Excel or Google Sheets) or with a plain text reader. Please refer to [Phase 2](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_2) folder for instructions on how to download and use the EM Cmap Scoring Tool of this second phase.


### :file_folder:Phase 3 & 4
The objective of [Phase 3 & 4](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_3_4) was to develop the Graphical User Interface (GUI) to allow the user for manual categorization of the concepts that were not found in the Wordbank after the categorical method was run.

The Manual categorization GUI appears for every file that was uploaded to be scored and allows the user to view the preassigned category, change it, or reject all assignations and leave the concepts under "No category". Please refer to [Phase 3 & 4](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_3_4) folder for instructions on how to download and use the EM Cmap Scoring Tool of these phases.


### :file_folder:Phase 5


# 📚 Theoretical Framework
![imagen](https://user-images.githubusercontent.com/78668372/222168066-8f58282b-3591-43e3-a3ed-1d50a78556a4.png)

Figure 1: Cmap example[1]
## Traditional Scoring Method
This method assigns a score based on the number of concepts (NC), the number of hierarchies (NH), the highest hierarchy (HH), and the number of cross links (NCL) between concepts.

As seen in Figure 1, the NC is the ammount of bubbles, the NH are the different paths that leave the root concept, the HH is the hierarchy containing most concepts, and the NCL are the connections between concepts of different hierarchies.

Score = (NC) + 5*(HH) + 10*(NCL)
## Categorical Scoring Method
This method identifies the number of concepts (NC) present in the Cmap, then classifies the concepts into categories, and lastly, it calculates the number of concepts in each category to finally compute the number of categories (NCAT) that contain at least one concept. After that, it calculates the number of  connections between concepts of different categories, better known as interlinks (NIL). The score is meassure by the level of complexity (CO) of the Cmap.

CO = NC*(NIL/NCAT)

On Figure 1, each concept would be assigned a number depending on the category for the NC and NCAT calculation, and them the connection between **Foundations** and **Floor** would be checked to see if the two concepts are from different categories.
# 📑 References
1. Watson MK, Barrella E, Pelkey J. Assessment of conceptual knowledge using a component-based concept map scoring program. The International journal of engineering education. 2018;34(3):1025-1037.
