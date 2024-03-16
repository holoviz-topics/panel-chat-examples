importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

function sendPatch(patch, buffers, msg_id) {
  self.postMessage({
    type: 'patch',
    patch: patch,
    buffers: buffers
  })
}

async function startApplication() {
  console.log("Loading pyodide!");
  self.postMessage({type: 'status', msg: 'Loading pyodide'})
  self.pyodide = await loadPyodide();
  self.pyodide.globals.set("sendPatch", sendPatch);
  console.log("Loaded!");
  await self.pyodide.loadPackage("micropip");
  const env_spec = ['https://cdn.holoviz.org/panel/wheels/bokeh-3.4.0-py3-none-any.whl', 'https://cdn.holoviz.org/panel/1.4.0-rc.2/dist/wheels/panel-1.4.0a3-py3-none-any.whl', 'pyodide-http==0.2.1']
  for (const pkg of env_spec) {
    let pkg_name;
    if (pkg.endsWith('.whl')) {
      pkg_name = pkg.split('/').slice(-1)[0].split('-')[0]
    } else {
      pkg_name = pkg
    }
    self.postMessage({type: 'status', msg: `Installing ${pkg_name}`})
    try {
      await self.pyodide.runPythonAsync(`
        import micropip
        await micropip.install('${pkg}');
      `);
    } catch(e) {
      console.log(e)
      self.postMessage({
	type: 'status',
	msg: `Error while installing ${pkg_name}`
      });
    }
  }
  console.log("Packages loaded!");
  self.postMessage({type: 'status', msg: 'Executing code'})
  const code = `

import asyncio

from panel.io.pyodide import init_doc, write_doc

init_doc()

"""
Demonstrates how to chain responses from a single message in the callback.

Highlight:

- The \`respond\` parameter in the \`send\` method is used to chain responses.
- It's also possible to use \`respond\` as a method to chain responses.
"""

from asyncio import sleep

import panel as pn

pn.extension()

PERSON_1 = "Happy User"
PERSON_2 = "Excited User"
PERSON_3 = "Passionate User"


async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    await sleep(2)
    if user == "User":
        instance.send(
            f"Hey, {PERSON_2}! Did you hear the user?",
            user=PERSON_1,
            avatar="😊",
            respond=True,  # This is the default, but it's here for clarity
        )
    elif user == PERSON_1:
        user_message = instance.objects[-2]
        user_contents = user_message.object
        yield pn.chat.ChatMessage(
            f'Yeah, they said "{user_contents}"! Did you also hear {PERSON_3}?',
            user=PERSON_2,
            avatar="😄",
        )
        instance.respond()
    elif user == PERSON_2:
        instance.send(
            f"Yup, I heard!",
            user=PERSON_3,
            avatar="😆",
            respond=False,
        )


chat_interface = pn.chat.ChatInterface(
    help_text="Send a message to start the conversation!", callback=callback
)
chat_interface.servable()


await write_doc()
  `

  try {
    const [docs_json, render_items, root_ids] = await self.pyodide.runPythonAsync(code)
    self.postMessage({
      type: 'render',
      docs_json: docs_json,
      render_items: render_items,
      root_ids: root_ids
    })
  } catch(e) {
    const traceback = `${e}`
    const tblines = traceback.split('\n')
    self.postMessage({
      type: 'status',
      msg: tblines[tblines.length-2]
    });
    throw e
  }
}

self.onmessage = async (event) => {
  const msg = event.data
  if (msg.type === 'rendered') {
    self.pyodide.runPythonAsync(`
    from panel.io.state import state
    from panel.io.pyodide import _link_docs_worker

    _link_docs_worker(state.curdoc, sendPatch, setter='js')
    `)
  } else if (msg.type === 'patch') {
    self.pyodide.globals.set('patch', msg.patch)
    self.pyodide.runPythonAsync(`
    from panel.io.pyodide import _convert_json_patch
    state.curdoc.apply_json_patch(_convert_json_patch(patch), setter='js')
    `)
    self.postMessage({type: 'idle'})
  } else if (msg.type === 'location') {
    self.pyodide.globals.set('location', msg.location)
    self.pyodide.runPythonAsync(`
    import json
    from panel.io.state import state
    from panel.util import edit_readonly
    if state.location:
        loc_data = json.loads(location)
        with edit_readonly(state.location):
            state.location.param.update({
                k: v for k, v in loc_data.items() if k in state.location.param
            })
    `)
  }
}

startApplication()
