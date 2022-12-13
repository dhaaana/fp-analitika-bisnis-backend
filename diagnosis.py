import keras
import mahotas as mh
import numpy as np
from keras.models import model_from_json
from imread import imread


def diagnosis(file, type):
    json = 'model-tbc.json' if type == 'tbc' else 'model-pneumonia.json'
    h5 = 'model-tbc.h5' if type == 'tbc' else 'model-pneumonia.h5'
    lab = {'Normal' : 0, 'TBC': 1} if type == 'tbc' else {'Normal': 0, 'Viral Pneumonia': 1, 'Covid': 2}
    IMM_SIZE = 224
    # Download image
    ##YOUR CODE GOES HERE##
    image = imread(file)
    
    # Prepare image to classification
    ##YOUR CODE GOES HERE##
    if len(image.shape) > 2:
        image = mh.resize_to(image, [IMM_SIZE, IMM_SIZE, image.shape[2]]) # resize of RGB and png images
    else:
        image = mh.resize_to(image, [IMM_SIZE, IMM_SIZE]) # resize of grey images    
    if len(image.shape) > 2:
        image = mh.colors.rgb2grey(image[:,:,:3], dtype = np.uint8)  # change of colormap of images alpha chanel delete

    # Load model  
    ##YOUR CODE GOES HERE##
    json_file = open(json, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(h5)

    # Normalize the data
    ##YOUR CODE GOES HERE##
    image = np.array(image)/255
    
    # Reshape input images
    ##YOUR CODE GOES HERE##
    image = image.reshape(-1, IMM_SIZE, IMM_SIZE, 1)
    
    # Predict the diagnosis
    ##YOUR CODE GOES HERE##
    preds = model.predict(image)
    preds=np.argmax(preds,axis=1)
    preds = preds.reshape(1,-1)[0]

    # Find the name of the diagnosis  
    ##YOUR CODE GOES HERE##
    diag = {i for i in lab if lab[i]==preds}

    return diag