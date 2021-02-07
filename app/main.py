import webview

# options for CEF, here: https://github.com/cztomczak/cefpython/blob/master/api/ApplicationSettings.md
from webview.platforms.cef import settings
settings.update({
    'product_version': '1.0.0',
    'app_user_model_id': 'com.stephen.osunrinde.20010266.joint_downloading_system_1_0_0',
    'background_color': 0x00,
    'persist_session_cookies': True,
    'downloads_enabled': True,
    'context_menu': {
        'enabled': True,
        'print': True,
        'devtools': False,
        'navigation': False,
        'view_source': False,
        'external_browser': False,
    },
    'ignore_certificate_errors': True
})


if __name__ == '__main__':
    webview.create_window(
        'Joint Downloading System',
        'http://localhost/JDS',
        confirm_close=True,
        frameless=False,
        width=1300,
        height=800,
        resizable=True,
    )
    webview.start(gui='cef')
