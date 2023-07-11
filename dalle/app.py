import asyncio
import os
from io import BytesIO

import aiohttp
import dotenv
import gradio as gr
import openai
from PIL import Image

_ = dotenv.load_dotenv(dotenv.find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")


async def get_image_async(urls: str) -> list[Image.Image]:
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(session.get(url)))
        responses = await asyncio.gather(*tasks)
        images = [Image.open(BytesIO(await response.read())) for response in responses]
        return images


async def gen_image(prompt: str, size: str, n: int):
    response = openai.Image.create(prompt=prompt,
                                   n=int(n),
                                   size=size,
                                   response_format="url")
    urls = [item['url'] for item in response.get("data")]
    images = await get_image_async(urls)
    return images


with gr.Blocks() as dalle:
    with gr.Column(variant="panel", scale=0):
        with gr.Row(variant="compact", equal_height=False):
            text = gr.Textbox(label="Enter your prompt",
                              placeholder="Enter your prompt",
                              elem_id="text",
                              interactive=True,
                              container=False,
                              scale=3)
            size = gr.Dropdown(label="Image size",
                               container=False,
                               value="512x512",
                               interactive=True,
                               elem_id='size',
                               choices=["256x256", "512x512", "1024x1024"],
                               scale=1)
            num_images = gr.Number(label="Number of images",
                                   container=False,
                                   interactive=True,
                                   elem_id="num_images",
                                   value=5,
                                   scale=1)

        button = gr.Button(value="Generate image",
                           container=False,
                           show_label=True,
                           variant='primary',
                           scale=1)

        gallery = gr.Gallery(label="Generated images",
                             show_label=True,
                             elem_id="gallery",
                             columns=[1],
                             rows=[num_images],
                             object_fit="contain",
                             height="auto")

    button.click(gen_image, inputs=[text, size, num_images], outputs=gallery)

if __name__ == '__main__':
    dalle.launch(server_port=int(os.getenv('PORT', 7860)),
                 server_name='0.0.0.0')
