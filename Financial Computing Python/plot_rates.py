from urllib.request import urlopen
from bs4 import BeautifulSoup


html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2017')

# BeautifulSoup Yield Curve data
bsyc = BeautifulSoup(html.read(), "lxml")

fout = open('yc_temp.txt', 'wt',
		encoding='utf-8')

fout.write(str(bsyc))

fout.close()


fin = open('yc_temp.txt', 'rt', encoding='utf-8')
bsyc = BeautifulSoup(fin.read(), "lxml")
fin.close()

# print the first table
# print(str(bsyc.table))
# ... not the one we want

# so get a list of all table tags
#table_list = bsyc.findAll('table')

# how many are there?
# print('there are', len(table_list), 'table tags')

# look at the first 50 chars of each table
#for t in table_list:
#    print(str(t)[:50])

# only one class="t-chart" table, so add that
# to findAll as a dictionary attribute
tc_table_list = bsyc.findAll('table',
                      { "class" : "t-chart" } )

# how many are there?
#print(len(tc_table_list), 't-chart tables')

# only 1 t-chart table, so grab it
tc_table = tc_table_list[0]

# what are this table's components/children?
#for c in tc_table.children:
#   print(str(c)[:50])

# tag tr means table row, containing table data
# what are the children of those rows?
#for c in tc_table.children:
#    for r in c.children:
#        print(str(r)[:50])

# we have found the table data!
# just get the contents of each cell
#for c in tc_table.children:
#    for r in c.children:
#        print(r.contents)

# the contents of each cell is a list of one
# string -- we can work with those!

# your HW4 part 1 code goes here

# 1.a
# daily_yield_curves is a list of rows, where each row is a list of strings
daily_yield_curves = []
for row in tc_table.children:
    row_list = []
    for cell in row.children:
        row_list.append(cell.contents[0])
    daily_yield_curves.append(row_list)

# row 0 is the column headers
# col 0 of rows 1 through len(my_table)-1 is the date
# convert all other cells from str to float
for rnum in range(1,len(daily_yield_curves)):
    for cnum in range(1,len(daily_yield_curves[rnum])):
        daily_yield_curves[rnum][cnum] = float(daily_yield_curves[rnum][cnum])

# save table into a neatly formatted text file
# (many ways to do this)
fout = open('daily_yield_curves.txt', 'wt', encoding='utf-8')
# Date column is 8 characters wide, interest rate columns are 6 characters wide (for '30 yr')
header_format = '{:8s}' + '{:>6s}' * (len(daily_yield_curves[0]) - 1) + '\n'
data_format = '{:8s}' + '{:>6.2f}' * (len(daily_yield_curves[1]) - 1) + '\n'
fout.write(header_format.format(*(daily_yield_curves[0])))
for i in range(1,len(daily_yield_curves)):
    fout.write(data_format.format(*(daily_yield_curves[i])))
fout.close()

# 1.b
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

# days (trading days) since 01/03/17
# (you could also count elapsed calendar days, if you wish, but it's quite a bit harder)
X = [ [x] * 11 for x in range(1, len(daily_yield_curves)) ]
print(X,'\n\n')

# months to maturity
Y = [ [1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360] for x in range(1, len(daily_yield_curves)) ]
print(Y,'\n\n')

# interest rates for each (days,months) pair
Z = [ daily_yield_curves[j][1:] for j in range(1, len(daily_yield_curves)) ]
print(Z)

# set up one figure containing the 3d surface and the wireframe
# make height 1.5 times width
fig = plt.figure(figsize=plt.figaspect(1.5))
ax = fig.add_subplot(2, 1, 1, projection='3d')

# Plot the 3d surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis (interest rate)
ax.set_zlim(0.0, 4.0)

# label the axes
ax.set_xlabel('trading days since 01/03/17')
ax.set_ylabel('months to maturity')
ax.set_zlabel('rate')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

# add a separate subplot for the wireframe
ax2 = fig.add_subplot(2, 1, 2, projection='3d')

# Plot the wireframe.
ax2.plot_wireframe(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=1, antialiased=False)

# Customize the z axis (interest rate)
ax2.set_zlim(0.0, 4.0)

# label the axes
ax2.set_xlabel('trading days since 01/03/17')
ax2.set_ylabel('months to maturity')
ax2.set_zlabel('rate')

plt.show()
