import html
import re
from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyfonts import load_font


# Function to remove text enclosed in different types of brackets
def remove_brackets(text):
    def remove_context(text, start, end):
        depth = 0
        result = ""
        for char in text:
            if char == start:
                depth += 1
            elif char == end:
                depth = max(0, depth - 1)
            elif depth == 0:
                result += char
        return result

    for brackets in ["()", "[]", "{}", "<>"]:
        text = remove_context(text, brackets[0], brackets[1])
    return text


# Function to collapse text at the first "/" and strip whitespace
def collapse(text):
    idx = text.find("/")
    return text[:idx].strip() if idx != -1 else text


# Function to check if text is valid (matches lowercase alphanumeric pattern)
def is_valid(text):
    return bool(re.fullmatch(r"[a-z]\w*", text))


# Function to clean a DataFrame
def clean_df(df):
    df = df.map(remove_brackets).map(collapse).map(lambda x: x.strip().lower())
    df = df[df.map(is_valid).all(axis=1)].drop_duplicates().reset_index(drop=True)
    return df


# Read and process the input file
with open("dict.cc.tsv", encoding="utf-8") as f:
    text = html.unescape(f.read())
    lines = [line for line in text.split("\n") if not line.startswith("#") and line]
    csv = "\n".join(lines)

# Load data into a DataFrame and clean it
columns = {0: "German", 1: "English"}
df = pd.read_csv(StringIO(csv), sep="\t", header=None, usecols=columns.keys())
df = df.rename(columns=columns).dropna()
df = clean_df(df)

# Create a heatmap DataFrame
heatmap = pd.crosstab(df["German"].str[0], df["English"].str[0])

# Plot configuration
plt.style.use("dark mode.mplstyle")
font = load_font(
    "https://github.com/googlefonts/lexend/blob/main/fonts/lexend/variable/Lexend%5BHEXP%2Cwght%5D.ttf?raw=true"
)

# Create and customize the plot
fig = plt.figure(figsize=(10, 10), dpi=300)
ax = fig.add_axes([0.15, 0.15, 0.7, 0.7])
im = ax.imshow(heatmap, cmap="magma")

# Set axis ticks and labels
ax.set_xticks(np.arange(heatmap.shape[0]))
ax.set_yticks(np.arange(heatmap.shape[0]))
ax.set_xticklabels(heatmap.index, font=font, ha="center")
ax.set_yticklabels(heatmap.index, font=font, ha="center", rotation=270)

# Customize tick parameters and labels
ax.tick_params(axis="both", pad=20, labelsize=20)
ax.set_xlabel("English", font=font, size=30, labelpad=30, ha="center", va="center")
ax.set_ylabel(
    "German", font=font, size=30, labelpad=30, rotation=270, ha="center", va="center"
)
ax.set_title(
    "The First Letter Of English And German Words", font=font, fontsize=30, pad=30
)

# Save and display the image
plt.savefig("first letter.png")
