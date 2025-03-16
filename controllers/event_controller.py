# core/event_system.py
from threading import Lock

class EventController:
    def __init__(self):
        self._lock = Lock()  # 新增锁对象
        self._listeners = {}
    
    def subscribe(self, event_type, listener):
        with self._lock:  # 加锁保护
            if event_type not in self._listeners:
                self._listeners[event_type] = []
            self._listeners[event_type].append(listener)

    def publish(self, event_type, *args, **kwargs):
        with self._lock:  # 加锁保护
            listeners = self._listeners.get(event_type, [])[:]
            
        for listener in listeners:  # 在锁外执行回调
            listener(*args, **kwargs)
