import linecache
import logging
import os
import tracemalloc


logger = logging.getLogger(__name__)
 
def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)
 
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        logger.info("#%s: %s:%s: %.1f KiB"
            % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            pass

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        logger.info("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    logger.info("Total allocated size: %.1f KiB" % (total / 1024))
    return total / 1024