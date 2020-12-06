import numpy as np
from scipy.linalg import eigh
from matplotlib import pyplot as plt

# enter number of stories
story = int(input("Enter the number of stories: "))

# enter the story stiffnesses
k_stories = []
for item in range(1,story+1):
  k_ = float(input(f"Enter the k{item}: "))
  k_stories.append(k_)

#enter the story masses
m_stories = []
for item in range(1,story+1):
  m_ = float(input(f"Enter the m{item}: "))
  m_stories.append(m_)

# creation of mass matrix of the system
I = np.identity(story)
M_system = I * m_stories

#creation of stiffness matrix of the system
K_system = np.zeros((story,story))
for i in range(story-1):
    for j in range(story):
        if i == j : 
            K_system[i,j]= k_stories[i] + k_stories[i+1]
        elif i - j == 1 :
            K_system[i,j]= -1* k_stories[i]
        elif j-i == 1:
            K_system[i,j]= -1* k_stories[j]                
        else: 
            K_system[i,j] = 0
            
K_system[story-1,story-1] = k_stories[-1]
K_system[story-1,story-2] = -1*k_stories[-1]


# calculation of eigenvalues and eigenvectors;
evals, evecs = eigh(K_system,M_system)

# calculation of natural frequencies and periods
frequencies = np.sqrt(evals)
periods = 2*np.pi/frequencies
print(f"natural frequencies: {frequencies}")
print(50*"=")
print(f"periods: {periods}")
print(50*"=")

# determination of the modal matrix
mods = evecs.copy()
for j in range(story):
  mods[0::,j] = evecs[0::,j]/evecs[-1,j]
print(f"MODAL MATRIX: \n{mods}")
print(50*"=")

# Plotting of the mode shapes
  # arrangement for modal matrix to plot
mod_g = np.zeros((story+1,story))
mod_g[1::,0::] = mods
mods_list = {}
for item in range(1,story+1):
  mods_list[item] = mod_g[0::,item-1]

  #Plotting
for item in range(1,story+1):
  plt.figure(figsize=(4,9))
  plt.grid(color= "r", axis="y")
  plt.plot(mods_list[item],range(0,story+1,1),"k*-")
  
  ax = plt.gca()
  ax.axes.yaxis.set_ticklabels([])
  
  for a,b in zip(mods_list[item], range(0,story+1,1)): 
    plt.text(a, b, str(np.around(a,4)), fontsize=20,bbox=dict(facecolor='w', alpha=0.5))
  
  plt.title(f'Mod {item}', fontsize=20, bbox=dict(facecolor='r', alpha=0.50))
  plt.show()
