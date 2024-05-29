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
  const env_spec = ['https://cdn.holoviz.org/panel/wheels/bokeh-3.4.1-py3-none-any.whl', 'https://cdn.holoviz.org/panel/1.4.2/dist/wheels/panel-1.4.2-py3-none-any.whl', 'pyodide-http==0.2.1']
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
  \nimport asyncio\n\nfrom panel.io.pyodide import init_doc, write_doc\n\ninit_doc()\n\n"""\nDemonstrates how to precisely control the callback response.\n\nHighlights:\n\n- Use a placeholder text to display a message while waiting for the response.\n- Use a placeholder threshold to control when the placeholder text is displayed.\n- Use send instead of stream/yield/return to keep the placeholder text while still sending a message, ensuring respond=False to avoid a recursive loop.\n- Use yield to continuously update the response message.\n- Use pn.chat.ChatMessage or dict to send a message with a custom user and avatar.\n"""\n\nfrom asyncio import sleep\nfrom random import choice\n\nimport panel as pn\n\npn.extension()\n\n\nasync def callback(contents: str, user: str, instance: pn.chat.ChatInterface):\n    await sleep(0.5)\n    # use send instead of stream/yield/return to keep the placeholder text\n    # while still sending a message; ensure respond=False to avoid a recursive loop\n    instance.send(\n        "Let me flip the coin for you...", user="Game Master", avatar="\U0001f3b2", respond=False\n    )\n    await sleep(1)\n\n    characters = "/|\\\\_"\n    index = 0\n    for _ in range(0, 28):\n        index = (index + 1) % len(characters)\n        # use yield to continuously update the response message\n        # use pn.chat.ChatMessage to send a message with a custom user and avatar\n        yield pn.chat.ChatMessage("\\r" + characters[index], user="Coin", avatar="\U0001fa99")\n        await sleep(0.005)\n\n    result = choice(["heads", "tails"])\n    if result in contents.lower():\n        # equivalently, use a dict instead of a pn.chat.ChatMessage\n        yield {"object": f"Woohoo, {result}! You win!", "user": "Coin", "avatar": "\U0001f3b2"}\n    else:\n        yield {"object": f"Aw, got {result}. Try again!", "user": "Coin", "avatar": "\U0001f3b2"}\n\n\nchat_interface = pn.chat.ChatInterface(\n    widgets=[\n        pn.widgets.RadioButtonGroup(\n            options=["Heads!", "Tails!"], button_type="primary", button_style="outline"\n        )\n    ],\n    callback=callback,\n    help_text="Select heads or tails, then click send!",\n    placeholder_text="Waiting for the result...",\n    placeholder_threshold=0.1,\n)\nchat_interface.servable()\n\n\nawait write_doc()
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
