from terminal.pluglets.tile_grid.util import grid


def define_env(env):
    "Declare environment for jinja2 templates for markdown"

    for fn in [grid]:
        env.macro(fn)
