import os

import numpy as np
import matplotlib.pyplot as plt
from skijumpdesign import Skier, Surface
from skijumpdesign.functions import make_jump

PATH_TO_THIS_FILE = os.path.abspath(__file__)
DIR_OF_THIS_FILE = os.path.dirname(PATH_TO_THIS_FILE)
PROJECT_ROOT = os.path.abspath(os.path.join(DIR_OF_THIS_FILE, '..'))


def compare_measured_to_designed(measured_surface, equiv_fall_height,
                                 parent_slope_angle, approach_length,
                                 takeoff_angle, xlim, ylim_top, ylim_bot,
                                 med_speed=None):

    skier = Skier()

    # NOTE : A different Skier() object is used internally in make_jump()
    slope, approach, takeoff, landing, landing_trans, flight, outputs = \
        make_jump(parent_slope_angle, 0.0, approach_length, takeoff_angle,
                  equiv_fall_height)

    # move the designed jump takeoff point to 0, 0
    delx, dely = -takeoff.end[0], -takeoff.end[1]
    for surface in (slope, approach, takeoff, landing, landing_trans, flight):
        surface.shift_coordinates(delx, dely)

    # generate some example flight paths
    design_speed = flight.speed[0]
    low_speed = 1/2*design_speed
    if med_speed is None:
        med_speed = 3/4*design_speed

    vel_vec = np.array([np.cos(np.deg2rad(takeoff_angle)),
                        np.sin(np.deg2rad(takeoff_angle))])

    flight_low = skier.fly_to(measured_surface, init_pos=takeoff.end,
                              init_vel=tuple(low_speed*vel_vec))
    flight_med = skier.fly_to(measured_surface, init_pos=takeoff.end,
                              init_vel=tuple(med_speed*vel_vec))
    flight_max = skier.fly_to(measured_surface, init_pos=takeoff.end,
                              init_vel=tuple(design_speed*vel_vec))

    # create the figure
    fig, (prof_ax, efh_ax) = plt.subplots(nrows=2,
                                          ncols=1,
                                          sharex=True,
                                          figsize=(5.25, 4.25),
                                          constrained_layout=True,
                                          gridspec_kw={'height_ratios':
                                                       [1, 0.75]},
                                          )

    efh_ax.grid(axis='x')
    prof_ax.grid()

    increment = 2.0

    dist_meas, efh_meas, speeds = measured_surface.calculate_efh(
        np.deg2rad(takeoff_angle), takeoff.end, skier, increment)

    meas_color = 'black'
    design_color = 'C2'  # mpl default green

    # bar graph for measured efh
    rects = efh_ax.bar(dist_meas, efh_meas,
                       color=meas_color,
                       align='center',
                       width=increment/2,
                       label="Measured Landing Surface")

    # adds takeoff speed just above the measured efh bars
    for rect, si in list(zip(rects[1:], speeds[1:])):
        height = rect.get_height()
        rect_x = rect.get_x() + rect.get_width()/2.0
        efh_ax.text(rect.get_x() + rect.get_width()/2.,
                    height + 0.65,
                    '{:1.1f}'.format(si),
                    fontsize='x-small',
                    ha='center',
                    va='bottom',
                    rotation=90,
                    bbox={'boxstyle': 'square,pad=0.1',
                          'color': 'white',
                          }
                    )
        efh_ax.arrow(rect_x, height, 0.0, 0.65, fc='gray', ec='gray')

    dist, efh, speeds = landing.calculate_efh(np.deg2rad(takeoff_angle),
                                              takeoff.end, skier, increment)

    efh_ax.bar(dist, efh,
               color=design_color,
               align='edge',  # shift bars slightly to not hide measured bars
               width=increment/2,
               label="Designed Landing Surface")

    dist, efh, speeds = landing_trans.calculate_efh(np.deg2rad(takeoff_angle),
                                                    takeoff.end, skier,
                                                    increment)

    efh_ax.bar(dist, efh, color='C2', align='edge', width=increment/2,
               label=None)

    prof_ax.plot(takeoff.x, takeoff.y, linewidth=2, color='C2', label=None)

    prof_ax.plot(flight_low.pos[:, 0], flight_low.pos[:, 1],
                 color='black',
                 linestyle='dashdot',
                 label='Flight @ {:1.0f} m/s'.format(low_speed))
    prof_ax.plot(flight_med.pos[:, 0], flight_med.pos[:, 1],
                 color='black',
                 linestyle='dashed',
                 label='Flight @ {:1.0f} m/s'.format(med_speed))
    prof_ax.plot(flight_max.pos[:, 0], flight_max.pos[:, 1],
                 color='black',
                 linestyle='dotted',
                 label='Flight @ {:1.0f} m/s'.format(design_speed))

    prof_ax.plot(landing.x, landing.y,
                 color='C2', linewidth=2, label=None)
    prof_ax.plot(landing_trans.x, landing_trans.y,
                 color='C2', linewidth=2,
                 label=None,
                 )

    prof_ax.plot(measured_surface.x, measured_surface.y,
                 color='black',
                 label=None,
                 )

    # horizontal lines for knee collapse and floor height
    # storey fall heights are calculated from Vish 2005 using
    # average_window_fall_height.py
    floor_line_color = 'gray'  # 'C1' #  (orange)
    efh_ax.axhline(8.8, color=floor_line_color, linestyle='solid',
                   label='Avg. 3 Story Fall Height')
    efh_ax.axhline(5.1, color=floor_line_color, linestyle='dashed',
                   label='Avg. 2 Story Fall Height')
    efh_ax.axhline(2.6, color=floor_line_color, linestyle='dashdot',
                   label='Avg. 1 Story Fall Height')
    # this value comes from Minetti1998
    efh_ax.axhline(1.5, color=floor_line_color, linestyle='dotted',
                   label='Knee Collapse Height')

    prof_ax.set_ylabel('Vertical Position [m]')
    efh_ax.set_ylabel('Equivalent Fall\nHeight [m]')
    efh_ax.set_xlabel('Horizontal Position [m]')

    prof_ax.set_xlim(*xlim)
    prof_ax.set_ylim(*ylim_top)

    efh_ax.set_xlim(*xlim)
    efh_ax.set_ylim(*ylim_bot)

    prof_ax.set_aspect('equal')

    prof_ax.legend()

    return prof_ax, efh_ax


