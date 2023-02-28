# EM-Cmap-Scoring-Tool
![imagen](https://user-images.githubusercontent.com/78668372/221963257-b3bbdacd-f424-4e56-be69-029b855b9072.png)
Repository containing the design documents and results for the Entrepreneurial Mindset Scoring Tool
## Developers
- Martha Lucía Cano Morales
- Eduardo Rodríguez Mejía
# How to Use the EM Cmap Scoring Tool
## Download the *Cmap_Scoring_Tool_Launcher.zip* file and then:
1. Extract it on your computer.
2. Open the *Cmap_Scoring_Tool_Launcher* folder
3. Run the **Cmap_Scoring_Tool_Launcher** executable file.
## Before going to the EM Cmap Scoring Tool
### Please open "Cmap Tools" and check the following:
- Check for misspellings via *Tools* -> *Spelling...*.

![imagen](https://user-images.githubusercontent.com/78668372/221964846-c655a7e2-d452-4543-b340-7428eea1434c.png)
- Check for hierarchical structure via *Format* -> *Autolayout*.

![imagen](https://user-images.githubusercontent.com/78668372/221965003-987d1b4c-d158-44f0-8a19-e9336c4b3551.png)
- Check that all concepts are in a concept bubble in one line.
	- The spelling should be the same throughout the maps that will be scored.
- Save the revised Cmaps as .cxl files via *File* -> *Export Cmap As* -> *CXL File...*.

![imagen](https://user-images.githubusercontent.com/78668372/221965129-f3d74c2d-c51c-4df2-8f51-24a8bd7a3c41.png)
## Using EM Cmap Scoring Tool:
### With the **EM Cmap Scoring Tool** runing
1. Select the scoring method. You can choose either **Traditional** or **Categorical**.

![imagen](https://user-images.githubusercontent.com/78668372/221965609-60028709-4a5a-4210-aa15-98f0a5f1c451.png)

2. Write down the root concept that will be used as the starting node for the calculations.
![imagen](https://user-images.githubusercontent.com/78668372/221965860-63296871-9595-4361-8268-8bd398952d6a.png)
3. Select the .cxl files for scoring.
![imagen](https://user-images.githubusercontent.com/78668372/221965947-a66c685b-1698-4db5-bb8e-8329a9206087.png)
![imagen](https://user-images.githubusercontent.com/78668372/221966966-51ff35f5-2ae9-4d29-984a-7f825f888fee.png)
4. Select the path for the results report and rename the file if you wish to. Results will be exported as .CVS.
![imagen](https://user-images.githubusercontent.com/78668372/221967024-b1dba369-0870-4922-a08e-3a0583c78603.png)
![imagen](https://user-images.githubusercontent.com/78668372/221967154-3c928bfc-49c7-405f-a1f1-37006ab02380.png)
5. Click the "Run" button and then open the results report.
![imagen](https://user-images.githubusercontent.com/78668372/221967275-ff384e7b-64ff-41aa-8f13-d844ca9d9717.png)
# Description:
The following repository contains the documentation and the codes for running and working with the EM Cmap Scoring Tool.
##  Conception
Here you will find the requirements for the sotfware and the functional block diagram of the solution.
## Planning
Here you will find the different codes for each of the block presented in the functional block diagram.
### Graphical User Interface (GUI)
The code for the main interface with the user. It allows the user to choose from two scoring methods (i.e., traditional or categorical), write down a root concept, file selection, and a path selection to save the results.
It also includes a *Help*, *Run*, and *Exit* buttons.
### Scoring Methods
Each scoring method will run independently under the GUI and will generate a *ScoringResult* file in the path selected by the user.
