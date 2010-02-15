# -*- coding: UTF-8 -*-
"""
The async threaded indexing class of thawab
Copyright © 2010, Muayyad Alsadi <alsadi@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"

"""
from Queue import Queue
from threading import Thread
from time import sleep

class AsyncIndex():
  def __init__(self, searchEngine, queueSize=0, workers=1):
    """
    if number of workers>1 then queued jobs need not be executed in order
    """
    self.searchEngine=searchEngine
    self.worders_n=workers
    self._q = Queue(queueSize)
    self.start()
    # we enqueue jobs like this
    #for item in source(): self._q.put(item)

  def queue(self, method, *args, **kw):
    """
    examples: queue("indexNew"); queue("indexKitab","kitab_name");
    """
    self._q.put((method, args, kw))

  def start(self):
    self.keepworking=True
    self.end_when_done=False
    self.started=False
    # here we create our thread pool of workers
    for i in range(self.worders_n):
      t = Thread(target=self._worker)
      t.setDaemon(True)
      t.start()
    # sleep to make sure all threads are waiting for jobs (inside loop)
    while not self.started: sleep(0.25)

  def jobs(self):
    """
    return number of queued jobs.
    """
    return self._q.qsize()

  def join(self):
    """
    block till queued jobs are done.
    """
    return self._q.join()

  def cancelQueued(self):
    self.keepworking=False
    self._q.join()
    self.started=False

  def endWhenDone(self):
    self.end_when_done=True
    self._q.join()
    self.started=False

  def _worker(self):
    while self.keepworking:
      self.started=True
      # get a job from queue or block sleeping till one is available
      iterm = self._q.get(not self.end_when_done)
      if item:
        method, args, kw=item
        f=getattr(self.searchEngine, method)
        f(*args,**kw)
        self._q.task_done()
      elif self._q.empty() and self.end_when_done: self.keepworking=False