# Vine v Bear Valley
landing_surface_data = np.loadtxt(os.path.join(PROJECT_ROOT, 'data',
                                               'california-2002-surface.csv'),
                                  delimiter=',',  # comma separated
                                  skiprows=1)  # skip the header row

landing_surface = Surface(landing_surface_data[:, 0],  # x values in meters
                          landing_surface_data[:, 1])  # y values in meters
takeoff_angle = 30.0  # degrees, matches measured from case data
takeoff_point = (0.0, 0.0)  # meters
fall_height = 1.0  # meters
slope_angle = -6.0  # degrees
approach_length = 420.0  # meters

profile_ax, efh_ax = compare_measured_to_designed(landing_surface, fall_height,
                                                  slope_angle, approach_length,
                                                  takeoff_angle,
                                                  (-10, 25), (-10, 5), (0, 6),
                                                  med_speed=10.0)
fig = profile_ax.figure
fig.savefig(os.path.join(PROJECT_ROOT, 'figures', 'vine-v-bear-valley.pdf'))

# Salvini v Snoqualmie
landing_surface_data = np.loadtxt(os.path.join(PROJECT_ROOT, 'data',
                                               'washington-2004-surface.csv'),
                                  delimiter=',',  # comma separated
                                  skiprows=1)  # skip the header row

landing_surface = Surface(landing_surface_data[:, 0],  # x values in meters
                          landing_surface_data[:, 1])  # y values in meters
takeoff_angle = 25.0  # degrees, matches measured from case data
takeoff_point = (0.0, 0.0)  # meters
fall_height = 1.0  # meters
slope_angle = -8.0  # degrees
approach_length = 280.0  # meters

profile_ax, efh_ax = compare_measured_to_designed(landing_surface, fall_height,
                                                  slope_angle, approach_length,
                                                  takeoff_angle,
                                                  (-10, 45), (-15, 5), (0, 16),
                                                  med_speed=15.0)

fig = profile_ax.figure
fig.savefig(os.path.join(PROJECT_ROOT, 'figures', 'salvini-v-snoqualmie.pdf'))
