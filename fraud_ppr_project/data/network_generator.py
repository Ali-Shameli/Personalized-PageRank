import csv
import random


def generate_fraud_dataset(num_edges, output_file):
    avg_degree = 5
    num_nodes = max(50, num_edges // avg_degree)

    all_users = list(range(num_nodes))

    fraud_percentage = 0.05
    num_fraudsters = max(1, int(num_nodes * fraud_percentage))

    fraudsters_set = set(random.sample(all_users, num_fraudsters))

    rows = []
    headers = ["source", "destination", "amount", "label"]

    for _ in range(num_edges):
        src = random.choice(all_users)
        dst = random.choice(all_users)

        while src == dst:
            dst = random.choice(all_users)

        amount = round(random.uniform(10.0, 10000.0), 2)

        label = 1 if dst in fraudsters_set else 0

        rows.append([src, dst, amount, label])

    try:
        with open(output_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        print(f"File saved as: {output_file}")
        print(f"Total Edges: {len(rows)}")
        print(f"Fraudulent Transactions: {sum(r[3] for r in rows)}")

    except IOError as e:
        print(f"Error writing to file: {e}")


if __name__ == "__main__":
    try:
        user_input = input("Enter number of edges: ")
        edges_count = int(user_input)

        dynamic_filename = f"synthetic_data_{edges_count}_edges.csv"

        generate_fraud_dataset(edges_count, dynamic_filename)

    except ValueError:
        print("Please enter a valid integer number.")