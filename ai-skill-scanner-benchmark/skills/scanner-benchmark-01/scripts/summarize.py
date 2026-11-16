"""Summarize text using a transformers pipeline."""
import sys

from jinja2 import Template
from transformers import pipeline


def main() -> None:
    text = " ".join(sys.argv[1:]) or "Hello world"
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(text, max_length=40, min_length=5)[0]["summary_text"]
    print(Template("Summary: {{ s }}").render(s=summary))


if __name__ == "__main__":
    main()
