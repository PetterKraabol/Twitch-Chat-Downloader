#!/usr/bin/env python3
import app


def main():
    output = app.download(app.arguments.video, app.arguments.format)
    print(output)


if __name__ == "__main__":
    main()
