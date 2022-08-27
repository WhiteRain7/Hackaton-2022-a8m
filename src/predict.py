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

def get_nn_model (layers_dimensions):
    dtype = torch.float
    device = torch.device("cpu")
    
    model = torch.nn.Sequential().to(device)
    
    model.append(torch.nn.Linear(layers_dimensions[0], layers_dimensions[1]))
    for i in range(1, len(layers_dimensions) - 1):
        model.append(torch.nn.ReLU())
        model.append(torch.nn.Linear(layers_dimensions[i], layers_dimensions[i+1]))

    return model

class emulate_loss:
    def item (self): return 99999999

def nn_learning(parsed, iterations = 50000, 
                        learning_rate = 1e-6, 
                        min_accuracy = None, 
                        forced_exit = False, 
                        auto_reiterate = False, 
                        max_renews = 0, 
                        per_iter = 0.3):
    if (type(parsed) is not dict or
        len(parsed.get('X', [])) == 0 or
        len(parsed.get('Y', [])) == 0):
            print('Incorrect data to prediction.')
            return
    

    x = torch.FloatTensor(parsed['X']) # list of lists of input data ==> tensor
    y = torch.FloatTensor(parsed['Y']) # list of lists of output data ==> tensor

    layers_dimensions = [
                         len(parsed['X'][0]),
                         100,
                         50,
                         20,
                         len(parsed['Y'][0])
                        ]

    model = get_nn_model(layers_dimensions)
    loss_fn = torch.nn.MSELoss(reduction='sum')
    optim = torch.optim.SGD(model.parameters(), lr = learning_rate)

    iterations_ten_percents = iterations // 10
    print('Learning NN.')

    t = 0
    all_iterations = 0
    loss_deltas = [0 for i in range(10)]
    per_iter *= 10
    prev_loss = 0
    base_iterations = iterations
    old_model = [None, emulate_loss()]
    
    while t < iterations:
        y_pred = model(x)
        loss = loss_fn(y_pred, y)
        optim.zero_grad()
        loss.backward()
        optim.step()

        if t % iterations_ten_percents == 0: print('Still learning... {}0% ==> {}'.format(t // iterations_ten_percents, loss.item()))
        t += 1
        all_iterations += 1

        loss_deltas.append(prev_loss - loss.item())
        loss_deltas.pop(0)
        prev_loss = loss.item()

        if t > iterations // 2:
            if min_accuracy:
                if loss.item() <= min_accuracy: # if min_accuracy reached
                    if forced_exit: t = iterations+1 # if forced: learning ends
                    else: iterations -= 100          # else: slowly stoping
            
            if auto_reiterate:
                if sum(loss_deltas) > per_iter * 2: iterations += 1 # if learning faster and effective
                elif sum(loss_deltas) < per_iter // 2: iterations -= 100 # if learning is very slow

            if max_renews > 0:
                if (loss.item() > (min_accuracy*100 if min_accuracy else 200) and sum(loss_deltas) < 3*per_iter or
                    loss.item() > (min_accuracy*20  if min_accuracy else 40 ) and sum(loss_deltas) < 2*per_iter or
                    loss.item() > (min_accuracy*5   if min_accuracy else 10 ) and sum(loss_deltas) < 1*per_iter): # if learning is very slow and loss is too large
                    max_renews -= 1

                    print('\nToo slowly ({}). Learning restarted. There are {} restarts left.'.format(round(loss_deltas[-1], 2), max_renews))
                    model = get_nn_model(layers_dimensions)
                    if loss.item() < old_model[1].item(): old_model = [model, loss]
                    optim = torch.optim.SGD(model.parameters(), lr = learning_rate)
                    t = 0
                    iterations = base_iterations
    
    if old_model[1].item() < loss.item(): model, loss = old_model
    
    print('Learning finished.\nFinal losses: ' + str(loss.item()) + '\nIterated', all_iterations, 'times.\n')

    return y_pred, model

#===========================================================

def sigmoid_learning(parsed, iterations = 50000, learning_rate = 1e-6, min_accuracy = None):
    if (type(parsed) is not dict or
        len(parsed.get('X', [])) == 0 or
        len(parsed.get('Y', [])) == 0):
            print('Incorrect data to prediction.')
            return

    import numpy as np

    def sigmoid(x):
        output = 1/(1+np.exp(-x))
        return output

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




