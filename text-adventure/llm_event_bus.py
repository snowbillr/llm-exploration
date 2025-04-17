import queue

class LLMEventBus:
    _queue = queue.SimpleQueue()

    @classmethod
    def has_events(cls):
        return not cls._queue.empty()

    @classmethod
    def put_event(cls, event):
        cls._queue.put(event)

    @classmethod
    def get_event(cls):
        return cls._queue.get()
