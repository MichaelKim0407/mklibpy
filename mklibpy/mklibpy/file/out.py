__author__ = 'Michael'


class MultiWriter(object):
    def __init__(self, pr=False, *files):
        self.__open = False
        self.__pr = pr
        self.__files = {}
        for f in files:
            self.add_file(f)
        self.__writers = {}

        self.logger = None

    def add_file(self, name, mode='w', *args, **kwargs):
        if name in self.__files:
            raise ValueError("\'{}\' already exists".format(name))
        self.__files[name] = mode, args, kwargs
        if self.__open:
            self.__open_writer(name)

    def set_mode(self, name, mode, *args, **kwargs):
        if name not in self.__files:
            raise ValueError("\'{}\' does not exist".format(name))
        if self.__open:
            raise Exception("Cannot change mode while the file is opened")
        self.__files[name] = mode, args, kwargs

    def __open_writer(self, name):
        mode, args, kwargs = self.__files[name]
        writer = open(name, mode=mode, *args, **kwargs)
        self.__writers[name] = writer

    def __enter__(self):
        for name in self.__files:
            self.__open_writer(name)
        self.__open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for name in self.__writers:
            # Although closing a file rarely raises Exceptions,
            # we must ensure that all files are closed.
            try:
                self.__writers[name].close()
            except:
                if self.logger is not None:
                    self.logger.warn("File \'{}\' failed to close".format(name))

    def __get_text(self, text, *args, **kwargs):
        if args or kwargs:
            return text.format(*args, **kwargs)
        else:
            return text

    def __write_files(self, text):
        for writer in self.__writers.values():
            writer.write(text)

    def write(self, text, *args, **kwargs):
        text = self.__get_text(text, *args, **kwargs)
        if self.__pr:
            print(text)
        self.__write_files(text)

    def writeline(self, text, *args, **kwargs):
        text = self.__get_text(text, *args, **kwargs)
        if self.__pr:
            print(text)
        self.__write_files(text + "\n")

    def writelines(self, *lines):
        for l in lines:
            self.writeline(l)
