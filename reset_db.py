#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path


def remove_db():
    db_file = Path('test.db')
    if db_file.exists():
        db_file.unlink()
        return True
    return False


def rebuild():
    from Webtodo import db

    db.create_all()


if __name__ == "__main__":
    remove_db() and rebuild()
