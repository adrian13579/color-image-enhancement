import matplotlib.image as mpimg
import numpy as np
import pywt
from scipy.optimize import newton

def convert_to_uint(x):
    m,n = x.shape
    for i in range(m):
        for j in range(n):
            x[i][j] = int(abs(x[i][j]))
            x[i][j] = max(x[i][j],0)
            x[i][j] = min(x[i][j],255)
    return x


def adaptation_average_grey(a_j,alpha):
    m,n = a_j.shape
    new_a_j = np.zeros((m,n))
    
    average = a_j.mean()
    for i in range(m):
        for j in range(n):
            new_a_j[i][j] = alpha*average + (1-alpha)*a_j[i][j]
            
    return new_a_j

def local_contrast_enhancement(d_jk,a_jk,w_j,k):
    m,n = d_jk.shape
    new_d_jk = np.zeros((m,n))
    
    T = d_jk.max()/k
    for i in range(m):
        for j in range(n):
            if d_jk[i][j] >= T:
                def F(x):
                    return x-d_jk[i][j] - w_j*a_jk[i][j]/x
                
                try:
                    new_d_jk[i][j] = newton(func=F, x0=d_jk[i][j])
                except RuntimeError:
                    new_d_jk[i][j] = d_jk[i][j] 
            else:
                new_d_jk[i][j] = d_jk[i][j]
            
    return new_d_jk
    

    
def enhance_image(img,alpha=0.1,wj=0.5,k=10,wavelet='sym8'):
    img = mpimg.imread(img)
    r = img[:,:,0]
    g = img[:,:,1]
    b = img[:,:,2]
    
    wp_r = pywt.WaveletPacket2D(data=r, wavelet=wavelet, mode='symmetric')
    wp_g = pywt.WaveletPacket2D(data=g, wavelet=wavelet, mode='symmetric')
    wp_b = pywt.WaveletPacket2D(data=b, wavelet=wavelet, mode='symmetric')
    
    new_r = provenzi_caselles(wp_r,alpha,wj,k)
    new_g = provenzi_caselles(wp_g,alpha,wj,k)
    new_b = provenzi_caselles(wp_b,alpha,wj,k)
    
    rgb = np.stack((new_r,new_g,new_b),axis=2).astype('uint8')
    return rgb
    
def provenzi_caselles(wp,alpha,wj,k):
    scale = wp.maxlevel
    scale_index = 'a'*(scale-1)   
    
    a_j = adaptation_average_grey(wp[scale_index+'a'].data,alpha)
    while len(scale_index) >= 0:

        wp[scale_index+'a'] = a_j
        wp[scale_index+'h'] = local_contrast_enhancement(wp[scale_index+'h'].data,a_j,wj,k)
        wp[scale_index+'v'] = local_contrast_enhancement(wp[scale_index+'v'].data,a_j,wj,k)
        wp[scale_index+'d'] = local_contrast_enhancement(wp[scale_index+'d'].data,a_j,wj,k)
        wp[scale_index].reconstruct()
        a_j = wp[scale_index].data
        if len(scale_index) > 0:
            scale_index= scale_index[:-1]
        else:
            break
    
    
    return convert_to_uint(wp.data)
    

