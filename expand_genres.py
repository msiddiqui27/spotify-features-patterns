import pandas as pd

# Load data
df = pd.read_csv('songs_normalize.csv')

print(f"Original dataset: {len(df)} rows")
print(f"Original unique genres: {df['genre'].nunique()}")

# Split genres and create one row per genre
rows = []
for idx, row in df.iterrows():
    genres = str(row['genre']).split(', ')
    for genre in genres:
        genre = genre.strip()
        if genre and genre != 'set()':  # Skip empty and weird values
            new_row = row.copy()
            new_row['genre'] = genre
            new_row['original_genre'] = row['genre']  # Keep original multi-genre tag
            rows.append(new_row)

# Create new dataframe
df_expanded = pd.DataFrame(rows)

print(f"\nExpanded dataset: {len(df_expanded)} rows")
print(f"Expanded unique genres: {df_expanded['genre'].nunique()}")
print("\nTop 15 genres after expansion:")
print(df_expanded['genre'].value_counts().head(15))

# Save expanded dataset
df_expanded.to_csv('songs_expanded_genres.csv', index=False)
print("\nSaved to: songs_expanded_genres.csv")

print("\nNote: Some songs now appear multiple times (once per genre)")
print("Example: 'Oops!...I Did It Again' if tagged 'pop, Dance/Electronic' becomes 2 rows")