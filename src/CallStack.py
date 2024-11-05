import hashlib
import random

class CallStack:
    def __init__(self, verbose=False):
        self.stack = []  # Stack of (function name, address, start time)
        self.verbose = verbose
        self.call_stack_history = []  # To store the full call stack history

    def _generate_color(self, name):
        random.seed(int(hashlib.sha256(name.encode()).hexdigest(), 16) % 10**8)
        return (random.random(), random.random(), random.random())

    def call(self, func_name, addr, mcycle):
        if self.stack and self.stack[-1][0] == func_name:
            print("Continuing in function", func_name) if self.verbose else None
            return

        print("Entering function", func_name) if self.verbose else None
        self.stack.append((func_name, addr, mcycle))

    def ret(self, func_name, mcycle):
        if self.stack:
            # Pop until func_name is matched
            fn, addr, start_time = "", None, 0

            # Check if the func_name is not present in the stack, if so just pop the first element
            if func_name not in [f[0] for f in self.stack]:
                fn, addr, start_time = self.stack.pop()
            else:
                while self.stack and self.stack[-1][0] != func_name:
                    fn, addr, start_time = self.stack.pop()

            end_time = mcycle

            # Record the call stack and duration for flame graph data
            call_stack = [f[0] for f in self.stack] + [fn]
            duration = end_time - start_time
            if duration > 0:  # Only include calls with a positive duration
                self.call_stack_history.append((";".join(call_stack), duration))
    

    def generate_flamegraph_data(self, file_name):
        with open(file_name, 'w') as f:
            for stack_str, duration in self.call_stack_history:
                f.write(f"{stack_str} {duration}\n")
