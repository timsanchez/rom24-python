import logging

logger = logging.getLogger()

import interp
import merc

def do_murde(ch, argument):
    ch.send("If you want to MURDER, spell it out.\n")
    return


interp.register_command(interp.cmd_type('murde', do_murde, merc.POS_FIGHTING, 0, merc.LOG_NORMAL, 0))
