import numpy as np
import matplotlib.pyplot as plt

batch_size=[1,4,8,16,32,64]
fig=plt.figure(figsize=(6,3))

plt.plot(batch_size,[480,200,140,120,90,90],c='red',label='DM')
plt.plot(batch_size,[400,160,130,120,110,110],c='blue',label='UCCA')

plt.legend(loc='upper right')
plt.xlabel('Batch Size')
plt.ylabel('Training Time/epoch (minutes)')
plt.xticks(batch_size)
# plt.title('Effect of batch-training for transition-based parser')

plt.show()