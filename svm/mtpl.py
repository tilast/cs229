from matplotlib import pyplot as plt
#
# current_color = 'red'
#
# class LineBuilder:
#     def __init__(self, line):
#         self.line = line
#         self.xs = list(line.get_xdata())
#         self.ys = list(line.get_ydata())
#         self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
#
#     def __call__(self, event):
#         print('click', event)
#         if event.inaxes!=self.line.axes: return
#         self.xs.append(event.xdata)
#         self.ys.append(event.ydata)
#         self.line.set_data(self.xs, self.ys)
#
#         self.line.figure.canvas.draw()
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click to build line segments')
# line, = ax.plot([], [], 'bx')  # empty line
# line2, = ax.plot([], [], 'ro')  # empty line
# linebuilder = LineBuilder(line)
# linebuilder2 = LineBuilder(line2)
#
# radio = RadioButtons(ax, ('red', 'blue'))
#
# def hzfunc(label):
#     hzdict = {}
#     ydata = hzdict[label]
#     l.set_ydata(ydata)
#     plt.draw()
# radio.on_clicked(hzfunc)
#
#
# plt.show()
#
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Button
#
# freqs = np.arange(2, 20, 3)
#
# fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.2)
# t = np.arange(0.0, 1.0, 0.001)
# s = np.sin(2*np.pi*freqs[0]*t)
# l, = plt.plot(t, s, lw=2)
#
#
# class Index(object):
#     ind = 0
#
#     def next(self, event):
#         self.ind += 1
#         i = self.ind % len(freqs)
#         ydata = np.sin(2*np.pi*freqs[i]*t)
#         l.set_ydata(ydata)
#         plt.draw()
#
#     def prev(self, event):
#         self.ind -= 1
#         i = self.ind % len(freqs)
#         ydata = np.sin(2*np.pi*freqs[i]*t)
#         l.set_ydata(ydata)
#         plt.draw()
#
# callback = Index()
# axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
# axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
# bnext = Button(axnext, 'Next')
# bnext.on_clicked(callback.next)
# bprev = Button(axprev, 'Previous')
# bprev.on_clicked(callback.prev)
#
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import CheckButtons
#
# t = np.arange(0.0, 2.0, 0.01)
# s0 = np.sin(2*np.pi*t)
# s1 = np.sin(4*np.pi*t)
# s2 = np.sin(6*np.pi*t)
#
# fig, ax = plt.subplots()
# l0, = ax.plot(t, s0, visible=False, lw=2)
# l1, = ax.plot(t, s1, lw=2)
# l2, = ax.plot(t, s2, lw=2)
# plt.subplots_adjust(left=0.2)
#
# rax = plt.axes([0.05, 0.4, 0.1, 0.15])
# check = CheckButtons(rax, ('2 Hz', '4 Hz', '6 Hz'), (False, True, True))
#
#
# def func(label):
#     if label == '2 Hz':
#         l0.set_visible(not l0.get_visible())
#     elif label == '4 Hz':
#         l1.set_visible(not l1.get_visible())
#     elif label == '6 Hz':
#         l2.set_visible(not l2.get_visible())
#     plt.draw()
# check.on_clicked(func)
#
# plt.show()

class clicker_class(object):
    def __init__(self, ax, pix_err=1):
        self.canvas = ax.get_figure().canvas
        self.cid = None
        self.pt_lst = []
        self.pt_plot = ax.plot([], [], marker='o',
                               linestyle='none', zorder=5)[0]
        self.pix_err = pix_err
        self.connect_sf()

    def set_visible(self, visible):
        '''sets if the curves are visible '''
        self.pt_plot.set_visible(visible)

    def clear(self):
        '''Clears the points'''
        self.pt_lst = []
        self.redraw()

    def connect_sf(self):
        if self.cid is None:
            self.cid = self.canvas.mpl_connect('button_press_event',
                                               self.click_event)

    def disconnect_sf(self):
        if self.cid is not None:
            self.canvas.mpl_disconnect(self.cid)
            self.cid = None

    def click_event(self, event):
        ''' Extracts locations from the user'''
        if event.key == 'shift':
            self.pt_lst = []
            return
        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:
            self.pt_lst.append((event.xdata, event.ydata))
        elif event.button == 3:
            self.remove_pt((event.xdata, event.ydata))

        self.redraw()

    def remove_pt(self, loc):
        if len(self.pt_lst) > 0:
            self.pt_lst.pop(np.argmin(map(lambda x:
                                          np.sqrt((x[0] - loc[0]) ** 2 +
                                                  (x[1] - loc[1]) ** 2),
                                          self.pt_lst)))

    def redraw(self):
        if len(self.pt_lst) > 0:
            x, y = zip(*self.pt_lst)
        else:
            x, y = [], []
        self.pt_plot.set_xdata(x)
        self.pt_plot.set_ydata(y)

        self.canvas.draw()

    def return_points(self):
        '''Returns the clicked points in the format the rest of the code expects'''
        return np.vstack(self.pt_lst).T

ax = plt.gca()
cc = clicker_class(ax)
plt.show()
