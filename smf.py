###################################################
#
#   Practical computation of SMF properties
#
###################################################

import pylab as pl

step_index = []
radial_coordinate = []

f = open('profiles/bi213_profile.dat', 'r')
for line in f.readlines():
    if line[0].isnumeric() or line[0] == '-':
        cols = line.split()
        # print(float(cols[0].replace(',', '.')), float(cols[1].replace(',', '.')))
        radial_coordinate.append(float(cols[0].replace(',', '.')))
        step_index.append(float(cols[1].replace(',', '.')))
f.close()

pl.plot(radial_coordinate, step_index)
pl.title('Bi213 refractive index profile')
pl.xlabel('Radial coordinate (mm)')
pl.ylabel('Step index')
pl.show()

profile = []
delta = []
radius = []

################################################
# Cutting conditions
# It is much easier to choose this stuff manually...
#

start = 0.0
stop = 5.0
core = 1.2
core_ind = 0

################################################

for ind, item in enumerate(radial_coordinate):
    profile.append([item, step_index[ind]])

for item in profile:
    if start <= item[0] < stop:
        radius.append(item[0])
        delta.append(item[1])

pl.plot(radius, delta)
pl.title('Bi213 refractive index profile')
pl.xlabel('Radial coordinate (mm)')
pl.ylabel('Step index')
pl.show()

for ind, item in enumerate(radius):
    if abs(item-core) <= 0.00001:
        core_ind = ind


profile_function = [(max(delta)**2 - n**2)/(max(delta)**2 - delta[core_ind]**2) for n in delta]

pl.plot(radius, profile_function)
pl.title('Bi213 profile function')
pl.xlabel('Radial coordinate (mm)')
pl.ylabel('Profile function')
pl.show()
