import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy import ndimage
from skimage import measure
from skimage.filters import threshold_otsu
from skimage.morphology import remove_small_objects

# -------------------------
# 1. Load volume
# -------------------------
data = np.load("baby_volume.npy")

print("Volume shape:", data.shape)
print("Value range:", data.min(), "to", data.max())

# -------------------------
# 2. Normalize
# -------------------------
data = (data - data.min()) / (data.max() - data.min())

# -------------------------
# 3. Smooth ultrasound noise
# -------------------------
data = gaussian_filter(data, sigma=1.5)

# -------------------------
# 4. Preview slice
# -------------------------
z = data.shape[2] // 2

plt.imshow(data[:, :, z], cmap="gray")
plt.title("Smoothed slice")
plt.axis("off")
plt.show()

# -------------------------
# 5. Automatic threshold
# -------------------------
threshold = threshold_otsu(data)
print("Threshold:", threshold)

binary = data > threshold

plt.imshow(binary[:, :, z], cmap="gray")
plt.title("Binary segmentation")
plt.axis("off")
plt.show()

# -------------------------
# 6. Remove tiny noise
# -------------------------
binary = remove_small_objects(binary, min_size=2000)

# -------------------------
# 7. Label all objects
# -------------------------
labels, num_objects = ndimage.label(binary)

print("Objects detected:", num_objects)

sizes = ndimage.sum(binary, labels, range(num_objects + 1))
sizes[0] = 0

# sort objects largest → smallest
sorted_labels = np.argsort(sizes)[::-1]

print("Object sizes:")
for i in range(num_objects):
    label_id = sorted_labels[i]
    if sizes[label_id] == 0:
        continue
    print(f"Object {label_id} size:", int(sizes[label_id]))

# -------------------------
# 8. OBJ export function
# -------------------------
def save_obj(filename, verts, faces):
    with open(filename, "w") as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

# -------------------------
# 9. Extract mesh for each object
# -------------------------
print("Extracting meshes...")

object_index = 1

for label_id in sorted_labels:

    if sizes[label_id] < 5000:   # skip tiny objects
        continue

    mask = labels == label_id
    volume = mask.astype(np.float32)

    if volume.max() == volume.min():
        continue

    verts, faces, normals, values = measure.marching_cubes(volume, level=0.5)

    filename = f"object_{object_index}.obj"
    save_obj(filename, verts, faces)

    print(f"Saved {filename} (size={int(sizes[label_id])})")

    object_index += 1

print("All objects exported.")