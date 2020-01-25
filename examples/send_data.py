#!/usr/bin/env python3

import asyncio
from mavsdk import System
from socketIO_client_nexus import SocketIO, BaseNamespace
from mavsdk import (MissionItem)

import time


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")
    return drone
    # Start the tasks
    # asyncio.ensure_future(print_battery(drone))
    # asyncio.ensure_future(print_gps_info(drone))
    # asyncio.ensure_future(print_in_air(drone))
    # asyncio.ensure_future(print_position(drone))
    # asyncio.ensure_future(send_copter_data(drone))

loop=asyncio.get_event_loop()
    # tasks = print_battery(drone),print_gps_info(drone) 
connect_task=run()
drone=loop.run_until_complete(connect_task)


    
try:
    #socket1 = SocketIO('http://192.168.1.100', 3000, verify=True) #establish socket connection to desired server
    #socket1 = SocketIO('http://drone.nicnepal.org', verify=True) #establish socket connection to desired server
    socket1 = SocketIO('https://nicwebpage.herokuapp.com', verify =True)
    socket = socket1.define(BaseNamespace,'/JT601')
    #socket = socket1.define(BaseNamespace,'/pulchowk')
    #socket.emit("joinPiPulchowk")
    socket.emit("joinPi")
    #socket.emit("usernamePassword",read_username_password())
except Exception as e:
    print('The server is down. Try again later.')





async def send_copter_data(drone):
    print("trying to connecttttttt to socket ")
    data={}
    data['conn']='True'
    print("data",data,socket)
    data["volt"]=5
    #     data['lat']=await position.latitude_deg
    #     data['lng']=await position.longitude_deg
    #     data['alt']=await position.relative_altitude
    # socket.emit('data',data)
    # async for battery in drone.telemetry.battery():
    #     data["volt"]=await battery.remaining_percent
    # async for gps_info in drone.telemetry.gps_info():
    #     data['numSat']=await gps_info.num_satellites
    #     data['fix']=await gps_info.fix_type
    # async for position in drone.telemetry.position():
    #     data['lat']=await position.latitude_deg
    #     data['lng']=await position.longitude_deg
    #     data['alt']=await position.relative_altitude
    # v=  asyncio.ensure_future(print_battery(drone))
    data['volt']=int(v)
    await asyncio.sleep(1)
    socket.emit('data',data)
    print("copter data",data)
    socket1.wait(seconds=0.8) #sends or waits for socket

async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")
        return battery.remaining_percent

async def print_gps_info(drone):
    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS info: {gps_info}") 
        return [gps_info.num_satellites,gps_info.fix_type]

async def print_in_air(drone):
    async for in_air in drone.telemetry.in_air():
        print(f"In air: {in_air}")


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(f"Position:{position}")
        if(position.relative_altitude_m):
            return [position.latitude_deg,position.longitude_deg,position.relative_altitude_m,position.absolute_altitude_m]
        else:
            return 0

async def print_heading(drone):
    async for position in drone.telemetry.attitude_euler():
        print(round(position.yaw_deg))
        return position.yaw_deg

async def print_status(drone):
    async for status in drone.telemetry.status_text():
        print(status)
        return status

async def start_flight(drone):
    mission_items = []
    mission_items.append(MissionItem(47.398039859999997,
                                     8.5455725400000002,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(47.398036222362471,
                                     8.5450146439425509,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))
    mission_items.append(MissionItem(47.397825620791885,
                                     8.5450092830163271,
                                     25,
                                     10,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan')))

    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_items)

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()

    await termination_task


def on_initiate_flight(var):
    print("fly",var)
    asyncio.ensure_future(start_flight(drone))

def set_mode_RTL(var):
    asyncio.ensure_future(rtl(drone))

def set_mode_LAND(var):
    asyncio.ensure_future(land(drone))

async def rtl(drone):
    await drone.action.return_to_launch()

async def land(drone):
    await drone.action.land()

async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current_item_index}/"
              f"{mission_progress.mission_count}")


async def observe_is_in_air(drone):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            await asyncio.get_event_loop().shutdown_asyncgens()
            return


if __name__ == "__main__":
    # Start the main function
    # drone = System()
    # drone.connect(system_address="udp://:14540")
    # time.sleep(80)
    # asyncio.ensure_future(run())


    # asyncio.ensure_future(print_in_air(drone))

    # print(drone)
    # Runs the event loop until the program is canceled with e.g. CTRL-C
    loop2=asyncio.get_event_loop()
    data={}
    data['conn']='True'
    # print("data",data,socket)
    # data["volt"]=5
    error={}
    while True:
        sub_tasks=print_battery(drone),print_gps_info(drone),print_position(drone)#,print_heading(drone)#,print_status(drone)
        # battery,gps_info,position,heading=loop2.run_until_complete(asyncio.gather(*sub_tasks))
        battery,gps_info, position=loop2.run_until_complete(asyncio.gather(*sub_tasks))

        # print(dir(a),b.__dict__)
        data["volt"]=battery
        # print(type(position))
        if isinstance(position,list):
            data['lat']=position[0]
            data['lng']=position[1]
            data['altr']=position[2]
            data['alt']=position[3]
        if isinstance(gps_info,list):
            data['numSat']=gps_info[0]
            data['fix']=str(gps_info[1])
        # data['head']=heading
        socket.emit('data',data)
        print("copter data",data)
        # error={'context':'STATUS','msg':str(status.text)}
        # socket.emit('errors',error)
        socket.on('initiate_flight',on_initiate_flight)#keep listening
        socket.on('RTL',set_mode_RTL)
        socket.on('LAND',set_mode_LAND)
        socket1.wait(seconds=0.5) #sends or waits for socket
        # loop2.close()
        # pass

