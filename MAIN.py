#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import os
import numpy as np
import matplotlib.pyplot as plt
from keras.models import *
from keras.layers import *
from keras.utils.vis_utils import plot_model
from IPython.display import SVG
from tensorflow.python.framework import ops
import scipy.io
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from IPython.display import clear_output
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.ndimage import interpolation


from keras import layers

def VisualGraphs(RstActual,RstBest,ZTuckerRepr,ConvCurve,Original,ColorBands):
    clear_output(wait=True)
    
    [m,n,L]=Original.shape
    
    #Choose 3 uniform bands from low-Rank Tucker Representation of Z            
    #bands = np.floor( np.linspace(L/4, 3*L/4, num=3)).astype(int)
    #xo = ZTuckerRepr[:,:,[bands[0],bands[1],bands[2]]]
    xo = ZTuckerRepr[:,:,ColorBands]
    xo[:,:,0] = (xo[:,:,0]-np.min(xo[:,:,0]))/(np.max(xo[:,:,0])-np.min(xo[:,:,0]))
    xo[:,:,1] = (xo[:,:,1]-np.min(xo[:,:,1]))/(np.max(xo[:,:,1])-np.min(xo[:,:,1]))
    xo[:,:,2] = (xo[:,:,2]-np.min(xo[:,:,2]))/(np.max(xo[:,:,2])-np.min(xo[:,:,2]))
    
    ErrActual = np.divide(np.power(np.sum(np.power(RstActual-Original,2),axis=2),0.5),np.power(np.sum(np.power(Original,2),axis=2),0.5))
    
    ErrBest = np.divide(np.power(np.sum(np.power(RstBest-Original,2),axis=2),0.5),np.power(np.sum(np.power(Original,2),axis=2),0.5))
    
    fig, axs = plt.subplots(1,4,figsize=(22,22))
    fig.subplots_adjust(left=.05, bottom=0.1, right=.9, top=0.9, wspace=0.05)            
    
    RGB = Original[:,:,ColorBands]#/np.max(Original)
    RGB = RGBZoom(RGB)
    axs[0].imshow(RGB)
    axs[0].set_title('Original')
    axs[0].axis('off')
    
    RGB = RstBest[:,:,ColorBands]#/np.max(RstBest)
    RGB = RGBZoom(RGB)
    axs[1].imshow(RGB)
    axs[1].set_title('Best Reconstruction')
    axs[1].axis('off')
    
    im = axs[2].imshow(ErrBest, cmap='hot', vmin=0, vmax=1)
    divider = make_axes_locatable(axs[2])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, cax=cax)
    axs[2].set_title('Relative Error Map\n Best Reconstruction')
    axs[2].axis('off')
    
    axs[3].imshow(xo)
    axs[3].set_title('3Bands from Tucker \n Representation of Z')
    axs[3].axis('off')
    
    fig, axs = plt.subplots(1,4,figsize=(14,14))
    fig.subplots_adjust(left=.05, bottom=0.1, right=.9, top=0.9, wspace=0.05)            
    
    asp = np.diff(axs[0].get_xlim())[0] / np.diff(axs[0].get_ylim())[0]
    axs[0].set_aspect(asp)
    axs[0].axis('off')
    
    RGB = RstActual[:,:,ColorBands]/np.max(RstBest)
    RGB = RGBZoom(RGB)
    axs[1].imshow(RGB)
    axs[1].set_title('Actual Reconstruction')
    axs[1].axis('off')
    
    im = axs[2].imshow(ErrActual, cmap='hot', vmin=0, vmax=1)
    divider = make_axes_locatable(axs[2])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    fig.colorbar(im, cax=cax)
    axs[2].set_title('Relative Error Map\n Actual Reconstruction')
    axs[2].axis('off')
    
    axs[3].plot(ConvCurve)
    axs[3].set_title('Convergence Curve\n (Best/Actual)PSNR: (%.2f,' %np.max(ConvCurve) +'%.2f)'%ConvCurve[-1])
    asp = np.diff(axs[3].get_xlim())[0] / np.diff(axs[3].get_ylim())[0]
    axs[3].set_aspect(asp)
    axs[3].yaxis.tick_right()
    
    plt.show()

def addGaussianNoise(y,SNR):
    
    sigma = np.sum(np.power(y,2))/(np.product(y.shape)*10**(SNR/10));
    w = np.random.normal(0, np.sqrt(sigma),size =y.shape);
    return y+w;


    return y+noise_y

