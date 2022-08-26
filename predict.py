import torch            

def predict(parsed, iterations = 50000, learning_rate = 1e-6, min_accuracy = None):
    if (type(parsed) is not dict or
        len(parsed.get('X', [])) == 0 or
        len(parsed.get('Y', [])) == 0):
            print('Incorrect data to prediction.')
            return
    
    dtype = torch.float
    device = torch.device("cpu")

    x = torch.FloatTensor(parsed['X']) # list of lists of input data ==> tensor
    y = torch.FloatTensor(parsed['Y']) # list of lists of output data ==> tensor

    layers_dimensions = [
                         len(parsed['X'][0]),
                         33,
                         20,
                         10,
                         5,
                         len(parsed['Y'][0])
                        ]

    layers = []
    for i in range(len(layers_dimensions) - 1):
        layer = torch.randn(layers_dimensions[i],
                            layers_dimensions[i+1],
                            device=device,
                            dtype=dtype,
                            requires_grad=True)

        layers.append(layer)

    iterations_ten_percents = iterations // 10
    print('Learning NN.')
    
    for t in range(iterations):
        y_pred = x.mm(layers[0])
                             
        for layer in layers: y_pred = y_pred.clamp(min = 0, max = 1).mm(layer)

        loss = (y_pred - y).pow(2).sum() # counting losses
        if t % iterations_ten_percents == 0: print('Still learning... {}0% ==> {}'.format(t // iterations_ten_percents, loss.item()))

        loss.backward()

        with torch.no_grad():
            for i in range(len(layers)):
                layers[i] -= learning_rate * layers[i].grad
                layers[i].grad.zero_()
    
    print('Learning finished.\nFinal losses: ' + str(loss.item()) + '\n')

    print('\n=============\n', layers, '\n=============\n')

    return y_pred.clamp(min = 0, max = 1)
