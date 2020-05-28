# -*- coding: utf-8 -*-
#
# Copyright 2016 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib
import os
import sys
import warnings

import click

from rqsdk.const import TAG_MAP, VERSION_MAP
from rqsdk.script_update import pip_install, update_bash_file


@click.group()
@click.help_option("-h", "--help")
def cli():
    """
    输入 rqsdk <COMMAND> --help 查看命令详情
    例如：rqsdk install --help
    """
    pass


@cli.command()
@click.argument('rqdatac_uri', default="", nargs=1)
def license(rqdatac_uri):
    """配置 license 到环境变量"""
    warnings.filterwarnings("ignore", message="rqdatac is already inited. Settings will be changed.")

    def _print_rqdata_info(uri):
        import rqdatac
        from rqdatac.share.errors import AuthenticationFailed
        try:
            rqdatac.init(uri=uri)
            _info = rqdatac.user.get_quota()
            click.echo("=" * 20)
            click.echo("license={uri}".format(uri=os.environ.get('RQDATAC2_CONF')))
            if _info['bytes_limit'] == 0:
                click.echo("该 license 无流量限制".format(_info['bytes_limit'] / 2 ** 10))
            else:
                click.echo("流量限制={}KB".format(_info['bytes_limit'] / 2 ** 10))
                click.echo("剩余流量={}KB".format((_info['bytes_limit'] - _info['bytes_used']) / 2 ** 10))
            click.echo("该 license 剩余有效天数为={}".format(_info['remaining_days']))
            click.echo("=" * 20)
        except AuthenticationFailed as r:
            click.echo("=" * 20)
            click.echo("登录失败，该 license 或用户无法用于初始化 rqdatac\n{}".format(uri))
            click.echo("请联系商务或技术支持")
            click.echo("=" * 20)
            return False
        return True

    if rqdatac_uri == "info":
        uri = os.environ.get('RQDATAC2_CONF')
        if uri is None:
            click.echo("当前环境没有配置license")
        else:
            _print_rqdata_info(uri)
        return

    while True:
        if not rqdatac_uri:
            uri = os.environ.get('RQDATAC2_CONF')
            if uri is None:
                click.echo("当前环境没有配置license")
                rqdatac_uri = None
            else:
                _print_rqdata_info(uri)
        if rqdatac_uri:
            from rqsdk.utils import init_rqdatac_env
            if ":" not in rqdatac_uri:
                rqdatac_uri = "license:{}".format(rqdatac_uri)
            init_rqdatac_env(rqdatac_uri)
            rqdatac_uri = os.environ['RQDATAC2_CONF']

            if not _print_rqdata_info(rqdatac_uri):
                rqdatac_uri = ""
            else:
                if sys.platform.startswith("win"):
                    os.popen("setx RQDATAC2_CONF {uri} ".format(uri=rqdatac_uri))
                else:
                    update_bash_file(rqdatac_uri)
                click.echo("当前 license 已设置为 {uri}".format(uri=rqdatac_uri))
                click.echo("请重启当前的 terminal ".format(uri=rqdatac_uri))
                return
        click.echo('如需修改请按照【用户名:密码】的格式输入您的用户名密码或直接键入license key。')
        click.echo('不更改则按 Enter 键退出')
        rqdatac_uri = input()
        click.echo()
        if not rqdatac_uri:
            return


@cli.command()
@click.argument('product', default="", nargs=1)
@click.option('-i', '--index-url', default="https://pypi.douban.com/simple/", help="指定默认源")
def update(product, index_url):
    """
    更新 rqsdk 及使用 rqsdk 安装的产品。

    \b
    输入 rqsdk update [<PRODUCT>] 安装对应产品，PRODUCT为空时默认更新已安装产品。例如 rqsdk update rqoptimizer。
    PRODUCT可选: rqdatac | rqfactor | rqoptimizer | rqalpha_plus

    """
    if product != "":
        if product not in VERSION_MAP.keys():
            click.echo("PRODUCT可选为:{}\n,当前为{}。".format(list(VERSION_MAP.keys()), product))
            return
        key = [product]
    else:
        key = ["rqdatac"]
        try:
            import rqalpha_plus
            key.append("rqalpha_plus")
        except ImportError:
            try:
                import rqfactor
                key.append("rqfactor")
            except ImportError:
                pass
            try:
                import rqoptimizer2
                key.append('rqoptimizer')
            except ImportError:
                pass

    full_name = "rqsdk[{}]".format(",".join(key))
    return pip_install(full_name, index_url)


