"""
.. _tut_viz_evoked:

=====================
Visualize Evoked data
=====================
"""
import os.path as op
import numpy as np
import matplotlib.pyplot as plt

import mne

###############################################################################
# In this tutorial we focus on plotting functions of :class:`mne.Evoked`.
# Here we read the evoked object from a file. Check out
# :ref:`tut_epoching_and_averaging` to get to this stage from raw data.
data_path = mne.datasets.sample.data_path()
fname = op.join(data_path, 'MEG', 'sample', 'sample_audvis-ave.fif')
evoked = mne.read_evokeds(fname, baseline=(None, 0), proj=True)
print(evoked)

###############################################################################
# Notice that ``evoked`` is a list of evoked instances. You can read only one
# of the categories by passing the argument ``condition`` to
# :func:`mne.read_evokeds`. To make things more simple for this tutorial, we
# read each instance to a variable.
evoked_l_aud = evoked[0]
evoked_r_aud = evoked[1]
evoked_l_vis = evoked[2]
evoked_r_vis = evoked[3]

###############################################################################
# Let's start with a simple one. We plot event related potentials / fields
# (ERP/ERF). The bad channels are not plotted by default. Here we explicitly
# set the exclude parameter to show the bad channels in red. All plotting
# functions of MNE-python return a handle to the figure instance. When we have
# the handle, we can customise the plots to our liking.
fig = evoked_l_aud.plot(exclude=())

###############################################################################
# All plotting functions of MNE-python returns a handle to the figure instance.
# When we have the handle, we can customise the plots to our liking. We can get
# rid of the empty space with a simple function call.
fig.tight_layout()

###############################################################################
# Now let's make it a bit fancier and only use MEG channels. Many of the
# MNE-functions include a ``picks`` parameter to include a selection of
# channels. ``picks`` is simply a list of channel indices that you can easily
# construct with :func:`mne.pick_types`. See also :func:`mne.pick_channels` and
# :func:`mne.pick_channels_regexp`.
# Using ``spatial_colors=True``, the individual channel lines are color coded
# to show the sensor positions - specifically, the x, y, and z locations of
# the sensors are transformed into R, G and B values.
picks = mne.pick_types(evoked_l_aud.info, meg=True, eeg=False, eog=False)
evoked_l_aud.plot(spatial_colors=True, gfp=True, picks=picks)

###############################################################################
# Notice the legend on the left. The colors would suggest that there may be two
# separate sources for the signals. This wasn't obvious from the first figure.
# Try painting the slopes with left mouse button. It should open a new window
# with topomaps (scalp plots) of the average over the painted area. There is
# also a function for drawing topomaps separately.
evoked_l_aud.plot_topomap()

###############################################################################
# By default the topomaps are drawn from evenly spread out points of time over
# the evoked data. We can also define the times ourselves.
times = np.arange(0.05, 0.151, 0.05)
evoked_r_aud.plot_topomap(times=times, ch_type='mag')

###############################################################################
# Or we can automatically select the peaks.
evoked_r_aud.plot_topomap(times='peaks', ch_type='mag')

###############################################################################
# You can take a look at the documentation of :func:`mne.Evoked.plot_topomap`
# or simply write ``evoked_r_aud.plot_topomap?`` in your python console to
# see the different parameters you can pass to this function. Most of the
# plotting functions also accept ``axes`` parameter. With that, you can
# customise your plots even further. First we shall create a set of matplotlib
# axes in a single figure and plot all of our evoked categories next to each
# other.
fig, ax = plt.subplots(1, 5)
evoked_l_aud.plot_topomap(times=0.1, axes=ax[0], show=False)
evoked_r_aud.plot_topomap(times=0.1, axes=ax[1], show=False)
evoked_l_vis.plot_topomap(times=0.1, axes=ax[2], show=False)
evoked_r_vis.plot_topomap(times=0.1, axes=ax[3], show=True)

###############################################################################
# Notice that we created five axes, but had only four categories. The fifth
# axes was used for drawing the colorbar. You must provide room for it when you
# create this kind of custom plots or turn the colorbar off with
# ``colorbar=False``. That's what the warnings are trying to tell you. Also, we
# used ``show=False`` for the three first function calls. This prevents the
# showing of the figure prematurely. The behavior depends on the mode you are
# using for your python session. See http://matplotlib.org/users/shell.html for
# more information.
#
# We can combine the two kinds of plots in one figure using the ``plot_joint``
# method of Evoked objects. Called as-is (``evoked.plot_joint()``), this
# function should give a stylish and informative display of spatio-temporal
# dynamics. Also note the ``topomap_args`` and ``ts_args`` parameters of
# :func:`mne.Evoked.plot_joint`. You can pass key-value pairs as a python
# dictionary that gets passed as parameters to the topomaps
# (:func:`mne.Evoked.plot_topomap`) and time series (:func:`mne.Evoked.plot`)
# of the joint plot.
# For specific styling, use these ``topomap_args`` and ``ts_args``
# arguments. Here, topomaps at specific time points (70 and 105 msec) are
# shown, sensors are not plotted, and the Global Field Power is shown:
ts_args = dict(gfp=True)
topomap_args = dict(sensors=False)
evoked_r_aud.plot_joint(title='right auditory', times=[.07, .105],
                        ts_args=ts_args, topomap_args=topomap_args)

###############################################################################
# We can also plot the activations as images. The time runs along the x-axis
# and the channels along the y-axis. The amplitudes are color coded so that
# the amplitudes from negative to positive translates to shift from blue to
# red. White means zero amplitude. You can use the ``cmap`` parameter to define
# the color map yourself. The accepted values include all matplotlib colormaps.
evoked_r_aud.plot_image(picks=picks)

###############################################################################
# Finally we plot the sensor data as a topographical view. In the simple case
# we plot only left auditory responses, and then we plot them all in the same
# figure for comparison. Click on the individual plots to open them bigger.
title = 'MNE sample data (condition : %s)'
evoked_l_aud.plot_topo(title=title % evoked_l_aud.comment)
colors = 'yellow', 'green', 'red', 'blue'
mne.viz.plot_evoked_topo(evoked, color=colors,
                         title=title % 'Left/Right Auditory/Visual')

###############################################################################
# Visualizing field lines in 3D
# -----------------------------
#
# We now compute the field maps to project MEG and EEG data to MEG helmet
# and scalp surface.
#
# To do this we'll need coregistration information. See
# :ref:`tut_forward` for more details.
#
# Here we just illustrate usage.

subjects_dir = data_path + '/subjects'
trans_fname = data_path + '/MEG/sample/sample_audvis_raw-trans.fif'

maps = mne.make_field_map(evoked_l_aud, trans=trans_fname, subject='sample',
                          subjects_dir=subjects_dir, n_jobs=1)

# explore several points in time
field_map = evoked_l_aud.plot_field(maps, time=.1)

###############################################################################
# .. note::
#     If trans_fname is set to None then only MEG estimates can be visualized.
