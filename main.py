import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
from utils import en_df, gp_df


merged_df = pd.merge(en_df, gp_df, how='inner', left_on=['Warehouse', 'traffic_stream', 'datetime'], right_on=['Warehouse', 'Traffic_stream', 'datetime'])

pearson_corr, _ = pearsonr(merged_df['klk_EN'], merged_df['total_count'])
spearman_corr, _ = spearmanr(merged_df['klk_EN'], merged_df['total_count'])


X = merged_df['klk_EN'].values
y = merged_df['total_count'].values

X_b = np.c_[np.ones((len(X), 1)), X]

theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)


en_before_gp = en_df[en_df['datetime'] < '2021-08-01']
X_pred = en_before_gp['klk_EN'].values
X_pred_b = np.c_[np.ones((len(X_pred), 1)), X_pred]
y_pred = X_pred_b.dot(theta_best)

predicted_gp_df = en_before_gp[['datetime', 'Warehouse', 'traffic_stream']].copy()
predicted_gp_df['predicted_total_count'] = y_pred


plt.figure(figsize=(12, 6))

plt.plot(gp_df['datetime'], gp_df['total_count'], label='Actual GP')
plt.plot(
    predicted_gp_df['datetime'],
    predicted_gp_df['predicted_total_count'],
    label='Predicted GP',
    linestyle='--'
    )

plt.xlabel('Date')
plt.ylabel('Number of Money Transfers')
plt.title('Actual and Predicted Number of Money Transfers (GP)')
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(merged_df['klk_EN'], merged_df['total_count'], alpha=0.5)
plt.xlabel('Number of Shipments (EN)')
plt.ylabel('Number of Money Transfers (GP)')
plt.title('Correlation between EN and GP')
plt.show()

print(f'Pearson correlation coefficient: {pearson_corr}')
print(f'Spearman rank correlation coefficient: {spearman_corr}')
