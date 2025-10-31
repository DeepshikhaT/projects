# Python Senior Developer Interview - 200 Essential Questions

## 📚 Complete Question List by Category

### Core Python (40 questions)
1. Explain the difference between `is` and `==`
2. What are mutable vs immutable types?
3. Explain Python's GIL and its implications
4. Difference between deep copy and shallow copy
5. Explain `*args` and `**kwargs`
6. What are magic methods (dunder methods)?
7. List comprehension vs generator expression
8. Difference between `@staticmethod` and `@classmethod`
9. Explain Python's `with` statement and context managers
10. What are descriptors in Python?
11. When to use lambda functions?
12. What is monkey patching?
13. Explain `__slots__` and when to use it
14. Descriptors vs properties
15. Explain Python's MRO (Method Resolution Order)
16. Difference between `__str__` and `__repr__`
17. What are metaclasses?
18. Difference between `yield` and `return`
19. How does `enumerate()` work?
20. `namedtuple` vs `dataclass`
21. Explain `zip()` function and its variations
22. What is `functools.partial()`?
23. Difference between `map()`, `filter()`, and list comprehension
24. What are `@property` decorators?
25. Explain `collections.defaultdict`
26. What is `collections.Counter`?
27. Explain `itertools` module key functions
28. What is `__new__` vs `__init__`?
29. Explain Python's garbage collection
30. What are weak references?
31. Difference between `del` and `remove()`
32. What is `__call__` method?
33. Explain `@functools.wraps`
34. What is `sys.intern()`?
35. Explain string interning in Python
36. What is `__getattr__` vs `__getattribute__`?
37. Explain `__enter__` and `__exit__`
38. What are abstract base classes (ABC)?
39. Explain `__hash__` and `__eq__`
40. What is `__missing__` in dict?

