import webview

# options for CEF, here: https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
from webview.platforms.cef import settings

settings.update({
    'product_version': '1.0.0',
    'app_user_model_id': 'com.stephen.osunrinde.20010266.joint_downloading_system_1_0_0',
    'background_color': 0xFF5220,
    'persist_session_cookies': True,
    'downloads_enabled': True,
    'context_menu': {
        'enabled': True,
        'print': False,
        'devtools': True,
        'navigation': False,
        'view_source': False,
        'external_browser': False,
    },
    'ignore_certificate_errors': True
})


def on_closed():
    print('pywebview window is closed')


def on_closing():
    print('pywebview window is closing')


def on_shown():
    print('pywebview window shown')


def on_loaded():
    print('DOM is ready')

    # unsubscribe event listener
    # webview.windows[0].loaded -= on_loaded
    # webview.windows[0].load_url('https://google.com')


if __name__ == '__main__':
    window = webview.create_window(
        'Joint Downloading System',
        'http://localhost/JDS',
        confirm_close=True,
        frameless=False,
        width=1300,
        height=1000,
        resizable=True,
        min_size=(800, 900),
    )
    webview.start(gui='cef')
