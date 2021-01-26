import asyncio
import http.server
import json
import os
import socketserver
import threading
import time

import pyautogui
import websockets

PORT = 8000
WS_PORT = 8001

LIVE2D_FULL_PATH = ''
SERVER_ROOT = ''
LIVE2D_MODEL = ''

file_server = None

stop_event = threading.Event()

initialized = False
should_reload_page = False


def update_path(path, level):
    global SERVER_ROOT, LIVE2D_MODEL

    root = path

    while level > 0:
        root = os.path.dirname(root)
        level -= 1

    SERVER_ROOT = root
    LIVE2D_MODEL = path[len(root):]

    if LIVE2D_MODEL.startswith('/'):
        LIVE2D_MODEL = LIVE2D_MODEL[1:]

    # print('update_path ', SERVER_ROOT, '|', LIVE2D_MODEL)


try:
    import obspython as obs
except ModuleNotFoundError:
    with open(os.path.dirname(__file__) + '/private.json', 'r') as p_file:
        p_json = json.load(p_file)
        update_path(p_json['live2dModel'], p_json['rootLevel'])


def script_description():
    return 'Displays a cursor-focusing Live2D model'


def script_load(settings):
    pass


def prop_modified(props, prop, settings):
    # print('prop_modified ', obs.obs_property_name(prop))

    status = 'Invalid Path' if not SERVER_ROOT else 'Invalid Port' if PORT == WS_PORT else 'OK'

    obs.obs_data_set_string(settings, 'info', '''Server Root:
%s

Page URL:
http://127.0.0.1:%d

Status:
%s
''' % (SERVER_ROOT or '<empty>', PORT, status))

    level_p = obs.obs_properties_get(props, 'root_level')

    obs.obs_property_int_set_limits(level_p, 1, total_levels(LIVE2D_FULL_PATH), 1)

    return True


def total_levels(path):
    level = 1

    while 1:
        if os.path.dirname(path) == path:
            return level

        path = os.path.dirname(path)
        level += 1


def script_properties():
    # print('script_properties')

    props = obs.obs_properties_create()

    model_p = obs.obs_properties_add_path(props, 'live2d_model', 'Live2D Model',
                                          obs.OBS_PATH_FILE, 'Live2D Model(*.json)', '')

    level_p = obs.obs_properties_add_int(props, 'root_level', 'Server Root Level', 1, total_levels(LIVE2D_FULL_PATH), 1)

    port_p = obs.obs_properties_add_int(props, 'port', 'Server Port', 1024, 65535, 1)
    ws_port_p = obs.obs_properties_add_int(props, 'ws_port', 'Websocket Port', 1024, 65535, 1)

    info_p = obs.obs_properties_add_text(props, 'info', 'Info', obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_enabled(info_p, False)

    obs.obs_properties_add_button(props, 'start', 'Apply Settings', apply_settings)

    obs.obs_property_set_modified_callback(model_p, prop_modified)
    obs.obs_property_set_modified_callback(level_p, prop_modified)
    obs.obs_property_set_modified_callback(port_p, prop_modified)
    obs.obs_property_set_modified_callback(ws_port_p, prop_modified)

    return props


def script_defaults(settings):
    obs.obs_data_set_default_int(settings, 'root_level', 1)
    obs.obs_data_set_default_int(settings, 'port', PORT)
    obs.obs_data_set_default_int(settings, 'ws_port', WS_PORT)


def script_update(settings):
    global initialized, PORT, WS_PORT, LIVE2D_FULL_PATH

    # print('script_update')

    PORT = obs.obs_data_get_int(settings, "port")
    WS_PORT = obs.obs_data_get_int(settings, "ws_port")
    LIVE2D_FULL_PATH = obs.obs_data_get_string(settings, "live2d_model")
    level = obs.obs_data_get_int(settings, "root_level")

    update_path(LIVE2D_FULL_PATH, level)

    if not initialized:
        initialized = True
        start_server()


def script_unload():
    shutdown_server()


# Static file server

class RequestHandler(http.server.SimpleHTTPRequestHandler):

    def log_request(self, code='-', size='-'):
        pass

    def log_error(self, _format, *args):
        self.log_message('%s ' + _format, self.path, *args)

    def do_GET(self):
        if self.path == '/setup':
            res_json = json.dumps({
                'model': LIVE2D_MODEL,
                'wsPort': WS_PORT
            }).encode('utf-8')

            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(res_json)))
            self.end_headers()

            self.wfile.write(res_json)
        else:
            super().do_GET()

    def translate_path(self, path):
        if path == '/index.html':
            return os.path.normpath(os.path.dirname(__file__) + '/index.html')

        result = super().translate_path(path)

        rel_path = os.path.relpath(result, os.getcwd())

        return os.path.join(SERVER_ROOT, rel_path)


def run_file_server():
    global file_server

    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        file_server = httpd
        httpd.serve_forever()


# Socket server

def run_ws_server():
    async def ws_handler(websocket, path):
        global should_reload_page

        try:
            if should_reload_page:
                should_reload_page = False
                await websocket.send('reload')

            while 1:
                await asyncio.sleep(0.02)
                await websocket.send(','.join(map(str, pyautogui.position())))
        except websockets.exceptions.ConnectionClosedOK:
            pass

    asyncio.set_event_loop(asyncio.new_event_loop())

    async def run_server(_stop):
        async with websockets.serve(ws_handler, 'localhost', WS_PORT):
            await _stop

    stop = asyncio.get_event_loop().run_in_executor(None, stop_event.wait)

    asyncio.get_event_loop().run_until_complete(run_server(stop))
    asyncio.get_event_loop().run_forever()


def apply_settings(*args):
    global should_reload_page

    should_reload_page = True
    start_server()


def start_server():
    if PORT == WS_PORT:
        print('Tow ports must not be the same (%s)' % PORT)
        return

    shutdown_server()

    time.sleep(0.5)

    server_thread = threading.Thread(target=run_file_server)
    server_thread.setDaemon(True)
    server_thread.start()

    ws_server_thread = threading.Thread(target=run_ws_server)
    ws_server_thread.setDaemon(True)
    ws_server_thread.start()

    print("Serving at port %d and %d" % (PORT, WS_PORT))


def shutdown_server():
    if file_server:
        file_server.shutdown()

    stop_event.set()
    stop_event.clear()

    print('Shutdown')


try:
    obs
except NameError:
    start_server()

    while 1:
        pass