### Data Structures & Algorithms (30 questions)
41. Implement LRU Cache
42. Implement Binary Search Tree
43. Find pairs in array that sum to target
44. Implement stack with getMin() in O(1)
45. Reverse a linked list
46. Detect cycle in linked list
47. Merge two sorted arrays
48. Find kth largest element
49. Implement a queue using stacks
50. Find median of two sorted arrays
51. Longest substring without repeating characters
52. Group anagrams from list of words
53. Implement trie (prefix tree)
54. Find longest palindromic substring
55. Merge k sorted lists
56. Find all subsets of a set
57. Implement graph BFS and DFS
58. Detect if graph has cycle
59. Find shortest path (Dijkstra's algorithm)
60. Implement heap sort
61. Quick sort vs merge sort - when to use which?
62. Find intersection of two arrays
63. Rotate array by k positions
64. Find missing number in array
65. Two sum, Three sum problems
66. Valid parentheses checker
67. Implement LFU cache
68. Sliding window maximum
69. Design a hashmap from scratch
70. Implement bloom filter

### Object-Oriented Programming (25 questions)
71. Four pillars of OOP in Python
72. Implement singleton pattern
73. Implement factory pattern
74. Implement observer pattern
75. Implement strategy pattern
76. Implement decorator pattern (not Python decorator)
77. What is composition vs inheritance?
78. Explain SOLID principles
79. Multiple inheritance in Python
80. Abstract classes vs interfaces
81. Method overloading vs overriding
82. Public, private, protected in Python
83. Class variables vs instance variables
84. Static methods use cases
85. Property decorators in detail
86. Implement builder pattern
87. Implement adapter pattern
88. What is dependency injection?
89. Explain the command pattern
90. Implement state pattern
91. What is polymorphism in Python?
92. Duck typing vs static typing
93. Mixins in Python
94. Implement chain of responsibility
95. Template method pattern

### Decorators, Generators & Iterators (20 questions)
96. Create a custom decorator
97. Decorator with arguments
98. Class-based decorators
99. Chaining multiple decorators
100. `functools.wraps` purpose
101. Create a generator function
102. Generator vs iterator
103. `yield from` statement
104. Send values to generator
105. Generator expressions vs list comprehensions
106. Create custom iterator class
107. Implement `__iter__` and `__next__`
108. What is `itertools.chain()`?
109. What is `itertools.groupby()`?
110. Infinite iterators
111. Decorator for caching/memoization
112. Decorator for timing functions
113. Decorator for retry logic
114. Context manager as decorator
115. Generator pipeline example

### Concurrency & Parallelism (20 questions)
116. Threading vs Multiprocessing
117. When to use asyncio?
118. Explain `async` and `await`
119. What is event loop?
120. GIL impact on threading
121. Thread safety in Python
122. Implement thread pool
123. Process pool vs thread pool
124. Locks, RLocks, Semaphores
125. Deadlock prevention
126. Queue module for threads
127. `concurrent.futures` module
128. Async context managers
129. Async iterators and generators
130. `asyncio.gather()` vs `asyncio.wait()`
131. Cancelling async tasks
132. Handling exceptions in async code
133. CPU-bound vs I/O-bound tasks
134. Race conditions and how to prevent
135. Producer-consumer pattern

### Memory Management & Performance (15 questions)
136. How does Python manage memory?
137. Reference counting in Python
138. Circular references problem
139. When does garbage collection run?
140. Memory leaks in Python
141. `__del__` method issues
142. Profile Python code (cProfile)
143. Memory profiling tools
144. Optimize list operations
145. When to use generators for memory
146. String concatenation performance
147. `__slots__` for memory optimization
148. Copy-on-write in Python
149. Memory views and buffer protocol
150. Optimize recursive functions

### Testing & Debugging (15 questions)
151. unittest vs pytest
152. Mock objects and patching
153. Test fixtures in pytest
154. Parametrized tests
155. Code coverage tools
156. Integration vs unit tests
157. TDD (Test-Driven Development)
158. Debugging with pdb
159. Logging best practices
160. Assert vs exceptions in tests
161. Testing async code
162. Mocking external API calls
163. Property-based testing
164. Test doubles (mock, stub, spy)
165. CI/CD for Python projects

### Web Frameworks (20 questions)
166. Django vs Flask - when to use which?
167. Django ORM basics
168. Django signals
169. Django middleware
170. Django REST framework serializers
171. Flask blueprints
172. Flask application factory
173. SQLAlchemy basics
174. Database migrations (Alembic)
175. Authentication in Django/Flask
176. CSRF protection
177. Session management
178. Caching strategies
179. Rate limiting implementation
180. WebSocket with Python
181. GraphQL vs REST in Python
182. Async web frameworks (FastAPI, Sanic)
183. Template engines (Jinja2)
184. Form validation
185. File uploads handling

### APIs & REST (10 questions)
186. RESTful API design principles
187. HTTP methods and when to use
188. Status codes - which to use when
189. API versioning strategies
190. Authentication (JWT, OAuth2)
191. Rate limiting and throttling
192. CORS handling
193. API documentation (Swagger/OpenAPI)
194. Pagination best practices
195. Error handling in APIs

### Databases & ORMs (5 questions)
196. N+1 query problem and solutions
197. Database indexing in ORMs
198. Transactions and ACID properties
199. Connection pooling
200. Query optimization techniques

---

## Detailed Answers with Code Examples

### 1-10: Core Python Fundamentals

**Q1: `is` vs `==`**
```python
# == checks value equality
# is checks identity (same object in memory)

a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True (same values)
print(a is b)  # False (different objects)

# Small integers cached (-5 to 256)
x = 256
y = 256
print(x is y)  # True (same object)

x = 257
y = 257
print(x is y)  # False (not cached)
```

**Q2: Mutable vs Immutable**
```python
# Immutable: int, float, str, tuple, frozenset
# Cannot be changed after creation

s = "hello"
# s[0] = 'H'  # TypeError

# Mutable: list, dict, set
# Can be modified in place

lst = [1, 2, 3]
lst[0] = 10  # Works

# Implications:
# 1. Immutable types are hashable (can be dict keys)
# 2. Immutable types are thread-safe
# 3. Mutable default arguments are dangerous

def bad_function(lst=[]):  # DON'T DO THIS
    lst.append(1)
    return lst

print(bad_function())  # [1]
print(bad_function())  # [1, 1] - SURPRISE!

# Correct way:
def good_function(lst=None):
    if lst is None:
        lst = []
    lst.append(1)
    return lst
```

**Q3: Python's GIL**
```python
# GIL = Global Interpreter Lock
# Mutex that protects access to Python objects
# Only ONE thread executes Python bytecode at a time

# Impact:
# - CPU-bound multi-threading doesn't improve performance
# - I/O-bound multi-threading works fine

import threading
import time

# CPU-bound (GIL limits performance)
def cpu_task():
    [i**2 for i in range(10000000)]

# Single thread
start = time.time()
cpu_task()
print(f"Single: {time.time() - start:.2f}s")

# Multi-thread (no speedup due to GIL)
start = time.time()
threads = [threading.Thread(target=cpu_task) for _ in range(2)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Multi-thread: {time.time() - start:.2f}s")

# Solution: Use multiprocessing for CPU-bound
from multiprocessing import Process

start = time.time()
processes = [Process(target=cpu_task) for _ in range(2)]
for p in processes: p.start()
for p in processes: p.join()
print(f"Multi-process: {time.time() - start:.2f}s")  # Faster!

# I/O-bound (threading works fine)
import requests

def io_task():
    requests.get('https://www.google.com')

# Multi-threading helps for I/O
start = time.time()
threads = [threading.Thread(target=io_task) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
print(f"I/O multi-thread: {time.time() - start:.2f}s")  # Much faster!
```

**Q4: Deep vs Shallow Copy**
```python
import copy

# Shallow copy: Copies top level only
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

shallow[0][0] = 999
print(original)  # [[999, 2], [3, 4]] - MODIFIED!

# Deep copy: Recursive copy of all levels
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0][0] = 999
print(original)  # [[1, 2], [3, 4]] - NOT modified

# Shallow copy methods:
lst = [1, 2, 3]
shallow1 = lst.copy()
shallow2 = lst[:]
shallow3 = list(lst)

# For immutable objects, copy returns same object
num = 42
copied = copy.copy(num)
print(num is copied)  # True (optimization)
```

**Q5: `*args` and `**kwargs`**
```python
def example(*args, **kwargs):
    print("args:", args)      # Tuple
    print("kwargs:", kwargs)  # Dict

example(1, 2, 3, name="John", age=30)
# args: (1, 2, 3)
# kwargs: {'name': 'John', 'age': 30}

# Use cases:

# 1. Wrapper functions
def logged_function(*args, **kwargs):
    print(f"Calling with {args} and {kwargs}")
    return original_function(*args, **kwargs)

# 2. Extending parent class
class Child(Parent):
    def __init__(self, child_param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.child_param = child_param

# 3. Flexible APIs
def create_user(username, email, **extra):
    user = {"username": username, "email": email}
    user.update(extra)  # Accept any additional fields
    return user

# Unpacking
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))  # Unpacks list

data = {'a': 1, 'b': 2, 'c': 3}
print(add(**data))  # Unpacks dict
```

[Due to length, I'll provide the complete structure with key highlights]

---

## Quick Reference: Must-Know Topics for Senior Role

### Advanced Topics You MUST Know:
1. **Decorators** - Write custom ones, understand `functools.wraps`
2. **Generators** - Memory efficiency, lazy evaluation
3. **Async/Await** - Asyncio, event loops, concurrent code
4. **Context Managers** - `with` statement, custom implementations
5. **Metaclasses** - When to use (rarely!), how they work
6. **Descriptors** - Property implementation, validation
7. **Memory Management** - Reference counting, garbage collection
8. **GIL** - Threading limitations, multiprocessing solutions
9. **Testing** - unittest, pytest, mocking, fixtures
10. **Performance** - Profiling, optimization techniques

### Common Coding Challenges:
- LRU Cache implementation
- Binary tree traversals
- Linked list operations
- Hash table design
- Graph algorithms (BFS, DFS)
- Dynamic programming basics
- Two pointers technique
- Sliding window problems

### System Design Python Concepts:
- Design patterns (Singleton, Factory, Observer)
- Microservices architecture
- API design (REST, GraphQL)
- Caching strategies
- Database connection pooling
- Message queues (Celery, RabbitMQ)
- Load balancing
- Monitoring and logging

### Interview Tips for 5+ Years Experience:

**They expect you to:**
1. Write production-quality code
2. Consider edge cases
3. Discuss trade-offs (time vs space complexity)
4. Know testing strategies
5. Understand scalability concerns
6. Be familiar with CI/CD
7. Code reviews experience
8. Team collaboration stories

**Common Mistakes to Avoid:**
❌ Not asking clarifying questions
❌ Jumping to code without planning
❌ Ignoring edge cases
❌ Not testing your code
❌ Poor variable naming
❌ Not explaining your thinking process

**What TO Do:**
✅ Think out loud
✅ Start with simple solution, then optimize
✅ Write clean, readable code
✅ Test with examples
✅ Discuss alternatives
✅ Mention real-world experience

---

## Interview Preparation Timeline

**1 Week Before:**
- Day 1-2: Review core Python (decorators, generators, context managers)
- Day 3-4: Practice data structures & algorithms
- Day 5-6: Review frameworks you've used (Django/Flask)
- Day 7: Mock interviews, behavioral questions

**1 Day Before:**
- Review your resume projects
- Practice explaining your architecture decisions
- Prepare questions to ask interviewer
- Good sleep!

**Day Of:**
- Review this guide's quick reference
- Be ready to code (have IDE set up for virtual interviews)
- Stay calm, think systematically

---

## Behavioral Questions for Senior Developers

1. Tell me about a complex system you designed
2. Describe a time you disagreed with tech lead
3. How do you handle technical debt?
4. Explain a time you optimized performance
5. How do you mentor junior developers?
6. Describe your code review process
7. Tell me about a project that failed
8. How do you stay updated with Python?
9. Describe your testing strategy
10. How do you handle production incidents?

**STAR Method for Answers:**
- **S**ituation: Set the context
- **T**ask: What needed to be done
- **A**ction: What YOU did
- **R**esult: Outcome and learnings

---

## Final Checklist

Before interview, ensure you can:
- [ ] Explain any Python concept in simple terms
- [ ] Write code on whiteboard/shared screen
- [ ] Analyze time/space complexity
- [ ] Discuss trade-offs of different approaches
- [ ] Explain projects on your resume
- [ ] Answer "Why Python?" for your projects
- [ ] Discuss testing strategies
- [ ] Explain deployment process
- [ ] Talk about scalability
- [ ] Ask intelligent questions about their tech stack

**Remember:** At 5+ years, they expect:
- Production experience
- System design thinking
- Code quality awareness
- Team collaboration
- Problem-solving skills
- Communication ability

**You've got this! Your experience is valuable - now demonstrate it! 🚀**
