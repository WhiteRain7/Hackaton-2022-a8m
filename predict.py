import torch
import math


dtype = torch.float
device = torch.device("cpu")


x = torch.FloatTensor([[0.1,0.1,1.],[0.2,0.2,1.],[0.3,0.3,0.3]]) # получить массив массивов
y = torch.FloatTensor([[1],[1],[0]]) # получить массив массивов # с одним значением в каждом

a = torch.randn(3, 1, device=device, dtype=dtype, requires_grad=True)
print(a)

learning_rate = 1e-6
for t in range(2000):
    y_pred = x.mm(a)

    loss = (y_pred - y).pow(2).sum()
    if t % 100 == 95:
        print(t, loss.item())

    loss.backward()

    with torch.no_grad():
        a -= learning_rate * a.grad
        a.grad.zero_()

print(f'Result: y_pred = {y_pred}, a = {a}')