def define_env(env):

    @env.macro
    def render_tiles(tiles):
        if tiles is not None:
            return "TODO: " + str(len(tiles))
        return "invalid_tiles"
