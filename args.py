import argparse

from ugly.devices import GetDevices

def Args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', type=str, default='unicornhathd',
                        help="""
                        Device type to control or emulate. One of: {}.
                        """.format(', '.join(GetDevices())))
    parser.add_argument('-D', '--driver', type=str, default='auto',
                        help="""
                        Driver for device. One of: legacy, terminal, ffmpeg.
                        or auto to use any available driver, or autoemu for
                        any available virtual driver.
                        """)
    parser.add_argument('-M', '--monitor', type=str, default=None,
                        help="""
                        Enable debug monitoring of the main device through
                        this driver. One of: terminal, ffmpeg, or auto for
                        any available virtual driver.
                        """)
    parser.add_argument('-F', '--fixed-timestep', action='store_true',
                        help="""
                        Use a fixed frame time step of 30 fps. Use when recording
                        video.
                        """)
    parser.add_argument('-r', '--rotation', type=int, default=0,
                        help="""
                        Rotate the logical display.
                        """)
    parser.add_argument('-o', '--orientation', type=int, default=0,
                        help="""
                        Orientation for virtual display, if using one.
                        """)
    parser.add_argument('--flip-h', action='store_true',
                        help="""
                        Horizontally flip the logical display.
                        """)
    parser.add_argument('--flip-v', action='store_true',
                        help="""
                        Vertically flip the logical display.
                        """)

    args = parser.parse_args()

    return args