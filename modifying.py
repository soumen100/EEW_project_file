import pandas as pd
import numpy as np

path = "D:\Data_10years\Modified data\Bageshwar_Three Component Data_Udham Singh Nagar - Sheet1.csv"

data = pd.read_csv(path)

acc = np.array(data['Acceleration'].values.tolist())

def classic_sta_lta_py(a, nsta, nlta):
    # The cumulative sum can be exploited to calculate a moving average (the
    # cumsum function is quite efficient)
    sta = np.cumsum(a ** 2)

    # Convert to float
    sta = np.require(sta, dtype=np.float)

    # Copy for LTA
    lta = sta.copy()

    # Compute the STA and the LTA
    sta[nsta:] = sta[nsta:] - sta[:-nsta]
    sta /= nsta
    lta[nlta:] = lta[nlta:] - lta[:-nlta]
    lta /= nlta
    sta[:nlta - 1] = 0

    dtiny = np.finfo(0.0).tiny
    idx = lta < dtiny
    lta[idx] = dtiny

    return sta / lta

sta_lta = classic_sta_lta_py(acc, 5, 120)

index = 0
for i in range(len(sta_lta)):
  if(sta_lta[i] >= 9):
    break

index = i + 1

if(index + 600 >= len(acc)):
  index = len(acc) // 2  

h = 0.005

velocity = []
sum = 0
for i in range(index, index + 601):
  velocity.append((h / 2) * (acc[i] + (2 * sum)))
  sum += acc[i]


disp = []
sum = 0
for i in range(len(velocity)):
  disp.append((h / 2) * (velocity[i] + (2 * sum)))
  sum += velocity[i]

pd = max(np.abs(disp))

vel2 = []
for i in velocity:
  vel2.append(i ** 2)

disp2 = []
for i in disp:
  disp2.append(i ** 2)

sum = 0
for i in range(len(vel2) - 1):
  sum += vel2[i]
num = ((h / 2) * (vel2[i] + (2 * sum)))

sum = 0
for i in range(len(disp2) - 1):
  sum += disp2[i]
deno = ((h / 2) * (disp2[i] + (2 * sum)))  

r = np.sqrt(num / deno)

tauc = (np.pi * 2) / r

print("Pd is ", pd)
print("Tauc is ", tauc)
