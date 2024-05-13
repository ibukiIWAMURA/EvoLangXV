import matplotlib.pyplot as plt

def TopSim(topsims, n_gens, out_path):
    T = list(range(n_gens))
    plt.figure(figsize=(10, 6))
    plt.ylim((-0.25, 1))
    plt.plot(T, topsims)
    plt.title('TopSims')
    plt.xlabel('generation')
    plt.ylabel('TopSim')
    plt.savefig(out_path)

def eps_len(epsilons, lengths, n_gens, out_path):
    T = list(range(n_gens))
    plt.figure(figsize=(10, 6))
    plt.scatter(epsilons, lengths, c=T, cmap='viridis', s=100, zorder=2)
    plt.colorbar(label='Time (T)')
    plt.xlim((-10, 110))

    for i in range(len(T) - 1):
        plt.arrow(epsilons[i], lengths[i], epsilons[i+1] - epsilons[i], lengths[i+1] - lengths[i], 
                shape='full', lw=1, length_includes_head=True, head_width=0.05, color='red')

    for i, txt in enumerate(T):
        plt.annotate(txt, (epsilons[i], lengths[i]), textcoords="offset points", xytext=(0,10), ha='center', zorder=1)

    plt.xlabel('ε')
    plt.ylabel('|G|')
    plt.title('Time evolution')
    plt.grid(True)
    plt.savefig(out_path)

def algo_counts(df, out_path):
    df.plot(kind='bar', stacked=True, grid=False, colormap='Set2')
    plt.xlabel('Generation')
    plt.ylabel('Counts')
    plt.xticks(rotation=90)
    plt.legend(title='Types')
    plt.savefig(out_path)
    
def plot_correct_failure_ratios(correct_ratios, failure_ratios, n_gens, out_path):
    T = list(range(1, n_gens + 1))  # 1からn_gensまでの世代
    plt.figure(figsize=(10, 6))
    plt.ylim((0, 1))  # 縦軸の範囲を0から1に制限
    plt.yticks(np.arange(0, 1.0, -1))
    plt.plot(T, correct_ratios, label='Correct Ratio', marker='o')
    plt.plot(T, failure_ratios, label='Failure Ratio', marker='o')
    plt.title('Correct and Failure Ratios Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Ratio')
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.savefig(out_path)
