# === MAIN SCRIPT: Estimate Drag Coefficient ===

from experimental.drag_fit import DragEstimator

# Create the estimator instance using the log file
estimator = DragEstimator(filepath='data/logs.csv')

# Estimate the best gamma using squared error minimization
best_gamma = estimator.estimate_gamma(initial_guess=0.1)

# Show result
if best_gamma is not None:
    print(f"\n✅ Estimated drag coefficient (gamma): {best_gamma:.4f}")
else:
    print("❌ Optimization failed. Check your data.")
