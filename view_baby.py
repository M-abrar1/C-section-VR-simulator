import numpy as np
import matplotlib.pyplot as plt

# Load your npy file
data = np.load('baby_volume.npy')

print("Volume shape:", data.shape)  # check dimensions

# Choose a slice index (z-axis)
z = data.shape[2] // 2  # middle slice
plt.imshow(data[:, :, z], cmap='gray')
plt.title(f"Slice {z} (axial view)")
plt.axis('off')
plt.show()


thresholds = [0.35, 0.40, 0.45, 0.50, 0.55]

for t in thresholds:
    binary = data > t
    plt.figure()
    plt.imshow(binary[:, :, z], cmap="gray")
    plt.title(f"Threshold {t}")
    plt.axis("off")