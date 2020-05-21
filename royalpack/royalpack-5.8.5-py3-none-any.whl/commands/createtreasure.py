from typing import *
import royalnet
import royalnet.commands as rc
import royalnet.utils as ru
from ..tables import Treasure


class CreatetreasureCommand(rc.Command):
    name: str = "createtreasure"

    description: str = "Crea un nuovo tesoro di Fiorygi."

    syntax: str = "{codice} {valore}"

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        author = await data.get_author(error_if_none=True)
        if "banker" not in author.roles:
            raise rc.UserError("Non hai permessi sufficienti per eseguire questo comando.")

        code = args[0]
        try:
            value = int(args[1])
        except ValueError:
            raise rc.InvalidInputError("Il valore deve essere maggiore o uguale a 0.")
        if value < 0:
            raise rc.InvalidInputError("Il valore deve essere maggiore o uguale a 0.")

        TreasureT = self.alchemy.get(Treasure)

        treasure = await ru.asyncify(data.session.query(TreasureT).get, code)
        if treasure is not None:
            raise rc.UserError("Esiste già un Treasure con quel codice.")

        treasure = TreasureT(
            code=code,
            value=value,
            redeemed_by=None
        )
        data.session.add(treasure)
        await data.session_commit()

        await data.delete_invoking()
        await data.reply("✅ Tesoro creato!")
