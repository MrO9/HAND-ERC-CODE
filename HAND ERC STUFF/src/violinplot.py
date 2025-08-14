import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Input data
data = {
    "Trial": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "1 to 1": [0.9826080172, 0.9873708301, 0.9773141692, 0.9794785121, 0.9659760889, 0.9670704029, 0.9670704029, 0.9871234634, 0.9910455445, 0.9668647365],
    "Pulley": [0.9585995346, 0.9636124483, 0.9445064254, 0.9510511372, 0.9642963652, 0.9524247441, 0.9525871066, 0.9647351164, 0.9458529458, 0.9700162661],
    "Bowden Tube": [0.5339336541, 0.7011548345, 0.6282209905, 0.6591230012, 0.6305631299, 0.6202286176, 0.6198086308, 0.6175640978, 0.6200426138, 0.6134465282],
    "Sliding Surface": [0.6610911241, 0.630599122, 0.6233844839, 0.6085526205, 0.5892683845, 0.6300275038, 0.7418126905, 0.8447520224, 0.5995423057, 0.7656191532],
    "Articulated Joint": [0.9103414172, 0.8900944139, 0.9582281467, 0.954925801, 0.8246807747, 0.7623196259, 0.769659684, 0.8177936357, 0.6688458898, 0.7536559632],
    "Rolling Surface": [0.6532895989, 0.6741113771, 0.7741837277, 0.6424019713, 0.6456879166, 0.5555858705, 0.6351848583, 0.5946646758, 0.6055626239, 0.6055626239]
}

# Convert to DataFrame and rename column
df = pd.DataFrame(data)
df = df.rename(columns={"1 to 1": "Control"})

# Convert to long-form DataFrame for seaborn
df_long = pd.melt(df, id_vars="Trial", var_name="Mechanism", value_name="Score")

# Convert Score to percentage
df_long["Score"] = df_long["Score"] * 100

custom_palette = {
    "Control": "#1f77b4",           # blue
    "Pulley": "#ff7f0e",            # orange
    "Bowden Tube": "#2ca02c",       # green
    "Sliding Surface": "#d62728",   # red
    "Articulated Joint": "#9467bd", # purple
    "Rolling Surface": "#8c564b"    # brown
}

# Plot
plt.figure(figsize=(12, 7))
sns.violinplot(
    x="Mechanism", 
    y="Score", 
    data=df_long, 
    inner="quartile", 
    palette=custom_palette
)

plt.xlabel("")  # Remove x-axis label
plt.ylabel("Percent (%)", fontsize=25)
plt.title("Force Efficiency Comparison", fontsize=15, fontweight='bold')
plt.xticks(rotation=30, fontsize=25)
plt.yticks(range(30, 111, 10), fontsize=35)
plt.ylim(30, 110)  
plt.tight_layout()
plt.show()
