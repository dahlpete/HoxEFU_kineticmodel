import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time

start = time.time()

# set some integration parameters
tol = 0.0001
maxdt = 1.0

ttot = 1e2 # seconds
dt = 1e-6

# a couple other parameters
k_NAD = 1e10
k_NADH = 1e10

plotrealtime=False
excel = False
csv = True

def select_subset(t_ar,ar):
	decades = np.arange(12,-1,-1)
	cnt = 0
	for k in decades:
		b = 10.0**(-1*k)
		c = 10.0**(-1*(k+1))
		ix1 = t_ar <= b
		ix2 = t_ar > c
		ix = ix1 * ix2
		tvals = t_ar[ix]
		pvals = ar[:,ix]
		if len(tvals) > 100:
			ixs = np.arange(0,len(tvals),int(round(len(tvals)/100)))
			tvals = np.array([tvals[l] for l in ixs])
			pvals = [pvals[:,l] for l in ixs]
			pvals = np.array(pvals).transpose()
		if cnt == 0:
			times = tvals
			values = pvals
		else:	
			times = np.append(times,tvals)
			values = np.append(values,pvals,axis=1)
		cnt+=1
	return np.array(times),np.array(values)
	
# Read in rate constants
if excel:
	df = pd.read_excel('rate_constants_HoxEFU_v2.xlsx')
	df.to_csv('rate_constants_HoxEFU_convert.csv')

	k_SQ2E = float(df.iloc[6,5])
	k_SQ2F2 = float(df.iloc[6,6])
	k_SQ2F4 = float(df.iloc[6,7])
	k_SQ2U41 = float(df.iloc[6,9])
	k_SQ2U42 = float(df.iloc[6,10])
	k_SQ2U43 = float(df.iloc[6,11])
	k_SQ2U2 = float(df.iloc[6,8])
	
	k_HQ2E = float(df.iloc[7,5])
	k_HQ2F2 = float(df.iloc[7,6])
	k_HQ2F4 = float(df.iloc[7,7])
	k_HQ2U41 = float(df.iloc[7,9])
	k_HQ2U42 = float(df.iloc[7,10])
	k_HQ2U43 = float(df.iloc[7,11])
	k_HQ2U2 = float(df.iloc[7,8])
	
	k_E2Q = float(df.iloc[8,2])
	k_E2SQ = float(df.iloc[8,3])
	k_E2F2 = float(df.iloc[8,6])
	k_E2F4 = float(df.iloc[8,7])
	k_E2U41 = float(df.iloc[8,9])
	k_E2U42 = float(df.iloc[8,10])
	k_E2U43 = float(df.iloc[8,11])
	k_E2U2 = float(df.iloc[8,8])
	
	k_F22Q = float(df.iloc[9,2])
	k_F22SQ = float(df.iloc[9,3])
	k_F22E = float(df.iloc[9,5])
	k_F22F4 = float(df.iloc[9,7])
	k_F22U41 = float(df.iloc[9,9])
	k_F22U42 = float(df.iloc[9,10])
	k_F22U43 = float(df.iloc[9,11])
	k_F22U2 = float(df.iloc[9,8])
	
	k_F42Q = float(df.iloc[10,2])
	k_F42SQ = float(df.iloc[10,3])
	k_F42E = float(df.iloc[10,5])
	k_F42F2 = float(df.iloc[10,6])
	k_F42U41 = float(df.iloc[10,9])
	k_F42U42 = float(df.iloc[10,10])
	k_F42U43 = float(df.iloc[10,11])
	k_F42U2 = float(df.iloc[10,8])
	
	k_U412Q = float(df.iloc[12,2])
	k_U412SQ = float(df.iloc[12,3])
	k_U412E = float(df.iloc[12,5])
	k_U412F2 = float(df.iloc[12,6])
	k_U412F4 = float(df.iloc[12,7])
	k_U412U42 = float(df.iloc[12,10])
	k_U412U43 = float(df.iloc[12,11])
	k_U412U2 = float(df.iloc[12,8])
	
	k_U422Q = float(df.iloc[13,2])
	k_U422SQ = float(df.iloc[13,3])
	k_U422E = float(df.iloc[13,5])
	k_U422F2 = float(df.iloc[13,6])
	k_U422F4 = float(df.iloc[13,7])
	k_U422U41 = float(df.iloc[13,9])
	k_U422U43 = float(df.iloc[13,11])
	k_U422U2 = float(df.iloc[13,8])
	
	k_U432Q = float(df.iloc[14,2])
	k_U432SQ = float(df.iloc[14,3])
	k_U432E = float(df.iloc[14,5])
	k_U432F2 = float(df.iloc[14,6])
	k_U432F4 = float(df.iloc[14,7])
	k_U432U41 = float(df.iloc[14,9])
	k_U432U42 = float(df.iloc[14,10])
	k_U432U2 = float(df.iloc[14,8])
	
	k_U22Q = float(df.iloc[11,2])
	k_U22SQ = float(df.iloc[11,3])
	k_U22E = float(df.iloc[11,5])
	k_U22F2 = float(df.iloc[11,6])
	k_U22F4 = float(df.iloc[11,7])
	k_U22U41 = float(df.iloc[11,9])
	k_U22U42 = float(df.iloc[11,10])
	k_U22U43 = float(df.iloc[11,11])

