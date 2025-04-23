# Olympic Data Analysis

A data engineering project that analyzes Olympic data using machine learning techniques to predict medal outcomes and analyze athlete performance.

## Project Overview

This project processes and analyzes Olympic data to:
- Predict medal outcomes based on athlete and team characteristics
- Analyze gender representation trends
- Identify factors contributing to team success
- Create visualizations of historical trends

## Project Structure

```
OlympicDataAnalysis/
├── rawdata/              # Raw data files
│   ├── Athletes.csv     # Athlete information
│   ├── Teams.csv        # Team-related data
│   ├── Medals.csv       # Medal distribution data
│   ├── Coaches.csv      # Coach information
│   └── EntriesGender.csv # Gender participation data
├── src/                  # Source code
│   ├── data/            # Data processing scripts
│   │   └── data_processor.py
│   ├── models/          # Machine learning models
│   │   └── medal_predictor.py
│   └── visualization/   # Data visualization scripts
│       └── data_visualizer.py
├── processed_data/       # Processed and cleaned data
├── visualizations/       # Generated visualizations
├── models/              # Trained machine learning models
├── notebooks/           # Jupyter notebooks for analysis
├── requirements.txt     # Project dependencies
└── README.md           # Project documentation
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Processing

Process and clean the raw data:
```bash
python src/data/data_processor.py
```

This will:
- Load and clean the raw data
- Merge datasets
- Prepare data for machine learning
- Save processed data to `processed_data/ml_ready_data.csv`

### Data Visualization

Generate visualizations:
```bash
python src/visualization/data_visualizer.py
```

This will create:
- Medal distribution plots
- Gender participation analysis
- Athlete characteristics visualization
- Correlation heatmaps

### Machine Learning

Train and evaluate the model:
```bash
python src/models/medal_predictor.py
```

This will:
- Train a Random Forest model
- Evaluate model performance
- Save the trained model
- Display feature importance

## Data Analysis

The project includes several key analyses:

1. **Medal Prediction**
   - Uses Random Forest classifier
   - Predicts medal outcomes based on team and athlete characteristics
   - Evaluates model performance using classification metrics

2. **Gender Analysis**
   - Analyzes gender participation across disciplines
   - Visualizes trends in gender representation
   - Identifies areas of gender imbalance

3. **Team Performance**
   - Analyzes factors contributing to team success
   - Visualizes medal distribution by country
   - Identifies patterns in successful teams

## Dependencies

- pandas==2.1.0
- numpy==1.24.3
- scikit-learn==1.3.0
- matplotlib==3.7.2
- seaborn==0.12.2
- pyspark==3.4.1
- python-dotenv==1.0.0
- jupyter==1.0.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Data source: [Olympic Data](https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results)
- Thanks to all contributors and maintainers 