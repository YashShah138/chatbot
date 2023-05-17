import requests
import nbformat
import os

# Step 2: Set up ChatGPT API
API_KEY = "your_api_key"
API_URL = "https://api.openai.com/v1/chat/completions"

# Step 3: Function to interact with the API
def interact_with_api(tags):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": f"Tags: {tags}"},
            {"role": "user", "content": ""}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Step 4: Retrieve relevant Markdown or Jupyter Notebook files
notebook_dir = "_notebooks"
post_dir = "_posts"

def process_notebooks(notebook_dir):
    for root, dirs, files in os.walk(notebook_dir):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)
                notebook = nbformat.read(notebook_path, as_version=nbformat.NO_CONVERT)

                # Step 5: Parse Markdown or Jupyter Notebook content
                tags = notebook["metadata"].get("tags", [])

                # Step 6: Invoke ChatGPT API
                api_output = interact_with_api(tags)

                # Step 7: Update Markdown or Jupyter Notebook content
                # Modify the notebook as per your requirements
                # For example, append the output as a markdown cell at the end
                new_cell = nbformat.v4.new_markdown_cell(source=api_output)
                notebook["cells"].append(new_cell)

                # Step 8: Save modified file
                nbformat.write(notebook, notebook_path)

def process_posts(post_dir):
    for root, dirs, files in os.walk(post_dir):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)

                # Step 5: Parse Markdown or Jupyter Notebook content
                with open(md_file_path, "r") as f:
                    content = f.read()
                tags_start = content.find("tags:")
                tags_end = content.find("\n", tags_start)
                tags = content[tags_start + 5:tags_end].strip() if tags_start != -1 else ""

                # Step 6: Invoke ChatGPT API
                api_output = interact_with_api(tags)

                # Step 7: Update Markdown or Jupyter Notebook content
                # Modify the content as per your requirements
                # For example, append the output as a new section
                updated_content = f"{content}\n\n## ChatGPT API Output\n\n{api_output}"

                # Step 8: Save modified file
                with open(md_file_path, "w") as f:
                    f.write(updated_content)

def main():
    notebook_dir = "_notebooks"
    post_dir = "_posts"

    process_notebooks(notebook_dir)
    process_posts(post_dir)


if __name__ == "__main__":
    main()