if csv:
	df = pd.read_csv('rate_constants_HoxEFU_corr_mod1.csv')

	k_SQ2E = float(df.iloc[5,5])
	k_SQ2F2 = float(df.iloc[5,6])
	k_SQ2F4 = float(df.iloc[5,7])
	k_SQ2U41 = float(df.iloc[5,9])
	k_SQ2U42 = float(df.iloc[5,10])
	k_SQ2U43 = float(df.iloc[5,11])
	k_SQ2U2 = float(df.iloc[5,8])
	
	k_HQ2E = float(df.iloc[6,5])
	k_HQ2F2 = float(df.iloc[6,6])
	k_HQ2F4 = float(df.iloc[6,7])
	k_HQ2U41 = float(df.iloc[6,9])
	k_HQ2U42 = float(df.iloc[6,10])
	k_HQ2U43 = float(df.iloc[6,11])
	k_HQ2U2 = float(df.iloc[6,8])
	
	k_E2Q = float(df.iloc[7,2])
	k_E2SQ = float(df.iloc[7,3])
	k_E2F2 = float(df.iloc[7,6])
	k_E2F4 = float(df.iloc[7,7])
	k_E2U41 = float(df.iloc[7,9])
	k_E2U42 = float(df.iloc[7,10])
	k_E2U43 = float(df.iloc[7,11])
	k_E2U2 = float(df.iloc[7,8])
	
	k_F22Q = float(df.iloc[8,2])
	k_F22SQ = float(df.iloc[8,3])
	k_F22E = float(df.iloc[8,5])
	k_F22F4 = float(df.iloc[8,7])
	k_F22U41 = float(df.iloc[8,9])
	k_F22U42 = float(df.iloc[8,10])
	k_F22U43 = float(df.iloc[8,11])
	k_F22U2 = float(df.iloc[8,8])
	
	k_F42Q = float(df.iloc[9,2])
	k_F42SQ = float(df.iloc[9,3])
	k_F42E = float(df.iloc[9,5])
	k_F42F2 = float(df.iloc[9,6])
	k_F42U41 = float(df.iloc[9,9])
	k_F42U42 = float(df.iloc[9,10])
	k_F42U43 = float(df.iloc[9,11])
	k_F42U2 = float(df.iloc[9,8])
	
	k_U412Q = float(df.iloc[11,2])
	k_U412SQ = float(df.iloc[11,3])
	k_U412E = float(df.iloc[11,5])
	k_U412F2 = float(df.iloc[11,6])
	k_U412F4 = float(df.iloc[11,7])
	k_U412U42 = float(df.iloc[11,10])
	k_U412U43 = float(df.iloc[11,11])
	k_U412U2 = float(df.iloc[11,8])
	
	k_U422Q = float(df.iloc[12,2])
	k_U422SQ = float(df.iloc[12,3])
	k_U422E = float(df.iloc[12,5])
	k_U422F2 = float(df.iloc[12,6])
	k_U422F4 = float(df.iloc[12,7])
	k_U422U41 = float(df.iloc[12,9])
	k_U422U43 = float(df.iloc[12,11])
	k_U422U2 = float(df.iloc[12,8])
	
	k_U432Q = float(df.iloc[13,2])
	k_U432SQ = float(df.iloc[13,3])
	k_U432E = float(df.iloc[13,5])
	k_U432F2 = float(df.iloc[13,6])
	k_U432F4 = float(df.iloc[13,7])
	k_U432U41 = float(df.iloc[13,9])
	k_U432U42 = float(df.iloc[13,10])
	k_U432U2 = float(df.iloc[13,8])
	
	k_U22Q = float(df.iloc[10,2])
	k_U22SQ = float(df.iloc[10,3])
	k_U22E = float(df.iloc[10,5])
	k_U22F2 = float(df.iloc[10,6])
	k_U22F4 = float(df.iloc[10,7])
	k_U22U41 = float(df.iloc[10,9])
	k_U22U42 = float(df.iloc[10,10])
	k_U22U43 = float(df.iloc[10,11])

print(np.array([k_E2Q,k_F22Q,k_F22SQ,k_SQ2F2,k_F42Q,k_SQ2U41,k_SQ2U42,k_SQ2U43,k_SQ2U2,k_U22F2,k_U412U2]))

# set initial conditions
NADHtot = 0.0 #float(df.iloc[1,2]) * 200e-6 * 1e9
NADtot = 0.0
if excel:
	c_hox = float(df.iloc[1,3]) * 200e-6 * 1e9
if csv:
	c_hox = float(df.iloc[1,4]) * 200e-6 * 1e9

c_hox = 10.0

c_NADH = c_hox   # this is bound NADH
c_NAD = 0.0       # this is bound NAD
c_ub = 0.0        # this is unbound Hox EFU

konNADH = 3.1e6
koffNADH = 100

konNAD = 1e6
koffNAD = 1350

c_NADHfree = 2000.0 # NADHtot - c_NADH
c_NADfree = 0.0 #NADtot - c_NAD

c_Q = c_hox
c_SQ = 0.0
c_HQ = 0.0

c_Eox = c_hox;    c_Ered = 0.0
c_F2ox = c_hox;   c_F2red = 0.0
c_F4ox = c_hox;   c_F4red = 0.0
c_U41ox = c_hox;  c_U41red = 0.0
c_U42ox = c_hox;  c_U42red = 0.0
c_U43ox = c_hox;  c_U43red = 0.0
c_U2ox = c_hox;   c_U2red = 0.0

i = 0; itot = 0
time_val = 0
ni = 500000

P = np.array([c_NADH,c_NAD,c_ub,c_NADHfree,c_NADfree,c_HQ,c_SQ,c_Q,c_Eox,c_Ered,c_F2ox,c_F2red,c_F4ox,c_F4red,c_U41ox,c_U41red,c_U42ox,c_U42red,c_U43ox,c_U43red,c_U2ox,c_U2red])
population = np.zeros([len(P),ni+1])
time_array = np.zeros(ni+1)

#initialize plots
fig,(ax1,ax2,ax3)=plt.subplots(1,3)
ax1.plot(time_array[:2],population[0,:2],color='k',label='NADH')
ax1.plot(time_array[:2],population[1,:2],color=[0.2,0.2,0.2],label='NAD')
ax1.plot(time_array[:2],population[2,:2],color=[0.6,0.6,0.6],label='unbound')
ax2.plot(time_array[:2],population[5,:2],color='r',label='HQ')
ax2.plot(time_array[:2],population[6,:2],color='b',label='SQ')
ax2.plot(time_array[:2],population[7,:2],color='g',label='Q')
ax3.plot(time_array[:2],population[9,:2],color='r',label='E')   # E  reduced pop
ax3.plot(time_array[:2],population[11,:2],color='c',label='F1') # F1 reduced pop
ax3.plot(time_array[:2],population[13,:2],color='y',label='F2') # F2 reduced pop
ax3.plot(time_array[:2],population[21,:2],color='m',label='U1') # U1 reduced pop
ax3.plot(time_array[:2],population[15,:2],color='k',label='U2') # U2 reduced pop
ax3.plot(time_array[:2],population[17,:2],color='g',label='U3') # U3 reduced pop
ax3.plot(time_array[:2],population[19,:2],color='b',label='U4') # U4 reduced pop

ax1.legend(loc='upper left')
ax2.legend(loc='upper left')
ax3.legend(loc='upper left')

first = True

