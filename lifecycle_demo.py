"""Small educational demonstration of object construction and cleanup."""

class LifecycleExample:
    def __init__(self, label):
        self.label = label
        print(f"Constructor (__init__): created {self.label}")

    def work(self):
        print(f"Method call: {self.label} is doing work")

    def __del__(self):
        # Educational only: timing of __del__ is not guaranteed.
        print(f"Destructor (__del__): cleanup for {self.label}")


def run_demo():
    print("Creating an object...")
    item = LifecycleExample("demo object")
    item.work()
    print("Deleting the reference explicitly...")
    del item
    print("The destructor may run now, but Python does not guarantee exact timing.")
