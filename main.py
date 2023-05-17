#### Resources Used
    #### https://youtu.be/LX_DXLlaymg
    #### https://youtu.be/pGOyw_M1mNE
    #### https://youtu.be/Vurdg6yrPL8
    #### ChatGPT API Documentation


import requests
import nbformat
import os

### Set up ChatGPT API + key ###
API_KEY = "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"
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
    ### Have to figure out how to add a cell that is .md
    ### Then format the response from API to be in md
    pass


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

### Runs program ###
if __name__ == "__main__":
    main()
