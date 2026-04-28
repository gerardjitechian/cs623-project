from colorama import Fore, Style


def color_text(text, color="", bright=False):
    """
    Apply simple terminal coloring.
    """
    brightness = Style.BRIGHT if bright else ""
    return f"{brightness}{color}{text}{Style.RESET_ALL}"


def title(text):
    return color_text(text, Fore.CYAN, bright=True)


def info(text):
    return color_text(text, Fore.CYAN)


def success(text):
    return color_text(text, Fore.GREEN)


def warning(text):
    return color_text(text, Fore.YELLOW)


def error(text):
    return color_text(text, Fore.RED)


def muted(text):
    return color_text(text, Style.DIM)


def status_label(label):
    """
    Color common status labels consistently.
    """
    if label == "[OK]":
        return success(label)

    if label == "[WARNING]":
        return warning(label)

    if label == "[ERROR]":
        return error(label)

    return label


def data_status_label(status):
    """
    Color the overall data status.
    """
    if status == "ORIGINAL":
        return success(status)

    if status == "MODIFIED":
        return error(status)

    return status


def connection_status_label(status):
    """
    Color the database connection status.
    """
    if status == "CONNECTED":
        return success(status)

    if status == "DISCONNECTED":
        return error(status)

    return status


def print_section(section_title, width=72):
    """
    Print a colored section heading.
    """
    print(f"\n{title(section_title)}")
    print("-" * width)


def print_status_row(status, item, detail):
    """
    Print one aligned status row with colored status labels.
    """
    colored_status = status_label(status)
    spacing = " " * max(0, 10 - len(status))

    print(f"{colored_status}{spacing} {item:<18} {detail}")