def RGBZoom(X):
    return X
    w = 6
    y = [6, 100+6]
    x = [6, 100+6]
    
    for i in range(3):
        Y = interpolation.zoom(X[75:107,101:133,i],100/32)   
        X[y[0]:y[1],x[0]:x[1],i] = Y
    
    
    X[y[0]-w:y[0],x[0]-w:x[1]+1,0] = np.ones(shape=(w,x[1]-x[0]+w+1))
    X[y[0]-w:y[0],x[0]-w:x[1]+1,1] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    X[y[0]-w:y[0],x[0]-w:x[1]+1,2] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    
    X[y[0]:y[1]+1+w,x[0]-w:x[0],0] = np.ones(shape=(y[1]-y[0]+w+1,w))
    X[y[0]:y[1]+1+w,x[0]-w:x[0],1] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    X[y[0]:y[1]+1+w,x[0]-w:x[0],2] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    
    X[y[1]+1:y[1]+w+1,x[0]:x[1]+w+1,0] = np.ones(shape=(w,x[1]-x[0]+w+1))
    X[y[1]+1:y[1]+w+1,x[0]:x[1]+w+1,1] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    X[y[1]+1:y[1]+w+1,x[0]:x[1]+w+1,2] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    
    X[y[0]-w:y[1]+1,x[1]+1:x[1]+w+1,0] = np.ones(shape=(y[1]-y[0]+w+1,w))
    X[y[0]-w:y[1]+1,x[1]+1:x[1]+w+1,1] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    X[y[0]-w:y[1]+1,x[1]+1:x[1]+w+1,2] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    
    w = 2
    y = [74, 107]
    x = [100, 133]    
    X[y[0]-w:y[0],x[0]-w:x[1]+1,0] = np.ones(shape=(w,x[1]-x[0]+w+1))
    X[y[0]-w:y[0],x[0]-w:x[1]+1,1] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    X[y[0]-w:y[0],x[0]-w:x[1]+1,2] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    
    X[y[0]:y[1]+1+w,x[0]-w:x[0],0] = np.ones(shape=(y[1]-y[0]+w+1,w))
    X[y[0]:y[1]+1+w,x[0]-w:x[0],1] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    X[y[0]:y[1]+1+w,x[0]-w:x[0],2] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    
    X[y[1]+1:y[1]+w+1,x[0]:x[1]+w+1,0] = np.ones(shape=(w,x[1]-x[0]+w+1))
    X[y[1]+1:y[1]+w+1,x[0]:x[1]+w+1,1] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    X[y[1]+1:y[1]+w+1,x[0]:x[1]+w+1,2] = np.zeros(shape=(w,x[1]-x[0]+w+1))
    
    X[y[0]-w:y[1]+1,x[1]+1:x[1]+w+1,0] = np.ones(shape=(y[1]-y[0]+w+1,w))
    X[y[0]-w:y[1]+1,x[1]+1:x[1]+w+1,1] = np.zeros(shape=(y[1]-y[0]+w+1,w))
    X[y[0]-w:y[1]+1,x[1]+1:x[1]+w+1,2] = np.zeros(shape=(y[1]-y[0]+w+1,w))
            
            
    return X

    
def Hxfunction2(x,largo,ancho,profun,H):
    Aux = tf.reshape(x,(largo,ancho,profun))
    Aux = tf.transpose(Aux,perm=[2,1,0])
    Aux = tf.reshape(Aux,(largo*ancho*profun,1))
    
    #print(Aux.shape)
    
    Aux = tf.sparse.sparse_dense_matmul(H,tf.cast(Aux,dtype=tf.float64))
    Aux = tf.reshape(Aux,(1,1,1,H.shape[0]))
    return Aux



