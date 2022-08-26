from this import d
import torch
import math

from csv_parser import ParsedContent

class PredictResult:
    y = []
    a = []
    loss = 0

    def __init__(self, y, a, loss):
        self.y = y.t().tolist()[0]
        self.a = a
        self.loss = loss

    def print(self):
        print('y = [')
        print(f'{", ".join([str(round(i, 2)) for i in self.y])}')
        print(f']\nloss = {self.loss}')

def predict(parsedData: ParsedContent):
    dtype = torch.float
    device = torch.device("cpu")

    x = torch.FloatTensor(parsedData.x) # получить массив массивов
    y = torch.FloatTensor(parsedData.y) # получить массив массивов # с одним значением в каждом

    a = torch.randn(len(parsedData.x[0]), len(parsedData.y[0]), device=device, dtype=dtype, requires_grad=True)
    #print(a)

    learning_rate = 1e-6
    for t in range(50000):
        y_pred = x.mm(a)

        loss = (y_pred - y).pow(2).sum()
        if t % 5000 == 4999:
            print(t, loss.item())

        loss.backward()

        with torch.no_grad():
            a -= learning_rate * a.grad
            a.grad.zero_()
    
    return PredictResult(y_pred, a, loss.item())