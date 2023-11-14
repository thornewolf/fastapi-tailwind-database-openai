import glob
import pathlib

import commonmark
import jinja2


def annotate_classes_on_html(html_string):
    # Parse the HTML string

    if False:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_string, "html.parser")
        return str(soup)

    # Find all <h1> elements and add the 'bold' class to them
    # h1_elements = soup.find_all("h1")
    # for h1 in h1_elements:
    #     h1["class"] = "text-3xl font-bold leading-tight text-gray-900"

    # # Find all <h2> elements and add the 'bold' class to them
    # h2_elements = soup.find_all("h2")
    # for h2 in h2_elements:
    #     h2["class"] = "text-2xl font-bold leading-tight text-gray-900"

    # # Find all <p> elements and add the 'mt-4 text-gray-700' class to them
    # p_elements = soup.find_all("p")
    # for p in p_elements:
    #     p["class"] = "mt-4 text-gray-700"

    # Return the modified HTML
    return html_string


def main():
    # get all markdown files in app/data/blog
    markdown_files = glob.glob("app/data/blog/*.md")
    print("Publishing markdown files:")
    print(markdown_files)

    for path in markdown_files:
        # Read Markdown file and convert to HTML
        with open(path, "r", encoding="utf-8") as md_file:
            markdown_text = md_file.read()
            html_string = commonmark.commonmark(markdown_text)

        # get the filename without the extension
        file_name = pathlib.Path(path).stem
        jenv = jinja2.Environment(loader=jinja2.FileSystemLoader("app/templates"))

        # Add 'bold' class to all <h1> elements
        modified_html = annotate_classes_on_html(html_string)

        modified_html = (
            """{% extends 'base.jinja' %}
    {% block body %}
    <section class="min-h-screen pb-4">
    <article class="prose max-w-5xl md:mt-8 lg:prose-lg mx-auto bg-white rounded-lg p-16">"""
            f"{ modified_html }"
            """</article>
    </section>
    {% endblock %}
    """
        )

        # Save the modified HTML to a new file or print it
        with open(
            f"app/templates/blog/generated/{file_name}.jinja", "w", encoding="utf-8"
        ) as html_file:
            html_file.write(modified_html)

    print("Done!")


if __name__ == "__main__":
    main()
