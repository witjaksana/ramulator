#!/usr/bin/python3
import os
import subprocess
import queue
import _thread

def wait(p, q, desc):
  try: p.wait()
  finally: q.put((desc, p.pid))

def main():
  pids = queue.Queue()
  try: os.mkdir('results/')
  except: pass
  cnt = 0
  for fn in os.listdir('cputraces'):
    if fn[0] == '.': continue
    of = open('results/'+fn, 'w')
    fn = 'cputraces/'+fn
    p = subprocess.Popen(["./ramulator-cputrace", fn], stdout=of)
    _thread.start_new_thread(wait, (p, pids, fn))
    cnt += 1
    print("spawned %s: %d (%d)" % (fn, p.pid, cnt))

  while cnt:
    desc, p = pids.get()
    print(desc, p, "finished")
    cnt -= 1


if __name__ == '__main__':
  main()
