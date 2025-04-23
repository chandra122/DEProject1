import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class DataVisualizer:
    def __init__(self, data_dir='rawdata'):
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / data_dir
        self.athletes_df = None
        self.medals_df = None
        self.gender_df = None

    def load_data(self):
        """Load the necessary data for visualization"""
        try:
            self.athletes_df = pd.read_csv(self.data_dir / 'Athletes.csv')
            self.medals_df = pd.read_csv(self.data_dir / 'Medals.csv')
            self.gender_df = pd.read_csv(self.data_dir / 'EntriesGender.csv')
            return self
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

    def plot_medal_distribution(self, save_path='visualizations/medal_distribution.png'):
        """Plot the distribution of medals by country"""
        if self.medals_df is None:
            raise ValueError("Medals data not loaded. Call load_data() first.")
        
        try:
            plt.figure(figsize=(12, 6))
            
            # Ensure 'Total' column exists and is numeric
            if 'Total' not in self.medals_df.columns:
                self.medals_df['Total'] = self.medals_df[['Gold', 'Silver', 'Bronze']].sum(axis=1)
            
            top_10 = self.medals_df.nlargest(10, 'Total')
            
            sns.barplot(x='NOC', y='Total', data=top_10)
            plt.title('Top 10 Countries by Total Medals')
            plt.xlabel('Country')
            plt.ylabel('Total Medals')
            plt.xticks(rotation=45)
            
            # Save the plot
            output_path = self.project_root / save_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            plt.close()
            print(f"Medal distribution plot saved to {output_path}")
        except Exception as e:
            print(f"Error creating medal distribution plot: {str(e)}")
            raise

    def plot_gender_participation(self, save_path='visualizations/gender_participation.png'):
        """Plot gender participation trends"""
        if self.gender_df is None:
            raise ValueError("Gender data not loaded. Call load_data() first.")
        
        try:
            plt.figure(figsize=(10, 6))
            
            # Calculate gender ratio
            gender_ratio = self.gender_df.groupby('Discipline').agg({
                'Female': 'sum',
                'Male': 'sum'
            }).reset_index()
            
            gender_ratio['Total'] = gender_ratio['Female'] + gender_ratio['Male']
            gender_ratio['Female_Ratio'] = gender_ratio['Female'] / gender_ratio['Total']
            
            # Plot top 10 disciplines by total participation
            top_10 = gender_ratio.nlargest(10, 'Total')
            
            sns.barplot(x='Discipline', y='Female_Ratio', data=top_10)
            plt.title('Female Participation Ratio by Discipline (Top 10)')
            plt.xlabel('Discipline')
            plt.ylabel('Female Participation Ratio')
            plt.xticks(rotation=45)
            
            # Save the plot
            output_path = self.project_root / save_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            plt.close()
            print(f"Gender participation plot saved to {output_path}")
        except Exception as e:
            print(f"Error creating gender participation plot: {str(e)}")
            raise

    def plot_athlete_characteristics(self, save_path='visualizations/athlete_stats.png'):
        """Plot athlete physical characteristics"""
        if self.athletes_df is None:
            raise ValueError("Athletes data not loaded. Call load_data() first.")
        
        try:
            plt.figure(figsize=(15, 5))
            
            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
            
            # Plot height distribution
            if 'Height' in self.athletes_df.columns:
                sns.histplot(data=self.athletes_df, x='Height', bins=30, ax=ax1)
                ax1.set_title('Athlete Height Distribution')
                ax1.set_xlabel('Height (cm)')
            else:
                ax1.set_title('Height data not available')
            
            # Plot weight distribution
            if 'Weight' in self.athletes_df.columns:
                sns.histplot(data=self.athletes_df, x='Weight', bins=30, ax=ax2)
                ax2.set_title('Athlete Weight Distribution')
                ax2.set_xlabel('Weight (kg)')
            else:
                ax2.set_title('Weight data not available')
            
            plt.tight_layout()
            
            # Save the plot
            output_path = self.project_root / save_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            plt.close()
            print(f"Athlete characteristics plot saved to {output_path}")
        except Exception as e:
            print(f"Error creating athlete characteristics plot: {str(e)}")
            raise

    def plot_correlation_heatmap(self, save_path='visualizations/correlation_heatmap.png'):
        """Plot correlation heatmap of athlete characteristics"""
        if self.athletes_df is None:
            raise ValueError("Athletes data not loaded. Call load_data() first.")
        
        try:
            # Select numeric columns
            numeric_cols = ['Age', 'Height', 'Weight']
            available_cols = [col for col in numeric_cols if col in self.athletes_df.columns]
            
            if len(available_cols) < 2:
                print("Not enough numeric columns available for correlation heatmap")
                return
            
            correlation_df = self.athletes_df[available_cols].corr()
            
            plt.figure(figsize=(8, 6))
            sns.heatmap(correlation_df, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap of Athlete Characteristics')
            
            # Save the plot
            output_path = self.project_root / save_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path)
            plt.close()
            print(f"Correlation heatmap saved to {output_path}")
        except Exception as e:
            print(f"Error creating correlation heatmap: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Example usage
        visualizer = DataVisualizer()
        visualizer.load_data()
        visualizer.plot_medal_distribution()
        visualizer.plot_gender_participation()
        visualizer.plot_athlete_characteristics()
        visualizer.plot_correlation_heatmap()
    except Exception as e:
        print(f"Error in main execution: {str(e)}") 