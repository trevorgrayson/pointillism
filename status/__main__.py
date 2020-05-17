import time
from datetime import datetime
import curses
from curses import wrapper


from json import loads
from urllib.request import urlopen
RSS_FEED = 'https://api.travis-ci.org/repos/trevorgrayson/pointillism/builds'

POLL_TIME = 3 # seconds

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

WIN = curses.newwin(1, 80, 0, curses.COLS - 1)


class Build:
    def __init__(self, **attrs):
        # print(attrs)
        self.number = int(attrs['number'])
        self.finished_at = attrs.get('finished_at')
        if self.finished_at:
            self.finished_at = datetime.strptime(self.finished_at, '%Y-%m-%dT%H:%M:%SZ')

        self.state = attrs['state']
        self.message = attrs['message']
        self._duration = attrs.get('duration')
        self.branch = attrs['branch']
        self.commit = attrs['commit']

    @property
    def is_finished(self):
        return self.state == 'finished'

    @property
    def duration(self):
        if self._duration:
            return f'{self._duration}s'

        return ''

    @property
    def ago(self):
        """ returns a string representation for user. """
        if self.finished_at:
            return datetime.now() - self.finished_at
        return 'running'

    def __str__(self):
        return '\t'.join(map(str,(
            # self.ago,
            # self.duration,
            self.number,
            self.state,
            self.branch[0:5],
            self.commit[0:5],
            self.message,
        )))


def cast_to(Type, alist):
    return list(map(lambda args: Type(**args), alist))


if __name__ == '__main__':
    stdscr.clear()
    start_build = 0
    start_time = datetime.now()
    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()

    while(True):
        with urlopen('https://api.travis-ci.org/repos/trevorgrayson/pointillism/builds') as fp:
            response = loads(fp.read())
            builds = cast_to(Build, response)
            build_number = builds[0].number
            # cache_length = fp.info()
            # NOTE presuming first build is the latest
            # for build in builds:
            value = str(builds[0])

            elapsed = datetime.now() - start_time
            value += f'>>{elapsed}'

            stdscr.addstr(0, 0, value)
            stdscr.move(0, 0)
            stdscr.refresh()

            if builds[0].state == 'finished':
                print(builds[0])
                exit(0)

            time.sleep(POLL_TIME)

