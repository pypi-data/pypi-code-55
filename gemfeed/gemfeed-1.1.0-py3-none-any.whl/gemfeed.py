#!/usr/bin/env python3
import argparse
import datetime
import glob
import os
import os.path
import re
import stat
import urllib.parse

from feedgen.feed import FeedGenerator

def is_world_readable(filename):
    """
    Return True if the named file is world readable, otherwise return False.
    """
    st = os.stat(filename)
    return st.st_mode & stat.S_IROTH

def extract_first_heading(filename, default=""):
    """
    Open a file which is presumed to contain text/gemini content and return
    the contents of the first heading line (regardless of heading level).
    If no heading lines are found, return the specified default.
    """
    with open(filename) as fp:
        for line in fp:
            if line.startswith("#"):
                while line[0] == "#":
                    line = line[1:]
                return line.strip()
    return default

def get_feed_title(directory):
    """
    If an index.gmi or index.gemini file exists and is worldreadable, return
    the content of the first heading line in the file, otherwise return a
    default feed title.
    """
    # By default, use the deepest directory name as a feed title
    # This needs a little care, as os.path.basename will return an empty
    # string if `directory` ends in a trailing slash...
    head, default = os.path.split(directory)
    if not default:
        default = os.path.basename(head)
    # Check for index files which may override the default
    for index_file in ("index.gmi", "index.gemini"):
        index_file = os.path.join(directory, index_file)
        if os.path.exists(index_file) and is_world_readable(index_file):
            return extract_first_heading(index_file, default)
    return default

def find_files(directory, n=10):
    """
    Return the n most recently created world readable files with extensions of
    .gmi or .gemini, as a list sorted from most to least recent.
    """
    files = []
    for extension in ("gmi", "gemini"):
        glob_pattern = os.path.join(directory, "*.{}".format(extension))
        files.extend(glob.glob(glob_pattern))
        index = os.path.join(directory, "index.{}".format(extension))
        if index in files:
            files.remove(index)
    files = [f for f in files if is_world_readable(f)]
    files.sort(key=os.path.getctime, reverse=True)
    return files[0:n]

def urljoin(base, url):
    """
    Return an absolute URL formed by combining the provided base and relative
    URLs.

    This is necessary because the various functions in Python's urllib to do
    this do not function as expected if the URL scheme is not recognised,
    which of course gemini:// is not.  Thus, we need to do a little dance
    where we transform gemini URLs to https URLs, join them, and then undo
    the transformation.
    """
    base = urllib.parse.urlsplit(base)
    base = base._replace(scheme="https")
    base = urllib.parse.urlunsplit(base)
    joined = urllib.parse.urljoin(base, url)
    joined = urllib.parse.urlsplit(joined)
    joined = joined._replace(scheme="gemini")
    return urllib.parse.urlunsplit(joined)

def populate_entry_from_file(filename, base_url, entry):
    """
    Set the id, title, updated and link attributes of the provided
    FeedGenerator entry object according the contents of the named
    Gemini file and the base URL.
    """
    url = urljoin(base_url, os.path.basename(filename))
    entry.guid(url)
    entry.link(href=url, rel="alternate")
    updated = get_update_time(filename)
    entry.updated(updated)
    default_title = os.path.splitext(os.path.basename(filename))[0]
    title = extract_first_heading(filename, default_title)
    entry.title(title)

def get_update_time(filename):
    """
    Return an update time for a Gemini file.

    If the filename begins with an ISO8601 date stamp, that date
    (with a time of midnight) will be used.  Otherwise, the file
    "creation time" (which in unix is actually the time of last
    metadata update) will be used instead as a best estimate.
    """
    # Check for leading YYYY-MM-DD
    basename = os.path.basename(filename)
    if re.search("^[0-9]{4}-[01][0-9]-[0-3][0-9]", basename):
        date = basename[0:10] + " Z" # Add UTC marker
        return datetime.datetime.strptime(date, "%Y-%m-%d %z")
    else:
        updated = os.path.getctime(filename)
        return datetime.datetime.fromtimestamp(updated, tz=datetime.timezone.utc)

def build_feed(directory, base_url, output="atom.xml", n=10, title="",
        subtitle="", author="", email="", verbose=False):
    """
    Build an Atom feed for all world readable Gemini files in the current
    directory, and write it to atom.xml.
    """
    # If a title hasn't been provided, try to get one from an index page
    if not title:
        title = get_feed_title(directory)

    # Let user know feed title and URL
    feed_url = urljoin(base_url, output)
    if verbose:
        print('Generating feed "{}", which should be served from {}'.format(title, feed_url))

    # Setup feed
    feed = FeedGenerator()
    feed.id(base_url)
    feed.title(title)
    if subtitle:
        feed.subtitle(subtitle)
    author_details = {}
    if author:
        author_details["name"] = author
    if email:
        author_details["email"] = email
    if author_details:
        feed.author(author_details)
    feed.link(href=feed_url, rel='self')
    feed.link(href=base_url, rel='alternate')

    # Add one entry per .gmi file
    files = find_files(directory, n)
    if not files:
        if verbose:
            print("No world-readable Gemini content found! :(")
        return
    for n, filename in enumerate(files):
        entry = feed.add_entry()
        populate_entry_from_file(filename, base_url, entry)
        if n == 0:
            feed.updated(entry.updated())
        if verbose:
            print("Adding {} with title '{}'...".format(os.path.basename(filename),
                entry.title()))

    # Write file
    output = os.path.join(directory, output)
    feed.atom_file(output, pretty=True)
    if verbose:
        print("Wrote Atom feed to {}.".format(output))

def main():
    """
    Parse command line arguments, do some minor processing, and then invoke
    the build_feed command with the provided settings.
    """

    # Get cwd as default value for --directory
    cwd = os.getcwd()

    # Parse arguments
    parser = argparse.ArgumentParser(description='Generate an Atom feed for Gemini content.')
    parser.add_argument('-a', '--author', dest='author', type=str,
            help="feed author's name")
    parser.add_argument('-b', '--base', dest='base_url', type=str,
            required=True, help='base URL for feed and entries')
    parser.add_argument('-d', '--directory', dest='directory', type=str,
            default=cwd, help='directory to find content and save feed to')
    parser.add_argument('-e', '--email', dest='email', type=str,
            help="feed author's email address")
    parser.add_argument('-n', dest='n', type=int, default=10,
            help='include N most recently created files in feed (default 10)')
    parser.add_argument('-o', '--output', dest='output', type=str,
            default="atom.xml", help='output filename')
    parser.add_argument('-q', '--quiet', dest='verbose', action="store_false",
            help='Write nothing to stdout under non-error conditions')
    parser.add_argument('-s', '--subtitle', dest='subtitle', type=str,
            help='feed subtitle')
    parser.add_argument('-t', '--title', dest='title', type=str,
            help='feed title')
    args = parser.parse_args()

    # Normalise base URL
    base_url = urllib.parse.urlsplit(args.base_url)
    if not base_url.netloc and base_url.path:
        # Handle a naked domain, which urlsplit will interpet at a local path
        base_url = base_url._replace(netloc=base_url.path, path="")
    base_url = base_url._replace(scheme="gemini")
    args.base_url = urllib.parse.urlunsplit(base_url)
    if not args.base_url.endswith("/"):
        args.base_url += "/"

    # Build the feed
    build_feed(args.directory, args.base_url, args.output, args.n, args.title,
            args.subtitle, args.author, args.email, args.verbose)

if __name__ == "__main__":
    main()
