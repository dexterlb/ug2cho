import click
import sys
import dataclasses
import os
import os.path

from ug2cho.html2ug import html2ug
from ug2cho.chordpro import ug_to_chordpro
from ug2cho.ug import UG
from ug2cho.download import download, URL

@dataclasses.dataclass
class File:
    path: str

    def open(self):
        return click.open_file(self.path)

    def read(self):
        with self.open() as f:
            return f.read()

class FileOrURLArg(click.ParamType):
    name = "file_or_url"

    def convert(self, value, param, ctx):
        url = URL.parse(value)
        if url:
            return url

        pt = click.Path(exists=True, file_okay=True, dir_okay=False, allow_dash=True)
        return File(path=pt.convert(value, param, ctx))

@click.command()
@click.option(
    '--in-format',
    type=click.Choice(['auto', 'html', 'ug']),
    default='auto',
    help='Input file format (defaults to "auto", which will detect HTML or UG-specific tags)',
)
@click.option(
    '--out-format', '-f',
    type=click.Choice(['auto', 'ug', 'cho', 'txt']),
    default='auto',
    help='Output file format (defaults to "auto", which will guess from extension and fallback to "cho")',
)
@click.option(
    '--cookies',
    type=click.Path(exists=True, dir_okay=False),
    help='Netscape-format cookiejar file to use when downloading URLs',
)

@click.argument('src', type=FileOrURLArg(), default='-')
@click.argument('dest', type=click.Path(file_okay=True, dir_okay=True), default='-')

def main(src, dest, in_format, out_format, cookies):
    '''
    Convert a leadsheet from ultimate-guitar.com into ChordPro or plain text.
    Also supports an intermediate format 'ug' that you can use to patch-up
    the leadsheet before it gets converted, in case chords contain typos.

    \b
    SRC can be:
        - a filename        (that will be read)
        - a http(s):// url  (that will be downloaded)
        - '-'               (for stdin)

    \b
    DEST can be:
        - a filename        (that will be written)
        - a directory       (a file with a "<artist> - <title>.<fmt>" filename will be created in it)
        - '-'               (for stdout)
    '''

    if type(src) is File:
        in_text = src.read()
    elif type(src) is URL:
        resp = download(src, cookies)
        if resp.status_code == 403:
            raise click.ClickException(
                "Server returned 403 (forbidden). This probably means that UG's cloudflare protection has activated. You can try passing --cookies with a cookiejar that has a non-expired UG cloudflare token.",
            )
        resp.raise_for_status()
        in_text = resp.text
    else:
        raise RuntimeError(f'unknown source type: {type(src)}')

    if in_format == 'auto':
        in_format = recognise_format(in_text)

    if in_format == 'html':
        ug = html2ug(in_text)
    elif in_format == 'ug':
        ug = UG.from_str(in_text)
    else:
        raise click.ClickException(f'unknown in_format ({in_format})')

    if out_format == 'auto':
        out_format = dest.split('.')[-1]
        if out_format not in {'ug', 'cho', 'txt'}:
            out_format = 'cho'

    if out_format == 'ug':
        out_data = ug.to_str()
    elif out_format == 'cho':
        out_data = ug_to_chordpro(ug)
    elif out_format == 'txt':
        out_data = ug.plain_text_leadsheet()
    else:
        raise click.ClickException(f'unknown out_format ({out_format})')

    if os.path.isdir(dest):
        dest = os.path.join(dest, f'{ug.metadata['artist_name']} - {ug.metadata['song_name']}.{out_format}')

    with click.open_file(dest, 'w') as destf:
        destf.write(out_data)

def recognise_format(text):
    if '<div class="js-store"' in text:
        return 'html'

    if '[tab]' in text:
        return 'ug'

    raise click.ClickException('could not autodetect input format')

if __name__ == "__main__":
    main()
