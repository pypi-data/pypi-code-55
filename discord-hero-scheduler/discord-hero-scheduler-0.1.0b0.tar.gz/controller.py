import asyncio
import datetime
import inspect

from functools import partial

import discord
from discord.ext.commands import Command

import hero
from hero import async_using_db
from hero.utils import maybe_coroutine

from sortedcontainers import SortedDict

from .models import Context, ScheduledTask


async def no_context_wrapper(func):
    async def wrapped_func(ctx, *args, **kwargs):
        return func(*args, **kwargs)
    return wrapped_func


class SchedulerController(hero.Controller):
    core: hero.Core

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.recently_expired_tasks = []
        self.cached_scheduled_tasks = {}
        self.current_timer = None

    @property
    def next_task_time(self):
        return next(iter(self.cached_scheduled_tasks.keys()))

    @async_using_db
    def generate_command(self, task: ScheduledTask):
        controller = self.core.get_controller(task.extension_name)
        method = getattr(controller, task.method_name)
        signature = inspect.signature(method)
        first_param = next(iter(signature.parameters.values()))
        pass_context = first_param.name == 'ctx' or first_param.annotation is hero.Context

        if not pass_context:
            method = no_context_wrapper(method)

        func = partial(maybe_coroutine, method)
        # wrap in generated command to enable converting of kwargs
        return Command(func, name=f"scheduled_{task.extension_name}_{task.method_name}", parent=self.core)

    @async_using_db
    def generate_context(self, task: ScheduledTask):
        ctx = task.context
        if ctx is None:
            ctx = Context()
        ctx.args = []
        ctx.kwargs = task.kwargs
        return ctx

    async def schedule_next_tasks(self):
        await self.core.wait_until_ready()
        if self.cached_scheduled_tasks:
            now = datetime.datetime.utcnow().timestamp()
            time, tasks = next(iter(self.cached_scheduled_tasks.items()))
            now = datetime.datetime.utcnow().timestamp()
            td = time - now
            timer = self.generate_timer(td, *tasks)
            self.current_timer = timer

    async def execute_task(self, task: ScheduledTask):
        command: Command = await self.generate_command(task)
        ctx = await self.generate_context(task)
        await ctx.fetch()
        await task.async_delete()
        await command.invoke(ctx)

    async def initialize(self):
        for task in self.recently_expired_tasks:
            self.core.loop.create_task(self.execute_task(task))
        self.recently_expired_tasks.clear()

        self.core.loop.create_task(self.schedule_next_tasks())

    async def timer(self, time: float, *tasks: ScheduledTask):
        await asyncio.sleep(time)
        for task in tasks:
            self.core.loop.create_task(self.execute_task(task))
        self.current_timer = None
        self.core.loop.create_task(self.schedule_next_tasks())

    def generate_timer(self, time, *tasks):
        return self.core.loop.create_task(self.timer(time, *tasks))

    async def schedule(self, controller_method, time: datetime.datetime, ctx=None,
                       time_tolerance=None, **kwargs):
        extension_name = controller_method.__self__.extension.name
        controller_method_name = controller_method.__name__

        if not getattr(controller_method, 'schedulable', False):
            raise ValueError(f"Controller method '{controller_method_name}' of "
                             f"extension '{extension_name}' is not schedulable")

        now = datetime.datetime.utcnow()
        if time - now < datetime.timedelta(seconds=29):  # to accomodate for a small delay
            raise ValueError("Scheduled task needs to be at least 30 seconds in the future to avoid conflicts")

        kwargs = {key: str(value) for key, value in kwargs.items()}

        if ctx is not None:
            ctx = await Context.from_discord_obj(ctx)

        scheduled_task = ScheduledTask(extension_name=extension_name,
                                       method_name=controller_method_name,
                                       kwargs=kwargs,
                                       when=time,
                                       time_tolerance=time_tolerance or ScheduledTask.time_tolerance.default,
                                       context=ctx)
        await scheduled_task.async_save()

        already_stored_tasks = self.cached_scheduled_tasks.get(time.timestamp())
        if already_stored_tasks:
            already_stored_tasks.append(scheduled_task)
        else:
            self.cached_scheduled_tasks[time.timestamp()] = [scheduled_task]

        if self.next_task_time > time.timestamp():
            self.current_timer.cancel()
            await self.schedule_next_tasks()

    @async_using_db
    def load_scheduled_tasks(self):
        """Returns an automatically sorted dict of timestamp: List[ScheduledTask]"""
        all_scheduled_tasks = list(ScheduledTask.objects.order_by('when').all())
        now = datetime.datetime.utcnow()

        for task in all_scheduled_tasks:
            if task.time_tolerance is None or now - task.when <= datetime.timedelta(seconds=task.time_tolerance):
                self.recently_expired_tasks.append(task)
            else:
                task.delete()

        unsorted_scheduled_tasks = {task.when.timestamp(): task for task in all_scheduled_tasks}
        scheduled_tasks = SortedDict()
        scheduled_tasks.update(unsorted_scheduled_tasks)
        self.cached_scheduled_tasks = scheduled_tasks
        return scheduled_tasks

    async def shutdown(self):
        # await self.core.change_presence(status=discord.Status.invisible)  # doesn't seem to do anything
        self.core._ready.clear()
        if self.current_timer is not None:
            self.current_timer.cancel()
        if hero.TEST:
            await asyncio.sleep(30)
        else:
            await asyncio.sleep(150)
        await self.core.logout()
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
