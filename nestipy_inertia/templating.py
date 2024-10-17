from typing import Any

from markupsafe import Markup
from minijinja import escape, pass_state
from .utils import InertiaContext


class State(object):
    """ A reference to the current state. """

    def lookup(self, *args, **kwargs) -> Any:  # real signature unknown
        """ Looks up a variable in the context """
        pass


@pass_state
def inertia_head(state: State) -> Markup:
    """
    Render the head section for the Inertia.js page.
    """
    inertia: InertiaContext = state.lookup("inertia")
    fragments = []

    if inertia.environment == "development":
        fragments.append(
            f'<script type="module" src="{escape(inertia.dev_url)}/@vite/client"></script>'
        )

    if inertia.is_ssr:
        if inertia.ssr_head is None:
            raise ValueError("SSR is enabled but no SSR head was provided")
        fragments.append(inertia.ssr_head)

    if inertia.css:
        for css_file in inertia.css:
            fragments.append(f'<link rel="stylesheet" href="{escape(css_file)}">')

    return Markup("\n".join(fragments))


@pass_state
def inertia_body(state: State) -> Markup:
    """
    Render the body section for the Inertia.js page.
    """
    inertia: InertiaContext = state.lookup("inertia")
    fragments = []

    if inertia.is_ssr:
        if inertia.ssr_body is None:
            raise ValueError("SSR is enabled but no SSR body was provided")
        fragments.append(inertia.ssr_body)
    else:
        if inertia.data is None:
            raise ValueError("No data was provided for the Inertia page")
        fragments.append(f"<div id=\"app\" data-page='{escape(inertia.data)}'></div>")
    # react refresh
    fragments.append(f'<script type="module" src="{escape(inertia.js)}"></script>')
    return Markup("\n".join(fragments))


@pass_state
def vite_react_refresh(state: State):
    inertia: InertiaContext = state.lookup("inertia")
    return Markup(f"""
            <script type="module">
            import RefreshRuntime from '{inertia.dev_url}/@react-refresh'
            RefreshRuntime.injectIntoGlobalHook(window)
            window.$RefreshReg$ = () => {'{}'}
            window.$RefreshSig$ = () => (type) => type
            window.__vite_plugin_react_preamble_installed__ = true
            </script>
        """)
