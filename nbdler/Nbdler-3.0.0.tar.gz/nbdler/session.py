
import asyncio
import xmlrpc
from .handler import Handler, SpeedAdjuster, Handlers, FileTempData
import threading
from concurrent.futures.thread import ThreadPoolExecutor



class SessionConfigure:
    def __init__(self, subprocess, max_speed, buffer_size, interval, **kwargs):
        self.max_speed = max_speed
        self.buffer_size = buffer_size
        self.subprocess = subprocess
        self.interval = interval
        self.kwargs = kwargs


class DownloadSession:
    def __init__(self, **kwargs):
        self._server = None
        self.config = SessionConfigure(**kwargs)

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.speed_adjuster = GlobalSpeedAdjuster(self)
        self.speed_adjuster.add_parent(self)

    def start(self):
        pass


class BaseDownloadSession:
    pass




class RPCDownloadSession:
    def __init__(self):
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class GlobalHandler(Handlers):
    pass


class ChildFileTempData(FileTempData):
    def __init__(self, global_handler):
        super().__init__()
        self.global_handler = global_handler

    def store_threadsafe(self, data):
        super().store_threadsafe(data)
        # 全局计数
        self._global_counter += len(data)

    async def store(self, data):
        await super().store(data)


class GlobalFileTempData(GlobalHandler):
    def __init__(self, session):
        super().__init__()
        self._session = session

    async def saving_state(self):
        """ 保存当前下载状态。

        以cfg的文件形式保存当前下载配置以备文件下载状态的恢复。
        """
        dumpy = self.parent.dumps()
        async with h.aio.open(f'{self.parent.file.pathname}.cfg', mode='w') as cfg_file:
            await cfg_file.write(json.dumps(dumpy))

    async def _release(self):
        buffers = self._buffers
        counter = self._counter
        self._counter = 0
        self._buffers = defaultdict(list)
        return await self._unreleased.put((counter, buffers))

    def store_threadsafe(self, data):
        """ 线程安全保存临时下载数据。"""
        with self._lock:
            block = _lookup_block()
            self._buffers[block.progress].append(data)
            self._counter += len(data)
            if self.parent.config.buffer_size <= self._counter:
                await_coroutine_threadsafe(self._release())

    async def store(self, data):
        """ 缓冲传输数据。

        当缓冲的数据超过了buffer_size，将对缓冲进行释放写入文件。

        Args:
            data: 要被缓冲的传输数据
        """
        block = _lookup_block()
        self._buffers[block.progress].append(data)
        self._counter += len(data)
        if self.parent.config.buffer_size <= self._counter:
            await self._release()

    async def prepare(self):
        self._unreleased = asyncio.Queue()

    async def run(self):
        unreleased = self._unreleased
        file = self.parent.file
        filepath = f'{file.pathname}{self.parent.config.downloading_ext}'

        # 通过下载块是否有walk_length的情况来判断是否需要重写文件。
        if not self.parent.block_grp.done_length():
            async with h.aio.open(f'{file.pathname}{self.parent.config.downloading_ext}', mode='wb') as fd:
                if file.size is not None:
                    await fd.seek(file.size - 1)
                    await fd.write(b'\x00')

        async with h.aio.open(filepath, mode='rb+') as fd:
            while True:
                result = await unreleased.get()
                if result is None:
                    break
                counter, buffers = result
                for pg, lines in buffers.items():
                    await fd.seek(pg.begin + pg.done_length)
                    await fd.writelines(lines)
                    pg.done(sum([len(line) for line in lines]))

                # 删除引用，尽快回收垃圾
                lines = None
                result = None
                buffers = None
                await self.saving_state()

    async def pause(self):
        await h.client_worker.join()
        await self._release()
        await self._unreleased.put(None)

    async def close(self):
        pass


class GlobalSpeedAdjuster(GlobalHandler):
    """ 全局速度调节器。"""
    def __init__(self, session):
        super().__init__()
        self._stopped = True
        self._session = session

    def create_handler(self):
        return ChildSpeedAdjuster(self)

    async def run(self):
        assert self._stopped
        self._stopped = False

        async_sleep = asyncio.sleep
        config = self.parent.config
        max_speed = config.max_speed
        fraction = 0
        if max_speed is not None:
            self._opened = True
        while True:
            if self._stopped:
                break
            await async_sleep(config.interval)

            # 当最大下载速度配置有变化后则响应相应的速度限速开关
            if config.max_speed != max_speed:
                # 最大速度限制参数被修改
                max_speed = config.max_speed
                if max_speed is None:
                    self._opened = False
                    await self._release_all()
                else:
                    self._opened = True
                    fraction = 0

            # 如果限制的下载速率就处理信号量
            if max_speed is not None:
                value = config.max_speed * config.interval / 8196

                # 由于下载客户端以单次读数据粒度进行限速，所以为了更细化的限速
                # 对计算出来的信号量粒度小数保留下来留给下次累加。
                fraction += value % 1
                value = int(value)
                if fraction >= 1:
                    value += 1
                    fraction -= 1
                with self._thread_cond:
                    async with self._async_cond:
                        self._sema_value = value
                        self._thread_cond.notify_all()
                        self._async_cond.notify_all()


class ChildSpeedAdjuster(Handler):
    """ 全局速度调节器控制的子调节器。"""
    name = SpeedAdjuster.name

    def __init__(self, global_adjuster, ):
        self._stopped = True
        self._global_adjuster = global_adjuster
        # 全局调节器方法下放
        self.acquire_threadsafe = global_adjuster.acquire_threadsafe
        self.acquire = global_adjuster.acquire

    async def prepare(self):
        pass

    async def run(self):
        assert self._stopped
        self._stopped = False

        async_sleep = asyncio.sleep
        block_grp = self.parent.block_grp
        config = self.parent.config
        while True:
            if self._stopped:
                break
            await async_sleep(config.interval)
            # 刷新总的下载块实时传输速率
            block_grp.usage_info.refresh()

    async def close(self):
        pass

    async def pause(self):
        self._stopped = True

    def __repr__(self):
        return f'<ChildSpeedAdjuster >'
