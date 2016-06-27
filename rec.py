import collections
#!/usr/bin/env python


# recursive version
def fr(args):
  if not args:
    return [""]
  r = []
  for i in args[0]:
    for tmp in fr(args[1:]):
      r.append(i + tmp)
  return r

# generator version
def fg(args):
  if not args:
    yield ""
    return
  for i in args[0]:
    for tmp in fg(args[1:]):
      yield i + tmp
  return

# non-recursive version
def f0(args):
  counter = [ 0 for i in args ]
  r = []
  while 1:
    r.append("".join([ arg1[i] for arg1,i in zip(args, counter) ]))
    carry = 1
    x = list(range(len(args)))
    x.reverse()  # x == [len(args)-1, len(args)-2, ..., 1, 0]
    for i in x:
      counter[i] += 1
      if counter[i] < len(args[i]):
        carry = 0
        break # leave "for"
      counter[i] = 0
    else:
      break # leave "while"
  return r

# iterator version
class fi:
  def __init__(self, args):
    self.args = args
    self.counter = [ 0 for i in args ]
    self.carry = 0
    return
  
  def __iter__(self):
    return self
  
  def __next__(self):
    if self.carry:
      raise StopIteration
    r = "".join([ arg1[i] for arg1,i in zip(self.args, self.counter) ])
    self.carry = 1
    x = list(range(len(self.args)))
    x.reverse()  # x == [len(args)-1, len(args)-2, ..., 1, 0]
    for i in x:
      self.counter[i] += 1
      if self.counter[i] < len(self.args[i]):
        self.carry = 0
        break
      self.counter[i] = 0
    return r

# lambda-encapsulation version
def fl(args, i=0, tmp="", parent_sibling=None):
  if not args:
    # at a leaf
    return (tmp, parent_sibling)
  if i < len(args[0]):
    # prepare my sibling
    sibling = fl(args, i+1, tmp, parent_sibling)
    return lambda: fl(args[1:], 0, tmp+args[0][i], sibling)
  else:
    # go up and visit the parent's sibling
    return parent_sibling

# traverse function for lambda version
def traverse(n):
  while n:
    if isinstance(n, collections.Callable):
      # node
      n = n()
    else:
      # leaf
      (result, n) = n
      print(result, end=' ')
  print()

# display
def display(x):
  for i in x:
    print(i, end=' ')
  print()
  return

# map for a generator
def gmap(f, x):
  for i in x:
    yield f(i)
  return


f = fr
#f = f0
#f = fi
f = fg
print(f)
display(f([]))
display(f(['abc']))
display(f(['abc', 'xyz']))
display(f(['abc', 'xyz', '12']))

#traverse(fl([]))
#traverse(fl(['abc']))
#traverse(fl(['abc', 'xyz']))
#traverse(fl(['abc', 'xyz', '12']))

# fr and f0 dumps core with ulimit -v 5000
#display(f(["abcdefghij","abcdefghij","abcdefghij","abcdefghij","abcdefghij"]))
