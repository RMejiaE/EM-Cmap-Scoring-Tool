# 💻 Entrepreneurial Mindset Concept Map Scoring Tool
## Developers :
- Martha Lucía Cano Morales 
- Eduardo Rodríguez Mejía 
# 📃 Description
The Entrepreneurial Mindset (EM) Concept Map (Cmap) Scoring Tool allows you to score a concept map using either a Traditional or Categorical assessment method. The default root concept is set to Entrepreneurial Mindset, but it can be changed to another root concept. For the Categorical assessment, a list of categories with its associated concepts is preinstalled in the software directories to be used when assessing the concepts maps. 

For future developers, it may be worth to review the [Naming Protocol](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase%201/Naming%20Protocol.md) that was used for this project.

This project was divided into 5 phases. The files for each one are located in separated folders within this repository. 
### :file_folder:Phase 1
The objective of [Phase 1](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase%201) was to develop the Graphical User Interface (GUI) of the scoring tool. Please refer to [Phase 1](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase%201) folder for instructions on how to download and use the EM Cmap Scoring Tool in this first phase.
### :file_folder:Phase 2
The objective of [Phase 2](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase%202) was to develop the algorithm for data extraction and the algorithms for identifying the different values needed for each scoring method (see below [Theoretical Framework](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool#-theoretical-framework)). Each scoring method was implemented in a different program file to be called by the main program (GUI) according to the user selection of the scoring method. All the extracted and classified information is saved in a .csv file to be read with a spreadsheet software tool like Excel or Google Sheets. Please refer to [Phase 2](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase%202) folder for instructions on how to download and use the EM Cmap Scoring Tool in this second phase.

### :file_folder:Phase 3
### :file_folder:Phase 4
### :file_folder:Phase 5


# 📚 Theoretical Framework
![imagen](https://user-images.githubusercontent.com/78668372/222168066-8f58282b-3591-43e3-a3ed-1d50a78556a4.png)

Figure 1: Cmap example[1]
## Traditional Scoring Method
This method assigns a score based on the number of concepts (NC), the number of hierarchies (NH), the highest hierarchy (HH), and the number of cross links (NCL)between concepts.

As seen in Figure 1, the NC is the ammount of bubbles, the NH are the different paths that leave the root concept, the HH is the hierarchy containing most concepts, and the NCL are the connections between concepts of different hierarchies.

Score = (NC) + 5*(HH) + 10*(NCL)
## Categorical Scoring Method
This method first categorizes the concepts into categories and then identifies the number of categories (NC) present in the Cmap, then it calculates the number of concepts in each category to finally compute the number of categories (NCAT) that contain at least one concept. After that, it calculates the number of  connections between concepts of different categories, better known as interlinks (NIL). The score is meassure by the level of complexity (CO) of the Cmap.

CO = NC*(NIL/NCAT)

On Figure 1, each concept would be assigned a number depending on the category for the NC and NCAT calculation, and them the connection between **Foundations** and **Floor** would be checked to see if the two concepts are from different categories.
# 📑 References
1. Watson MK, Barrella E, Pelkey J. Assessment of conceptual knowledge using a component-based concept map scoring program. The International journal of engineering education. 2018;34(3):1025-1037.
