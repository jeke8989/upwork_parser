
def get_proxies() -> list[str | None]:
    with open("proxies.txt") as f:
        file_content = f.read()
    proxies = file_content.splitlines()
    return proxies
