from __future__ import absolute_import
import fire


def hello(name="World"):
    return "Hello %s!" % name


def main():
    fire.Fire(hello)


if __name__ == '__main__':
    main()
