import logging
import interp

logger = logging.getLogger()

from handler_room import find_door
from interp import cmd_type
import merc
import game_utils
import state_checks
import handler_game

def do_close(ch, argument):
    argument, arg = game_utils.read_word(argument)
    if not arg:
        ch.send("Close what?\n")
        return

    obj = ch.get_item_here(arg)
    if obj:
        # portal stuff */
        if obj.item_type == merc.ITEM_PORTAL:
            if not state_checks.IS_SET(obj.value[1], merc.EX_ISDOOR) or state_checks.IS_SET(obj.value[1],
                                                                                            merc.EX_NOCLOSE):
                ch.send("You can't do that.\n")
                return
            if state_checks.IS_SET(obj.value[1], merc.EX_CLOSED):
                ch.send("It's already closed.\n")
                return
            state_checks.SET_BIT(obj.value[1], merc.EX_CLOSED)
            handler_game.act("You close $p.", ch, obj, None, merc.TO_CHAR)
            handler_game.act("$n closes $p.", ch, obj, None, merc.TO_ROOM)
            return
        # 'close object' */
        if obj.item_type != merc.ITEM_CONTAINER:
            ch.send("That's not a container.\n")
            return
        if state_checks.IS_SET(obj.value[1], merc.CONT_CLOSED):
            ch.send("It's already closed.\n")
            return
        if not state_checks.IS_SET(obj.value[1], merc.CONT_CLOSEABLE):
            ch.send("You can't do that.\n")
            return
        state_checks.SET_BIT(obj.value[1], merc.CONT_CLOSED)
        handler_game.act("You close $p.", ch, obj, None, merc.TO_CHAR)
        handler_game.act("$n closes $p.", ch, obj, None, merc.TO_ROOM)
        return
    door = find_door(ch, arg)
    if find_door(ch, arg) >= 0:
        # 'close door'
        pexit = merc.rooms[ch.in_room].exit[door]
        if state_checks.IS_SET(pexit.exit_info, merc.EX_CLOSED):
            ch.send("It's already closed.\n")
            return
        state_checks.SET_BIT(pexit.exit_info, merc.EX_CLOSED)
        handler_game.act("$n closes the $d.", ch, None, pexit.keyword, merc.TO_ROOM)
        ch.send("Ok.\n")

        # close the other side
        to_room = pexit.to_room
        pexit_rev = to_room.exit[merc.rev_dir[door]] if pexit.to_room else None
        if to_room and pexit_rev and pexit_rev.to_room == ch.in_room:
            state_checks.SET_BIT(pexit_rev.exit_info, merc.EX_CLOSED)
            for rch in to_room.people:
                handler_game.act("The $d closes.", rch, None, pexit_rev.keyword, merc.TO_CHAR)


interp.register_command(cmd_type('close', do_close, merc.POS_RESTING, 0, merc.LOG_NORMAL, 1))
