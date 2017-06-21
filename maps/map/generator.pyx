import noise
import numpy as np
cimport numpy as np

import matplotlib.pyplot as plt
import matplotlib

from skimage import measure # for marching-squares contour

from scipy import interpolate


import progressbar

RESOLUTION = 1024
SYMPLEX_PERSISTENCE = 0.54
SYMPLEX_OCTAVES = 8
POLAR_DEPRESSION_AMPLITUDE = 2
POLAR_DEPRESSION_WIDTH = 1.0
CRATER_NUMBER = 1000
CRATER_AVERAGE_RADIUS = 0.014
CRATER_AMPLITUDE = 0.08

CONSTANT_OFFSET = 1.9



WATER_LEVEL = 0.0
Z_FACTOR = 20.0
LATITUDE_SCALING = 0.95
INCLINATION = 2.2


DRAW_DROP_PATHS = False

cdef int EROSION_DROPLETS_NUMBER = 30000
cdef int EROSION_MAX_ITERATIONS = 64
cdef float EROSION_INERTIA = 0.1
cdef float EROSION_MINSLOPE = 0.01
cdef float EROSION_CAPACITY = 1024
cdef float EROSION_DEPOSITION = 0.1
cdef float EROSION_EROSION = 0.5
cdef float EROSION_EVAPORATION = 1.0 - 0.01
cdef float EROSION_GRAVITY = 1
cdef int EROSION_RADIUS = 0


cdef int erosion_distribution_normalization = (2*EROSION_RADIUS + 1) ** 2

cdef int X,Y,i,crater_grid_size
cdef float x,y,r
cdef float crater_size

size = RESOLUTION
shape = (size,size)

pfpf = np.array([.5,.5])


drop_paths = []

def generate():
    height = np.zeros(shape, dtype=float)

    print "generating random terrain..."

    for X in range(size):
        for Y in range(size):
            x = float(X)/size - .5
            y = float(Y)/size - .5

            height[X,Y] =   - POLAR_DEPRESSION_AMPLITUDE*np.exp(-(x*x + y*y)/POLAR_DEPRESSION_WIDTH) + \
                            noise.snoise2(x,y,octaves=SYMPLEX_OCTAVES, persistence = SYMPLEX_PERSISTENCE)

    print "generating craters..."

    bar = progressbar.ProgressBar()
    for i in bar(range(CRATER_NUMBER)):
        crater_size = np.random.exponential(CRATER_AVERAGE_RADIUS)        # crater radius
        crater_grid_size = int(np.rint(crater_size*size))
        crater_position = np.random.uniform(-0.5,0.5,(2,))
        crater_grid_position = np.rint((crater_position+pfpf) * size).astype(np.int)

        crater_amplitude = CRATER_AMPLITUDE * np.sqrt(crater_size/CRATER_AVERAGE_RADIUS)

    #    print "crater at",crater_grid_position,"radius",crater_grid_size

        for X in range(crater_grid_position[0] - crater_grid_size, crater_grid_position[0] + crater_grid_size):
            for Y in range(crater_grid_position[1] - crater_grid_size, crater_grid_position[1] + crater_grid_size):
                if (X<0) or (X>=size) or (Y<0) or (Y>=size):
    #                print "bro"
                    continue
     #           print "bra"
                pos = np.array([float(X)/size,float(Y)/size]) - pfpf
                r = np.linalg.norm(crater_position - pos) / crater_size * 1.5 
                height[X,Y] += crater_amplitude * \
                        ( min(r**4 - .5, np.exp(-2*r*r))  )

    # fix

    height += CONSTANT_OFFSET

    # erosion

    uneroded_height = np.copy(height)

    cdef int iteration 
    cdef int xx,yy
    cdef float u,v, water, capacity, sediment, dropped_sediment, velocity, vsq


    print "Erosion..."

    drop_position = np.array([0,0]).astype(int)



    cdef int batch
    cdef int batch_size = 50
    cdef int num_batches = int(EROSION_DROPLETS_NUMBER / batch_size)

    bar = progressbar.ProgressBar()


    for batch in bar(range(num_batches)):

        #update heightmap interpolant function
        height_interpolant = interpolate.RectBivariateSpline( np.arange(0,size,1), np.arange(0,size,1), height, kx = 1, ky=1)

        for i in range(batch_size):
            position = np.random.uniform(0,size,(2,))
            direction = np.random.randn(2)
            direction /= np.linalg.norm(direction)
            velocity = 1

            water = 1
            sediment = 0
            
            if i == 0:
                drop_path = ([],[])

            for iteration in range(EROSION_MAX_ITERATIONS):

                if i==0:
                    drop_path[0].append(position[0])
                    drop_path[1].append(position[1])

                if water < 0.001:
                    break

                position_frac,position_floor = np.modf(position)
                xx = position_floor[0]
                yy = position_floor[1]
                u = position_frac[0]
                v = position_frac[1]

                if (xx <= 0) or (xx >= size - 1) or (yy <= 0) or (yy >= size -1):
                    break

                gradient_old = np.array( [
                    (height[xx+1,yy]    - height[xx,yy])    *(1-v) +\
                    (height[xx+1,yy+1]  - height[xx,yy+1])  *v , \
                    (height[xx,yy+1]    - height[xx,yy])    *(1-u) +\
                    (height[xx+1,yy+1]  - height[xx+1,yy])    *u \
                        ])

                direction = direction * EROSION_INERTIA - gradient_old * (1 - EROSION_INERTIA)
                direction /= np.linalg.norm(direction)

                height_old = height_interpolant(position[0],position[1])
 
                #print height_old, height[xx,yy]

                if(height_old < WATER_LEVEL):
                    break               

                position = position + direction

                height_new = height_interpolant(position[0],position[1])


                delta_height = height_new - height_old

                if delta_height > 0:
                    # rising terrain

                    # we passed a pit
                    # drop to fill pit
                    drop_sediment = min(sediment,delta_height)

                else:
                    # dropping terrain

                    # compute capacity
                    capacity = max(-delta_height,EROSION_MINSLOPE) * velocity * water * EROSION_CAPACITY

                    if (sediment > capacity):
                        drop_sediment = (sediment - capacity)*EROSION_DEPOSITION
                    else:
                        #print "dh", delta_height
                        #print "cap", capacity
                        #print "sed", sediment
                        #print
                        drop_sediment = - min ((capacity-sediment) * EROSION_EROSION , - delta_height)

                    sediment -= drop_sediment




                # update velocity and water
                vsq = velocity*velocity + delta_height * EROSION_GRAVITY
                if (vsq < 0):
                    break
                else:
                    velocity = np.sqrt(vsq)
                water = water * EROSION_EVAPORATION

                # depose material

                #print drop_sediment
                #height[xx-EROSION_RADIUS:xx+EROSION_RADIUS+1,yy-EROSION_RADIUS:yy + EROSION_RADIUS+1] += drop_sediment/erosion_distribution_normalization
                height[xx,yy] += drop_sediment / 2.
                height[xx-1,yy] += drop_sediment / 2.
                height[xx,yy-1] += drop_sediment / 8.
                height[xx+1,yy] += drop_sediment / 8.
                height[xx,yy+1] += drop_sediment / 8.

                
            if i == 0:
                drop_paths.append(drop_path)

    eroded_height = np.copy(height)

    

    np.save(open('heightmap.npy','w'),height)
    np.save(open('uneroded_heightmap.npy','w'),uneroded_height)


