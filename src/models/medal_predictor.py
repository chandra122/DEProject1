import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

class MedalPredictor:
    def __init__(self, data_path='processed_data/ml_ready_data.csv'):
        # Get the project root directory
        self.project_root = Path(__file__).parent.parent.parent
        self.data_path = self.project_root / data_path
        self.model = None
        self.scaler = StandardScaler()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self):
        """Load and prepare the data for training"""
        try:
            if not self.data_path.exists():
                raise FileNotFoundError(f"Data file not found at {self.data_path}")
            
            df = pd.read_csv(self.data_path)
            
            if 'Won_Medal' not in df.columns:
                raise ValueError("Target column 'Won_Medal' not found in data")
            
            # Separate features and target
            X = df.drop('Won_Medal', axis=1)
            y = df['Won_Medal']
            
            # Handle missing values in features
            X = X.fillna(X.mean())
            
            # Split the data
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Scale the features
            self.X_train = self.scaler.fit_transform(self.X_train)
            self.X_test = self.scaler.transform(self.X_test)
            
            print("Data loaded and prepared for training")
            return self
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            raise

    def train_model(self):
        """Train the Random Forest model"""
        if self.X_train is None or self.y_train is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        try:
            # Check for class imbalance
            class_counts = np.bincount(self.y_train)
            if len(class_counts) < 2:
                raise ValueError("Not enough classes in target variable")
            
            # Adjust class weights if imbalanced
            class_weights = 'balanced' if min(class_counts) / max(class_counts) < 0.5 else None
            
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                class_weight=class_weights,
                random_state=42
            )
            
            self.model.fit(self.X_train, self.y_train)
            print("Model trained successfully")
            return self
        except Exception as e:
            print(f"Error training model: {str(e)}")
            raise

    def evaluate_model(self):
        """Evaluate the model's performance"""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        try:
            # Make predictions
            y_pred = self.model.predict(self.X_test)
            
            # Print evaluation metrics
            print("\nClassification Report:")
            print(classification_report(self.y_test, y_pred))
            
            print("\nConfusion Matrix:")
            print(confusion_matrix(self.y_test, y_pred))
            
            return self
        except Exception as e:
            print(f"Error evaluating model: {str(e)}")
            raise

    def save_model(self, model_path='models/medal_predictor.joblib'):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        try:
            # Create directory if it doesn't exist
            output_path = self.project_root / model_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the model and scaler
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.X_train.columns.tolist() if hasattr(self.X_train, 'columns') else None
            }
            
            joblib.dump(model_data, output_path)
            print(f"Model saved to {output_path}")
            return self
        except Exception as e:
            print(f"Error saving model: {str(e)}")
            raise

    def get_feature_importance(self):
        """Get and display feature importance"""
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        try:
            # Get feature importance
            importance = self.model.feature_importances_
            
            # Get feature names if available
            if hasattr(self.X_train, 'columns'):
                feature_names = self.X_train.columns
            else:
                feature_names = [f'Feature_{i}' for i in range(len(importance))]
            
            # Create a DataFrame for better visualization
            feature_importance = pd.DataFrame({
                'Feature': feature_names,
                'Importance': importance
            })
            
            # Sort by importance
            feature_importance = feature_importance.sort_values('Importance', ascending=False)
            
            print("\nTop 10 Most Important Features:")
            print(feature_importance.head(10))
            
            return feature_importance
        except Exception as e:
            print(f"Error getting feature importance: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Example usage
        predictor = MedalPredictor()
        predictor.load_data()
        predictor.train_model()
        predictor.evaluate_model()
        predictor.save_model()
        predictor.get_feature_importance()
    except Exception as e:
        print(f"Error in main execution: {str(e)}") 