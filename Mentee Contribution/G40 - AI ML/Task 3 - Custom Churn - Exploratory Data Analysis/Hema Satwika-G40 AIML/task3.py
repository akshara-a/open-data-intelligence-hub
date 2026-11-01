#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[3]:


import pandas as pd

df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

df.head()


# In[4]:


df.shape


# In[5]:


df = pd.read_csv("Sample - Superstore.csv", encoding="cp1252")


# In[7]:


df.info()


# In[8]:


df.describe()


# In[9]:


#. Data Cleaning
#Missing Values
df.isnull().sum()


# In[10]:


df.duplicated().sum()


# In[11]:


df = df.drop_duplicates()


# In[13]:


df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])


# In[14]:


#4. Exploratory Data Analysis
#Category-wise Sales
df.groupby("Category")["Sales"].sum()


# In[15]:


#Region-wise Sales
df.groupby("Region")["Sales"].sum()


# In[16]:


#Segment-wise Sales
df.groupby("State")["Profit"].sum().sort_values(ascending=False).head(10)


# In[17]:


#State-wise Profit
df.groupby("State")["Profit"].sum().sort_values(ascending=False).head(10)


# In[18]:


#Top 10 Products by Sales
df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10)


# In[19]:


#5. Visualizations
#Chart 1: Sales by Category
sns.barplot(
    x=df.groupby("Category")["Sales"].sum().index,
    y=df.groupby("Category")["Sales"].sum().values
)
plt.title("Sales by Category")
plt.show()


# In[20]:


#Chart 2: Profit by Region
sns.barplot(
    x=df.groupby("Region")["Profit"].sum().index,
    y=df.groupby("Region")["Profit"].sum().values
)
plt.title("Profit by Region")
plt.show()


# In[21]:


#Chart 3: Segment Distribution
df["Segment"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%"
)
plt.title("Customer Segments")
plt.ylabel("")
plt.show()


# In[22]:


#Chart 4: Sales Distribution
sns.histplot(df["Sales"], bins=30, kde=True)
plt.title("Sales Distribution")
plt.show()


# In[23]:


#Chart 5: Discount vs Profit
sns.scatterplot(
    x="Discount",
    y="Profit",
    data=df
)
plt.title("Discount vs Profit")
plt.show()


# In[24]:


#Chart 6: Correlation Heatmap
plt.figure(figsize=(8,6))

sns.heatmap(
    df[["Sales","Profit","Quantity","Discount"]].corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Heatmap")
plt.show()


# In[ ]:


6. Final Insights
Key Business Insights
Technology category generates the highest sales.
West region contributes the highest revenue.
California is the top-performing state.
Higher discounts often reduce profit.
Consumer segment contributes the largest share of sales.
Some products generate negative profit despite high sales


# In[ ]:


7. Recommendations
Business Suggestions
Focus on Technology products.
Reduce excessive discounting.
Expand successful West region strategies.
Improve performance in low-profit regions.
Promote high-margin products.
Use targeted marketing for Consumer segment.

