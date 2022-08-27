import torch            

def learning(parsed, iterations = 50000, learning_rate = 1e-6, min_accuracy = None):
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
                         1000,
                         500,
                         50,
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
                             
        for layer in layers[1:]: y_pred = y_pred.clamp(min = 0, max = 1).mm(layer)

        loss = (y_pred - y).pow(2).sum() # counting losses
        if t % iterations_ten_percents == 0: print('Still learning... {}0% ==> {}'.format(t // iterations_ten_percents, loss.item()))

        loss.backward()

        with torch.no_grad():
            for i in range(len(layers)):
                layers[i] -= learning_rate * layers[i].grad
                layers[i].grad.zero_()
    
    print('Learning finished.\nFinal losses: ' + str(loss.item()) + '\n')

    print('\n=============\n', layers, '\n=============\n')

    return y_pred, layers

#===========================================================     

def nn_learning(parsed, iterations = 50000, learning_rate = 1e-6, min_accuracy = None):
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
                         50,
                         len(parsed['Y'][0])
                        ]

    model = torch.nn.Sequential().to(device)
    
    model.append(torch.nn.Linear(layers_dimensions[0], layers_dimensions[1]))
    
    for i in range(1, len(layers_dimensions) - 1):
        model.append(torch.nn.ReLU())
        model.append(torch.nn.Linear(layers_dimensions[i], layers_dimensions[i+1]))
    
    loss_fn = torch.nn.MSELoss(reduction='sum')
    optim = torch.optim.SGD(model.parameters(), lr = learning_rate)

    iterations_ten_percents = iterations // 10
    print('Learning NN.')
    
    for t in range(iterations):
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        optim.zero_grad()
        loss.backward()
        optim.step()

        if t % iterations_ten_percents == 0: print('Still learning... {}0% ==> {}'.format(t // iterations_ten_percents, loss.item()))
    
    print('Learning finished.\nFinal losses: ' + str(loss.item()) + '\n')

    return y_pred, model

#===========================================================

def sigmoid_learning(parsed, iterations = 50000, learning_rate = 1e-6, min_accuracy = None):
    if (type(parsed) is not dict or
        len(parsed.get('X', [])) == 0 or
        len(parsed.get('Y', [])) == 0):
            print('Incorrect data to prediction.')
            return

    import numpy as np

    # подсчитаем нелинейную сигмоиду
    def sigmoid(x):
        output = 1/(1+np.exp(-x))
        return output

    # преобразуем результат сигмоиды к производной
    def sigmoid_output_to_derivative(output):
        return output*(1-output)
        
    dtype = torch.float
    device = torch.device("cpu")

    x = np.array(parsed['X']) # list of lists of input data ==> np_array
    y = np.array(parsed['Y']) # list of lists of output data ==> np_array

    layers_dimensions = [
                         len(parsed['X'][0]),
                         1000,
                         500,
                         50,
                         5,
                         len(parsed['Y'][0])
                        ]

    np.random.seed(1)
    layers = []
    for i in range(len(layers_dimensions) - 1):
        layer = 2*np.random.random((layers_dimensions[i], layers_dimensions[i+1])) - 1
        layers.append(layer)

    iterations_ten_percents = iterations // 10
    print('Learning NN.')
    
    for t in range(iterations):
        layers_pred = [x]
        for i in range(len(layers)):
            layers_pred.append(sigmoid(np.dot(layers_pred[i], layers[i])))

        if t%50000 == 0: print('Still learning... #{}'.format(t))

        layer_error = y - layers[-1].T
        layer_delta = layer_error * sigmoid_output_to_derivative(layers_pred[-1])

        for i in range(len(layers)-2, -1, -1):
            layer_error = layer_delta.dot(layers[i].T)
            layer_delta = layer_error * sigmoid_output_to_derivative(layers_pred[i])

            weight_update = layers[i].dot(layer_delta)
            layers[i] += learning_rate * weight_update
    
    print('Learning finished.\nFinal losses: ' + str(loss.item()) + '\n')

    print('\n=============\n', layers, '\n=============\n')

    return y_pred

#===========================================================

def predict (data):
    x = torch.FloatTensor([data]) # list of input data ==> tensor
    return model(x)[0]

def predict_all (data, model):
    x = torch.FloatTensor(data) # list of lists of input data ==> tensor
    return model(x)




