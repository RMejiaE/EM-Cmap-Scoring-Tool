# Entrepreneural Mindset Concept Map Scoring Tool
## Developers
- Martha Lucía Cano Morales
- Eduardo Rodríguez Mejía
# Description
The Entrepreneurial Mindset (EM) Concept Map (Cmap) Scoring Tool will allow you to score a concept map base on either a Traditional or Categorical assessment method. The Concept EM is the default option for the tool, and a list of categories with its associated concepts is preinstalled in the software directories for the addecuate comparisons and calculations.
# Theoretical Framework
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
# References
1. Watson MK, Barrella E, Pelkey J. Assessment of conceptual knowledge using a component-based concept map scoring program. The International journal of engineering education. 2018;34(3):1025-1037.
