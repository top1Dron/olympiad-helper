# Linux only
import resource
import logging
import psutil
import subprocess


logger = logging.getLogger(__name__)

class MemoryLimiter:
    '''
    class for setting limits for memory usage
    '''

    MAX_MEMORY_LIMIT = 64 * 1.048576 * 1024 * 1024 #64 MiB


    def __init__(self, memory_limit=70368744.177664):
        '''
        object initializator to set problem memory limit
        '''

        self.MAX_MEMORY_LIMIT = memory_limit


    def limit_virtual_memory(self):
        logger.info(f'{type(self.MAX_VIRTUAL_MEMORY)}: {self.MAX_VIRTUAL_MEMORY}')
        resource.setrlimit(resource.RLIMIT_AS, (self.MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))

 
class ProcessTimer:
  def __init__(self,command):
    self.command = command
    self.execution_state = False
 
  def execute(self):
    self.max_vms_memory = 0
    self.max_rss_memory = 0
 
    self.t1 = None
    self.t0 = time.time()
    self.p = subprocess.Popen(self.command,shell=False)
    self.execution_state = True
 
  def poll(self):
    if not self.check_execution_state():
      return False
 
    self.t1 = time.time()
 
    try:
      pp = psutil.Process(self.p.pid)
 
      #obtain a list of the subprocess and all its descendants
      descendants = list(pp.get_children(recursive=True))
      descendants = descendants + [pp]
 
      rss_memory = 0
      vms_memory = 0
 
      #calculate and sum up the memory of the subprocess and all its descendants 
      for descendant in descendants:
        try:
          mem_info = descendant.get_memory_info()
 
          rss_memory += mem_info[0]
          vms_memory += mem_info[1]
        except psutil.error.NoSuchProcess:
          #sometimes a subprocess descendant will have terminated between the time
          # we obtain a list of descendants, and the time we actually poll this
          # descendant's memory usage.
          pass
      self.max_vms_memory = max(self.max_vms_memory,vms_memory)
      self.max_rss_memory = max(self.max_rss_memory,rss_memory)
 
    except psutil.error.NoSuchProcess:
      return self.check_execution_state()
 
 
    return self.check_execution_state()
 
 
  def is_running(self):
    return psutil.pid_exists(self.p.pid) and self.p.poll() == None
  def check_execution_state(self):
    if not self.execution_state:
      return False
    if self.is_running():
      return True
    self.executation_state = False
    self.t1 = time.time()
    return False
 
  def close(self,kill=False):
 
    try:
      pp = psutil.Process(self.p.pid)
      if kill:
        pp.kill()
      else:
        pp.terminate()
    except psutil.error.NoSuchProcess:
      pass
