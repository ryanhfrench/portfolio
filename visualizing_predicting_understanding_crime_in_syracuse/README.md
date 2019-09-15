# Visualizing, Predicting, & Understanding Crime in Syracuse
## Utilizing R

### Summary
As an avid gamer when I discovered the Video Game Sales dataset on Kaggle (https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings) I was excited to see what different forms of visualizations I could create. In regards to the overall presentation, I wanted to embrace the culture of video games from a stylistic point of view and opted for a retro-themed color scheme and image style.

### Poster
![Poster](poster_image.png)

### Files
**resources:** The folder that holds the resources for the poster accents and the wordcloud. </br>
**visualizations:** The folder that holds the visualization outputs from the R script. </br>
**Video_Games_Sales.csv:** Data on the video game industry sales for the last 30 years. </br>
**code.R:** The Script for importing, cleaning, and munging the data from </br> *Video_Games_Sales_as_at_22_Dec_2016.csv* as well as building the visualizations programmatically. </br>
**poster.pdf:** The final completed poster from Adobe Illustrator. </br>
**poster_image.png:** An image of the poster to be displayed on GitHub. </br>
**poster_project.ai:** The Adobe Illustrator project file for further processing of the visualizations generated in R. </br>

### Attributes
#### As represented in the MySQL database and Tableau dashboard, definitions provided by Spotify  
**ADDRESS:** The address at which the crime occurred, scaled to the block level for anonymization purposes. *(string)* <br/>
**Arrest:** Whether or not an arrest occurred. *(string)* <br/>    
**Attempt:** Whether a crime was completed or merely attempted. *(string)* <br/>   
**CODE DEFINED:** The code associated with the type of crime (LARCENY, ROBBERY, AGRIVATED ASSAULT, etc). *(string)* <br/>     
**DATE:** The date on which the crime was reported. *(datetime)* <br/>     
**DRNUMB:** The unique ID for each instance of crime reported. *(int)* <br/>    
**FID:** The unique ID for each row in the data from the repository. *(int)* <br/>   
**LarcenyCode:** The location at which the Larceny took place (From Mailbox, From Building, From Motor Vehicle). *(string)* <br/>       
**TIMEEND:** The time at which responding to the crime ended. *(int)* <br/>  
**TIMESTART:** The time at which the crime was first reported. *(int)* <br/>   
