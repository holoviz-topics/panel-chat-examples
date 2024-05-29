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
  \nimport asyncio\n\nfrom panel.io.pyodide import init_doc, write_doc\n\ninit_doc()\n\n"""\nDemonstrates how to create a slim \`ChatInterface\` that fits in the sidebar.\n\nHighlights:\n\n- The \`ChatInterface\` is placed in the sidebar.\n- Set \`show_*\` parameters to \`False\` to hide the respective buttons.\n- Use \`message_params\` to customize the appearance of each chat messages.\n"""\nimport panel as pn\n\npn.extension()\n\n\nasync def callback(contents: str, user: str, instance: pn.chat.ChatInterface):\n    message = f"Echoing {user}: {contents}"\n    return message\n\n\nchat_interface = pn.chat.ChatInterface(\n    callback=callback,\n    show_send=False,\n    show_rerun=False,\n    show_undo=False,\n    show_clear=False,\n    show_avatar=False,\n    show_timestamp=False,\n    show_button_name=False,\n    show_reaction_icons=False,\n    sizing_mode="stretch_width",\n    height=700,\n    message_params={\n        "stylesheets": [\n            """\n            .message {\n                font-size: 1em;\n            }\n            .name {\n                font-size: 0.9em;\n            }\n            .timestamp {\n                font-size: 0.9em;\n            }\n            """\n        ]\n    },\n)\n\nmain = """\nWe've put a *slim* \`ChatInterface\` in the sidebar. In the main area you\ncould add the object you are chatting about\n"""\n\npn.template.FastListTemplate(\n    main=[main],\n    sidebar=[chat_interface],\n    sidebar_width=500,\n).servable()\n\n\nawait write_doc()
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
