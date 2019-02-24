import torch
import numpy as np

# print torch.__version__

#numpy and tensor
# np_data = np.arange(6).reshape((2,3))
# torch_data = torch.from_numpy(np_data)
# tensor2array = torch_data.numpy()
#
# print np_data
# print torch_data
# print tensor2array

#abs
data = [[1,2],[3,4]]
tensor=torch.FloatTensor(data)

data = np.array(data)

# print tensor

# print(
#     # '\nnumpy:', np.matmul(data,data),
#     # '\ntorch:', torch.mm(tensor,tensor),
#     # '\nnumpy_dot', data.dot(data),
#     # '\ntorch_dot', torch.dot(tensor,tensor)
#     torch.tensor([2, 3]).dot(torch.tensor([2, 1]))
# )

from torch.autograd import Variable

# tensor = torch.FloatTensor([[1,2],[3,4]])
# variable = Variable(tensor, requires_grad=True)
#
# print tensor
# print variable
#
# v_out = torch.mean(variable*variable)
#
# print variable.grad
# v_out.backward()
# print variable.grad
# print variable.data.numpy()

import torch.nn.functional as F
import matplotlib.pyplot as plt

#fake data
x = torch.linspace(-5, 5, 100)
x = Variable(x)
x_np = x.data.numpy()

y_relu = F.relu(x).data.numpy()
y_softplus = F.softplus(x).data.numpy()

plt.figure(1, figsize=(8, 6))
plt.subplot(211)
plt.plot(x_np, y_relu, c='red', label='relu')
plt.ylim((-1, 5))
plt.legend(loc='best')

plt.subplot(212)
plt.plot(x_np, y_softplus, c='red', label='softplus')
plt.ylim((-0.2, 6))
plt.legend(loc='best')

plt.show()
