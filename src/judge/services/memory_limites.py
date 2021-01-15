# Linux only
import resource
import logging


logger = logging.getLogger(__name__)

class MemoryLimiter:
    '''
    class for setting limits for memory usage
    '''

    MAX_MEMORY_LIMIT = 64 * 1.048576 * 1024 * 1024 #64 MiB


    def __init__(self, memory_limit=70368744.177664):
        '''
        constructor to set problem memory limit
        '''

        self.MAX_MEMORY_LIMIT = memory_limit


    @classmethod
    def limit_virtual_memory(cls):
        logger.info(f'{type(self.MAX_VIRTUAL_MEMORY)}: {self.MAX_VIRTUAL_MEMORY}')
        resource.setrlimit(resource.RLIMIT_AS, (self.MAX_VIRTUAL_MEMORY, resource.RLIM_INFINITY))
