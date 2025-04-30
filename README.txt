# SecureSamplingProject

This project implements and compares a cryptographically secure discrete Laplace sampler with a traditional naive Laplace sampling method. It includes statistical validation, performance analysis, and visual comparisons between both samplers.

## How to Run

1. Install the required Python libraries:

   pip install numpy matplotlib seaborn scipy

2. Run the following script to validate and compare the samplers:

   python run_sampling.py

This will generate:
- 100,000 samples from both original and secure samplers
- Four plots for comparison:
  - Histogram
  - KDE (Estimated PDF)
  - Empirical CDF
  - Boxplot

## Functionality Included

- SecureDiscreteLaplaceSampler: cryptographically secure, constant-time noise generation
- Original naive Laplace sampler: for baseline comparison
- Statistical testing using Kolmogorov-Smirnov and Chi-Square tests
- Timing attack resistance checks
- Visualization of statistical differences using matplotlib and seaborn

## Functionality Not Included

- No user interface or API integration
- No full differential privacy framework support (e.g., Gaussian or Exponential noise)
- No real-world dataset integration; sampling is synthetic and self-contained

## Project Structure

run_sampling.py        - Main driver script to run and plot experiments  
secure_sampling.py     - Secure and original Laplace sampler implementations  
README.md              - Documentation and usage instructions

## Author

Mohamed Hesham Mahmoud  
Master of Science in Computer Science  
Texas State University, San Marcos  
