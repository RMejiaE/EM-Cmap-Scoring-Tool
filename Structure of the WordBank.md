# :bridge_at_night:Structure of the WordBank

The new structure of the [WordBank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_2/WordBank.csv) was defined by rows. Each category or subcategory with the words that belongs to it must occupy one single row (Figure 9). This row structure was defined because the programming libraries manage data in files as natural language does, from left to right. 

The previous structure of the Word Bank in the Excel File “2022-July Word Banks.xslx” was defined in columns, each Subcategory and the words that belonged to it occupied one column and each category encompassed several columns. To read this structure with the Python File library would had implied complicated algorithms. It was simpler to change the structure of the Word Bank file.

| ![imagen](https://user-images.githubusercontent.com/78668372/231847521-a5610fa5-086c-4dc7-b747-6f6cd5564cad.png) |
| :-: |
| Figure 9: New structure for the [WordBank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_2/WordBank.csv) |

In the new [WordBank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_2/WordBank.csv) structure each Category or Subcategory row must have the following elements:
1.	The first cell has the identifier number of the category to which the subcategory belongs. If the row corresponds to a Category instead of a Subcategory, this number will correspond to the identifier number of the Category itself.
2.	The second cell has the identifier number of the Subcategory. If the row corresponds to a Category instead of a Subcategory. This cell will have the identifier of the Category itself. 
3.	The third cell has the name of the Category or Subcategory. Note: the name in this cell is also included when the code searches for a concept within the word bank.
4.	The following cells include all the concepts in that category. Concepts can have more than one word. Each concept has to occupy one cell. Each row can have as many concepts as needed.  If a Category has no concepts directly related to it, but only through subcategories, these cells can be empty.  
