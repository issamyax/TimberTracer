def plot_results(init_stock, products_stock, yearly_emissions, material_sub, energy_sub, yearly_recycling,n):
    """
    This function render plots of wood stock, emissions, energy and material substitution as well as the annual recycling
    """

    # initial total stock in m3
    total_stock = round(sum(init_stock['post_process_volume']),2)

    # Prepare data:
    # f2 is the cumulative list of yearly_emissions
    f2 = [yearly_emissions[0]]
    for i in range(2, n + 1):
        f2.append(f2[i - 2] + yearly_emissions[i - 1])

    # s2 is the cumulative list of material_sub
    s2 = [material_sub[0]]
    for i in range(2, n + 1):
        s2.append(s2[i - 2] + material_sub[i - 1])

    # s4 is the cumulative list of energy_sub
    s4 = [energy_sub[0]]
    for i in range(2, n + 1):
        s4.append(s4[i - 2] + energy_sub[i - 1])

    # Create a figure and three subplots
    fig, axes = plt.subplots(1, 4, figsize=(20, 5), sharey=True)

    # Plot the first plot in the first subplot
    axes[0].plot(range(1, n+1), energy_sub, label="annual substitution")
    axes[0].plot(range(1, n+1), s4, label="cumulative substitution")
    axes[0].set_title('Material substitution \n(Initial stock ~{} m3)'.format(total_stock))
    axes[0].set_xlabel('time')
    axes[0].set_ylabel('tC')
    axes[0].legend()

    # Plot the second plot in the second subplot
    axes[1].plot(range(1, n+1), f2, label="cumulative emissions")
    axes[1].plot(range(1, n+1), products_stock, label="Wood stock evolution")
    axes[1].set_title('Stock and emissions evolution \n(Initial stock ~{} m3)'.format(total_stock))
    axes[1].set_xlabel('time')
    axes[1].set_ylabel('tC')
    axes[1].legend()

    # Plot the third plot in the third subplot
    axes[2].plot(range(1, n+1), s2, label='cumulative substitution')
    axes[2].plot(range(1, n+1), material_sub, label='annual substitution')
    axes[2].set_title('Energy substitution \n(Initial stock ~{} m3)'.format(total_stock))
    axes[2].set_xlabel('time')
    axes[2].set_ylabel('tC')
    axes[2].legend()

    # Plot the fourth plot in the fourth subplot
    axes[3].plot(range(1, n+1), yearly_recycling)
    axes[3].set_title('annual recycling \n(Initial stock ~{} m3)'.format(total_stock))
    axes[3].set_xlabel('time')
    axes[3].set_ylabel('tC x10')

    # Adjust the subplot layout
    plt.subplots_adjust(bottom=0.2)

    # Return the figure
    return fig
