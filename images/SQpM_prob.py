import math
import random

def random_points(n):
    points = []
    for i in xrange(n):
        points.append((1000*random.random(),1000*random.random()))
    return points

n = 50
m = 30
p = 5
clients = random_points(n)
sites = random_points(m)
servers = random.sample(sites,p)

sets = dict()
for client in clients:
    d = 1500.0
    #print('Busca server de cliente')
    for server in servers:
        x = client[0] - server[0]
        y = client[1] - server[1]
        s = math.sqrt(x * x + y * y)
        if s < d:
            p = server
            d = s
    if p not in sets :
        sets[p] = []
        #print('Se agrega punto\n')
    sets[p].append(client)

i = 1
for p in servers:
    st = sets[p]
    tmp = open('tmp_'+str(i)+'.dat','w')
    for client in st :
        tmp.write(str(client[0])+' '+str(client[1])+'\n')
    tmp.close()
    i += 1

tmp = open('sites.dat','w')
for p in sites :
    tmp.write(str(p[0])+' '+str(p[1])+'\n')
tmp.close()

tmp = open('servers.dat','w')
for server in servers:
    tmp.write(str(server[0])+' '+str(server[1])+'\n')
tmp.close()

# GnuPlot commands
tmp = open('tmp.gp','w')
tmp.write('set term svg \n')
tmp.write('set output \'SQpM_problem.svg\'\n')
tmp.write('set title "n = '+str(n)+' m = '+str(m)+' p = 5"\n')
tmp.write('set xrange [-50:1050]\n')
tmp.write('set yrange [-50:1050]\n')
tmp.write('set key outside \n')
tmp.write('set key bmargin \n')
tmp.write('unset border \n')
tmp.write('unset yzeroaxis \n')
tmp.write('unset xtics \n')
tmp.write('unset ytics \n')
tmp.write('unset ztics \n')
tmp.write('set style fill solid 1.0 border -1\n')
colors = ["cyan","gold","red","blue","brown"]
i = 1
for server in servers:
    tmp.write('set object '+str(i)+' rect from '
              +str(server[0]-15)+','+str(server[1]-15)+' to '
              +str(server[0]+15)+','+str(server[1]+15)
              +' fc rgb "'+colors[i-1]+'"\n')
    i += 1
i = 1
tmp.write('plot ')
for p in sets :
    filename = 'tmp_'+str(i)+'.dat'
    tmp.write('"'+filename+'" using 1:2:(12) with circles notitle lc rgb "'+colors[i-1]+'", ')
    i += 1
tmp.write('"servers.dat" using 1:2 w p lt 2 pt 5 lc rgb "dark-grey" title "Servers", ')
tmp.write('"sites.dat" using 1:2 w p lt 2 pt 7 lc rgb "dark-grey" title "Potential sites"')
tmp.write('\n')
tmp.close()

from os import system, remove
system('gnuplot tmp.gp')
remove('tmp.gp')
remove('sites.dat')
remove('servers.dat')
i = 1
for p in sets :
    filename = 'tmp_'+str(i)+'.dat'
    i += 1
    remove(filename)