while time_val < ttot:

	# Term 1: Euler
	F1_NADH = dt * (konNADH*c_ub*c_NADHfree - koffNADH*c_NADH + c_HQ*k_NAD*c_NAD - c_Q*k_NADH*c_NADH)
	F1_NAD = dt * (konNAD*c_ub*c_NADfree - koffNAD*c_NAD + c_Q*k_NADH*c_NADH - c_HQ*k_NAD*c_NAD)
	F1_ub = dt * (koffNADH*c_NADH + koffNAD*c_NAD - konNADH*c_ub*c_NADHfree - konNAD*c_ub*c_NADfree)
	F1_NADHfree = dt * (koffNADH*c_NADH - konNADH*c_ub*c_NADHfree)
	F1_NADfree = dt * (koffNAD*c_NAD - konNAD*c_ub*c_NADfree)

	a = c_HQ*(k_HQ2E*c_Eox + k_HQ2F2*c_F2ox + k_HQ2F4*c_F4ox + k_HQ2U41*c_U41ox + k_HQ2U42*c_U42ox + k_HQ2U43*c_U43ox + k_HQ2U2*c_U2ox)
	b1 = c_SQ*(k_E2SQ*c_Ered + k_F22SQ*c_F2red + k_F42SQ*c_F4red + k_U412SQ*c_U41red + k_U422SQ*c_U42red + k_U432SQ*c_U43red + k_U22SQ*c_U2red)
	b2 = c_SQ*(k_SQ2E*c_Eox + k_SQ2F2*c_F2ox + k_SQ2F4*c_F4ox + k_SQ2U41*c_U41ox + k_SQ2U42*c_U42ox + k_SQ2U43*c_U43ox + k_SQ2U2+c_U2ox)
	c = c_Q*(k_E2Q*c_Ered + k_F22Q*c_F2red + k_F42Q*c_F4red + k_U412Q*c_U41red + k_U422Q*c_U42red + k_U432Q*c_U43red + k_U22Q*c_U2red)
	d = c_Q*k_NADH*c_NADH
	e = c_HQ*k_NAD*c_NAD

	F1_HQ = dt * (b1 - a + d - e) 
	F1_SQ = dt * (c + a - b1 - b2)
	F1_Q = dt * (b2 - c - d + e)

	F1_Eo = dt * (c_Ered*(k_E2Q*c_Q + k_E2SQ*c_SQ + k_E2F2*c_F2ox + k_E2F4*c_F4ox + k_E2U41*c_U41ox + k_E2U42*c_U42ox + k_E2U43*c_U43ox + k_E2U2*c_U2ox) \
                      - c_Eox*(k_HQ2E*c_HQ + k_SQ2E*c_SQ + k_F22E*c_F2red + k_F42E*c_F4red + k_U412E*c_U41red + k_U422E*c_U42red + k_U432E*c_U43red + k_U22E*c_U2red))
	F1_Er = -1*F1_Eo

	F1_F2o = dt * (c_F2red*(k_F22Q*c_Q + k_F22SQ*c_SQ + k_F22E*c_Eox + k_F22F4*c_F4ox + k_F22U41*c_U41ox + k_F22U42*c_U42ox + k_F22U43*c_U43ox + k_F22U2*c_U2ox) \
                       - c_F2ox*(k_HQ2F2*c_HQ + k_SQ2F2*c_SQ + k_E2F2*c_Ered + k_F42F2*c_F4red + k_U412F2*c_U41red + k_U422F2*c_U42red + k_U432F2*c_U43red + k_U22F2*c_U2red))
	F1_F2r = -1*F1_F2o

	F1_F4o = dt * (c_F4red*(k_F42Q*c_Q + k_F42SQ*c_SQ + k_F42E*c_Eox + k_F42F2*c_F2ox + k_F42U41*c_U41ox + k_F42U42*c_U42ox + k_F42U43*c_U43ox + k_F42U2*c_U2ox) \
                       - c_F4ox*(k_HQ2F4*c_HQ + k_SQ2F4*c_SQ + k_E2F4*c_Ered + k_F22F4*c_F2red + k_U412F4*c_U41red + k_U422F4*c_U42red + k_U432F4*c_U43red + k_U22F4*c_U2red))
	F1_F4r = -1*F1_F4o

	F1_U41o = dt * (c_U41red*(k_U412Q*c_Q + k_U412SQ*c_SQ + k_U412E*c_Eox + k_U412F2*c_F2ox + k_U412F4*c_F4ox + k_U412U42*c_U42ox + k_U412U43*c_U43ox + k_U412U2*c_U2ox) \
                        - c_U41ox*(k_HQ2U41*c_HQ + k_SQ2U41*c_SQ + k_E2U41*c_Ered + k_F22U41*c_F2red + k_F42U41*c_F4red + k_U422U41*c_U42red + k_U432U41*c_U43red + k_U22U41*c_U2red))
	F1_U41r = -1*F1_U41o

	F1_U42o = dt * (c_U42red*(k_U422Q*c_Q + k_U422SQ*c_SQ + k_U422E*c_Eox + k_U422F2*c_F2ox + k_U422F4*c_F4ox + k_U422U41*c_U41ox + k_U422U43*c_U43ox + k_U422U2*c_U2ox) \
                        - c_U42ox*(k_HQ2U42*c_HQ + k_SQ2U42*c_SQ + k_E2U42*c_Ered + k_F22U42*c_F2red + k_F42U42*c_F4red + k_U412U42*c_U41red + k_U432U42*c_U43red + k_U22U42*c_U2red))
	F1_U42r = -1*F1_U42o

	F1_U43o = dt * (c_U43red*(k_U432Q*c_Q + k_U432SQ*c_SQ + k_U432E*c_Eox + k_U432F2*c_F2ox + k_U432F4*c_F4ox + k_U432U41*c_U41ox + k_U432U42*c_U42ox + k_U432U2*c_U2ox) \
                        - c_U43ox*(k_HQ2U43*c_HQ + k_SQ2U43*c_SQ + k_E2U43*c_Ered + k_F22U43*c_F2red + k_F42U43*c_F4red + k_U412U43*c_U41red + k_U422U43*c_U42red + k_U22U43*c_U2red))
	F1_U43r = -1*F1_U43o

	F1_U2o = dt * (c_U2red*(k_U22Q*c_Q + k_U22SQ*c_SQ + k_U22E*c_Eox + k_U22F2*c_F2ox + k_U22F4*c_F4ox + k_U22U41*c_U41ox + k_U22U42*c_U42ox + k_U22U43*c_U43ox) \
                       - c_U2ox*(k_HQ2U2*c_HQ + k_SQ2U2*c_SQ + k_E2U2*c_Ered + k_F22U2*c_F2red + k_F42U2*c_F4red + k_U412U2*c_U41red + k_U422U2*c_U42red + k_U432U2*c_U43red))
	F1_U2r = -1*F1_U2o


	# terms for F2
	c2_NADH = c_NADH + 0.5*F1_NADH;    c2_NAD = c_NAD + 0.5*F1_NAD;     c2_ub = c_ub + 0.5*F1_ub
	c2_NADHfree = c_NADHfree + 0.5*F1_NADHfree;     c2_NADfree = c_NADfree + 0.5*F1_NADfree
	c2_Q = c_Q + 0.5*F1_Q
	c2_SQ = c_SQ + 0.5*F1_SQ
	c2_HQ = c_HQ + 0.5*F1_HQ
	c2_Eox = c_Eox + 0.5*F1_Eo;        c2_Ered = c_Ered + 0.5*F1_Er
	c2_F2ox = c_F2ox + 0.5*F1_F2o;     c2_F2red = c_F2red + 0.5*F1_F2r
	c2_F4ox = c_F4ox + 0.5*F1_F4o;     c2_F4red = c_F4red + 0.5*F1_F4r
	c2_U41ox = c_U41ox + 0.5*F1_U41o;  c2_U41red = c_U41red + 0.5*F1_U41r
	c2_U42ox = c_U42ox + 0.5*F1_U42o;  c2_U42red = c_U42red + 0.5*F1_U42r
	c2_U43ox = c_U43ox + 0.5*F1_U43o;  c2_U43red = c_U43red + 0.5*F1_U43r
	c2_U2ox = c_U2ox + 0.5*F1_U2o;     c2_U2red = c_U2red + 0.5*F1_U2r

	
	# Term 2
	F2_NADH = dt * (konNADH*c2_ub*c2_NADHfree - koffNADH*c2_NADH + c2_HQ*k_NAD*c2_NAD - c2_Q*k_NADH*c2_NADH)
	F2_NAD = dt * (konNAD*c2_ub*c2_NADfree - koffNAD*c2_NAD + c2_Q*k_NADH*c2_NADH - c2_HQ*k_NAD*c2_NAD)
	F2_ub = dt * (koffNADH*c2_NADH + koffNAD*c2_NAD - konNADH*c2_ub*c2_NADHfree - konNAD*c2_ub*c2_NADfree)
	F2_NADHfree = dt * (koffNADH*c2_NADH - konNADH*c2_ub*c2_NADHfree)
	F2_NADfree = dt * (koffNAD*c2_NAD - konNAD*c2_ub*c2_NADfree)

	a = c2_HQ*(k_HQ2E*c2_Eox + k_HQ2F2*c2_F2ox + k_HQ2F4*c2_F4ox + k_HQ2U41*c2_U41ox + k_HQ2U42*c2_U42ox + k_HQ2U43*c2_U43ox + k_HQ2U2*c2_U2ox)
	b1 = c2_SQ*(k_E2SQ*c2_Ered + k_F22SQ*c2_F2red + k_F42SQ*c2_F4red + k_U412SQ*c2_U41red + k_U422SQ*c2_U42red + k_U432SQ*c2_U43red + k_U22SQ*c2_U2red)
	b2 = c2_SQ*(k_SQ2E*c2_Eox + k_SQ2F2*c2_F2ox + k_SQ2F4*c2_F4ox + k_SQ2U41*c2_U41ox + k_SQ2U42*c2_U42ox + k_SQ2U43*c2_U43ox + k_SQ2U2+c2_U2ox)
	c = c2_Q*(k_E2Q*c2_Ered + k_F22Q*c2_F2red + k_F42Q*c2_F4red + k_U412Q*c2_U41red + k_U422Q*c2_U42red + k_U432Q*c2_U43red + k_U22Q*c2_U2red)
	d = c2_Q*k_NADH*c2_NADH
	e = c2_HQ*k_NAD*c2_NAD

	F2_HQ = dt * (b1 - a + d - e) 
	F2_SQ = dt * (c + a - b1 - b2)
	F2_Q =  dt * (b2 - c - d + e)

	F2_Eo = dt * (c2_Ered*(k_E2Q*c2_Q + k_E2SQ*c2_SQ + k_E2F2*c2_F2ox + k_E2F4*c2_F4ox + k_E2U41*c2_U41ox + k_E2U42*c2_U42ox + k_E2U43*c2_U43ox + k_E2U2*c2_U2ox) \
                      - c2_Eox*(k_HQ2E*c2_HQ + k_SQ2E*c2_SQ + k_F22E*c2_F2red + k_F42E*c2_F4red + k_U412E*c2_U41red + k_U422E*c2_U42red + k_U432E*c2_U43red + k_U22E*c2_U2red))
	F2_Er = -1*F2_Eo

	F2_F2o = dt * (c2_F2red*(k_F22Q*c2_Q + k_F22SQ*c2_SQ + k_F22E*c2_Eox + k_F22F4*c2_F4ox + k_F22U41*c2_U41ox + k_F22U42*c2_U42ox + k_F22U43*c2_U43ox + k_F22U2*c2_U2ox) \
                       - c2_F2ox*(k_HQ2F2*c2_HQ + k_SQ2F2*c2_SQ + k_E2F2*c2_Ered + k_F42F2*c2_F4red + k_U412F2*c2_U41red + k_U422F2*c2_U42red + k_U432F2*c2_U43red + k_U22F2*c2_U2red))
	F2_F2r = -1*F2_F2o

	F2_F4o = dt * (c2_F4red*(k_F42Q*c2_Q + k_F42SQ*c2_SQ + k_F42E*c2_Eox + k_F42F2*c2_F2ox + k_F42U41*c2_U41ox + k_F42U42*c2_U42ox + k_F42U43*c2_U43ox + k_F42U2*c2_U2ox) \
                       - c2_F4ox*(k_HQ2F4*c2_HQ + k_SQ2F4*c2_SQ + k_E2F4*c2_Ered + k_F22F4*c2_F2red + k_U412F4*c2_U41red + k_U422F4*c2_U42red + k_U432F4*c2_U43red + k_U22F4*c2_U2red))
	F2_F4r = -1*F2_F4o

	F2_U41o = dt * (c2_U41red*(k_U412Q*c2_Q + k_U412SQ*c2_SQ + k_U412E*c2_Eox + k_U412F2*c2_F2ox + k_U412F4*c2_F4ox + k_U412U42*c2_U42ox + k_U412U43*c2_U43ox + k_U412U2*c2_U2ox) \
                        - c2_U41ox*(k_HQ2U41*c2_HQ + k_SQ2U41*c2_SQ + k_E2U41*c2_Ered + k_F22U41*c2_F2red + k_F42U41*c2_F4red + k_U422U41*c2_U42red + k_U432U41*c2_U43red + k_U22U41*c2_U2red))
	F2_U41r = -1*F2_U41o

	F2_U42o = dt * (c2_U42red*(k_U422Q*c2_Q + k_U422SQ*c2_SQ + k_U422E*c2_Eox + k_U422F2*c2_F2ox + k_U422F4*c2_F4ox + k_U422U41*c2_U41ox + k_U422U43*c2_U43ox + k_U422U2*c2_U2ox) \
                        - c2_U42ox*(k_HQ2U42*c2_HQ + k_SQ2U42*c2_SQ + k_E2U42*c2_Ered + k_F22U42*c2_F2red + k_F42U42*c2_F4red + k_U412U42*c2_U41red + k_U432U42*c2_U43red + k_U22U42*c2_U2red))
	F2_U42r = -1*F2_U42o

	F2_U43o = dt * (c2_U43red*(k_U432Q*c2_Q + k_U432SQ*c2_SQ + k_U432E*c2_Eox + k_U432F2*c2_F2ox + k_U432F4*c2_F4ox + k_U432U41*c2_U41ox + k_U432U42*c2_U42ox + k_U432U2*c2_U2ox) \
                        - c2_U43ox*(k_HQ2U43*c2_HQ + k_SQ2U43*c2_SQ + k_E2U43*c2_Ered + k_F22U43*c2_F2red + k_F42U43*c2_F4red + k_U412U43*c2_U41red + k_U422U43*c2_U42red + k_U22U43*c2_U2red))
	F2_U43r = -1*F2_U43o

	F2_U2o = dt * (c2_U2red*(k_U22Q*c2_Q + k_U22SQ*c2_SQ + k_U22E*c2_Eox + k_U22F2*c2_F2ox + k_U22F4*c2_F4ox + k_U22U41*c2_U41ox + k_U22U42*c2_U42ox + k_U22U43*c2_U43ox) \
	               - c2_U2ox*(k_HQ2U2*c2_HQ + k_SQ2U2*c2_SQ + k_E2U2*c2_Ered + k_F22U2*c2_F2red + k_F42U2*c2_F4red + k_U412U2*c2_U41red + k_U422U2*c2_U42red + k_U432U2*c2_U43red))
	F2_U2r = -1*F2_U2o


	# terms for F3
	c3_NADH = c_NADH + 0.5*F2_NADH;    c3_NAD = c_NAD + 0.5*F2_NAD;     c3_ub = c_ub + 0.5*F2_ub
	c3_NADHfree = c_NADHfree + 0.5*F2_NADHfree;     c3_NADfree = c_NADfree + 0.5*F2_NADfree
	c3_Q = c_Q + 0.5*F2_Q
	c3_SQ = c_SQ + 0.5*F2_SQ
	c3_HQ = c_HQ + 0.5*F2_HQ
	c3_Eox = c_Eox + 0.5*F2_Eo;        c3_Ered = c_Ered + 0.5*F2_Er
	c3_F2ox = c_F2ox + 0.5*F2_F2o;     c3_F2red = c_F2red + 0.5*F2_F2r
	c3_F4ox = c_F4ox + 0.5*F2_F4o;     c3_F4red = c_F4red + 0.5*F2_F4r
	c3_U41ox = c_U41ox + 0.5*F2_U41o;  c3_U41red = c_U41red + 0.5*F2_U41r
	c3_U42ox = c_U42ox + 0.5*F2_U42o;  c3_U42red = c_U42red + 0.5*F2_U42r
	c3_U43ox = c_U43ox + 0.5*F2_U43o;  c3_U43red = c_U43red + 0.5*F2_U43r
	c3_U2ox = c_U2ox + 0.5*F2_U2o;     c3_U2red = c_U2red + 0.5*F2_U2r


	# Term 3
	F3_NADH = dt * (konNADH*c3_ub*c3_NADHfree - koffNADH*c3_NADH + c3_HQ*k_NAD*c3_NAD - c3_Q*k_NADH*c3_NADH)
	F3_NAD = dt * (konNAD*c3_ub*c3_NADfree - koffNAD*c3_NAD + c3_Q*k_NADH*c3_NADH - c3_HQ*k_NAD*c3_NAD)
	F3_ub = dt * (koffNADH*c3_NADH + koffNAD*c3_NAD - konNADH*c3_ub*c3_NADHfree - konNAD*c3_ub*c3_NADfree)
	F3_NADHfree = dt * (koffNADH*c3_NADH - konNADH*c3_ub*c3_NADHfree)
	F3_NADfree = dt * (koffNAD*c3_NAD - konNAD*c3_ub*c3_NADfree)

	a = c3_HQ*(k_HQ2E*c3_Eox + k_HQ2F2*c3_F2ox + k_HQ2F4*c3_F4ox + k_HQ2U41*c3_U41ox + k_HQ2U42*c3_U42ox + k_HQ2U43*c3_U43ox + k_HQ2U2*c3_U2ox)
	b1 = c3_SQ*(k_E2SQ*c3_Ered + k_F22SQ*c3_F2red + k_F42SQ*c3_F4red + k_U412SQ*c3_U41red + k_U422SQ*c3_U42red + k_U432SQ*c3_U43red + k_U22SQ*c3_U2red)
	b2 = c3_SQ*(k_SQ2E*c3_Eox + k_SQ2F2*c3_F2ox + k_SQ2F4*c3_F4ox + k_SQ2U41*c3_U41ox + k_SQ2U42*c3_U42ox + k_SQ2U43*c3_U43ox + k_SQ2U2+c3_U2ox)
	c = c3_Q*(k_E2Q*c3_Ered + k_F22Q*c3_F2red + k_F42Q*c3_F4red + k_U412Q*c3_U41red + k_U422Q*c3_U42red + k_U432Q*c3_U43red + k_U22Q*c3_U2red)
	d = c3_Q*k_NADH*c3_NADH
	e = c3_HQ*k_NAD*c3_NAD
	
	F3_HQ = dt * (b1 - a + d - e)
	F3_SQ = dt * (c + a - b1 - b2)
	F3_Q =  dt * (b2 - c - d + e)
	
	F3_Eo = dt * (c3_Ered*(k_E2Q*c3_Q + k_E2SQ*c3_SQ + k_E2F2*c3_F2ox + k_E2F4*c3_F4ox + k_E2U41*c3_U41ox + k_E2U42*c3_U42ox + k_E2U43*c3_U43ox + k_E2U2*c3_U2ox) \
	             - c3_Eox*(k_HQ2E*c3_HQ + k_SQ2E*c3_SQ + k_F22E*c3_F2red + k_F42E*c3_F4red + k_U412E*c3_U41red + k_U422E*c3_U42red + k_U432E*c3_U43red + k_U22E*c3_U2red))
	F3_Er = -1*F3_Eo
	
	F3_F2o = dt * (c3_F2red*(k_F22Q*c3_Q + k_F22SQ*c3_SQ + k_F22E*c3_Eox + k_F22F4*c3_F4ox + k_F22U41*c3_U41ox + k_F22U42*c3_U42ox + k_F22U43*c3_U43ox + k_F22U2*c3_U2ox) \
	              - c3_F2ox*(k_HQ2F2*c3_HQ + k_SQ2F2*c3_SQ + k_E2F2*c3_Ered + k_F42F2*c3_F4red + k_U412F2*c3_U41red + k_U422F2*c3_U42red + k_U432F2*c3_U43red + k_U22F2*c3_U2red))
	F3_F2r = -1*F3_F2o
	
	F3_F4o = dt * (c3_F4red*(k_F42Q*c3_Q + k_F42SQ*c3_SQ + k_F42E*c3_Eox + k_F42F2*c3_F2ox + k_F42U41*c3_U41ox + k_F42U42*c3_U42ox + k_F42U43*c3_U43ox + k_F42U2*c3_U2ox) \
	              - c3_F4ox*(k_HQ2F4*c3_HQ + k_SQ2F4*c3_SQ + k_E2F4*c3_Ered + k_F22F4*c3_F2red + k_U412F4*c3_U41red + k_U422F4*c3_U42red + k_U432F4*c3_U43red + k_U22F4*c3_U2red))
	F3_F4r = -1*F3_F4o
	
	F3_U41o = dt * (c3_U41red*(k_U412Q*c3_Q + k_U412SQ*c3_SQ + k_U412E*c3_Eox + k_U412F2*c3_F2ox + k_U412F4*c3_F4ox + k_U412U42*c3_U42ox + k_U412U43*c3_U43ox + k_U412U2*c3_U2ox) \
	               - c3_U41ox*(k_HQ2U41*c3_HQ + k_SQ2U41*c3_SQ + k_E2U41*c3_Ered + k_F22U41*c3_F2red + k_F42U41*c3_F4red + k_U422U41*c3_U42red + k_U432U41*c3_U43red + k_U22U41*c3_U2red))
	F3_U41r = -1*F3_U41o
	
	F3_U42o = dt * (c3_U42red*(k_U422Q*c3_Q + k_U422SQ*c3_SQ + k_U422E*c3_Eox + k_U422F2*c3_F2ox + k_U422F4*c3_F4ox + k_U422U41*c3_U41ox + k_U422U43*c3_U43ox + k_U422U2*c3_U2ox) \
	               - c3_U42ox*(k_HQ2U42*c3_HQ + k_SQ2U42*c3_SQ + k_E2U42*c3_Ered + k_F22U42*c3_F2red + k_F42U42*c3_F4red + k_U412U42*c3_U41red + k_U432U42*c3_U43red + k_U22U42*c3_U2red))
	F3_U42r = -1*F3_U42o
	
	F3_U43o = dt * (c3_U43red*(k_U432Q*c3_Q + k_U432SQ*c3_SQ + k_U432E*c3_Eox + k_U432F2*c3_F2ox + k_U432F4*c3_F4ox + k_U432U41*c3_U41ox + k_U432U42*c3_U42ox + k_U432U2*c3_U2ox) \
	               - c3_U43ox*(k_HQ2U43*c3_HQ + k_SQ2U43*c3_SQ + k_E2U43*c3_Ered + k_F22U43*c3_F2red + k_F42U43*c3_F4red + k_U412U43*c3_U41red + k_U422U43*c3_U42red + k_U22U43*c3_U2red))
	F3_U43r = -1*F3_U43o
	
	F3_U2o = dt * (c3_U2red*(k_U22Q*c3_Q + k_U22SQ*c3_SQ + k_U22E*c3_Eox + k_U22F2*c3_F2ox + k_U22F4*c3_F4ox + k_U22U41*c3_U41ox + k_U22U42*c3_U42ox + k_U22U43*c3_U43ox) \
	              - c3_U2ox*(k_HQ2U2*c3_HQ + k_SQ2U2*c3_SQ + k_E2U2*c3_Ered + k_F22U2*c3_F2red + k_F42U2*c3_F4red + k_U412U2*c3_U41red + k_U422U2*c3_U42red + k_U432U2*c3_U43red))
	F3_U2r = -1*F3_U2o


	# terms for F4
	c4_NADH = c_NADH + F3_NADH;    c4_NAD = c_NAD + F3_NAD;     c4_ub = c_ub + F3_ub
	c4_NADHfree = c_NADHfree + F3_NADHfree;     c4_NADfree = c_NADfree + F3_NADfree
	c4_Q = c_Q + F3_Q
	c4_SQ = c_SQ + F3_SQ
	c4_HQ = c_HQ + F3_HQ
	c4_Eox = c_Eox + F3_Eo;        c4_Ered = c_Ered + F3_Er
	c4_F2ox = c_F2ox + F3_F2o;     c4_F2red = c_F2red + F3_F2r
	c4_F4ox = c_F4ox + F3_F4o;     c4_F4red = c_F4red + F3_F4r
	c4_U41ox = c_U41ox + F3_U41o;  c4_U41red = c_U41red + F3_U41r
	c4_U42ox = c_U42ox + F3_U42o;  c4_U42red = c_U42red + F3_U42r
	c4_U43ox = c_U43ox + F3_U43o;  c4_U43red = c_U43red + F3_U43r
	c4_U2ox = c_U2ox + F3_U2o;     c4_U2red = c_U2red + F3_U2r


	# Term 4
	F4_NADH = dt * (konNADH*c4_ub*c4_NADHfree - koffNADH*c4_NADH + c4_HQ*k_NAD*c4_NAD - c4_Q*k_NADH*c4_NADH)
	F4_NAD = dt * (konNAD*c4_ub*c4_NADfree - koffNAD*c4_NAD + c4_Q*k_NADH*c4_NADH - c4_HQ*k_NAD*c4_NAD)
	F4_ub = dt * (koffNADH*c4_NADH + koffNAD*c4_NAD - konNADH*c4_ub*c4_NADHfree - konNAD*c4_ub*c4_NADfree)
	F4_NADHfree = dt * (koffNADH*c4_NADH - konNADH*c4_ub*c4_NADHfree)
	F4_NADfree = dt * (koffNAD*c4_NAD - konNAD*c4_ub*c4_NADfree)

	a = c4_HQ*(k_HQ2E*c4_Eox + k_HQ2F2*c4_F2ox + k_HQ2F4*c4_F4ox + k_HQ2U41*c4_U41ox + k_HQ2U42*c4_U42ox + k_HQ2U43*c4_U43ox + k_HQ2U2*c4_U2ox)
	b1 = c4_SQ*(k_E2SQ*c4_Ered + k_F22SQ*c4_F2red + k_F42SQ*c4_F4red + k_U412SQ*c4_U41red + k_U422SQ*c4_U42red + k_U432SQ*c4_U43red + k_U22SQ*c4_U2red)
	b2 = c4_SQ*(k_SQ2E*c4_Eox + k_SQ2F2*c4_F2ox + k_SQ2F4*c4_F4ox + k_SQ2U41*c4_U41ox + k_SQ2U42*c4_U42ox + k_SQ2U43*c4_U43ox + k_SQ2U2+c4_U2ox)
	c = c4_Q*(k_E2Q*c4_Ered + k_F22Q*c4_F2red + k_F42Q*c4_F4red + k_U412Q*c4_U41red + k_U422Q*c4_U42red + k_U432Q*c4_U43red + k_U22Q*c4_U2red)
	d = c4_Q*k_NADH*c4_NADH
	e = c4_HQ*k_NAD*c4_NAD
	
	F4_HQ = dt * (b1 - a + d - e)
	F4_SQ = dt * (c + a - b1 - b2)
	F4_Q =  dt * (b2 - c - d + e)

	F4_Eo = dt * (c4_Ered*(k_E2Q*c4_Q + k_E2SQ*c4_SQ + k_E2F2*c4_F2ox + k_E2F4*c4_F4ox + k_E2U41*c4_U41ox + k_E2U42*c4_U42ox + k_E2U43*c4_U43ox + k_E2U2*c4_U2ox) \
	             - c4_Eox*(k_HQ2E*c4_HQ + k_SQ2E*c4_SQ + k_F22E*c4_F2red + k_F42E*c4_F4red + k_U412E*c4_U41red + k_U422E*c4_U42red + k_U432E*c4_U43red + k_U22E*c4_U2red))
	F4_Er = -1*F4_Eo
	
	F4_F2o = dt * (c4_F2red*(k_F22Q*c4_Q + k_F22SQ*c4_SQ + k_F22E*c4_Eox + k_F22F4*c4_F4ox + k_F22U41*c4_U41ox + k_F22U42*c4_U42ox + k_F22U43*c4_U43ox + k_F22U2*c4_U2ox) \
	              - c4_F2ox*(k_HQ2F2*c4_HQ + k_SQ2F2*c4_SQ + k_E2F2*c4_Ered + k_F42F2*c4_F4red + k_U412F2*c4_U41red + k_U422F2*c4_U42red + k_U432F2*c4_U43red + k_U22F2*c4_U2red))
	F4_F2r = -1*F4_F2o
	 
	F4_F4o = dt * (c4_F4red*(k_F42Q*c4_Q + k_F42SQ*c4_SQ + k_F42E*c4_Eox + k_F42F2*c4_F2ox + k_F42U41*c4_U41ox + k_F42U42*c4_U42ox + k_F42U43*c4_U43ox + k_F42U2*c4_U2ox) \
	              - c4_F4ox*(k_HQ2F4*c4_HQ + k_SQ2F4*c4_SQ + k_E2F4*c4_Ered + k_F22F4*c4_F2red + k_U412F4*c4_U41red + k_U422F4*c4_U42red + k_U432F4*c4_U43red + k_U22F4*c4_U2red))
	F4_F4r = -1*F4_F4o
	 
	F4_U41o = dt * (c4_U41red*(k_U412Q*c4_Q + k_U412SQ*c4_SQ + k_U412E*c4_Eox + k_U412F2*c4_F2ox + k_U412F4*c4_F4ox + k_U412U42*c4_U42ox + k_U412U43*c4_U43ox + k_U412U2*c4_U2ox) \
	               - c4_U41ox*(k_HQ2U41*c4_HQ + k_SQ2U41*c4_SQ + k_E2U41*c4_Ered + k_F22U41*c4_F2red + k_F42U41*c4_F4red + k_U422U41*c4_U42red + k_U432U41*c4_U43red + k_U22U41*c4_U2red))
	F4_U41r = -1*F4_U41o
	
	F4_U42o = dt * (c4_U42red*(k_U422Q*c4_Q + k_U422SQ*c4_SQ + k_U422E*c4_Eox + k_U422F2*c4_F2ox + k_U422F4*c4_F4ox + k_U422U41*c4_U41ox + k_U422U43*c4_U43ox + k_U422U2*c4_U2ox) \
	               - c4_U42ox*(k_HQ2U42*c4_HQ + k_SQ2U42*c4_SQ + k_E2U42*c4_Ered + k_F22U42*c4_F2red + k_F42U42*c4_F4red + k_U412U42*c4_U41red + k_U432U42*c4_U43red + k_U22U42*c4_U2red))
	F4_U42r = -1*F4_U42o
	
	F4_U43o = dt * (c4_U43red*(k_U432Q*c4_Q + k_U432SQ*c4_SQ + k_U432E*c4_Eox + k_U432F2*c4_F2ox + k_U432F4*c4_F4ox + k_U432U41*c4_U41ox + k_U432U42*c4_U42ox + k_U432U2*c4_U2ox) \
	               - c4_U43ox*(k_HQ2U43*c4_HQ + k_SQ2U43*c4_SQ + k_E2U43*c4_Ered + k_F22U43*c4_F2red + k_F42U43*c4_F4red + k_U412U43*c4_U41red + k_U422U43*c4_U42red + k_U22U43*c4_U2red))
	F4_U43r = -1*F4_U43o
	 
	F4_U2o = dt * (c4_U2red*(k_U22Q*c4_Q + k_U22SQ*c4_SQ + k_U22E*c4_Eox + k_U22F2*c4_F2ox + k_U22F4*c4_F4ox + k_U22U41*c4_U41ox + k_U22U42*c4_U42ox + k_U22U43*c4_U43ox) \
	              - c4_U2ox*(k_HQ2U2*c4_HQ + k_SQ2U2*c4_SQ + k_E2U2*c4_Ered + k_F22U2*c4_F2red + k_F42U2*c4_F4red + k_U412U2*c4_U41red + k_U422U2*c4_U42red + k_U432U2*c4_U43red))
	F4_U2r = -1*F4_U2o	


	# calculate step
	dNADH = (1/6)*F1_NADH + (1/3)*F2_NADH + (1/3)*F3_NADH + (1/6)*F4_NADH
	dNAD = (1/6)*F1_NAD + (1/3)*F2_NAD + (1/3)*F3_NAD + (1/6)*F4_NAD
	dub = (1/6)*F1_ub + (1/3)*F2_ub + (1/3)*F3_ub + (1/6)*F4_ub
	dNADHfree = (1/6)*F1_NADHfree + (1/3)*F2_NADHfree + (1/3)*F3_NADHfree + (1/6)*F4_NADHfree
	dNADfree = (1/6)*F1_NADfree + (1/3)*F2_NADfree + (1/3)*F3_NADfree + (1/6)*F4_NADfree
	dHQ = (1/6)*F1_HQ + (1/3)*F2_HQ + (1/3)*F3_HQ + (1/6)*F4_HQ
	dSQ = (1/6)*F1_SQ + (1/3)*F2_SQ + (1/3)*F3_SQ + (1/6)*F4_SQ
	dQ = (1/6)*F1_Q + (1/3)*F2_Q + (1/3)*F3_Q + (1/6)*F4_Q
	dEo = (1/6)*F1_Eo + (1/3)*F2_Eo + (1/3)*F3_Eo + (1/6)*F4_Eo
	dEr = (1/6)*F1_Er + (1/3)*F2_Er + (1/3)*F3_Er + (1/6)*F4_Er
	dF2o = (1/6)*F1_F2o + (1/3)*F2_F2o + (1/3)*F3_F2o + (1/6)*F4_F2o
	dF2r = (1/6)*F1_F2r + (1/3)*F2_F2r + (1/3)*F3_F2r + (1/6)*F4_F2r
	dF4o = (1/6)*F1_F4o + (1/3)*F2_F4o + (1/3)*F3_F4o + (1/6)*F4_F4o
	dF4r = (1/6)*F1_F4r + (1/3)*F2_F4r + (1/3)*F3_F4r + (1/6)*F4_F4r
	dU41o = (1/6)*F1_U41o + (1/3)*F2_U41o + (1/3)*F3_U41o + (1/6)*F4_U41o
	dU41r = (1/6)*F1_U41r + (1/3)*F2_U41r + (1/3)*F3_U41r + (1/6)*F4_U41r
	dU42o = (1/6)*F1_U42o + (1/3)*F2_U42o + (1/3)*F3_U42o + (1/6)*F4_U42o
	dU42r = (1/6)*F1_U42r + (1/3)*F2_U42r + (1/3)*F3_U42r + (1/6)*F4_U42r
	dU43o = (1/6)*F1_U43o + (1/3)*F2_U43o + (1/3)*F3_U43o + (1/6)*F4_U43o
	dU43r = (1/6)*F1_U43r + (1/3)*F2_U43r + (1/3)*F3_U43r + (1/6)*F4_U43r
	dU2o = (1/6)*F1_U2o + (1/3)*F2_U2o + (1/3)*F3_U2o + (1/6)*F4_U2o
	dU2r = (1/6)*F1_U2r + (1/3)*F2_U2r + (1/3)*F3_U2r + (1/6)*F4_U2r

	# evaluate step size
	dAll = np.array([dNADH,dNAD,dub,dNADHfree,dNADfree,dHQ,dSQ,dQ,dEo,dEr,dF2o,dF2r,dF4o,dF4r,dU41o,dU41r,dU42o,dU42r,dU43o,dU43r,dU2o,dU2r])
	abs_dy = np.abs(dAll)
	max_abs_dy = np.max(abs_dy)

	if max_abs_dy <= tol:
		proceed = True
		dt = dt*2.5
		if dt > maxdt:
			dt = maxdt
	elif max_abs_dy > tol:
		dt = dt / 2.0
		proceed = False


	# calculate new populations
	if proceed:
		c_NADH += dNADH;  c_NAD += dNAD;     c_ub += dub
		c_NADHfree += dNADHfree;             c_NADfree += dNADfree
		c_HQ += dHQ;      c_SQ += dSQ;       c_Q += dQ
		c_Eox += dEo;     c_Ered += dEr
		c_F2ox += dF2o;   c_F2red += dF2r
		c_F4ox += dF4o;   c_F4red += dF4r
		c_U41ox += dU41o; c_U41red += dU41r
		c_U42ox += dU42o; c_U42red += dU42r
		c_U43ox += dU43o; c_U43red += dU43r
		c_U2ox += dU2o;   c_U2red += dU2r
	
	
		population[:,i] = np.array([c_NADH,c_NAD,c_ub,c_NADHfree,c_NADfree,c_HQ,c_SQ,c_Q,c_Eox,c_Ered,c_F2ox,c_F2red,c_F4ox,c_F4red,c_U41ox,c_U41red,c_U42ox,c_U42red,c_U43ox,c_U43red,c_U2ox,c_U2red])
		time_array[i] = time_val
	
		i += 1; itot += 1; time_val += dt

		if i % 10000 == 0:
			j = i-100
			print('time elapsed = %.5e seconds' % time_val)
			if plotrealtime:
				ax1.plot(time_array,population[0,j:i],color='k',label='NADH')
				ax1.plot(time_array,population[1,j:i],color=[0.2,0.2,0.2],label='NAD')
				ax1.plot(time_array,population[2,j:i],color=[0.6,0.6,0.6],label='unbound')
				ax1.set_xscale('log')

				ax2.plot(time_array[j:i],population[5,j:i],color='r',label='HQ')
				ax2.plot(time_array[j:i],population[6,j:i],color='b',label='SQ')
				ax2.plot(time_array[j:i],population[7,j:i],color='g',label='Q')
				ax2.set_xscale('log')

				ax3.plot(time_array[j:i],population[9,j:i],color='r',label='E')   # E  reduced pop
				ax3.plot(time_array[j:i],population[11,j:i],color='c',label='F1') # F1 reduced pop
				ax3.plot(time_array[j:i],population[13,j:i],color='y',label='F2') # F2 reduced pop
				ax3.plot(time_array[j:i],population[21,j:i],color='m',label='U1') # U1 reduced pop
				ax3.plot(time_array[j:i],population[15,j:i],color='k',label='U2') # U2 reduced pop
				ax3.plot(time_array[j:i],population[17,j:i],color='g',label='U3') # U3 reduced pop
				ax3.plot(time_array[j:i],population[19,j:i],color='b',label='U4') # U4 reduced pop
				ax3.set_xscale('log')
				plt.pause(0.05)

		if i % 100000 == 0:
			tm1 = time_array[:i]
			pop1 = population[:,:i]
			tm2,pop2 = select_subset(tm1,pop1)
			if first:
				tm = tm2
				pop = pop2
			else:
				tm = np.append(tm,tm2)
				pop = np.append(pop,pop2,axis=1)
			first = False

			# reinitialize time_array and population
			time_array = np.zeros(ni+1)
			population = np.zeros([len(P),ni+1])
			i = 0
			

			fOUT = open('HoxEFU_electron_dynamics_temp.txt','w')
			print('time(s)\tHQ\tSQ\tQ\tE\tF1\tF2\tU1\tU2\tU3-His\tU4\tNADH\tNAD\tunbound\tNADHfree\tNADfree',file=fOUT)
			for j in range(len(tm)):
				print('%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e' % (tm[j],pop[5,j],pop[6,j],pop[7,j],pop[9,j],pop[11,j],pop[13,j],pop[21,j],pop[15,j],pop[17,j],pop[19,j],pop[0,j],pop[1,j],pop[2,j],pop[3,j],pop[4,j]),file=fOUT)
			fOUT.close()