class XoLayer(layers.Layer):
    def __init__(self, shape_original = (256,256, 10), shape_compressed = (256,256,10),Nbits = 8, MaxValue =1,MinValue=-1):
        super(XoLayer, self).__init__()

        self.largo  = shape_original[0]
        self.ancho  = shape_original[1]
        self.profun  = shape_original[2]
        self.Max =MaxValue;
        self.Min = MinValue;
        self.Nbits = Nbits

        self.largo_fac = shape_compressed[0]
        self.ancho_fac = shape_compressed[1]
        self.profun_fac = shape_compressed[2]

          
        self.kernel = self.add_weight(shape=(self.largo_fac*self.ancho_fac,self.profun_fac), 
                             initializer=tf.keras.initializers.Constant(value=0.01),#'glorot_normal',
                             trainable=True)
           
        self.Dx    = self.add_weight(shape=(self.largo,self.largo_fac),
                             initializer=tf.keras.initializers.Constant(value=0.01), # uniform
                             trainable=True)
        self.Dy    = self.add_weight(shape=(self.ancho_fac,self.ancho),
                             initializer=tf.keras.initializers.Constant(value=0.01),
                             trainable=True)
        self.Dz    = self.add_weight(shape=(self.profun_fac,self.profun),
                            initializer=tf.keras.initializers.Constant(value=0.01),
                             trainable=True)


        
    def call(self, inputs):
        
        kernel_ = tf.quantization.fake_quant_with_min_max_args(self.kernel, min=self.Min, max=self.Max, num_bits=self.Nbits, narrow_range=False, name=None)
        Dx_ = tf.quantization.fake_quant_with_min_max_args(self.Dx, min=self.Min, max=self.Max, num_bits=self.Nbits, narrow_range=False, name=None)
        Dy_ = tf.quantization.fake_quant_with_min_max_args(self.Dy, min=self.Min, max=self.Max, num_bits=self.Nbits, narrow_range=False, name=None)
        Dz_ = tf.quantization.fake_quant_with_min_max_args(self.Dz, min=self.Min, max=self.Max, num_bits=self.Nbits, narrow_range=False, name=None)
        
        #Aux = tf.transpose(tf.matmul(Dz_,kernel_))
        #Aux = tf.reshape(Aux,( self.largo_fac,self.ancho_fac*self.profun))

        #Aux = tf.matmul(Dx_,Aux)
        #Aux = tf.reshape(Aux,(self.largo,self.ancho_fac,self.profun))
        #Aux = tf.transpose(Aux,perm=[1,0,2])
        #Aux = tf.reshape(Aux,(self.ancho_fac,self.ancho*self.profun))
        #Aux = tf.matmul(Dy_,Aux)
        #Aux = tf.reshape(Aux,(self.ancho,self.largo,self.profun))
        #Aux = tf.reshape(tf.transpose(Aux,perm=[1,0,2]),(1,self.ancho,self.largo,self.profun))
        
        Aux = (tf.matmul(kernel_,Dz_))
        Aux = tf.reshape(Aux,( self.largo_fac,self.ancho_fac*self.profun))
        Aux = tf.matmul(Dx_,Aux)
        Aux = tf.reshape(Aux,(self.largo,self.ancho_fac,self.profun))
        Aux = tf.transpose(Aux,perm=[0,2,1])
        Aux = tf.reshape(Aux,(self.largo*self.profun,self.ancho_fac))
        Aux = tf.matmul(Aux,Dy_)
        Aux = tf.reshape(Aux,(self.largo,self.profun,self.ancho))
        Aux = tf.reshape(tf.transpose(Aux,perm=[0,2,1]),(1,self.largo,self.ancho,self.profun))
        
        return  Aux
    

def fun_PSNR(img,res):

    [M,N,L]=img.shape
    temp=1./(M*N*L)*np.sum(np.power(img-res,2))
    psnr= 10*np.log10(np.max(np.power(img,2)/temp))
    return psnr    


def residualNet(pretrained_weights = None,input_size = (256,256,1), L=10, H=0, fact = 0.5):
    
    inputs = Input(input_size)
    inicial = XoLayer(largo = input_size[0], ancho = input_size[1], profun = L, fact = fact)(inputs)
    
    drop1 = Dropout(0.2)(inicial)
    conv1 = Conv2D(L,3,activation='relu',use_bias=True,padding='same',kernel_initializer='he_normal')(drop1)
    conv1 = Conv2D(L,1,activation='relu',use_bias=True,padding='same',kernel_initializer='he_normal')(conv1)
    
    
    conv8 = Conv2D(L,3,activation='relu',use_bias=True,padding='same',kernel_initializer='he_normal')(conv1)
    conv8 = Conv2D(L,1,activation='relu',use_bias=True,padding='same',kernel_initializer='he_normal')(conv8)
    
    
    conv8 = Add()([conv8,conv1])
    
    final =Lambda(lambda x: Hxfunction(x,largo=input_size[0],ancho=input_size[1],profun=L,H=H)) (conv8)
    
    model = Model(input = inputs, output = final)

    if(pretrained_weights):
    	model.load_weights(pretrained_weights)

    return model



