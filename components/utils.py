import threading


class SaveThread(threading.Thread):
    def __init__(self, callback, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.callback = callback
        self.kwargs = kwargs.get('kwargs')
        self.url = None
        self.method = None
        if self.kwargs:
            self.url = self.kwargs.get('url')
            self.method = self.kwargs.get('method')
        run_original = self.run

        def run_with_except_hook():
            try:
                run_original()
            except Exception as e:
                data = (self.url, 'with error {}'.format(e), self.method)
                self.callback(data)
            else:
                data = (self.url, 'successful', self.method)
                self.callback(data)

        self.run = run_with_except_hook
