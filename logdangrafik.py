import sys
import matplotlib.pyplot as plt

satir = []
for line in open(sys.argv[1]):
    if "avg" in line:
        satir.append(line)

iterasyon = []
orta_loss = []

for i in range(len(satir)):
    lineParts = satir[i].split(',')
    iterasyon.append(int(lineParts[0].split(':')[0]))
    orta_loss.append(float(lineParts[1].split()[0]))

fig = plt.figure()
for i in range(0, len(satir)):
    plt.plot(iterasyon[i:i+2], orta_loss[i:i+2], 'r.-')

plt.xlabel('iterasyon sayısı')
plt.ylabel('Ortalama Loss')
fig.savefig('plot.png', dpi=1000)

