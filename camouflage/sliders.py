import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider

from config import ha
from onepair import model

plt.rcParams['figure.figsize'] = [12, 6]

def ix(v,x):
    n = (v - x[0])/(x[-1] - x[0]) * (len(x)-1)
    return round(n)

# Figure and subplots
fig, ax = plt.subplots()
fig.subplots_adjust(left=0.5, bottom=0.25)

# Horizontal slider
init_tperi = 0.1
ax_tperi = fig.add_axes([0.5, 0.1, 0.4, 0.03])
tperi_slider = Slider(
    ax=ax_tperi,
    label='T_peri',
    valmin=0,
    valmax=1,
    valinit=init_tperi,
)

# Vertical sliders
slax = [0,0,0,0,0,0,0]
slider = [0,0,0,0,0,0,0]
pname = ['$e$',r'$\omega$',r'$\theta_1$',r'$\theta_2$','$a$','$I$',r'$\Omega$']
valmin = [0,   0, 0.1, 0.1,   1,   0,  0]
valmax = [1, 360, 2.0, 2.0, 3, 180, 180]
valinit = [0.146, 300, 0.78, 0.45, 1.5, 114, 132]

S = len(slax)

for s in range(S):
    slax[s] = fig.add_axes([0.05+s/18, 0.25, 0.0225, 0.63])
    slider[s] = Slider(
    ax=slax[s],
    label=pname[s],
    valmin=valmin[s],
    valmax=valmax[s],
    valinit=valinit[s],
    orientation="vertical"
)

# Create mock data
#
e,aper,one,two,a,inc,lasc = [s.val for s in slider]
iph = tperi_slider.val
jd0 = 2460000
jd = jd0 + np.random.random(120) * 10
per = 4.0145
mea = ((jd - jd0) % per) * 2*np.pi/per
data = model(ha(jd),mea-2*np.pi*iph,e,aper,one,two,a,inc,lasc)
data += 0.05 * np.random.random(len(data))

# Initialize main plot
#
Ph,H = 360, 360
hg = np.linspace(-np.pi,np.pi,H)
ph = np.linspace(0,2*np.pi,Ph)
sig = np.zeros(shape=(H,Ph))

def reval():
    global sig
    e,aper,one,two,a,inc,lasc = [s.val for s in slider]
    iph = tperi_slider.val
    for i,f in enumerate(ph):
        sig[:,i] = model(hg,f-2*np.pi*iph,e,aper,one,two,a,inc,lasc)
    for n in range(len(jd)):
        i = ix(mea[n],ph)
        j = ix(ha(jd[n]),hg)
        S = 2
        sig[j-S:j+S,i-S:i+S] = data[n]
    sig[0,0] = 0
    sig[-1,-1] = 1

reval()

obj = ax.imshow(sig)
ax.set_xlabel('Orbital phase (deg)')
ax.set_ylabel('Hour angle (deg)')

# When a slider value changes
#
def update(val):
    reval()
    obj.set_data(sig)
    fig.canvas.draw()

tperi_slider.on_changed(update)
for s in range(S):
    slider[s].on_changed(update)

# Reset button and function
#
resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.975')

def reset(event):
    tperi_slider.reset()
    for s in range(S):
        slider[s].reset()

button.on_clicked(reset)

plt.show()
