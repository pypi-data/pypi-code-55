import asyncio
import datetime

import hero
from hero import checks

from .controller import SchedulerController


class Scheduler(hero.Cog):
    ctl: SchedulerController
    core: hero.Core

    @hero.listener()
    async def on_ready(self):
        if self.ctl.current_timer is None:
            await self.ctl.load_scheduled_tasks()
            self.core.loop.create_task(self.ctl.initialize())

    @hero.command()
    @checks.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        self.core.loop.create_task(self.ctl.shutdown())
