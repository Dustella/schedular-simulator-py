proceses = [

    {
        "name": "P1",
        "PID": 1,
        "commands": [
            {
                "actions": "malloc",
                "size": 4,
                "target": 1
            },
            {
                "actions": "visit",
                "target": 1
            },
            {
                "actions": "malloc",
                "size": 4,
                "target": 9
            },
            {
                "actions": "free",
                "target": 9,
                "size": 4
            },
            {
                "actions": "malloc",
                "size": 4,
                "target": 18
            },
            {
                "actions": "free",
                "target": 1,
                "size": 4
            },
            {
                "actions": "free",
                "target": 18, "size": 4
            }
        ]
    },
    {
        "name": "P11",
        "PID": 11,
        "commands": [
            {
                "actions": "malloc",
                "size": 4,
                "target": 1
            },
            {
                "actions": "visit",
                "target": 1
            },
            {
                "actions": "malloc",
                "size": 14,
                "target": 9
            },
            {
                "actions": "malloc",
                "size": 4,
                "target": 18
            },
            {
                "actions": "free",
                "target": 1,
                "size": 4
            },
            {
                "actions": "free",
                "target": 9,
                "size": 14
            },
            {
                "actions": "free",
                "target": 18, "size": 4
            }
        ]
    },
    {
        "name": "MenTest",
        "PID": 0,
        "commands": [
            {
                "actions": "read_file",
                "target": "file_test_1"
            },
            {
                "actions": "write_file",
                "target": "file_test_1"
            },
            {
                "actions": "malloc",
                "size": 4,
                "target": 20
            },
            # visit 20
            {
                "actions": "visit",
                "target": 20
            },
            {
                "actions": "read_file",
                "target": "file_test_4"
            },
            {
                "actions": "free",
                "target": 20,
                "size": 4
            },
            {
                "actions": "write_file",
                "target": "file_test_4"
            }
        ]


    },
    {
        "name": "P3",
        "PID": 3,
        "commands": [
            {
                "actions": "use_device",
                "target": "device_1"
            },
            {
                "actions": "malloc",
                "size": 4,
                "target": 9
            },
            {
                "actions": "free",
                "target": 9,
                "size": 4
            },
            {
                "actions": "malloc",
                "size": 4,
                "target": 18
            },
            {
                "actions": "release_device",
                "target": "device_1"
            },
            {
                "actions": "free",
                "target": 18,
                "size": 4
            },

        ]
    },
    {
        "name": "P4",
        "PID": 4,
        "commands": [
            {
                "actions": "create_thread",
                "target": "thread_1"
            },
            {
                "actions": "destroy_thread",
                "target": "thread_1",
            },
        ]
    }
]


def get_all_devices():
    devices = set()
    for process in proceses:
        for command in process['commands']:
            if command['actions'] == 'use_device' or command['actions'] == 'release_device':
                devices.add(command['target'])
    return devices


def get_all_files():
    files = set()
    for process in proceses:
        for command in process['commands']:
            if "actions" not in command:
                continue
            if command['actions'] == 'read_file' or command['actions'] == 'write_file':
                files.add(command['target'])
    return files
