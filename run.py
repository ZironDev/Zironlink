# Zironlink -- public redacted build. Full source in the private repo.

import os
import sys
import pathlib
if sys.platform == 'win32':
    _here = pathlib.Path(__file__).parent.resolve()
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(str(_here))
    os.environ['PATH'] = str(_here) + os.pathsep + os.environ.get('PATH', '')
from app import winfix
winfix.apply()
import uvicorn
from app.config import settings
if __name__ == '__main__':
    uvicorn.run('app.main:app', host=settings.HOST, port=settings.PORT, reload=False)
