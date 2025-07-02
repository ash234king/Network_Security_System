import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv("Network_Data\phisingData.csv")
print(len(df.columns))
## so in this data we are having 30 features

print(df.info())
## all the columns are of int types
print(df.isnull().sum())
## the data is having no null values

## 1 denotes all good
## -1 denotes phishing
## 0 denotes suspicious


for col in df.columns:
    print(f"{col} : {df[col].unique()}")

## so out of all columns URL_Length , double_slash_redirecting, having_sub_domain, SSLfinal_state, URL_of_Anchor and Links_in _tags, SFH, web_traffic, Links_pointing_to_page are having values as 1,0 or -1 
## and rest all are having 1 or -1

## heatmap
palette={
    1:"red",
    -1:"green",
}
sns.pairplot(df[['URL_Length', 'having_Sub_Domain', 'SSLfinal_State', 'web_traffic', 'Result']],hue='Result',palette=palette)
plt.show()

## correlation
plt.figure(figsize=(24,20))
corr=df.corr()
sns.heatmap(corr,annot=True,cmap='plasma')
plt.show()
## The result that whether the site is phishing or not is mostly dependent on two features URL_of_Anchor and SSLfinal_state

## url_length analysis
counter=df['URL_Length'].value_counts()
labels=counter.index
values=counter.values

fig,ax=plt.subplots(1,2,figsize=(12,6))

sns.barplot(x=labels,y=values,ax=ax[0],palette=["green","red","yellow"])
ax[0].set_title("Bar chart of URL_Length")
ax[0].set_xlabel("Class")
ax[0].set_ylabel("Counts")
ax[1].pie(values,labels=labels,explode=(0,0.05,0.2),colors=["green","red","yellow"],autopct='%1.1f%%')
ax[1].set_title("Pie chart for URL_Length")

##Insights
## In URL_Length -1 is apperaing most off the times i.e 81 % and 1 is appearing 17.7% and 0 is  1.2% 


plt.tight_layout()
plt.show()

## SSLfinal_state
counter=df['SSLfinal_State'].value_counts()
labels=counter.index
values=counter.values
fig,ax=plt.subplots(1,2,figsize=(12,6))
ax[0].pie(values,labels=labels,explode=(0,0.05,0.02),colors=["green","red","yellow"],autopct='%1.1f%%')
ax[0].set_title("Pie chart for SSLfinal_State")

sns.histplot(df['SSLfinal_State'].head(1000),ax=ax[1],kde=True)
ax[1].set_title("Histplot for SSLfinal_State")
ax[1].set_xlabel("Class")
ax[1].set_xlabel("Counts")
plt.tight_layout()
plt.show()

##Insights
## In the SSLfinal_State the
## 1 is 57.3%
## 0 is 10.6%
## -1 is 32.2%


## URL_of_Anchor
counter=df['URL_of_Anchor'].value_counts()
labels=counter.index
values=counter.values

fig,ax=plt.subplots(1,2,figsize=(12,6))

ax[0].pie(values,labels=labels,explode=(0,0.05,0.2),colors=["green","red","yellow"],autopct='%1.1f%%')
ax[0].set_title("Pie chart for URL_of_Anchor")

sns.histplot(df['URL_of_Anchor'].head(1000),ax=ax[1],kde=True)
ax[1].set_title("Histplot for URL_of_Anchor")
ax[1].set_xlabel("Class")
ax[1].set_xlabel("Counts")
plt.tight_layout()
plt.show()

##Insights
## In the URL_of_Anchor the
## 1 is 22%
## 0 is 48.3%
## -1 is 29.7%

## URL_of_Anchor
counter=df['Result'].value_counts()
labels=counter.index
values=counter.values

fig,ax=plt.subplots(1,2,figsize=(12,6))

ax[0].pie(values,labels=labels,explode=(0,0.05),colors=["red","yellow"],autopct='%1.1f%%')
ax[0].set_title("Pie chart for Result")

sns.histplot(df['Result'].head(1000),ax=ax[1],kde=True)
ax[1].set_title("Histplot for Result")
ax[1].set_xlabel("Class")
ax[1].set_xlabel("Counts")
plt.tight_layout()
plt.show()

##Insights
## The Results of the sites are given as : -
## 1 is 55.7 %
## -1 is 44.3%



###Box Plots
fig,ax=plt.subplots(1,3,figsize=(24,20))
sns.boxplot(x='URL_of_Anchor', y='web_traffic', data=df,ax=ax[0])
sns.boxplot(x='SSLfinal_State', y='web_traffic', data=df,ax=ax[1])
sns.boxplot(x='Result', y='web_traffic', data=df,ax=ax[2])
plt.tight_layout()
plt.show()
##Insights
## when median at 0 then traffic is balanced 
## when median is around -1  then we have more consistent traffic
## when median is greater than 0  then we have higher traffic


##violinplots
sns.violinplot(y=df['SSLfinal_State'],color='pink')
plt.title('Distribution of SSLfinal_State')
plt.show()
##Insights 
## most of the sites given are 1 i.e valid      because the stretch is more at 1

sns.violinplot(y=df['URL_of_Anchor'],color='red')
plt.title('Distribution of URL of anchor')  
plt.show()
##Insights 
## most of the sites given are 0 i.e suspicious      because the stretch is more at 0

sns.violinplot(y=df['URL_Length'],color='purple')
plt.title('Distribution of URL length')
plt.show()
##Insights
## most of the sites given are -1 i.e  not valid      because the stretch is more at -1
## for 0 it is not that much compared to -1 and 1
