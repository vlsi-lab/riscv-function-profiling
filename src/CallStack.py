import hashlib
import random

class CallStack:
    def __init__(self, verbose=False):
        self.stack = []  # Stack of (function name, address, start time)
        self.times = []  # List of (start time, end time)
        self.time_counter = 0
        self.verbose = verbose
        self.call_stack_history = []  # To store the full call stack history

    def _generate_color(self, name):
        random.seed(int(hashlib.sha256(name.encode()).hexdigest(), 16) % 10**8)
        return (random.random(), random.random(), random.random())

    def call(self, func_name, addr):
        # Check if the func_name is equal to the last one
        if self.stack and self.stack[-1][0] == func_name:
            print("Continuing in function", func_name) if self.verbose else None
            self.tick()
            return

        print("Entering function", func_name) if self.verbose else None
        self.stack.append((func_name, addr, self.time_counter))
        self.times.append((self.time_counter, None))  # Start time, end time

    def tick(self):
        self.time_counter += 1

    def ret(self, func_name):
        if self.stack:
            # Pop until func_name is matched
            fn, addr, start_time = "", None, 0

            # Check if the func_name is not present in the stack, if so just pop the first element
            if func_name not in [f[0] for f in self.stack]:
                fn, addr, start_time = self.stack.pop()
            else:
                while self.stack and self.stack[-1][0] != func_name:
                    fn, addr, start_time = self.stack.pop()

            end_time = self.time_counter
            self.times[-1] = (self.times[-1][0], end_time)  # Set end time

            # Record the call stack and duration for flame graph data
            call_stack = [f[0] for f in self.stack] + [fn]
            duration = end_time - start_time
            if duration > 0:  # Only include calls with a positive duration
                self.call_stack_history.append((";".join(call_stack), duration))
    

    def generate_flamegraph_data(self, file_name):
        with open(file_name, 'w') as f:
            for stack_str, duration in self.call_stack_history:
                f.write(f"{stack_str} {duration}\n")
