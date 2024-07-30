import panel as pn
from openai import AsyncOpenAI

pn.extension()


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    if api_key_input.value:
        # use api_key_input.value if set, otherwise use OPENAI_API_KEY
        aclient.api_key = api_key_input.value

    response = await aclient.images.generate(
        model=model_buttons.value,
        prompt=contents,
        n=n_images_slider.value,
        size=size_buttons.value,
    )

    image_panes = [
        (str(i), pn.pane.Image(data.url)) for i, data in enumerate(response.data)
    ]
    return pn.Tabs(*image_panes) if len(image_panes) > 1 else image_panes[0][1]


def update_model_params(model):
    if model == "dall-e-2":
        size_buttons.param.update(
            options=["256x256", "512x512", "1024x1024"],
            value="256x256",
        )
        n_images_slider.param.update(
            start=1,
            end=10,
            value=1,
        )
    else:
        size_buttons.param.update(
            options=["1024x1024", "1024x1792", "1792x1024"],
            value="1024x1024",
        )
        n_images_slider.param.update(
            start=1,
            end=1,
            value=1,
        )


aclient = AsyncOpenAI()
api_key_input = pn.widgets.PasswordInput(
    placeholder="sk-... uses $OPENAI_API_KEY if not set",
    sizing_mode="stretch_width",
    styles={"color": "black"},
)
model_buttons = pn.widgets.RadioButtonGroup(
    options=["dall-e-2", "dall-e-3"],
    value="dall-e-2",
    name="Model",
    sizing_mode="stretch_width",
)
size_buttons = pn.widgets.RadioButtonGroup(
    options=["256x256", "512x512", "1024x1024"],
    name="Size",
    sizing_mode="stretch_width",
)
n_images_slider = pn.widgets.IntSlider(
    start=1, end=10, value=1, name="Number of images"
)
pn.bind(update_model_params, model_buttons, watch=True)
chat_interface = pn.chat.ChatInterface(
    callback=callback,
    callback_user="DALL·E",
    help_text="Send a message to get a reply from DALL·E!",
)
template = pn.template.BootstrapTemplate(
    title="OpenAI DALL·E",
    header_background="#212121",
    main=[chat_interface],
    header=[api_key_input],
    sidebar=[model_buttons, size_buttons, n_images_slider],
)
template.servable()
