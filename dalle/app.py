import os

import gradio as gr
import openai
import dotenv

_ = dotenv.load_dotenv(dotenv.find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


def gen_image(prompt, size="512x512"):
    response = openai.Image.create(prompt=prompt,
                                   n=5,
                                   size=size,
                                   response_format="url")
    images = [item['url'] for item in response.to_dict()["data"]]
    return images


with gr.Blocks() as dalle:
    with gr.Column(variant="panel"):
        with gr.Row(variant="compact"):
            text = gr.Textbox(label="Enter your prompt",
                              show_label=False,
                              max_lines=1,
                              placeholder="Enter your prompt",
                              container=False)
            btn = gr.Button("Generate image")

        gallery = gr.Gallery(label="Generated images",
                             show_label=False,
                             elem_id="gallery",
                             columns=[5],
                             rows=[2],
                             object_fit="contain",
                             height="auto")

    btn.click(gen_image, text, gallery)

if __name__ == '__main__':
    dalle.launch()
