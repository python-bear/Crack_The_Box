from bin import intro
from bin import game


intro.main(show_cc=False, time_scale=1.4)

application = game.Game()
application.run()
