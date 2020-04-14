import asyncio
from contextlib import suppress


class NormalScheduler:
    def __init__(self, func):
        self._func = func
        self._task = None

    async def start(self):
        # Start task to call func once in event loop
        self._task = asyncio.create_task(self._run())
        return self._task

    async def _run(self):
        self._func()


class PeriodicScheduler:
    def __init__(self, func, period, timeout=None):
        self._func = func
        self._period = period
        self._is_started = False
        self._task = None
        self._timeout = timeout

    async def start(self):
        if not self._is_started:
            self._is_started = True
            # Start task to call func periodically:
            self._task = asyncio.create_task(self._run())
            await self._task
            return self._task
            #
            # if self._timeout:
            #     await asyncio.sleep(self._timeout)
            # else:
            #     await self._task

    async def stop(self):
        if self._is_started:
            self._is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            self._func()
            await asyncio.sleep(self._period)
