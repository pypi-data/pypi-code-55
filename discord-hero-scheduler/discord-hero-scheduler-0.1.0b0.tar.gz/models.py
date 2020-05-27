import hero
from hero import async_using_db, Context, models, fields
from hero.utils import async_to_sync

from .fields import JSONField


class Context(models.DiscordModel):
    message = fields.MessageField(null=True, blank=True, on_delete=fields.SET_NULL)
    prefix = fields.CharField(max_length=64, null=True, blank=True)
    command_name = fields.CharField(max_length=256, null=True, blank=True)
    args_and_kwargs = JSONField(default={})

    _discord_cls = Context

    @property
    def args(self):
        if self.is_fetched:
            return self._discord_obj.args
        return self.args_and_kwargs['args']

    @property
    def kwargs(self):
        if self.is_fetched:
            return self._discord_obj.kwargs
        kwargs = self.args_and_kwargs.copy()
        if 'args' in kwargs:
            kwargs.pop('args')
        return kwargs

    @property
    def _state(self):
        if hasattr(self, '_discord_obj'):
            return self._discord_obj._state
        else:
            return self.message._state

    @classmethod
    @async_using_db
    def from_discord_obj(cls, discord_obj):
        message = async_to_sync(models.Message.from_discord_obj(discord_obj.message))
        prefix = discord_obj.prefix
        command_name = discord_obj.command_name
        args_and_kwargs = discord_obj.kwargs or {}
        if discord_obj.args:
            args_and_kwargs['args'] = discord_obj.args
        if not args_and_kwargs:
            args_and_kwargs = None
        return cls(message=message, prefix=prefix, command_name=command_name, args_and_kwargs=args_and_kwargs)

    async def fetch(self):
        if self.message is not None:
            message = await self.message.fetch()
            args_and_kwargs = self.args_and_kwargs.copy()
            self._core: hero.Core
            command = self._core.get_command(self.command_name)
            ctx = hero.Context(message=message, bot=self._core, args=args_and_kwargs.pop('args', []),
                               kwargs=args_and_kwargs, prefix=self.prefix, command=command)
            self._discord_obj = ctx
            return ctx
        else:
            return False


class ScheduledTask(models.Model):
    extension_name = fields.CharField(max_length=64)
    method_name = fields.CharField(max_length=128)
    kwargs = JSONField(null=True, blank=True)
    when = fields.DateTimeField(db_index=True)
    time_tolerance = fields.IntegerField(default=300, null=True)  # seconds | None means infinite time tolerance
    context = fields.ForeignKey(Context, null=True, blank=True, on_delete=fields.SET_NULL)
