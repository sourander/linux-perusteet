import re

from pathlib import Path
from typing import Generator
from dataclasses import dataclass
from textwrap import dedent

PATH_TO_SEARCH = Path("docs")
EXERCISE_INDEX_DST = Path("docs/exercises.md")

@dataclass
class MarkdownWithExercises:
    priority: int
    heading: str
    exercises: list[str]

def extract_md_exercises(file: Path) -> MarkdownWithExercises | None:

    def extract_priority(content: str) -> int:
        priority = re.search(r"priority: (\d+)", content)
        return int(priority.group(1)) if priority else 999

    def extract_heading(content: str) -> str:
        headings = re.search(r"^# (.+)", content, re.MULTILINE)
        return headings.group(1) if headings else "No heading found"

    def extract_exercises(content: str) -> list[str]:
        pattern = r'^!!! question\s*"(.*Tehtävä.*)"\s*'
        exercises = re.findall(pattern, content, flags=re.IGNORECASE | re.MULTILINE)
        return exercises

    
    content = file.read_text()
    priority = extract_priority(content)
    heading = extract_heading(content)
    exercises = extract_exercises(content)
    
    return MarkdownWithExercises(priority, heading, exercises) if exercises else None

def get_markdows_by_priority(directory: Path) -> list[MarkdownWithExercises]:
    mds_with_exercises = []

    for file in directory.glob("**/*.md"):
        md_with_exercises = extract_md_exercises(file)
        if md_with_exercises:
            mds_with_exercises.append(md_with_exercises)

    return sorted(mds_with_exercises, key=lambda x: x.priority)

def create_content(directory: Path) -> str:
    """Create the docs/exercises.md file based on MarkdownWithExercises objects."""
    
    file_prefix = dedent("""
    # Tehtäväkooste
     
    Tässä tiedostossa on listattuna **kaikki** materiaalin tehtävät. Osa niistä ei välttämättä 
    kuulu sinun kurssitoteutukseesi. Huomaa, että tämä tiedosto luodaan automaattisesti parsimalla 
    kaikki repositorion Markdown-tiedostot läpi. Mikäli huomaat puuttuvia tehtäviä, ilmoita opettajalle.
    Otsikon perässä suluissa oleva numero on järjestysprioriteetti: se vaikuttaa vain tämän listan järjestykseen.
                         
    Lista hyödyntää Material for MkDocs -teeman [Tasklist](https://squidfunk.github.io/mkdocs-material/reference/lists/#using-task-lists) -ominaisuutta.
                         
    Kopioi tehtävälista leikepöydälle ja muokkaa se sinun käyttöösi sopivaksi.\n\n
    """)
    
    content = ""

    ordered_markdowns = get_markdows_by_priority(directory)

    for md in ordered_markdowns:
        content += f"## {md.heading} ({md.priority})\n\n"
        for task in md.exercises:
            content += f"- [ ] {task}\n"
        content += "\n"

    content_as_code_block = f"""```markdown\n{content}\n```"""

    return file_prefix + content_as_code_block

def write_content(content: str, destination: Path):
    with open(EXERCISE_INDEX_DST, "w") as f:
        f.write(content)

if __name__ == "__main__":
    md_content = create_content(Path(PATH_TO_SEARCH))
    write_content(md_content, destination=EXERCISE_INDEX_DST)
