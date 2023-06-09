#### Resources Used
    #### https://youtu.be/LX_DXLlaymg
    #### https://youtu.be/pGOyw_M1mNE
    #### https://youtu.be/Vurdg6yrPL8
    #### ChatGPT API Documentation


import requests
import nbformat
import os

### Set up ChatGPT API + key ###
with open('api_key.txt', 'r') as file:
    API_KEY = file.read().strip()
API_URL = "https://api.openai.com/v1/chat/completions"

### Function to interact with the API ###
def interact_with_api(api_tags):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    ### Body of data sent to api ###
    payload = {
        "messages": [
            ### Designates what the ChatGPT is supposed to act as ###
            {"role": "system", "content": "You are a computer science assistant that generates examples based on tags given to you."},
            ### This is what is sent to the API ###
            {"role": "user", "content": f" {api_tags} "}
        ]
    }
    ### POST method to the api ###
    response = requests.post(API_URL, headers=headers, json=payload)
    ### Gets the first response ###
    return response.json()["choices"][0]["message"]["content"]


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
    ### Loops through _posts dir ###
    for root, dirs, files in os.walk(post_dir):
        for file in files:
            if file.endswith(".md"):
                # Have to figure out a way to exclude all the autogenerated .md files for deployment #
                md_file_path = os.path.join(root, file)

                ### Parse Markdown content ###
                with open(md_file_path, "r") as f:
                    content = f.read()
                tags_start = content.find("api_tags:")
                tags_end = content.find("\n", tags_start)
                ### Extracts the tags from the Markdown file content ###
                    #### +5 == check words/chars after "tags: ""
                    #### checks if there are tags, and if there are it is assigned to the `tags` variable
                    #### if no tags ==> tags = ""
                tags = content[tags_start + 5:tags_end].strip() if tags_start != -1 else ""

                ### Invoke ChatGPT API ###
                api_output = interact_with_api(tags)

                ### Update Markdown or content ###
                updated_content = f"{content}\n\n## ChatGPT API Output\n\n{api_output}"

                ### Save modified file ###
                with open(md_file_path, "w") as f:
                    f.write(updated_content)



def main():
    ### Retrieve relevant .md and .ipynb files ###
    notebook_dir = "_notebooks"
    post_dir = "_posts"

    process_notebooks(notebook_dir)
    process_posts(post_dir)

    print("Program Run Successfully!")

### Runs program ###
if __name__ == "__main__":
    main()
