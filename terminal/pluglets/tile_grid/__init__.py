from terminal.pluglets.tile_grid.util import grid


def define_env(env):
    "Declare environment for jinja2 templates for markdown"
    chatter = env.start_chatting("terminal.pluglets.tile_grid")
    for fn in [grid]:
        env.macro(fn)
        chatter("added %s macro" % fn.__name__)
