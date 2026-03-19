import sys

if sys.platform == "win32":

    class HTML:
        def __init__(self, string=None, base_url=None, **kwargs):
            self._html = string

        def write_pdf(self, path, **kwargs):
            print(f"[SKIP] PDF generisanje nije podržano na Windowsu. Path: {path}")
            with open(path.replace(".pdf", ".html"), "w", encoding="utf-8") as f:
                f.write(self._html or "")

else:
    pass
