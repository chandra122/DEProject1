import pandas as pd
import numpy as np
from pathlib import Path
import os

class DataProcessor:
    def __init__(self, data_dir='rawdata'):
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent.parent
        self.data_dir = self.project_root / data_dir
        self.athletes_df = None
        self.teams_df = None
        self.medals_df = None
        self.coaches_df = None
        self.gender_df = None

    def load_data(self):
        """Load all CSV files into pandas DataFrames"""
        try:
            # Load athletes data
            self.athletes_df = pd.read_csv(self.data_dir / 'Athletes.csv')
            print("Athletes data loaded. Columns:", self.athletes_df.columns.tolist())
            
            # Load other data
            self.teams_df = pd.read_csv(self.data_dir / 'Teams.csv')
            print("Teams data loaded. Columns:", self.teams_df.columns.tolist())
            
            self.medals_df = pd.read_csv(self.data_dir / 'Medals.csv')
            print("Medals data loaded. Columns:", self.medals_df.columns.tolist())
            
            self.coaches_df = pd.read_csv(self.data_dir / 'Coaches.csv')
            print("Coaches data loaded. Columns:", self.coaches_df.columns.tolist())
            
            self.gender_df = pd.read_csv(self.data_dir / 'EntriesGender.csv')
            print("Gender data loaded. Columns:", self.gender_df.columns.tolist())
            
            return self
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

    def clean_athletes_data(self):
        """Clean and preprocess athletes data"""
        if self.athletes_df is None:
            raise ValueError("Athletes data not loaded. Call load_data() first.")
        
        try:
            # Basic cleaning
            self.athletes_df = self.athletes_df.drop_duplicates()
            
            # Drop the unnamed index column if it exists
            if self.athletes_df.columns[0] == 'Unnamed: 0':
                self.athletes_df = self.athletes_df.drop('Unnamed: 0', axis=1)
            
            # Ensure required columns exist
            required_cols = ['Name', 'NOC', 'Discipline']
            missing_cols = [col for col in required_cols if col not in self.athletes_df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns in athletes data: {missing_cols}")
            
            print("Athletes data cleaned")
            return self
        except Exception as e:
            print(f"Error cleaning athletes data: {str(e)}")
            raise

    def clean_medals_data(self):
        """Clean and preprocess medals data"""
        if self.medals_df is None:
            raise ValueError("Medals data not loaded. Call load_data() first.")
        
        try:
            # Basic cleaning
            self.medals_df = self.medals_df.drop_duplicates()
            
            # Drop the unnamed index column if it exists
            if self.medals_df.columns[0] == 'Unnamed: 0':
                self.medals_df = self.medals_df.drop('Unnamed: 0', axis=1)
            
            # Rename Team/NOC to NOC for consistency
            if 'Team/NOC' in self.medals_df.columns:
                self.medals_df = self.medals_df.rename(columns={'Team/NOC': 'NOC'})
            
            # Convert medal counts to numeric
            medal_columns = ['Gold', 'Silver', 'Bronze', 'Total']
            for col in medal_columns:
                if col in self.medals_df.columns:
                    self.medals_df[col] = pd.to_numeric(self.medals_df[col], errors='coerce')
                    self.medals_df[col] = self.medals_df[col].fillna(0)
                else:
                    print(f"Warning: Column '{col}' not found in medals data")
            
            print("Medals data cleaned")
            return self
        except Exception as e:
            print(f"Error cleaning medals data: {str(e)}")
            raise

    def clean_teams_data(self):
        """Clean and preprocess teams data"""
        if self.teams_df is None:
            raise ValueError("Teams data not loaded. Call load_data() first.")
        
        try:
            # Basic cleaning
            self.teams_df = self.teams_df.drop_duplicates()
            
            # Drop the unnamed index column if it exists
            if self.teams_df.columns[0] == 'Unnamed: 0':
                self.teams_df = self.teams_df.drop('Unnamed: 0', axis=1)
            
            print("Teams data cleaned")
            return self
        except Exception as e:
            print(f"Error cleaning teams data: {str(e)}")
            raise

    def merge_datasets(self):
        """Merge relevant datasets for analysis"""
        if any(df is None for df in [self.athletes_df, self.teams_df, self.medals_df]):
            raise ValueError("Required datasets not loaded. Call load_data() first.")
        
        try:
            # Print column names for debugging
            print("Athletes columns:", self.athletes_df.columns.tolist())
            print("Teams columns:", self.teams_df.columns.tolist())
            print("Medals columns:", self.medals_df.columns.tolist())
            
            # Clean teams data before merging
            self.clean_teams_data()
            
            # Merge athletes with teams
            merged_df = pd.merge(
                self.athletes_df,
                self.teams_df,
                on=['NOC', 'Discipline'],
                how='left'
            )
            
            # Merge with medals
            merged_df = pd.merge(
                merged_df,
                self.medals_df,
                on=['NOC'],
                how='left'
            )
            
            # Fill missing medal values with 0
            medal_columns = ['Gold', 'Silver', 'Bronze', 'Total']
            for col in medal_columns:
                if col in merged_df.columns:
                    merged_df[col] = merged_df[col].fillna(0)
            
            print("Datasets merged successfully")
            return merged_df
        except Exception as e:
            print(f"Error merging datasets: {str(e)}")
            raise

    def prepare_for_ml(self, merged_df):
        """Prepare data for machine learning"""
        try:
            # Print available columns for debugging
            print("Available columns:", merged_df.columns.tolist())
            
            # Select features for ML
            features = ['NOC', 'Discipline']
            
            # Ensure all required features exist
            available_features = [col for col in features if col in merged_df.columns]
            if not available_features:
                raise ValueError("No valid features found for ML")
            
            print("Using features:", available_features)
            
            # Create target variable (whether athlete won a medal)
            if 'Total' in merged_df.columns:
                merged_df['Won_Medal'] = merged_df['Total'].apply(lambda x: 1 if x > 0 else 0)
            else:
                raise ValueError("'Total' column not found for creating target variable")
            
            # One-hot encode categorical variables
            ml_df = pd.get_dummies(merged_df[available_features])
            
            # Add target variable
            ml_df['Won_Medal'] = merged_df['Won_Medal']
            
            print("Data prepared for machine learning")
            return ml_df
        except Exception as e:
            print(f"Error preparing data for ML: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Example usage
        processor = DataProcessor()
        processor.load_data()
        processor.clean_athletes_data()
        processor.clean_medals_data()
        merged_data = processor.merge_datasets()
        ml_data = processor.prepare_for_ml(merged_data)
        
        # Save processed data
        output_path = processor.project_root / 'processed_data' / 'ml_ready_data.csv'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        ml_data.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")
    except Exception as e:
        print(f"Error in main execution: {str(e)}") 