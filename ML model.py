import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt

# Set display options to show the full row
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)     # Show all rows
pd.set_option('display.max_colwidth', None) # Show full content of each column
pd.set_option('display.expand_frame_repr', False)  # Do not wrap to multiple lines

# Load the data
df = pd.read_csv('player_stats.csv')

# Ensure that the starting_lineup and opposing_lineup are lists (not necessary here but just in case)
df['starting_lineup'] = df['starting_lineup'].apply(eval)
df['opposing_lineup'] = df['opposing_lineup'].apply(eval)

# Apply MultiLabelBinarizer to starting_lineup
mlb_starting = MultiLabelBinarizer()
starting_lineup_encoded = pd.DataFrame(mlb_starting.fit_transform(df['starting_lineup']),
                                       columns=mlb_starting.classes_,
                                       index=df.index)

# Apply MultiLabelBinarizer to opposing_lineup
mlb_opposing = MultiLabelBinarizer()
opposing_lineup_encoded = pd.DataFrame(mlb_opposing.fit_transform(df['opposing_lineup']),
                                       columns=[f"opp_{player}" for player in mlb_opposing.classes_],
                                       index=df.index)

# Combine all encoded columns with the home_away feature
X = pd.concat([df[['home_away']],
               opposing_lineup_encoded], axis=1)

# Set points as the target variable
df['PTS'] = df['PTS']

# Combine features and target into one DataFrame for AutoGluon
df_ag = pd.concat([X, df['PTS']], axis=1)

# Split the data into training and test sets
train_data = df_ag.sample(frac=0.7, random_state=42)
test_data = df_ag.drop(train_data.index)

# Define the predictor
predictor = TabularPredictor(label='PTS', eval_metric='mean_squared_error')

# Train the model
predictor.fit(train_data)

# Evaluate the model
performance = predictor.evaluate(test_data)

# Print performance
print(performance)

# Residual Analysis
y_true = test_data['PTS']
y_pred = predictor.predict(test_data)
residuals = y_true - y_pred
plt.scatter(y_pred, residuals, alpha=0.4)
plt.title('Residual Analysis')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.show()

print("Model training and evaluation with AutoGluon complete.")
