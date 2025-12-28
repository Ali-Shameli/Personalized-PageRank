def get_manual_graph_data():
    """
    Collects raw graph edges and seeds from user manually.
    Returns raw lists (before mapping).
    """
    print("\n--- Manual Graph Data Entry ---")
    print("Format: source destination weight")
    print("Example: 10 20 5.5")
    print("Type 'end' to finish adding edges.\n")

    src_list = []
    dst_list = []
    weights_list = []

    # Edge Collection Loop
    while True:
        line = input("Edge (src dst weight) or 'end': ").strip()
        if line.lower() == 'end':
            break

        parts = line.split()
        if len(parts) != 3:
            print("Invalid format. Need 3 values.")
            continue

        try:
            s = int(parts[0])
            d = int(parts[1])
            w = float(parts[2])
            src_list.append(s)
            dst_list.append(d)
            weights_list.append(w)
        except ValueError:
            print("Invalid numbers. Integers for IDs, float for weight.")

    # Seed Collection
    print("\nEnter Fraud Seeds (IDs separated by space):")
    seeds_input = input("> ").strip()
    raw_seeds = []
    if seeds_input:
        try:
            raw_seeds = [int(x) for x in seeds_input.split()]
        except ValueError:
            print("Invalid seeds. Proceeding with empty seed list.")

    return src_list, dst_list, weights_list, raw_seeds