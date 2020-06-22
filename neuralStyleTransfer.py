import matplotlib.pyplot as plt
from NST import NST
from config import setting
Neiron = NST(setting)
Neiron.create_my_samples()
Neiron.run_style_transfer()

fig,axes = plt.subplots(figsize=(10,10))
axes.axis('off')
plt.imshow(Neiron.images[40])
fig.savefig('замок')
