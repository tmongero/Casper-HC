def get_capabilties(server_domain):
    return {
        "name": "Casper",
        "key": "com.jamfit.casper",
        "description": "A friendly HipChat plugin to Jamf Pro that allows a room to search "
                       "inventory and receive notifications from webhook events.",
        "capabilities": {
            "installable": {
                "callbackUrl": "https://{}/hipchat/installable".format(server_domain),
                "allowGlobal": False,
                "allowRoom": True
            },
            "configurable": {
                "url": "https://{}/hipchat/configure".format(server_domain)
            },
            "hipchatApiConsumer": {
                "scopes": [
                    "send_notification"
                ],
                "fromName": "Casper"
            },
            "webhook": [
                {
                    "url": "https://{}/message/help".format(server_domain),
                    "pattern": "^casper\s(?:h|help)(?:\s|$)",
                    "event": "room_message",
                    "authentication": "jwt",
                    "name": "Help"
                },
                {
                    "url": "https://{}/message/version".format(server_domain),
                    "pattern": "^casper\s(?:v|version)(?:\s|$)",
                    "event": "room_message",
                    "authentication": "jwt",
                    "name": "Version"
                },
                {
                    "url": "https://{}/message/computers".format(server_domain),
                    "pattern": "^casper\s(?:c|computers?)(?:\s|$)",
                    "event": "room_message",
                    "authentication": "jwt",
                    "name": "Computers"
                },
                {
                    "url": "https://{}/message/mobiledevices".format(server_domain),
                    "pattern": "^casper\s(?:m|mobiles?)(?:\s|$)",
                    "event": "room_message",
                    "authentication": "jwt",
                    "name": "Mobile Devices"
                },
                {
                    "url": "https://{}/message/users".format(server_domain),
                    "pattern": "^casper\s(?:u|users?)(?:\s|$)",
                    "event": "room_message",
                    "authentication": "jwt",
                    "name": "Users"
                }
            ],
        },
        "links": {
            "self": "https://{}/hipchat/capabilities".format(server_domain)
        }
    }