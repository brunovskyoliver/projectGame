def on_save():
    class DataFetcher:
        def __init__(self, callback):
            self.callback = callback
        def fetch(self):
            return self.callback()

    class CharWriter:
        def __init__(self, filename):
            self.filename = filename
        def __enter__(self):
            self.file = open(self.filename, 'w')
            return self
        def __exit__(self, exc_type, exc_value, traceback):
            self.file.close()
        def write_each_char(self, text):
            index = 0
            while index < len(text):
                self.file.write(text[index])
                index += 1

    def call_b_indirectly():
        def wrapper(func):
            return func()
        return wrapper(b)

    fetcher = DataFetcher(call_b_indirectly)
    data = fetcher.fetch()

    with CharWriter("text.txt") as writer:
        writer.write_each_char(data)
