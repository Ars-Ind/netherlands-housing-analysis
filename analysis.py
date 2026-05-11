import pandas as pd
import matplotlib.pyplot as plt

# load Excel dataset
df = pd.read_excel("kamernet_rental_data_set.xlsx")

# remove useless column
df = df.drop(columns=["Unnamed: 0"])

# clean Rent column
df["Rent"] = df["Rent"].str.replace(",-", "", regex=False)
df["Rent"] = pd.to_numeric(df["Rent"])

# clean Meters column
df["Meters"] = df["Meters"].str.replace(" m2", "", regex=False)
df["Meters"] = pd.to_numeric(df["Meters"])

# create price per square meter column
df["Price_per_m2"] = df["Rent"] / df["Meters"]

# show first rows
print("\nFIRST 5 ROWS:\n")
print(df.head())

# average rent
print("\nAVERAGE RENT:\n")
print(df["Rent"].mean())

# listings count by city
print("\nNUMBER OF LISTINGS BY CITY:\n")
print(df["City"].value_counts().head(20))

# keep only cities with 5+ listings
city_counts = df["City"].value_counts()

valid_cities = city_counts[city_counts >= 5].index

filtered_df = df[df["City"].isin(valid_cities)]

# average rent by city
print("\nAVERAGE RENT BY CITY:\n")

print(
    filtered_df.groupby("City")["Rent"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# price per square meter by city
print("\nPRICE PER M2 BY CITY:\n")

print(
    filtered_df.groupby("City")["Price_per_m2"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

# chart 1 - average rent
top_rent_cities = (
    filtered_df.groupby("City")["Rent"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

top_rent_cities.plot(kind="bar")

plt.title("Top 10 Most Expensive Cities by Average Rent")

plt.xlabel("City")

plt.ylabel("Average Rent (€)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# chart 2 - price per m²
top_price_m2 = (
    filtered_df.groupby("City")["Price_per_m2"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12,6))

top_price_m2.plot(kind="bar")

plt.title("Top 10 Most Expensive Cities by Price per m²")

plt.xlabel("City")

plt.ylabel("Average Price per m² (€)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# scatter plot: Rent vs Apartment Size

plt.figure(figsize=(10,6))

plt.scatter(filtered_df["Meters"], filtered_df["Rent"])

plt.title("Relationship Between Apartment Size and Rent")

plt.xlabel("Apartment Size (m²)")

plt.ylabel("Rent (€)")

plt.tight_layout()

plt.show()