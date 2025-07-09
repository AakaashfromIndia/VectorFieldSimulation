import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import FancyArrowPatch
from scipy.interpolate import griddata

width, height = 10, 10
resolution = 20
high_res = 200
x = np.linspace(-width/2, width/2, resolution)
y = np.linspace(-height/2, height/2, resolution)
X, Y = np.meshgrid(x, y)

x_high = np.linspace(-width/2, width/2, high_res)
y_high = np.linspace(-height/2, height/2, high_res)
X_high, Y_high = np.meshgrid(x_high, y_high)

a = float(input('Enter a (x component): '))
b = float(input('Enter b (y component): '))
print(a,"î","+",b,"ĵ")

U_init = a * np.ones_like(X)
V_init = b * np.ones_like(Y)
U_res = U_init.copy()
V_res = V_init.copy()

def calculate_properties(U, V, x, y):
    dU_dx, dU_dy = np.gradient(U, x, y, edge_order=2)
    dV_dx, dV_dy = np.gradient(V, x, y, edge_order=2)
    grad_mag = np.sqrt(dU_dx**2 + dU_dy**2 + dV_dx**2 + dV_dy**2)
    divergence = dU_dx + dV_dy
    curl = dV_dx - dU_dy
    return grad_mag, divergence, curl

fig, axs = plt.subplots(1, 2, figsize=(13, 6))
plt.subplots_adjust(left=0.07, right=0.89, bottom=0.28)
quiver_init = axs[0].quiver(X, Y, U_init, V_init, color='k')
axs[0].set_title('Initial Field (Draw Arrows)')
axs[0].set_xlim(-width/2, width/2)
axs[0].set_ylim(-height/2, height/2)
axs[0].grid(True, linestyle='--')

quiver_res = axs[1].quiver(X, Y, U_res, V_res, color='k')
axs[1].set_title('Resultant Field')
axs[1].set_xlim(-width/2, width/2)
axs[1].set_ylim(-height/2, height/2)
axs[1].grid(True, linestyle='--')

orig_pos_rhs = axs[1].get_position().frozen()
cax = fig.add_axes([0.91, 0.13, 0.015, 0.7])

drawn_arrows = []
drawing = False
start = None
live_arrow = None
heatmap_res = None

def interpolate_property(prop):
    points = np.vstack((X.ravel(), Y.ravel())).T
    return griddata(points, prop.ravel(), (X_high, Y_high), method='cubic')

def clear_rhs_overlay():
    global heatmap_res
    if heatmap_res is not None:
        try:
            heatmap_res.remove()
        except Exception:
            pass
        heatmap_res = None
    cax.cla()
    axs[1].set_position(orig_pos_rhs)
    plt.draw()

def show_field_res(event=None):
    clear_rhs_overlay()
    quiver_res.set_UVC(U_res, V_res)
    quiver_res.set_visible(True)
    axs[1].set_title('Resultant Field')
    plt.draw()

def overlay_heatmap(mode):
    clear_rhs_overlay()
    grad, div, curl = calculate_properties(U_res, V_res, x, y)
    if mode == 'gradient':
        data = interpolate_property(grad)
        cmap = 'viridis'
        title = 'Gradient Overlay'
    elif mode == 'divergence':
        data = interpolate_property(div)
        cmap = 'coolwarm'
        title = 'Divergence Overlay'
    elif mode == 'curl':
        data = interpolate_property(curl)
        cmap = 'plasma'
        title = 'Curl Overlay'
    else:
        return
    global heatmap_res
    heatmap_res = axs[1].imshow(
        data, extent=[-width/2, width/2, -height/2, height/2],
        origin='lower', cmap=cmap, alpha=0.6, aspect='auto'
    )
    cb = fig.colorbar(heatmap_res, cax=cax)
    cb.ax.tick_params(labelsize=10)
    axs[1].set_title(f'Resultant Field + {title}')
    quiver_res.set_UVC(U_res, V_res)
    quiver_res.set_visible(True)
    plt.draw()

def overlay_gradient(event=None):
    overlay_heatmap('gradient')

def overlay_divergence(event=None):
    overlay_heatmap('divergence')

def overlay_curl(event=None):
    overlay_heatmap('curl')

def on_press(event):
    global drawing, start, live_arrow
    if event.inaxes != axs[0]:
        return
    drawing = True
    start = (event.xdata, event.ydata)
    if live_arrow:
        live_arrow.remove()
        live_arrow = None

def on_motion(event):
    global live_arrow, start
    if not drawing or start is None or event.inaxes != axs[0]:
        return
    x0, y0 = start
    x1, y1 = event.xdata, event.ydata
    if live_arrow:
        live_arrow.remove()
    live_arrow = FancyArrowPatch((x0, y0), (x1, y1), color='red', arrowstyle='->', mutation_scale=18, linewidth=2)
    axs[0].add_patch(live_arrow)
    plt.draw()

def on_release(event):
    global drawing, start, live_arrow
    if not drawing or start is None or event.inaxes != axs[0]:
        return
    x0, y0 = start
    x1, y1 = event.xdata, event.ydata
    if x0 is None or y0 is None or x1 is None or y1 is None:
        drawing = False
        start = None
        return
    arr = FancyArrowPatch((x0, y0), (x1, y1), color='red', arrowstyle='->', mutation_scale=18, linewidth=2)
    axs[0].add_patch(arr)
    drawn_arrows.append(((x0, y0), (x1, y1)))
    if live_arrow:
        live_arrow.remove()
        live_arrow = None
    plt.draw()
    drawing = False
    start = None

def calculate_resultant(event=None):
    global U_res, V_res
    U_res = U_init.copy()
    V_res = V_init.copy()
    influence_strength = 2.0  # Adjust for effect
    for arrow in drawn_arrows:
        (x0, y0), (x1, y1) = arrow
        dx, dy = x1 - x0, y1 - y0
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                rx, ry = X[i, j] - x0, Y[i, j] - y0
                dist = np.hypot(rx, ry) + 1e-5  # Avoid div by zero
                U_res[i, j] += influence_strength * dx / dist
                V_res[i, j] += influence_strength * dy / dist
    show_field_res()

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# RHS Buttons (for overlays)
axfield_res = plt.axes([0.55, 0.17, 0.15, 0.06])
axgrad_res = plt.axes([0.72, 0.17, 0.15, 0.06])
axdiv_res  = plt.axes([0.55, 0.08, 0.15, 0.06])
axcurl_res = plt.axes([0.72, 0.08, 0.15, 0.06])
bfield_res = Button(axfield_res, 'Display only field')
bgrad_res = Button(axgrad_res, 'Overlay gradient')
bdiv_res = Button(axdiv_res, 'Overlay divergence')
bcurl_res = Button(axcurl_res, 'Overlay curl')
bfield_res.on_clicked(show_field_res)
bgrad_res.on_clicked(overlay_gradient)
bdiv_res.on_clicked(overlay_divergence)
bcurl_res.on_clicked(overlay_curl)

# Calculate Resultant Button
axcalc = plt.axes([0.12, 0.12, 0.27, 0.06])
bcalc = Button(axcalc, 'Calculate Resultant')
bcalc.on_clicked(calculate_resultant)

plt.show()
