# Tutorial information
slug = "js4py"
title = "JavaScript for Python Programmers"
subtitle = "an introduction for the reluctant and weary"
repo = f"https://github.com/gvwilson/{slug}"
author = {
    "name": "Greg Wilson",
    "email": "gvwilson@third-bit.com",
    "site": "https://third-bit.com/",
}
lang = "en"
highlight = "tango.css"
plausible = "third-bit.com"
archive = f"{slug}-examples.zip"
# isbn = ""
# hardcopy = ""
# cover = f"{slug}-cover.png"
timing = False

# Chapters.
chapters = [
    "intro",
    "server",
    "finale",
]

# Appendices.
appendices = [
    "bib",
    "license",
    "conduct",
    "contrib",
    "glossary",
    "colophon",
    "contents",
]

# Files to copy verbatim.
copy = [
    "*.jpg",
    "*.js",
    "*.json",
    "*.out",
    "*.png",
    "*.py",
    "*.sh",
    "*.svg",
    "*.txt",
    "*.yml",
]

# Exclusions (don't process).
exclude = {
    "*.dot",
    "*.xml",
}

# Files known to be unincluded.
unincluded = {
}

# Theme information.
theme = "mccole"
src_dir = "src"
out_dir = "docs"
extension = "/"

# Enable various Markdown extensions.
markdown_settings = {
    "extensions": [
        "markdown.extensions.extra",
        "markdown.extensions.smarty",
        "pymdownx.superfences",
    ]
}

# Show theme.
if __name__ == "__main__":
    print(theme)
