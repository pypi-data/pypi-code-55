from Isomap import Psychological_Study, Faces

# First we instantiate the class, making sure to provide the data or filepath. If both are provided, it takes the filepath over the data.
# Make sure to provide the correct filepath.

# Load the brain dataset.
path = r'C:\\Users\\Flash\\Desktop\\GT Masters\\CSE6740\\Homework 3\\homework3\\data\\n90pol.csv'

problem_two = Psychological_Study(path = path)

# Let's print the response data, minus the column names.
print(problem_two.np_y)
# Let's print the first 5 points of the data, minus the response column and the column names.
print(problem_two.np_data[:5])     

# Now we will project the data to the top 2 principal directions. 
problem_two.pca()
problem_two.plot_top_2_principal_components()

# Print the two dimensional histogram
problem_two.two_dimensional_histrogram()

# Now lets implement the KDE.
problem_two.kernel_density_estimation()

# Visualize the conditional distribution of the volume of the amygdala as a function of political orientation
problem_two.kde_conditional_distribution()
# One bin's volume -> 0.8 * 0.9 = 0.72
# Another bin's volume -> 1.1 * 0.80 = 0.88
# Percent difference -> about ~18%
# What this is saying is that there is about a 18% difference in the volume of the amygdala as a funciton of political orientation.

# View the conditional distribution of the volume of the acc as a function of political orientation.
problem_two.kde_conditional_distribution(feature = 'acc')
# As before, this actually eludes to the same volume difference of the acc as a function of political views.

matFile = sio.loadmat('isomap.mat')
#data = matFile['data']
# Helps see global options: print(sorted(matFile.keys()))
# There are 4096 images: print(len(matFile['images']))
# First dimension: print(matFile['images'][:, 0])
# In order to visualize we need to reshape the column stored picture: data.reshape(64,64)
# To visualize: plt.imshow(data)

# Let's try on first image
data = matFile['images'][:,0]
data = data.reshape(64,64)
print(data.shape)

def show_image_function(data):
        try:
            if data.shape[0] != 64 or data.shape[1] != 64:
                data = data.reshape(64,64)
            plt.imshow(data)
        except:
            print("The image dimensions provided during the initiationalization of this class did not accurary reflect the image loaded. \
                  Remember that the images are stored columnwise, so make sure to reshape into a 64 x 64 matrix. \
                  Please re-enter these dimensions in order to show the image.")
            
show_image_function(data)

# Let's print 80 images, using all makes the output too small. 
new_data = matFile['images']
fig=plt.figure(figsize=(64, 64))
columns = 2
# For all use rows = 349
rows = 40
for i in range(1, columns*rows +1):
    img = new_data[:, i-1]
    img = img.reshape(64,64)
    fig.add_subplot(rows, columns, i)
    plt.imshow(img)
plt.show()

problem_one = Faces(data = matFile)

# Let's generate a similarity graph with the Euclidean distance, at least 100 neighbors per. 
problem_one_distance_matrix, problem_one_percent_fully_connected_neighbors = problem_one.similarity_graph(distance = "euclidean")

problem_one_distance_matrix.iloc[:5,:5]

# Now let's plot the adjacency matrix, or visualize the graph and illustrate a few images corresponds to nodes at diﬀerent parts of the graph.
problem_one_distance_matrix.plot(kind='scatter',x = 0, y = 0,color='red')
plt.show()

# Let's see the first new image created by the Euclidean distance metric.
problem_one.show_new_image(np.array(problem_one_distance_matrix.iloc[0,:]))

# Let's see the first 5.
fig=plt.figure(figsize=(64, 64))
for i in range(0, 5):
    img = np.array(problem_one_distance_matrix.iloc[i, :])
    img = img.reshape(64,64)
    fig.add_subplot(rows, columns, i+1)
    plt.imshow(img)
plt.show()
# As you can observe, there is a very defined structure to the faces after composing the similarity matrix. 

# Implement the ISOMAP algorithm and apply it to this graph to obtain a d = 2-dimensional embedding. Present a plot of this embedding
transformed = problem_one.isomap(graph = problem_one_distance_matrix)

# Here a plot of the transformed matrix using the ISOMAP algorithm.
plt.scatter(transformed[:,0], transformed[:, 1])
#rint(transformed[:, 0])

# Let's pick two points that are close to one another an see the similiarities among the images.
np.where(transformed[:, 0] > 125) 

problem_one.show_new_image(np.array(problem_one_distance_matrix.iloc[70,:]))

problem_one.show_new_image(np.array(problem_one_distance_matrix.iloc[71,:]))

data_71 = matFile['images'][:,70]
data_71 = data_71.reshape(64,64)
data_72 = matFile['images'][:, 71]
data_72 = data_72.reshape(64,64)

show_image_function(data_71)

# The only problem left is to re-run the above with an L1 distance metric: Manhattan. 
# This time we will consolidate it: to save both of our time!
problem_one_L1 = Faces(data = matFile)
problem_one_L1_distance_matrix, problem_one_L1_percent_fully_connected_neighbors = problem_one.similarity_graph(distance = "cityblock")

# Now let's plot the adjacency matrix, or visualize the graph and illustrate a few images corresponds to nodes at diﬀerent parts of the graph.
problem_one_L1_distance_matrix.plot(kind='scatter',x = 0, y = 0,color='red')
plt.show()

# Let's see the first 5.
fig=plt.figure(figsize=(64, 64))
for i in range(0, 5):
    img = np.array(problem_one_L1_distance_matrix.iloc[i, :])
    img = img.reshape(64,64)
    fig.add_subplot(rows, columns, i+1)
    plt.imshow(img)
plt.show()
# As stated earlier, the structure is well defined and shows consistency. It should appear that the same points in manifold space are related by localized pixel intensity.

# Implement the ISOMAP algorithm and apply it to this graph to obtain a d = 2-dimensional embedding. Present a plot of this embedding
transformed_L1 = problem_one.isomap(graph = problem_one_L1_distance_matrix)

plt.scatter(transformed_L1[:,0], transformed_L1[:, 1])
#print(transformed[:, 0])
# Observe that there is a well defined pattern based on the previously mentioned predictors: orientation, localization of pixel intensity, and shape.

# Could make the following into constraint equations. Here would be the intersection of sets. 
print(np.where(transformed_L1[:, 0] < 1000))
print(np.where(transformed_L1[:, 1] < 250))
print(np.where(transformed_L1[:, 1] > 0))
# Let's use 8, 9, and 10

data_9 = matFile['images'][:,8]
data_9 = data_9.reshape(64,64)
data_11 = matFile['images'][:,10]
data_11 = data_11.reshape(64,64)
data_10 = matFile['images'][:, 9]
data_10 = data_10.reshape(64,64)

show_image_function(data_9)