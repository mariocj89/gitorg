from gitorg import gitorg, load_config


def main():
    conf = load_config()
    gitorg(obj={}, default_map=conf)

if __name__ == '__main__':  # pragma: no cover
    exit(main())
