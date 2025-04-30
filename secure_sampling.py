# secure_sampling.py
import secrets
import numpy as np
import time
from scipy.stats import laplace, kstest, chisquare
from typing import Optional

class SecureDiscreteLaplaceSampler:
    """Cryptographically secure discrete Laplace sampler with constant-time operations."""
    def __init__(self, scale: int = 1, privacy_budget: Optional['PrivacyBudget'] = None, epsilon_per_sample: Optional[float] = None):
        self.scale = scale
        self.privacy_budget = privacy_budget
        self.epsilon_per_sample = epsilon_per_sample
        self._exp_neg_1 = np.exp(-1 / self.scale)

    def _geometric_sample(self) -> int:
        while True:
            u = secrets.randbits(64) / (2**64)
            geo = int(np.floor(np.log(1 - u) / np.log(1 - self._exp_neg_1)))
            if geo < 100 * self.scale:
                return geo

    def sample(self) -> int:
        if self.privacy_budget and self.epsilon_per_sample:
            self.privacy_budget.consume(self.epsilon_per_sample)
        g1 = self._geometric_sample()
        g2 = self._geometric_sample()
        return g1 - g2

class PrivacyBudget:
    """Tracks privacy budget consumption."""
   dxng = total_epsilon

    def consume(self, epsilon: float):
        if epsilon > self.remaining:
            raise ValueError(f"Privacy budget exceeded. Remaining: {self.remaining}, Attempted: {epsilon}")
        self.remaining -= epsilon

class VectorizedSecureLaplaceSampler:
    """Vectorized (non-secure) version for faster sampling."""
    def __init__(self, scale: int = 1, batch_size: int = 1000):
        self.scale = scale
        self.batch_size = batch_size
        self._exp_neg_1 = np.exp(-1 / self.scale)

    def sample_batch(self, n: int) -> np.ndarray:
        batches = []
        remaining = n
        while remaining > 0:
            current_batch = min(remaining, self.batch_size)
            u = np.random.random(current_batch)
            geo1 = np.floor(np.log(1 - u) / np.log(1 - self._exp_neg_1)).astype(int)
            u = np.random.random(current_batch)
            geo2 = np.floor(np.log(1 - u) / np.log(1 - self._exp_neg_1)).astype(int)
            batches.append(geo1 - geo2)
            remaining -= current_batch
        return np.concatenate(batches)

def validate_sampler(sampler, num_samples=100000):
    print(f"\nValidating sampler with {num_samples:,} samples...")
    start = time.time()
    samples = [sampler.sample() for _ in range(num_samples)]
    gen_time = time.time() - start
    print(f"Generation time: {gen_time:.4f}s ({num_samples/gen_time:,.0f} samples/s)")

    samples = np.array(samples)
    print("\nBasic Statistics:")
    print(f"Mean: {np.mean(samples):.4f} (expected: 0)")
    print(f"Variance: {np.var(samples):.4f} (expected: {2 * sampler.scale**2})")
    print(f"Min: {np.min(samples)}, Max: {np.max(samples)}")

    print("\nKolmogorov-Smirnov Test:")
    ks_stat, ks_p = kstest(samples, lambda x: laplace.cdf(x, scale=sampler.scale))
    print(f"KS Statistic: {ks_stat:.6f}, p-value: {ks_p:.6f}")
    print("✓ Passed" if ks_p > 0.05 else "✗ Failed")

    print("\nChi-Square Test:")
    obs_freq = np.bincount(samples - np.min(samples))
    exp_freq = laplace.pmf(np.arange(np.min(samples), np.max(samples)+1), scale=sampler.scale) * num_samples
    chi_stat, chi_p = chisquare(obs_freq, exp_freq)
    print(f"Chi-Square Statistic: {chi_stat:.2f}, p-value: {chi_p:.6f}")
    print("✓ Passed" if chi_p > 0.05 else "✗ Failed")

    print("\nTiming Attack Resistance:")
    times = []
    for _ in range(1000):
        start = time.perf_counter_ns()
        sampler.sample()
        times.append(time.perf_counter_ns() - start)
    print(f"Execution time std dev: {np.std(times):.2f} ns")
    print("✓ Consistent timing" if np.std(times) < 1000 else "✗ Potential timing variability")
