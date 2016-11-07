from acid.handlers import BaseHandler
from acid.nvim.extras import build_window

def format_payload(payload):
    if type(payload) == str:
        return [payload]

    ls = []
    try:
        for k, v in payload.items():
            key = k.lower()
            if key not in {'ns', 'session', 'id'}:
                if '\n' in v:
                    header, *trailer = v.split('\n')
                else:
                    header,  trailer = v, []

                if header.isspace() or header is "":
                    header, trailer = trailer[0], trailer[1:]

                ls.append("[{: <9}] => {}".format(
                    key.upper(), str(header)
                ).strip())

                for i in trailer:
                    ls.append("{: <14} {}".format("", str(i)))
    finally:
        return ls


class Handler(BaseHandler):

    name = "Proto"

    def on_init(self):
        self.bufs = {}

    def on_pre_handle(self, msg_id, *args):
        buffer_exists = msg_id in self.bufs
        window_exists = self.nvim.funcs.winbufnr(self.bufs.get(msg_id)) >= 0

        if (not buffer_exists or not window_exists):
            self.buf_nr = build_window(self.nvim, nolist=1, ansiesc=1, close=1)

    def on_handle(self, msg, *_):
        [self.nvim.buffers[self.buf_nr].append(i)
         for i
         in format_payload(msg)
         if not i.isspace()]