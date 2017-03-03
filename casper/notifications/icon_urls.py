import flask

ICONS = {
    ('iPhone1,1'): {
        'url': 'images/devices/com.apple.iphone-64.png',
        'url@2x': 'images/devices/com.apple.iphone-128.png'
    },
    ('iPhone1,2', 'iPhone2,1'): {
        'url': 'images/devices/com.apple.iphone-3g-64.png',
        'url@2x': 'images/devices/com.apple.iphone-3g-128.png'
    },
    ('iPhone3,1', 'iPhone3,3', 'iPhone4,1'): {
        'url': 'images/devices/com.apple.iphone-4-white-64.png',
        'url@2x': 'images/devices/com.apple.iphone-4-white-128.png'
    },
    ('iPhone5,1', 'iPhone5,2'): {
        'url': 'images/devices/com.apple.iphone-5-white-64.png',
        'url@2x': 'images/devices/com.apple.iphone-5-white-128.png'
    },
    ('iPhone5,3'): {
        'url': 'images/devices/com.apple.iphone-5c-blue-64.png',
        'url@2x': 'images/devices/com.apple.iphone-5c-blue-128.png'
    },
    ('iPhone6,1'): {
        'url': 'images/devices/com.apple.iphone-5s-white-64.png',
        'url@2x': 'images/devices/com.apple.iphone-5s-white-128.png'
    },
    ('iPhone7,2'): {
        'url': 'images/devices/com.apple.iphone-6-white-64.png',
        'url@2x': 'images/devices/com.apple.iphone-6-white-128.png'
    },
    ('iPhone7,1'): {
        'url': 'images/devices/com.apple.iphone-6-plus-white-64.png',
        'url@2x': 'images/devices/com.apple.iphone-6-plus-white-128.png'
    },
    ('iPhone8,1'): {
        'url': 'images/devices/com.apple.iphone-6s-white-64.png',
        'url@2x': 'images/devices/com.apple.iphone-6s-plus-white-128.png'
    },
    ('iPhone8,2'): {
        'url': 'images/devices/com.apple.iphone-64.png',
        'url@2x': 'images/devices/com.apple.iphone-128.png'
    },

    ('iPad1,1'): {
        'url': 'images/devices/com.apple.ipad-64.png',
        'url@2x': 'images/devices/com.apple.ipad-128.png'
    },
    ('iPad2,1', 'iPad2,2', 'iPad2,3', 'iPad2,4', 'iPad3,1', 'iPad3,2', 'iPad3,3', 'iPad3,4', 'iPad3,5', 'iPad3,6'): {
        'url': 'images/devices/com.apple.ipad-2-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-2-white-128.png'
    },
    ('iPad2,5', 'iPad2,6', 'iPad2,7'): {
        'url': 'images/devices/com.apple.ipad-mini-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-mini-white-128.png'
    },
    ('iPad4,4', 'iPad4,5'): {
        'url': 'images/devices/com.apple.ipad-mini2-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-mini2-white-128.png'
    },
    ('iPad4,7', 'iPad4,8'): {
        'url': 'images/devices/com.apple.ipad-mini3-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-mini3-white-128.png'
    },
    ('iPad5,1', 'iPad5,2'): {
        'url': 'images/devices/com.apple.ipad-mini4-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-mini4-white-128.png'
    },
    ('iPad4,1', 'iPad4,2'): {
        'url': 'images/devices/com.apple.ipad-air-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-air-white-128.png'
    },
    ('iPad5,3', 'iPad5,4'): {
        'url': 'images/devices/com.apple.ipad-air2-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-air2-white-128.png'
    },
    ('iPad6,7', 'iPad6,8'): {
        'url': 'images/devices/com.apple.ipad-pro-white-64.png',
        'url@2x': 'images/devices/com.apple.ipad-pro-white-128.png'
    },

    ('AppleTV2,1', 'AppleTV3,1', 'AppleTV3,2'): {
        'url': 'images/devices/com.apple.apple-tv-64.png',
        'url@2x': 'images/devices/com.apple.apple-tv-128.png'
    },
    ('AppleTV5,3'): {
        'url': 'images/devices/com.apple.apple-tv-4-64.png',
        'url@2x': 'images/devices/com.apple.apple-tv-4-128.png'
    }
}


def icon_url(model):
    for key, value in ICONS.iteritems():
        if model in key:
            return {
                'url': flask.url_for('static', filename=ICONS[key]['url'], _external=True),
                'url@2x': flask.url_for('static', filename=ICONS[key]['url@2x'], _external=True)
            }

    return {
        'url': flask.url_for('static', filename='images/mobiledevices_32.png', _external=True),
        'url@2x': flask.url_for('static', filename='images/mobiledevices_64.png', _external=True)
    }
