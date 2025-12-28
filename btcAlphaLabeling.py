import pandas as pd


def create_labeled_dataset(input_file, output_file):
    # Load the original dataset
    print(f"Loading {input_file}...")
    df = pd.read_csv(input_file, names=['source', 'target', 'rating', 'time'])

    # Identify top 30 frauds (same logic as before)
    node_stats = df.groupby('target')['rating'].agg(['sum', 'count'])
    # Sort by sum (ascending) then count (descending)
    top_30_nodes = node_stats.sort_values(
        by=['sum', 'count'],
        ascending=[True, False]
    ).head(30).index.tolist()

    print(f"Top 30 fraud nodes identified. Examples: {top_30_nodes[:5]}")

    # Process the dataframe for the new format
    # Create the 'label' column: 1 if target is in top_30, else 0
    df['label'] = df['target'].apply(lambda x: 1 if x in top_30_nodes else 0)

    # Convert ratings to absolute values (No negative numbers allowed)
    df['amount'] = df['rating'].abs()

    # Select and reorder columns (Source, Target, Amount, Label)
    # This removes the 'time' column automatically
    final_df = df[['source', 'target', 'amount', 'label']]

    # Save to new CSV
    final_df.to_csv(output_file, index=False)



# Run the script
create_labeled_dataset('soc-sign-bitcoinalpha.csv', 'transactions_bitcoin_labeled.csv')