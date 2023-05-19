# :open_file_folder: Phase 3 & 4
For naming protocol within the code, please refer to the [Naming Protocol](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Naming%20protocol.md) documentation.
## :wrench: Installing EM Cmap Scoring Tool
- Please go over and click the [**EM_Cmap_Scoring_Tool_Launcher.zip**](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_3_4/EM_Cmap_Scoring_Tool_Launcher.zip) at the top of this page, then clik on the *Download* option on the right side of the screen.
- Under your computer folder, right-click **EM_Cmap_Scoring_Tool_Launcher.zip** and select *Extract all*.
  - :warning: Please do not go diectly into the .zip folder
  
| ![imagen](https://user-images.githubusercontent.com/78668372/233404342-ba3c8d10-e2c7-437e-a0da-82f20dab5c04.png) |
| :-: |
| Figure 1: .zip extraction procedure |

- Open the resuting folder after the extraction and double click on the **Cmap_Scoring_Tool_Launcher** application file to run the program (Figure 2).

| ![imagen](https://user-images.githubusercontent.com/78668372/230093790-764e3e18-1c3c-4f5b-88ff-1b8e95e21c47.png) |
| :-: |
| Figure 2: Launch program |

- If Windows alerts you because of the application beign unknown, please click on *Run anyway* or *More information* and then *Run anyway*

| <img src="https://user-images.githubusercontent.com/78668372/229847812-d8e15832-8819-401c-af6d-07d6c938bb0a.png" width=50% height=60%> |
| :-: |
| Figure 3: Protection window |

For future developers, the [Raw Code](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_3_4/Raw%20code) folder contains the originl .py files of this phase. For editing the raw code, please donwload the files on the [Raw Code](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/tree/main/Phase_3_4/Raw%20code) folder into your computer via right-click -> *Save link as*.

## 📋 Wordbank update
The Wordbank file was updated to have only one concept per cell for the test performed.
The updated version can be seen in [Wordbank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_3_4/WordBank.csv) under this phase folder.
## 🔮 Manual Categorization Graphical User Interface (GUI)
The manual categorization GUI presents the user the information of the concepts that did not have any category becuase they are not present in the [Wordbank](https://github.com/RMejiaE/EM-Cmap-Scoring-Tool/blob/main/Phase_3_4/WordBank.csv) file. In this interface, the concepts are presented in the first column, the pre assigned category based on the implemented algorithm, and a dropdown menu. The drop down menu is set by default to the pre assigned category, but the user can choose another category if they find it more appropriate.

| ![imagen](https://user-images.githubusercontent.com/78668372/239608086-5f552523-32ec-4c0c-8c35-85ca7c3b10aa.png) |
| :-: |
| Figure 4: Manual categrization GUI. |

The options for the manual categorization GUI are *Accept all assignement* and *Reject all assignements and leave all concepts in "No category"*.
- If the user would like to leave the concepts in the pre assigned categories or manually select a category for one or more concepts, the *Actions* menu should be left in *Accept all assignements*. For a  manual selection, the user must choose the desired category from the dropdown menu for the categories that they want to change and finally click on *Continue*.
- If the user would like to leave the concepts in *"No category"*, the *Actions* menu should be switched to *Reject all assignements and leave all concepts in "No category"*. Finally, the user must click on *Continue*

After clicking *Continue*, the program will either present the next Cmap for manual categorization or end the execution, and present the message window indicating that the categorical scoring was performed succesfully.