@cli.command()
@click.argument('product', default="", nargs=1)
@click.option('-i', '--index-url', default="https://pypi.douban.com/simple/", help="指定默认源")
def install(product, index_url):
    """
    安装产品。

    \b
    输入 rqsdk install <PRODUCT> 安装对应产品。例如 rqsdk install rqoptimizer。
    PRODUCT 可选: rqdatac | rqfactor | rqoptimizer | rqalpha_plus
    * rqdatac - 金融数据API（默认已安装）
    * rqalpha_plus - 多资产回测引擎
    * rqoptimizer - 股票优化器
    * rqfactor - 因子投研和检验
    """

    if product == 'rqsdk':
        full_name = product
    elif product in VERSION_MAP.keys():
        from rqsdk import __version__
        full_name = "rqsdk[{}]=={}".format(product, __version__)
    elif product != "":
        click.echo("请输入正确的产品名称:{}。当前输入为{}".format(list(VERSION_MAP.keys()), product))
    else:
        click.echo("请输入产品名称:{}".format(list(VERSION_MAP.keys())))
        return
    return pip_install(full_name, index_url)


@cli.command()
def shell():
    """打开 ipython 并执行 rqdatac init"""
    import rqdatac
    rqdatac.init()
    try:
        from IPython import embed
    except ImportError:
        click.echo("请安装ipython:pip install ipython")
    else:
        embed()


@cli.command()
def version():
    """获取版本信息"""
    from rqsdk import __version__
    click.echo("rqsdk=={}".format(__version__))
    for item in VERSION_MAP['rqalpha_plus']:
        try:
            package_name = item.split("==")[0]
            _package = importlib.import_module(package_name)
            click.echo("{}=={}".format(package_name, _package.__version__))
        except:
            pass


@cli.command()
@click.option(
    '-d', '--data-bundle-path', default=os.path.expanduser('~/.rqalpha-plus'), type=click.Path(file_okay=False),
    help="bundle 目录，默认为 ~/.rqalpha-plus"
)
@click.option(
    "--minbar", multiple=True, type=click.STRING,
    help="更新分钟线数据，可选的参数值有 [{}] 或 underlying_symbol 或 order_book_id".format(", ".join(TAG_MAP))
)
@click.option(
    "--tick", multiple=True, type=click.STRING,
    help="更新tick数据，可选的参数值有 [{}] 或 underlying_symbol 或 order_book_id".format(", ".join(TAG_MAP))
)
@click.option("--daybar/--no-daybar", default=True, help="是否更新日线，默认更新日线")
@click.option("--with-derivatives", is_flag=True, default=False, help="更新分钟线和 tick 时同时更新选择的合约的衍生品数据")
@click.option('-c', '--concurrency', type=click.INT, default=3, help="并行的线程数量，需要低于 rqdatac 的最大可用连接数")
def update_data(data_bundle_path, minbar, tick, daybar, with_derivatives, concurrency):
    """更新运行回测所需的历史数据"""
    try:
        import rqdatac
        rqdatac.init()
    except ValueError as e:
        click.echo('rqdatac init failed with error: {}'.format(e))
        click.echo('请先使用rqsdk license 初始化')
        return 1

    try:
        from rqalpha_plus.bundle import update_bundle_from_rqdatac
        return update_bundle_from_rqdatac(concurrency, data_bundle_path, daybar, minbar, tick, with_derivatives)
    except ImportError:
        click.echo("""请先使用'rqsdk install rqalpha_plus'安装rqalpha_plus""")


@cli.command()
@click.option(
    '-d', '--data-bundle-path', default=os.path.expanduser('~/.rqalpha-plus'), type=click.Path(file_okay=False),
    help="bundle 目录，默认为 ~/.rqalpha-plus"
)
@click.option("--sample", is_flag=True, help="下载数据样例")
def download_data(data_bundle_path, sample=True):
    """下载样例回测数据"""
    try:
        from rqalpha_plus.bundle import download_simple_bundle
        return download_simple_bundle(data_bundle_path, sample=sample)
    except ImportError:
        click.echo("""请先使用'rqsdk install rqalpha_plus'安装rqalpha_plus""")