time_array = tm
population = pop

# only save 100 data points per decade
#time_array,population = select_subset(time_array,population)

end = time.time(); elapsed=(end-start)/60
print('Integration complete: time elapsed = %.3f min' % elapsed)

fOUT = open('HoxEFU_electron_dynamics.txt','w')
print('time(s)\tHQ\tSQ\tQ\tE\tF1\tF2\tU1\tU2\tU3-His\tU4',file=fOUT)
for i in range(len(time_array)):
        print('%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e\t%.5e' % (time_array[i],population[2,i],population[3,i],population[4,i],population[6,i],population[8,i],population[10,i],population[18,i],population[12,i],population[14,i],population[16,i]),file=fOUT)
fOUT.close()


# generate plot with final data
ax1.plot(time_array,population[0,:],color='k',label='NADH')
ax1.plot(time_array,population[1,:],color=[0.2,0.2,0.2],label='NAD')
ax1.plot(time_array,population[2,:],color=[0.6,0.6,0.6],label='unbound')
ax1.set_xscale('log')

ax2.plot(time_array,population[5,:],color='r',label='HQ')
ax2.plot(time_array,population[6,:],color='b',label='SQ')
ax2.plot(time_array,population[7,:],color='g',label='Q')
ax2.set_xscale('log')

ax3.plot(time_array,population[9,:],color='r',label='E')   # E  reduced pop
ax3.plot(time_array,population[11,:],color='c',label='F1')  # F1 reduced pop
ax3.plot(time_array,population[13,:],color='y',label='F2') # F2 reduced pop
ax3.plot(time_array,population[21,:],color='m',label='U1') # U1 reduced pop
ax3.plot(time_array,population[15,:],color='k',label='U2') # U2 reduced pop
ax3.plot(time_array,population[17,:],color='g',label='U3') # U3 reduced pop
ax3.plot(time_array,population[19,:],color='b',label='U4') # U4 reduced pop
ax3.set_xscale('log')

plt.show()




