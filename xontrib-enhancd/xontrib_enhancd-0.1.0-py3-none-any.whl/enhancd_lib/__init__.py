import builtins
import xonsh

x_env: xonsh.environ.Env = builtins.__xonsh__.env
x_execer: xonsh.execer.Execer = builtins.__xonsh__.execer
x_aliases: xonsh.aliases.Aliases = builtins.aliases
