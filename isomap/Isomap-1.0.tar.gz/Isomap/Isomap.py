import csv
import numpy as np
import numpy.matlib
import pandas as pd
import scipy.sparse.linalg as ll
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import preprocessing
from sklearn.manifold import Isomap
import scipy.io as sio 
from scipy.spatial.distance import pdist, squareform

# Let's start with part two of the homework then come back to part one.
# Here is a class that defines and augments our psychological study. 
# Each part will be explained with an example solving one part of the homework.
class Psychological_Study:
    
    def __init__(self, data = "None", path = "None"):
        if path != "None":
            data = pd.read_csv(path, header = None).to_numpy()
        self.data = data
        
        # Take all of the response data, minus the column names.
        self.np_y = np.array(self.data[1:, 2]).astype('int')
        # Take all of the data, minus the response column and the column names.
        self.np_data = np.array(data[1:,:2]).astype('float')
        
        
    def pca(self, num_components = 2):
        ndata = preprocessing.scale(self.np_data)
        self.m, n = ndata.shape
        #self.m, n = self.np_data.shape
        C = np.matmul(ndata.T, ndata)/self.m
        #C = np.matmul(self.np_data.T, self.np_data)/self.m
        # pca the data
        S, self.V = ll.eigs(C,k = num_components)
    
    def plot_top_2_principal_components(self, gridno = 40):
        self.pdata = np.round(np.dot(self.np_data,-self.V.real),2)
        plt.scatter(self.pdata[np.where(self.np_y == 2),0],self.pdata[np.where(self.np_y == 2),1])
        plt.scatter(self.pdata[np.where(self.np_y == 3),0],self.pdata[np.where(self.np_y == 3),1])
        plt.scatter(self.pdata[np.where(self.np_y == 4),0],self.pdata[np.where(self.np_y == 4),1])
        plt.scatter(self.pdata[np.where(self.np_y == 5),0],self.pdata[np.where(self.np_y == 5),1])
        
        self.min_data = self.pdata.min(0)
        self.max_data = self.pdata.max(0)
        
        self.gridno = gridno
        inc1 = (self.max_data[0]-self.min_data[0])/self.gridno
        inc2 = (self.max_data[1]-self.min_data[1])/self.gridno
        self.gridx, self.gridy = np.meshgrid( np.arange(self.min_data[0], self.max_data[0]+inc1,inc1), np.arange(self.min_data[1], self.max_data[1]+inc2,inc2) )
        gridall = [self.gridx.flatten(order = 'F'), self.gridy.flatten(order = 'F')]
        self.gridall = (np.asarray(gridall)).T
        self.gridallno, self.nn= self.gridall.shape
        self.norm_pdata = (np.power(self.pdata, 2)).sum(axis=1)
        self.norm_gridall = (np.power(self.gridall, 2)).sum(axis=1)
        self.ones_pdata = np.ones((self.pdata.shape[1], self.gridall.shape[1]))
        
        plt.show()
    
    def clear_plot(self):
        plt.clear()
        
    def two_dimensional_histrogram(self, nbin = 30):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d') # change to 2d. 
        hist, xedges, yedges = np.histogram2d(self.pdata[:,0], self.pdata[:,1], bins=nbin)
        xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])
        xpos = xpos.flatten()/2.
        ypos = ypos.flatten()/2.
        zpos = np.zeros_like (xpos)
        dx = xedges [1] - xedges [0]
        dy = yedges [1] - yedges [0]
        dz = hist.flatten()
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz )
    
    def kernel_density_estimation(self, bandwidth = 1):
        cross = np.dot(np.dot(self.pdata, self.ones_pdata),self.gridall.T)
        dist2 = np.repeat(self.norm_pdata, repeats = self.gridallno).reshape((len(self.norm_pdata), self.gridallno))+np.tile(self.norm_gridall, self.m).reshape((len(self.norm_pdata), self.gridallno)) - 2* cross
        kernelvalue = np.exp(-dist2/2)*1/(np.sqrt(2*np.pi))
        mkde = sum(kernelvalue) / self.m
        # Reshape back to grid, this will truncate some of the data.
        mkde = np.round(mkde[:((self.gridno+1) **2)])
        self.mkde = ((mkde.T).reshape(self.gridno+1, self.gridno+1)).T
    
    def kde_conditional_distribution(self, feature = 'amygdala', nbin = 2):
        #  'amygdala' = condition distribution of the volume of the amygdala as a function of political orientation
        #  'acc' = condition distribution of the volume of the acc as a function of political orientation
        if feature == 'amygdala':
            pointer = 0
        else:
            pointer = 1
        min_data = min(self.pdata[:,pointer])
        max_data = max(self.pdata[:,pointer])
        sbin = (max_data - min_data) / nbin
        #create the bins
        boundary = np.arange(min_data-0.001, max_data,sbin)
        # just loop over the data points, and count how many of data points are in each bin
        myhist = np.zeros(nbin+1)
        for i in range (self.m):
            whichbin = np.max(np.where(self.pdata[i,0] > boundary))
            myhist[whichbin] = myhist[whichbin] + 1

        myhist = np.divide(np.dot(myhist, nbin), self.m)
        # bar chart
        plt.figure()
        plt.bar(boundary+0.5 * sbin, myhist, align='center', alpha=0.5)
        plt.show()


