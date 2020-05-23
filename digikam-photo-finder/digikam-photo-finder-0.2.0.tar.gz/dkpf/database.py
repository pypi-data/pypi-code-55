import os
import sqlite3
from collections import defaultdict
from functools import cached_property


class DigikamDB:
    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(self.path)

    def execute(self, query, *args, **kwargs):
        cur = self.conn.cursor()
        cur.execute(query, *args, **kwargs)
        return cur

    @cached_property
    def tags_tree(self):
        cur = self.execute(
            """
            SELECT pid, id FROM TagsTree
        """
        )

        tree = defaultdict(set)
        for pid, tid in cur:
            tree[pid].add(tid)

        return tree

    @cached_property
    def paths_by_tagset(self):
        query = """
            SELECT Albums.relativePath, Images.name, ImageTags.tagId
            FROM Albums
            INNER JOIN Images
            ON Albums.id == Images.album
            INNER JOIN ImageTags
            ON Images.id == ImageTags.imageid
        """
        cur = self.execute(query)
        tags_by_path = defaultdict(set)
        for album, image, tagId in cur:
            album = album.lstrip("/")
            path = os.path.join(album, image)
            tags_by_path[path].add(tagId)

        result = defaultdict(list)
        for path, tags in tags_by_path.items():
            result[tuple(sorted(tags))].append(path)

        return result

    def get_tag_ids(self, names):
        if isinstance(names, str):
            names = [names]

        cur = self.execute(
            f"""
            SELECT id FROM Tags
            WHERE name IN ({','.join('?' * len(names))})
        """,
            names,
        )

        return [t[0] for t in cur.fetchall()]

    def get_paths(self, names):
        tids = self.get_tag_ids(names)

        def matches(tags):
            for tid in tids:
                if tid in tags:
                    continue

                if tid in self.tags_tree and any(
                    t in tags for t in self.tags_tree[tid]
                ):
                    continue

                return False

            return True

        result = []
        for tags, paths in self.paths_by_tagset.items():
            if matches(tags):
                result.extend(paths)
        return sorted(result)
