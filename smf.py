###################################################
#
#   Practical computation of SMF properties
#
###################################################

import pylab as pl
import math

##################################################
# Raw data
#

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
cladding_index = 1.46

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

#####################################################
# Profile function
#

for ind, item in enumerate(radius):
    if abs(item - core) <= 0.00001:
        core_ind = ind

NA = math.sqrt((max(delta) + cladding_index) ** 2 - (delta[core_ind] + cladding_index) ** 2)
print('NA = ', NA)

profile_function = [((max(delta) + cladding_index) ** 2 - (n + cladding_index) ** 2) / (NA ** 2) for n in delta]

pl.plot(radius, profile_function)
pl.title('Bi213 profile function')
pl.xlabel('Radial coordinate (mm)')
pl.ylabel('Profile function')
pl.show()

# l = range(len(profile_function))
# radius.extend([ radius[len(radius)-1] + (n+1) * (radius[len(radius)-1]-radius[len(radius)-2]) for n in l ])
# profile_function.extend([profile_function[len(profile_function)-1]] * len(profile_function))

prof_func = []

for ind, item in enumerate(profile_function):
    prof_func.append([radius[ind] / core, item])

###################################################
# Fiber parameters
#

a = 1000  # The radius of the fiber
wave = 1700  # The wavelength of operation

V = a * 2 * math.pi * NA / wave

print('V =', V)

##################################################
# Fundamental mode field
#

V2 = V * V

fw = 0.5
Dfw = 0.25
field = []
field1 = []
field2 = []

field.append(1)
field1.append(0)
field2.append(-fw * V2 / 2)

E = 0
E1 = 0
E2 = 0

while True:
    prev_coord = 0
    for ind, item in enumerate(prof_func):
        if ind > 0:
            E = field[ind - 1] + field1[ind - 1] * (item[0] - prev_coord)
            E1 = field1[ind - 1] + field2[ind - 1] * (item[0] - prev_coord)
            E2 = -(E1 / item[0]) - E * (fw - item[1]) * V2

            field.append(E)
            field1.append(E1)
            field2.append(E2)

            prev_coord = item[0]

    if E < 0:
        fw -= Dfw
        Dfw /= 2
        del field[1:]
        del field1[1:]
        del field2[1:]
    elif E > .001:
        fw += Dfw
        Dfw /= 2
        del field[1:]
        del field1[1:]
        del field2[1:]
    else:
        break

print('fw = ', fw)

pl.plot(radius, [n / max(delta) for n in delta])
pl.plot(radius, field)
pl.title('Bi213 field distribution')
pl.xlabel('Radial coordinate (mm)')
pl.ylabel('Field')
pl.show()

####################################################################
# Second mode cutoff
#

V2c = 4
DV2c = 2
SMfield = []
SMfield1 = []
SMfield2 = []

SMfield.append(0)
SMfield1.append(1)
SMfield2.append(0)

E = 0
E1 = 0
E2 = 0

Test = 0

while True:
    prev_coord = 0
    for ind, item in enumerate(prof_func):
        if ind > 0:
            E = SMfield[ind - 1] + SMfield1[ind - 1] * (item[0] - prev_coord)
            E1 = SMfield1[ind - 1] + SMfield2[ind - 1] * (item[0] - prev_coord)
            E2 = -(E1 / item[0]) - E * ((1 - item[1]) * V2c - 1 / (item[0]*item[0]))

            SMfield.append(E)
            SMfield1.append(E1)
            SMfield2.append(E2)

            prev_coord = item[0]

            if ind == core_ind:
                Test = E + E1

    if Test < -.0001:
        V2c -= DV2c
        DV2c /= 2
        del SMfield[1:]
        del SMfield1[1:]
        del SMfield2[1:]
    elif Test > .0001:
        V2c += DV2c
        DV2c /= 2
        del SMfield[1:]
        del SMfield1[1:]
        del SMfield2[1:]
    else:
        break

print('Vc = ', math.sqrt(V2c))

pl.plot(radius, [n / max(delta) for n in delta])
pl.plot(radius, SMfield)
pl.title('Bi213 Second mode field distribution')
pl.xlabel('Radial coordinate (mm)')
pl.ylabel('Field')
pl.show()
