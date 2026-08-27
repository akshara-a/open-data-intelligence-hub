**Olympic Athlete Events Dataset Analysis Report**


**1. Project Title**


Exploratory Data Analysis of Olympic Athlete Events Dataset


**2. Objective**


The objective of this project is to analyze historical Olympic athlete data to discover trends, patterns, and insights related to athlete participation, demographics, sports popularity, and medal achievements.


**3. Dataset Information**
Item	Value
Dataset Name	Olympic Athlete Events
File Format	CSV
Records	271,116 (before cleaning)
Features	15 Columns
Source	Olympic Athlete Events Dataset
Domain	Sports Analytics
Columns Included
ID
Name
Sex
Age
Height
Weight
Team
NOC
Games
Year
Season
City
Sport
Event
Medal

**4. Data Cleaning Process**


Several preprocessing techniques were applied to improve data quality.

Missing Value Handling
Column	Action
Name	Filled with "Unknown"
Age	Median Imputation
Height	Median Imputation
Weight	Median Imputation
ID	Rows removed if missing
Duplicate Handling
Duplicate records identified and removed.
Text Standardization
Removed leading/trailing spaces.
Standardized medal values.
Converted categorical text to consistent formatting.
Data Type Conversion

Converted the following columns to numeric:

ID
Age
Height
Weight
Year
Column Renaming

Converted all column names to:

Lowercase
Underscore-separated format

Example:

Height → height

Weight → weight

**5. Exploratory Data Analysis (EDA)**

5.1 Summary Statistics

Key numerical statistics were generated for:

Age
Height
Weight
Year

Insights:

Athlete age varies significantly across sports.
Height and weight distributions indicate different physical requirements among sports.
Participation spans more than a century of Olympic history.
5.2 Sport Participation Analysis

The frequency count of athletes by sport was calculated.

Key Findings
Athletics had the highest participation.
Swimming ranked among the most popular sports.
Team sports generally showed larger athlete counts.
5.3 Medal Analysis

Medal categories analyzed:

Gold
Silver
Bronze
No Medal
Findings
Majority of athletes participated without winning medals.
Gold medal winners represent a small percentage of total athletes.
5.4 Gender Distribution

Analysis performed using the Sex column.

Findings
Male athletes historically outnumber female athletes.
Female participation has increased significantly in recent Olympics.

**6. Filtering Analysis**

Gold Medalists

Filtered athletes who won Gold medals.

Insights:

Gold medal winners represent elite performers across multiple sports.
Athletes Older Than 30

Analyzed experienced athletes.

Insights:

Sports such as shooting and equestrian events contain older athletes.
Physically demanding sports tend to have younger participants.
Female Athletes

Examined participation trends.

Insights:

Female participation has steadily increased over time.
Certain sports show stronger female representation.
Indian Athletes

Filtered using:

noc == "IND"

Insights:

Strong participation in Hockey, Shooting, Wrestling, and Athletics.
Increased representation observed in recent Olympic years.

**7. Grouping and Aggregation Analysis**

Sport-wise Aggregation

Calculated:

Athlete Count
Average Age
Minimum Age
Maximum Age
Findings

Different sports exhibit unique athlete age profiles:

Gymnastics → younger athletes
Equestrian → older athletes
Sport and Gender Analysis

Grouped by:

Sport
Sex

Metrics:

Athlete Count
Average Age
Average Height
Average Weight
Findings
Male athletes generally have higher average height and weight.
Significant physical differences exist across sports.

**8. Feature Engineering**

Age Group Classification

Athletes categorized into:

Age Range	Group
≤18	Teen
19–30	Young Adult
31–45	Adult
46–60	Middle Age
>60	Senior
Findings

Most Olympic athletes belong to the Young Adult category.

BMI Calculation

Formula:

BMI = Weight / Height²

Insights
Sports requiring endurance show lower average BMI.
Strength sports generally have higher BMI values.
Medal Status

Created a new feature:

Winner
Participant

This simplified medal analysis.

Olympic Era Classification

Athletes grouped into:

Era	Years
Early Olympics	Before 1950
Modern Olympics	1950–1999
Recent Olympics	2000+
Findings

Participation increased dramatically during the Recent Olympics era.

**9. Visualization Analysis**

Chart 1: Top 10 Sports by Participation

Insights:

Athletics dominates participation.
Swimming consistently ranks among top sports.
Team sports attract large numbers of competitors.
Chart 2: Age Distribution Histogram

Insights:

Most athletes are between 20 and 30 years old.
Very young and very old athletes are relatively rare.
Chart 3: Olympic Participation Trend

Insights:

Participation has grown steadily over the decades.
Modern Olympics attract significantly more athletes than earlier editions.

**10. Correlation Analysis**

Numerical Features Studied
Age
Height
Weight
Year
BMI
Correlation Heatmap Findings
Strong Positive Correlation
Height ↔ Weight

Taller athletes tend to weigh more.

Weak Correlation
Age ↔ Height
Age ↔ Weight

Age has limited influence on body measurements.

Time Trend
Year shows slight relationships with athlete characteristics, indicating evolving participation patterns over time.

**11. Key Insights**

Athletics is the most participated Olympic sport.
Most athletes are aged between 20–30 years.
Male athletes historically outnumber female athletes.
Olympic participation has increased significantly over time.
Height and weight show strong positive correlation.
Most participants do not win medals.
Young Adult athletes dominate Olympic competitions.
Different sports exhibit distinct physical profiles.

**12. Conclusion**

The Olympic Athlete Events dataset provides valuable insights into athlete demographics, participation trends, and performance characteristics across Olympic history. Through data cleaning, feature engineering, visualization, and correlation analysis, the project successfully identified meaningful patterns in athlete participation, age distribution, gender representation, and sports popularity. These insights can support sports analytics, athlete performance studies, and future Olympic research.

Tools Used
Python
Pandas
NumPy
Matplotlib
Seaborn
Techniques Used
Data Cleaning
Missing Value Treatment
Duplicate Removal
Feature Engineering
Grouping & Aggregation
Data Visualization
Correlation Analysis
Exploratory Data Analysis (EDA)