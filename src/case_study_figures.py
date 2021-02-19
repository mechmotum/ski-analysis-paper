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
                                 takeoff_angle, skier, xlim):

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
    med_speed = 3/4*design_speed

    vel_vec = np.array([np.cos(np.deg2rad(takeoff_angle)),
                        np.sin(np.deg2rad(takeoff_angle))])

    flight_low = skier.fly_to(measured_surface, init_pos=takeoff.end,
                              init_vel=tuple(low_speed*vel_vec))
    flight_med = skier.fly_to(measured_surface, init_pos=takeoff.end,
                              init_vel=tuple(med_speed*vel_vec))

    # create the figure
    fig, (prof_ax, efh_ax) = plt.subplots(2, 1,
                                          sharex=True,
                                          #constrained_layout=True,
                                          #subplot_kw={'adjustable': 'box'},
                                          )

    # horizontal lines for knee collapse and floor height
    # storey fall heights are calculated from Vish 2005 using
    # average_window_fall_height.py
    efh_ax.axhline(8.8, color='C1', linestyle='solid',
                   label='Avg. 3 Story Fall Height')
    efh_ax.axhline(5.1, color='C1', linestyle='dashed',
                   label='Avg. 2 Story Fall Height')
    efh_ax.axhline(2.6, color='C1', linestyle='dashdot',
                   label='Avg. 1 Story Fall Height')
    # this value comes from Minetti1998
    efh_ax.axhline(1.5, color='C1', linestyle='dotted',
                   label='Knee Collapse Height')

    increment = 1.0

    dist, efh, speeds = measured_surface.calculate_efh(
        np.deg2rad(takeoff_angle), takeoff.end, skier, increment)

    rects = efh_ax.bar(dist, efh, color='black', align='center',
                       width=increment/2, label="Measured Landing Surface")
    for rect, si in list(zip(rects, speeds))[::2]:
        height = rect.get_height()
        efh_ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '{:1.1f}'.format(si), fontsize='xx-small', ha='center',
                    va='bottom', rotation=90)

    dist, efh, speeds = landing.calculate_efh(np.deg2rad(takeoff_angle),
                                              takeoff.end, skier, increment)

    efh_ax.bar(dist, efh, color='C2', align='edge', width=increment/2,
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
    prof_ax.plot(flight.pos[:, 0], flight.pos[:, 1],
                 color='black',
                 linestyle='dotted',
                 label='Flight @ {:1.0f} m/s'.format(design_speed))

    prof_ax.plot(landing.x, landing.y,
                 color='C2', linewidth=2, label=None)
    prof_ax.plot(landing_trans.x, landing_trans.y,
                  color='C2', linewidth=2,
                  label='Designed Landing Surface')

    prof_ax.plot(measured_surface.x, measured_surface.y,
                                    color='black',
                                    label="Measured Landing Surface")

    #prof_ax.set_title('Design Speed: {:1.0f} m/s'.format(design_speed))

    prof_ax.set_ylabel('Vertical Position [m]')
    efh_ax.set_ylabel('Equivalent Fall Height [m]')
    efh_ax.set_xlabel('Horizontal Position [m]')

    efh_ax.grid()
    prof_ax.grid()
    #efh_ax.legend(loc='upper left')
    #prof_ax.legend(loc='lower left')

    prof_ax.set_xlim(xlim)
    #efh_ax.set_xlim(xlim)

    prof_ax.set_aspect('equal') #, share=True)
    #efh_ax.set_aspect('equal')



    return prof_ax, efh_ax


# Vine v Bear Valley
landing_surface_data = np.loadtxt(os.path.join(PROJECT_ROOT, 'data',
                                               'california-2002-surface.csv'),
                                  delimiter=',',  # comma separated
                                  skiprows=1)  # skip the header row

landing_surface = Surface(landing_surface_data[:, 0],  # x values in meters
                          landing_surface_data[:, 1])  # y values in meters
takeoff_angle = 30.0  # degrees
takeoff_point = (0.0, 0.0)  # meters
fall_height = 1.0  # meters
slope_angle = -8.0  # degrees
approach_length = 180.0  # meters

skier = Skier()

profile_ax, efh_ax = compare_measured_to_designed(landing_surface, fall_height,
                                                  slope_angle, approach_length,
                                                  takeoff_angle, skier,
                                                  (-10, 25))
ylim = profile_ax.get_ylim()
profile_ax.set_ylim((-20.0, ylim[1]))

fig = profile_ax.figure

fig.set_figwidth(5.25)

fig.savefig(os.path.join(PROJECT_ROOT, 'figures', 'vine-v-bear-valley.pdf'))

# Salvini v Snoqualmie
landing_surface_data = np.loadtxt(os.path.join(PROJECT_ROOT, 'data',
                                               'washington-2004-surface.csv'),
                                  delimiter=',',  # comma separated
                                  skiprows=1)  # skip the header row

landing_surface = Surface(landing_surface_data[:, 0],  # x values in meters
                          landing_surface_data[:, 1])  # y values in meters
takeoff_angle = 25.0  # degrees
takeoff_point = (0.0, 0.0)  # meters
fall_height = 1.0  # meters
slope_angle = -10.0  # degrees
approach_length = 220.0  # meters

skier = Skier()

profile_ax, efh_ax = compare_measured_to_designed(landing_surface, fall_height,
                                                  slope_angle, approach_length,
                                                  takeoff_angle, skier,
                                                  (-10, 45))

ylim = profile_ax.get_ylim()
profile_ax.set_ylim((-30.0, ylim[1]))

fig = profile_ax.figure

fig.set_figwidth(5.25)

fig.savefig(os.path.join(PROJECT_ROOT, 'figures', 'salvini-v-snoqualmie.pdf'))
