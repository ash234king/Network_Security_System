import os
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
from networksecurity.exception.exception import NetworkSecurityException

sns.set_theme(style="whitegrid")

class EDAProcessor:
    def __init__(self,df:pd.DataFrame,output_dir:str="static/eda_outputs"):
        self.df=df.head(50)
        self.output_dir=output_dir
        os.makedirs(self.output_dir,exist_ok=True)
    def generate_bar_plot(self):
        try:
            for col in self.df.select_dtypes(include='number').columns[:1]:
                plt.figure(figsize=(6,4))
                self.df[col].value_counts().plot(kind='bar', color='skyblue')
                plt.title(f"Bar chart of {col}")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, "bar_chart.png"))
                plt.close()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def generate_pie_chart(self):
        try:
            for col in self.df.select_dtypes(include='number').columns[:1]:
                plt.figure(figsize=(6,6))
                self.df[col].value_counts().plot.pie(autopct='%1.1f%%')
                plt.ylabel('')
                plt.title(f"Pie Chart of {col}")
                plt.tight_layout()
                plt.savefig(os.path.join(self.output_dir, "pie_chart.png"))
                plt.close()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def generate_frequency_chart(self):
        try:
            for col in self.df.select_dtypes(include='number').columns[:1]:
                sns.histplot(self.df[col], kde=True, color='orange')
                plt.title(f"Frequency Chart of {col}")
                plt.tight_layout()
                plt.savefig(f"{self.output_dir}/frequency_chart.png")
                plt.close()
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def generate_corr_heatmap(self):
        try:
            plt.figure(figsize=(10, 8))
            corr = self.df.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
            plt.title("Correlation Matrix")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, "correlation_heatmap.png"))
            plt.close()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def generate_violin_plots(self):
        try:
            for col in self.df.select_dtypes(include='number').columns[:1]:
                plt.figure(figsize=(6, 4))
                sns.violinplot(y=self.df[col], color='purple')
                plt.title(f"Violin Plot of {col}")
                plt.tight_layout()
                filepath = os.path.join(self.output_dir, "violin_plot.png")
                plt.savefig(filepath)
                plt.close()
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def generate_box_plots(self):
        try:
            for col in self.df.select_dtypes(include='number').columns[:1]:
                plt.figure(figsize=(6, 4))
                sns.boxplot(y=self.df[col], color='green')
                plt.title(f"Box Plot of {col}")
                plt.tight_layout()
                filepath = os.path.join(self.output_dir, f"box_plot.png")
                plt.savefig(filepath)
                plt.close()
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_all(self):
        self.generate_bar_plot()
        self.generate_pie_chart()
        self.generate_frequency_chart()
        self.generate_box_plots()
        self.generate_corr_heatmap()
        self.generate_violin_plots()