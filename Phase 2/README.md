# :open_file_folder: Phase 2
For naming protocol within the code, please refer to the [Naming Protocol](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase%201/Naming%20Protocol.md) documentation.
## Installing EM Cmap Scoring Tool
- Please go over and click the [**EM_Cmap_Scoring_Tool_Launcher.zip**](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase%201/EM_Cmap_Scoring_Tool_Launcher.zip) "ACTUALIZAR ENLACE" at the top of this page, then clik on the *Download* option on the right side of the screen.
- Under your computer folder, right-click **EM_Cmap_Scoring_Tool_Launcher.zip** and select *Extract all*.
  - :warning: Please do not go diectly into the .zip folder
  
| <img width="563" alt="Captura de pantalla 2023-03-01 101322" src="https://user-images.githubusercontent.com/78668372/223776969-f07bc721-ec6c-4edc-beee-e0263be39050.png"> |
| :-: |
| Figure 1: .zip extraction procedure (ACTUALIZAR) |

- Open the folder and double click on the **Cmap_Scoring_Tool_Launcher** application file to run the program.
- If Windows alerts you because of the application beign unknown, please click on *More information* and then *Run anyway*.

| <img width="563" alt="Captura de pantalla 2023-03-01 101322" src="https://user-images.githubusercontent.com/78668372/224074516-2b689602-805b-48e7-affd-0149b474207b.png"> | <img width="563" alt="Captura de pantalla 2023-03-01 101322" src="https://user-images.githubusercontent.com/78668372/224074782-b8429dd4-adbf-4614-b538-6eea69e693db.png"> | 
| :-: | :-: |
| Figure 2 a): Protection window (ACTUALIZAR) | Figure 2 b)): Running the application (ACTUALIZAR) |

For future developers, the [Raw Code](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase%202/Raw%20Code) folder contains the originl .py files of this phase. For editing the raw code, please donwload the files on the [Raw Code](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase%202/Raw%20Code) folder into your computer via right-click -> *Save link as*.

## Scoring Methods 
The program receives the Cmap files as a .cxl extention that contains the different concepts listed and the connections between them. The extraction algorithm takes all the concepts and concepts linked pairs and stores them as two lists to be used for scoring calculation.
### Traditional
The number of concepts (NC) is obtained by counting all the concepts, excluding the root concept, present in the Cmap.The number of hierarchies (NH) is obtained by identifying the concepts that are connected directly to the root conept. The highest hierarchy (HH) corresponds to the hierarchy with the longest number of concepts. Lastly, the number of cross links (NCL) is obtained by counting the connections between paired concepts that are from different hierarchies.

| ![imagen](https://user-images.githubusercontent.com/78668372/229618016-94668494-1f69-418b-9535-5520c98fda32.png) | ![imagen](https://user-images.githubusercontent.com/78668372/229618225-0650527c-9952-4f7c-af26-fb7dd75c95c5.png) | ![imagen](https://user-images.githubusercontent.com/78668372/229618261-4721051f-92f2-4f9b-9fdc-54e18428638a.png) |
| :-: | :-: | :-: |
| Figure 3: EM Cmap example with number of concepts (NC) identification. | Figure 4: Number of hierarchies (NH) and highest hierarcy (HH) identification. | Figure 5: Number of interlinks (NIL) identification. |

### Categorical
The number of concepts (NC) is obtained by counting all the concepts, excluding the root concept, present in the Cmap.The number of categories (NCAT) is obtained by classifying the concepts present into each of the categories and counting the ones that contain at least one concept. For the case of Entrepreneurial Mindset (EM), the cateogries were defined by the [Word Bank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase%202/WordBank.csv) developed by the research team members. Lastly, the number of interlinks (NIL) is obtained by counting the connections between paired concepts that are from different categories.

| ![imagen](https://user-images.githubusercontent.com/78668372/229618016-94668494-1f69-418b-9535-5520c98fda32.png) | ![imagen](https://user-images.githubusercontent.com/78668372/229618225-0650527c-9952-4f7c-af26-fb7dd75c95c5.png) | ![imagen](https://user-images.githubusercontent.com/78668372/229618261-4721051f-92f2-4f9b-9fdc-54e18428638a.png) |
| :-: | :-: | :-: |
| Figure 6: EM Cmap example with number of concepts (NC) identification. | Figure 7: Number of categories (NCAT) identification. | Figure 8: Number of interlinks (NIL) identification. |

Figure 6 shows the number of concepts in the Cmap. After listing them, they are categorized (Figure 7) and finally interlinks are identified (Figure 8).
For this example, the NC will correspond to 9, NCAT will be 3, and NIL value corresponds to 2.
