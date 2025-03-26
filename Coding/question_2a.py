import math
import numpy as np
import requests
import pylhe
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


url = "https://www.ppe.gla.ac.uk/~abuckley/top.lhe"
response = requests.get(url)

with open("data.lhe", mode="wb") as file:
    file.write(response.content)

events = pylhe.read_lhe_with_attributes("data.lhe")
flat_pt_values = []


def print_summary():
    print("Summary of the first 10 events: ")
    for i, event in enumerate(events, start=1):
        total_particles = len(event.particles)
        final_particles = (p for p in event.particles if p.status == 1)

        particles = list(final_particles)
        num_final_particles = len(particles)
        energy = sum(p.e for p in particles)
        momenta_sum = sum(p.px + p.py + p.pz for p in particles)

        print(f"\nEvent {i}:")
        print(f"Total particles: {total_particles}")
        print(f"Final-state particles: {num_final_particles}")
        print(f"Final-state momentum sums:")
        print(f"    M: {momenta_sum}")
        print(f"    E: {energy}")

        # Breaks after printing information for 10 events
        if i == 10:
            break


def plot_hist_and_normal():
    all_transverse_momenta = []

    for i, event in enumerate(events):
        event_momenta = {}
        for j, particle in enumerate(event.particles):
            # Select only the top quarks
            if particle.id == 6:
                pt = math.sqrt(particle.px ** 2 + particle.py ** 2)
                event_momenta[j] = {
                    "pdgId": particle.id,
                    "pt": pt
                }
        all_transverse_momenta.append(event_momenta)

    print("\nSummary:")
    print(f"Total events processed: {len(all_transverse_momenta)}")
    total_particles = sum(len(event) for event in all_transverse_momenta)
    print(f"Total particles (top quarks) processed: {total_particles}")

    for event in all_transverse_momenta:
        for particle_data in event.values():
            flat_pt_values.append(particle_data["pt"])

    mu, std = norm.fit(flat_pt_values)

    plt.hist(flat_pt_values, bins=50, density=True, color='skyblue')

    mini, maxi = plt.xlim()
    x = np.linspace(mini, maxi, 200)
    p = norm.pdf(x, mu, std)

    # Plot the normal distribution
    plt.plot(x, p, 'r--', linewidth=2, label='Normal distribution')
    plt.xlabel("Transverse Momentum (GeV)")
    plt.ylabel("Density")
    plt.title("Histogram of Transverse Momenta with Normal Fit")
    plt.legend()
    plt.show()


def plot_boxplot():
    plt.figure(figsize=(8, 2))
    plt.boxplot(flat_pt_values, vert=False)
    plt.xlabel("Transverse Momentum (GeV)")
    plt.title("Box Plot of Transverse Momenta (Top Quarks)")
    plt.show()


def plot_violinplot():
    plt.figure(figsize=(8, 2))
    sns.violinplot(data=flat_pt_values, orient="h", inner="box")
    plt.xlabel("Transverse Momentum (GeV)")
    plt.title("Violin Plot of Transverse Momenta (Top Quarks)")
    plt.show()


if __name__ == "__main__":
    print_summary()
    plot_hist_and_normal()
    plot_boxplot()
    plot_violinplot()
