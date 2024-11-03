import matplotlib.pyplot as plt


# Assume data is preprocessed and ready in variables: `block_index`, `mining_time`, `difficulty`

def plot_gpt_suggestion(block_index: list, mining_time: list, bit_difficulty: list) -> None:
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Bar plot for Mining Time
    ax1.bar(block_index, mining_time, color='green', alpha=0.6, label='Block Mining Time (seconds)')
    ax1.set_xlabel('Block Index')
    ax1.set_ylabel('Block Mining Time (seconds)', color='green')
    ax1.tick_params(axis='y', labelcolor='green')

    # Line plot for Difficulty
    ax2 = ax1.twinx()
    ax2.plot(block_index, bit_difficulty, color='blue', linestyle='-', linewidth=1.5, label='Difficulty')
    ax2.set_ylabel('Difficulty / Bit Difficulty', color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    # Add grid and title
    ax1.grid(visible=True, which='major', color='grey', linestyle='--', linewidth=0.5)
    plt.title("Blockchain Mining Analysis\nKey Parameters: Initial Difficulty, Target Time, Adjustment Interval")

    # Customize legend
    fig.legend(loc="upper right", bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

    # Show plot
    plt.tight_layout()
    plt.show()


# Example usage:
# plot_gpt_suggestion(block_index=[1, 2, 3, 4, 5], mining_time=[0.5, 0.6, 0.7, 0.8, 0.9], difficulty=[1, 2, 3, 4, 5])

# block_index =
# mining_time =
# bit_difficulty =
# plot_gpt_suggestion(block_index=block_index, mining_time=mining_time, bit_difficulty=bit_difficulty)