class Faces:
    
    def __init__(self, data = "None", filename = "None", data_col = 64, data_row = 64):
        
        self.data_col = data_col
        self.data_row = data_row

        if filename != "None":
            data = sio.loadmat(filename)
        self.data = data
        
    def similarity_graph(self, distance):
        temp = pd.DataFrame(new_data[:,:])
        try:
            row_dist = round(pd.DataFrame(squareform(pdist(temp, metric = distance))))
        except:
            print("The distance didn't work so we are now using the euclidean distance.")
            row_dist = round(pd.DataFrame(squareform(pdist(temp, metric = 'euclidean'))))
        print("You will get returned the graph and the percentage of fully connected neighbors. ")
        
        total = []
        for x in range(0, 699):
            temp_total = 0
            for i in row_dist.iloc[:,x]:
                if i != 0.0:
                    temp_total += 1
            total.append(temp_total)
        not_4095 = [i for i in total if i != 4095]
        fully_connected_neighbors = len(not_4095)/698 * 100
        
        return row_dist, fully_connected_neighbors
    
    def isomap(self, graph, num_components = 2, n_neighbors_during_cal = 100):
        
        ##### NOT MY CODE OR COMMENT, SOURCE CODE FROM SCIKIT #####
        embedding = Isomap(n_components= num_components)
        
        # First the `n_neighbors` nearest neighbors of X are found in the training data, and from these the shortest 
        # geodesic distances from each point in X to each point in the training data are computed in order to construct the kernel. 
        # The embedding of X is the projection of this kernel onto the embedding vectors of the training set.
        
        X_transformed = embedding.fit_transform(graph[:n_neighbors_during_cal])
        ##### NOT MY CODE OR COMMENT, SOURCE CODE FROM SCIKIT #####
        
        return X_transformed
    
    def two_dimensional_embedding_plot(self):
        pass
    
    def show_new_image(self, new_data):
        try:
            image = new_data.reshape(64,64)
            plt.imshow(image)
        except:
            print("The image dimensions provided during the initiationalization of this class did not accurary reflect the image loaded. \
                  Remember that the images are stored columnwise, so make sure to reshape into a 64 x 64 matrix. \
                  Please re-enter these dimensions in order to show the image.")
    
    def show_image_function(self,image_index):
        image = self.data[:, image_index]
        try:
            image = image.reshape(64,64)
            plt.imshow(image)
        except:
            print("The image dimensions provided during the initiationalization of this class did not accurary reflect the image loaded. \
                  Remember that the images are stored columnwise, so make sure to reshape into a 64 x 64 matrix. \
                  Please re-enter these dimensions in order to show the image.")problem_one = Faces(data = matFile)