def UNetL(pretrained_weights = None,input_size = (256,256,1), L=10, H=0, fact = 0.5):
    L_2 = 2*L;
    L_3 = 3*L;
    L_4 = 4*L;
    
    startLayer = Input(input_size)  
    inicial = XoLayer(largo=input_size[0], ancho=input_size[1], profun=L, fact=fact)(startLayer)
    
    conv1 = Dropout(0.2)(inicial)
    conv1 = Conv2D(L, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
    conv1 = Conv2D(L, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(L_2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
    conv2 = Conv2D(L_2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv2)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(L_3, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
    conv3 = Conv2D(L_3, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv3)    
    pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
    conv4 = Conv2D(L_4, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool3)
    conv4 = Conv2D(L_4, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv4)    

    up5 = Conv2D(L_3, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv4))
    merge5 = concatenate([conv3, up5], axis=3)
    conv5 = Conv2D(L_3, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge5)
    conv5 = Conv2D(L_3, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv5)

    up6 = Conv2D(L_2, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv5))
    merge6 = concatenate([conv2, up6], axis=3)
    conv6 = Conv2D(L_2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge6)
    conv6 = Conv2D(L_2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv6)

    up7 = Conv2D(L, 2, activation='relu', padding='same', kernel_initializer='he_normal')(
        UpSampling2D(size=(2, 2))(conv6))
    merge7 = concatenate([conv1, up7], axis=3)
    conv7 = Conv2D(L, 3, activation='relu', padding='same', kernel_initializer='he_normal')(merge7)
    conv7 = Conv2D(L, 3, activation='relu', padding='same', kernel_initializer='he_normal',)(conv7)

    conv8 = Conv2D(L, 1)(conv7)
    
    final =Lambda(lambda x: Hxfunction(x,largo=input_size[0],ancho=input_size[1],profun=L,H=H)) (conv8)

    model = Model(input=startLayer, output=final)

    if (pretrained_weights):
        model.load_weights(pretrained_weights)

    return model


def Auto_encoder(pretrained_weights=None, input_size=(256, 256, 1), L=10, H=0, fact=0.5):
    L_2 = 2 * L;
    L_3 = 3 * L;
    L_4 = 4 * L;
    
    inputs = Input(input_size)    
    inicial = XoLayer(largo=input_size[0], ancho=input_size[1], profun=L, fact=fact)(inputs)
    
    # the encoder part
    conv1 = Dropout(0.2)(inicial)    
    conv1 = Conv2D(L, 3, activation='relu', padding='same', kernel_initializer='he_normal')(conv1)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(L_2, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool1)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(L_3, 3, activation='relu', padding='same', kernel_initializer='he_normal')(pool2)
    pool3 = MaxPooling2D(pool_size=(4, 4))(conv3)
    
    convup2=Conv2DTranspose(filters=L_3, kernel_size=(3, 3), strides=4, activation='relu', padding='same')(pool3)
    convup3=Conv2DTranspose(filters=L_2, kernel_size=(3, 3), strides=2, activation='relu', padding='same')(pool2)
    conv8=Conv2DTranspose(filters=L, kernel_size=(3, 3), strides=2, activation='relu', padding='same')(convup3)


    final = Lambda(lambda x: Hxfunction(x, largo=input_size[0],ancho=input_size[1],profun=L, H=H))(conv8)

    model = Model(input=inputs, output=final)

    if (pretrained_weights):
        model.load_weights(pretrained_weights)

    return model



from keras import backend as K
class myCallback(tf.keras.callbacks.Callback):
     

    def __init__(self,Xorig=0,Freq=0,ColorBands = 0,BestPSNR = 0, Best = 0,Nbits = 0):
        super(myCallback, self).__init__()
        self.my_PSNR = []
        self.Xorig = Xorig;
        self.Best = Best;
        self.BestPSNR = BestPSNR;
        self.Freq = Freq
        self.ColorBands = ColorBands
        self.BestWeights = [];
        self.Nbits = Nbits
        

    def on_epoch_end(self, epoch, logs={}):
        Freq = self.Freq
        
        
        
        if np.mod(epoch,Freq)==0:            
            img = self.Xorig;
                        
            
            [m,n,L] = img.shape
           
            func = K.function([self.model.layers[0].input],[self.model.layers[1].output])
            xo = func(np.zeros(shape=(m,n,L)))
            xo = np.asarray(xo).reshape((m,n,L),order="F")
            
            func = K.function([self.model.layers[0].input],[self.model.layers[len(self.model.layers)-1].output])
            result = func(np.zeros(shape=(m,n,L)))
            result = np.asarray(result).reshape((m,n,L),order="F")
            
            
            psnr = fun_PSNR(img,result)
            self.my_PSNR.append(psnr) 
            
            
            if psnr >= self.BestPSNR:                
                self.Best = result
                self.BestWeights = self.model.get_weights()
                self.BestPSNR = psnr
                setattr(self.model, 'Best', self.Best)
                setattr(self.model, 'BestWeights', self.BestWeights)
                setattr(self.model, 'BestPSNR', self.BestPSNR)
            
                                
            setattr(self.model, 'PSNRs', self.my_PSNR)
            
        if np.mod(epoch,Freq)==0: 

            self.model.layers[2].rate=0.5
            
            VisualGraphs(result,self.Best,xo,self.my_PSNR,img,self.ColorBands)
            print('Epoch %05d: PSNR %6.3f : Max PSNR %6.3f, Nbits = %05d' % (epoch, psnr,np.max([psnr,self.BestPSNR]),self.Nbits))
           
