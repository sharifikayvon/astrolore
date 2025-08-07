import webview
import threading
import time

url = "https://aladin.u-strasbg.fr/AladinLite/?target=10.68470833%2041.26903611&fov=1.5&survey=P%2FDSS2%2Fcolor"

def scale_page(window):
    # wait for page to load (adjust time as needed)
    time.sleep(2)
    # inject JS to scale page
    js_code = """
    document.body.style.zoom = '80%';
    """
    window.evaluate_js(js_code)

window = webview.create_window("Aladin Viewer", url, width=600, height=400)

# run JS injection in a separate thread after window creation
#threading.Thread(target=scale_page, args=(window,), daemon=True).start()

webview.start()
