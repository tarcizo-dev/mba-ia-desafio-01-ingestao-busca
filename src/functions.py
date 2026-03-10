def print_overwrite(text):
    print("\r\x1b[2K", end="")
    print(f"\r{text}", end="", flush=True)