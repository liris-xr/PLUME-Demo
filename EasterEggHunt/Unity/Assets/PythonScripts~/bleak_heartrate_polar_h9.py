from pylsl import StreamInfo, StreamOutlet, cf_float32

import asyncio
import bitstruct
import struct

from bleak import BleakClient
from bleak.uuids import uuid16_dict

sampling_rate = 200 # Hz

uuid16_dict = {v: k for k, v in uuid16_dict.items()}

ADDRESS = "E9:BD:6C:76:70:21"
## UUID for model number ##
MODEL_NBR_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(uuid16_dict.get("Model Number String"))
## UUID for manufacturer name ##
MANUFACTURER_NAME_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(uuid16_dict.get("Manufacturer Name String"))
## UUID for battery level ##
BATTERY_LEVEL_UUID = "0000{0:x}-0000-1000-8000-00805f9b34fb".format(uuid16_dict.get("Battery Level"))
HR_MEAS = "00002A37-0000-1000-8000-00805F9B34FB"

def create_lsl_stream_outlet(stream_name: str):
    info = StreamInfo(name=stream_name, type='HR', channel_count=1, nominal_srate=sampling_rate, channel_format=cf_float32, source_id=ADDRESS)
    info.desc().append_child_value("manufacturer", "Polar")
    return StreamOutlet(info)

def on_receive_data_callback(lsl_stream_outlet: StreamOutlet, hr_val: int):
    lsl_stream_outlet.push_sample([hr_val])
    print(f"HR Value: {hr_val}")

async def run(address, lsl_stream_outlet: StreamOutlet):

    async with BleakClient(address) as client:

        connected = await client.is_connected()
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        manufacturer_name = await client.read_gatt_char(MANUFACTURER_NAME_UUID)
        battery_level = await client.read_gatt_char(BATTERY_LEVEL_UUID)
        
        print("Connected: {0}".format(connected))
        print("Model Number: {0}".format("".join(map(chr, model_number))), flush=True)
        print("Manufacturer Name: {0}".format("".join(map(chr, manufacturer_name))), flush=True)
        print("Battery Level: {0}%".format(int(battery_level[0])), flush=True)
        
        def hr_val_handler(sender, data):
            """Simple notification handler for Heart Rate Measurement."""
            (hr_fmt, _, _, _, _) = bitstruct.unpack("b1b1b1b1b1<", data)

            if hr_fmt:
                hr_val, = struct.unpack_from("<H", data, 1)
            else:
                hr_val, = struct.unpack_from("<B", data, 1)
            on_receive_data_callback(lsl_stream_outlet, hr_val)

        await client.start_notify(HR_MEAS, hr_val_handler)

        while await client.is_connected():
            await asyncio.sleep(1.0 / sampling_rate)

if __name__ == "__main__":
    address = (ADDRESS)
    loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    lsl_stream_outlet = create_lsl_stream_outlet("Polar H9")
    loop.run_until_complete(run(address, lsl_stream_outlet))

