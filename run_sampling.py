# run_sampling.py



from secure_sampling import SecureDiscreteLaplaceSampler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Number of samples
num_samples = 100000

# Initialize secure sampler
secure_sampler = SecureDiscreteLaplaceSampler(scale=2)
secure_samples = np.array([secure_sampler.sample() for _ in range(num_samples)])

# Define original naive sampler
def original_laplace_sample():
    u = np.random.random()
    return np.sign(u - 0.5) * np.log(1 - 2 * abs(u - 0.5))

orig_samples = np.array([original_laplace_sample() for _ in range(num_samples)])

# Set up plots
fig, axs = plt.subplots(2, 2, figsize=(15, 12))

# 1. Histogram
axs[0, 0].hist(orig_samples, bins=100, alpha=0.5, label='Original')
axs[0, 0].hist(secure_samples, bins=100, alpha=0.5, label='Secure')
axs[0, 0].set_title("Histogram")
axs[0, 0].legend()
axs[0, 0].grid(True)

# 2. KDE (Estimated PDF)
sns.kdeplot(orig_samples, ax=axs[0, 1], label='Original')
sns.kdeplot(secure_samples, ax=axs[0, 1], label='Secure')
axs[0, 1].set_title("KDE (PDF)")
axs[0, 1].legend()
axs[0, 1].grid(True)

# 3. Empirical CDF
sns.ecdfplot(orig_samples, ax=axs[1, 0], label='Original')
sns.ecdfplot(secure_samples, ax=axs[1, 0], label='Secure')
axs[1, 0].set_title("Empirical CDF")
axs[1, 0].legend()
axs[1, 0].grid(True)

# 4. Boxplot
axs[1, 1].boxplot([orig_samples, secure_samples], labels=["Original", "Secure"])
axs[1, 1].set_title("Boxplot")
axs[1, 1].grid(True)

plt.suptitle("Original vs Secure Laplace Sampling – Full Comparison", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