def draw():
    #load

    height = np.load('heightmap.npy')
    uneroded_height = np.load('uneroded_heightmap.npy')



    # gradient and shading

    print "computing gradient and shading..."

    gradient = np.gradient(height)
    gradient_norm = np.sqrt( gradient[0]**2 + gradient[1]**2)
    slope = np.arctan(Z_FACTOR * gradient_norm)
    aspect = np.arctan2(gradient[0],gradient[1])


    cozenith = .5
    sizenith = .5
    az = 3*np.pi/4
    coaz = .5

    shade = cozenith * np.cos(slope) + sizenith * np.sin(slope) * np.cos(az - aspect)

    
    sea_mask = np.ma.masked_array( np.zeros(height.shape), mask = height > WATER_LEVEL)
#    np.place(sea_mask, height > WATER_LEVEL, 0 )

    print "finding contours..."

    shores_contours = measure.find_contours(height, WATER_LEVEL)
    middle_contours = measure.find_contours(height, WATER_LEVEL+0.3)

    contours = shores_contours + middle_contours



    cmap_height = matplotlib.cm.ScalarMappable(cmap="Wistia")
    cmap_height.set_clim(WATER_LEVEL,None)
    cmap_slope = matplotlib.cm.ScalarMappable(cmap="YlOrBr")
    cmap_shade = matplotlib.cm.ScalarMappable(cmap="Greys")
    cmap_shade.set_clim(0,1)

    cmap_sea = matplotlib.colors.LinearSegmentedColormap.from_list(
            "sea", [ (115./255.,96./255.,127./255.), (1,1,1) ],2 )


    colour_height = cmap_height.to_rgba(height)
    colour_shade = cmap_shade.to_rgba(shade)
    colour_slope = cmap_slope.to_rgba(slope)

    colour_terrain_final =  colour_shade*colour_height

    print "plot colour map..."

    plt.imshow(colour_terrain_final)
    #plt.imshow(shade, cmap = "Greys"  )
    #plt.imshow( height - uneroded_height)


    plt.imshow(sea_mask, cmap = cmap_sea)


    print "drawing seas..."

    # draw shores

    #seas_patches = []
    for n, contour in enumerate(contours):
    #    contour_upright = np.copy(contour)[:,[1,0]]
    #    poly = matplotlib.patches.Polygon( contour_upright , True)
    #    seas_patches.append(poly)
        plt.plot(contour[:, 1], contour[:, 0], linewidth=1,color="k")

    #seas_patches_collection = matplotlib.collections.PatchCollection(seas_patches, cmap=matplotlib.cm.jet)
    #plt.gca().add_collection(seas_patches_collection)


    #gX, gY = np.meshgrid( np.arange(0,size,1), np.arange(0,size,1))
    #
    #fig = plt.figure()
    #ax = fig.add_subplot(111,projection='3d')
    #ax.plot_surface(gX,gY,height)


    print "drawing grid..."

    latitude_15 = plt.Circle((size/2, size/2), size/2 * LATITUDE_SCALING, color='k', fill=False, linewidth=0.5)
    plt.gca().add_artist(latitude_15)

    latitude_polar = plt.Circle((size/2, size/2), size/2 * (INCLINATION / 15.) * LATITUDE_SCALING, color='k', fill=False, linewidth=0.5, linestyle='--')
    plt.gca().add_artist(latitude_polar)


    # drop paths

    if DRAW_DROP_PATHS:
        for p in drop_paths:
            plt.plot(p[0],p[1],linewidth=0.5, color="w")


    plt.axis('off')
    plt.gca().set_position([0,0,1,1])

    plt.xlim([0,size])
    plt.ylim([0,size])
    #plt.gca().set_xlim([0,size])

    plt.tight_layout()


    print "saving..."

    plt.savefig("map.svg", bbox_inches = "tight", transparent = True)

