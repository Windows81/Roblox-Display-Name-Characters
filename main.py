import roblox

DATABASE_TYPE = roblox.display_name_database
SCRAPER_TYPE = roblox.display_name_scraper


def get_iden_list(database: DATABASE_TYPE, args):
    mode = args.mode
    if mode == 'holes':
        return [
            i
            for (beg, end, diff) in database.get_holes()
            for i in range(beg + 1, end)
        ]

    start_def_min = (database.get_max() or SCRAPER_TYPE.RANGE_MIN - 1) + 1
    start_def_max = (database.get_min() or SCRAPER_TYPE.RANGE_MAX + 1) - 1

    if mode == 'expand':
        if args.up:
            ss = start_def_min
            stop = SCRAPER_TYPE.RANGE_MAX
            incr = +1

        elif args.down:
            ss = start_def_max
            stop = SCRAPER_TYPE.RANGE_MAX
            incr = -1

    else:
        incr = args.incr
        if args.ss < 0:
            ss = \
                start_def_min\
                if args.incr > 0 else \
                start_def_max
        if args.stop < 0:
            stop = \
                SCRAPER_TYPE.RANGE_MAX \
                if args.incr > 0 else\
                SCRAPER_TYPE.RANGE_MIN

    return list(range(ss, stop, incr))


if __name__ == "__main__":
    import argparse
    import warnings
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--threads", default=SCRAPER_TYPE.DEFAULT_THREAD_COUNT, required=False, type=int)
    subparser = parser.add_subparsers(dest='mode')

    sub_iterate = subparser.add_parser('iterate')
    sub_iterate.add_argument("-incr", default=1, required=False, type=int)
    sub_iterate.add_argument("-ss", default=-1, required=False, type=int)
    sub_iterate.add_argument(
        "--stop", "-to", default=-1, required=False, type=int)

    sub_holes = subparser.add_parser('holes')

    sub_expand = subparser.add_parser('expand')
    mutex_expand = sub_expand.add_mutually_exclusive_group(required=True)
    mutex_expand.add_argument('--up', action='store_true')
    mutex_expand.add_argument('--down', action='store_true')

    args = parser.parse_args()
    database = DATABASE_TYPE()

    scraper = SCRAPER_TYPE(
        database=database,
        iden_list=get_iden_list(database, args),
        thread_count=args.threads,
    )
    scraper.run()
