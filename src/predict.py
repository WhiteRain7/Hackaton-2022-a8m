import torch

def learning(parsed, iterations = 50000, learning_rate = 1e-6, min_accuracy = None):
    '''
        It's an old "learning" function, you should use "nn_learning" instead.
    '''
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

def nn_learning(parsed, iterations = 50000,     # Base count of iterations of NN
                        learning_rate = 1e-6,   # 
                        min_accuracy = None,    # If loss reached this value, NN will slowly decrease number of iterations
                        forced_exit = False,    # If True, NN learning will immediately end when reached min_accuracy
                        auto_reiterate = False, # If True, NN will do extra iterations, if loss regress is faster enough, 
                                                # also it will reduce iteration number, if loss will decreasing too slowly
                        max_renews = 0,         # If NN is learning too slowly, it do restart with new layers. Here you can
                                                # specify how many restarts available (if 0 - NN will not do any restarts).
                                                # After finishing, NN will use layer with the lowest loss.
                        per_iter = 0.3,         # Specify the suitable number of loss decreasing (used with previous args)
                        print_logs = True):
    if (type(parsed) is not dict or
        len(parsed.get('X', [])) == 0 or
        len(parsed.get('Y', [])) == 0):
            if print_logs: print('Incorrect data to learning.')
            else: raise TypeError('Incorrect data to learning.')
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
    if print_logs: print('Learning NN.')

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

        if t % iterations_ten_percents == 0 and print_logs: print('Still learning... {}0% ==> {}'.format(t // iterations_ten_percents, loss.item()))
        t += 1
        all_iterations += 1

        loss_deltas.append(prev_loss - loss.item())
        loss_deltas.pop(0)
        prev_loss = loss.item()

        if t > iterations // 3:
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

                    if print_logs: print('\nToo slowly ({}). Learning restarted. There are {} restarts left.'.format(round(loss_deltas[-1], 2), max_renews))
                    model = get_nn_model(layers_dimensions)
                    if loss.item() < old_model[1].item(): old_model = [model, loss]
                    optim = torch.optim.SGD(model.parameters(), lr = learning_rate)
                    t = 0
                    iterations = base_iterations
    
    if old_model[1].item() < loss.item(): model, loss = old_model
    
    if print_logs: print('Learning finished.\nFinal losses: ' + str(loss.item()) + '\nIterated', all_iterations, 'times.\n')

    return y_pred, model

#===========================================================

def predict (data):
    '''
        Predicts single list of input values.
    '''
    x = torch.FloatTensor([data]) # list of input data ==> tensor
    return model(x)[0]

def predict_all (data, model):
    '''
        Predicts list of lists of input values.
    '''
    x = torch.FloatTensor(data) # list of lists of input data ==> tensor
    return model(x)




