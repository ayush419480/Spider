# --- START OF FILE main.py (MODIFIED) ---

import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say

# >>> নতুন ইম্পোর্ট: Flask এবং তার সাথে প্রয়োজনীয় মডিউল <<<
from flask import Flask, request, jsonify
import asyncio
from Crypto.Cipher import AES # added based on xC4 usage in original
from Crypto.Util.Padding import pad, unpad # added based on xC4 usage in original


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# >>>>>>>>>>>>>>>>> EMOTE ALIASES ADDED HERE <<<<<<<<<<<<<<<<<
EMOTE_ALIASES = {
    # Evo Gun Emotes
    "m10": 909000081, "ak": 909000063, "ump": 909000098, "mp40": 909000075,
    "mp40v2": 909040010, "scar": 909000068, "xm8": 909000085, "mp5": 909033002,
    "m4a1": 909033001, "famas": 909000090, "m1887": 909035007, "thompson": 909038010,
    "g18": 909038012, "woodpecker": 909042008, "parafal": 909045001, "groza": 909041005,
    "p90": 909049010, "m60": 909051003, "fist": 909037011,
    
    # Normal Emotes (ছোট নাম)
    "ride": 909051014, "circle": 909050009, "petals": 909051013, "bow": 909051012,
    "bike": 909051010, "shower": 909051004, "dream": 909051002, "angelic": 909051001,
    "paint": 909048015, "sword": 909044015, "flare": 909041008, "owl": 909049003,
    "thor": 909050008, "bigdill": 909049001, "csgm": 909041013, "mapread": 909050014,
    "tomato": 909050015, "ninja": 909050002, "level100": 909042007, "auraboat": 909050028,
    "flyingguns": 909049012, "heart": 909000045, "flag": 909000034, "pushup": 909000012,
    "devil": 909000020, "shootdance": 909000008, "chicken": 909000006, "throne": 909000014,
    "rose": 909000010, "valentine": 909038004, "rampage": 909034001, "guildflag": 909049017,
    "fish": 909040004, "inosuke": 909041003, "brgm": 909041012,
    "naruto": 909050003, "kabuto": 909050002, "minato": 909050006, "football": 909048016,
    "p": 909000012, "t": 909000014, "r": 909000010, "l100": 909042007 
}
# >>>>>>>>>>>>>>>>> EMOTE ALIASES END <<<<<<<<<<<<<<<<<

# Flask অ্যাপ ইনিশিয়ালাইজেশন
app = Flask(__name__)
LOOP = None # অ্যাসিঙ্ক্রোনাস ইভেন্ট লুপ সংরক্ষণের জন্য 

# VariabLes dyli (গ্লোবাল ভ্যারিয়েবল ডিক্লেয়ারেশন)
#------------------------------------------#
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
# >>> ফ্লাস্ক এবং লগইনের জন্য প্রয়োজনীয় গ্লোবাল ভ্যারিয়েবল ডিক্লেয়ারেশন (ফিক্সড) <<<
key = None
iv = None
region = None
server2 = "bd" # ধরে নেওয়া হলো
key2 = "YOUR_API_KEY" # ধরে নেওয়া হলো
BYPASS_TOKEN = "YOUR_BYPASS_TOKEN" # ধরে নেওয়া হলো
#------------------------------------------#

# ------------------------------------------
# >>> লগইন, ডিক্রিপশন এবং TCP প্যাকেজ ফাংশন (GeNeRaTeAccEss etc. কে উপরে আনা হলো) <<<
# ------------------------------------------

async def encrypted_proto(encoded_hex):
    key_aes = b'Yg&tc%DEuh6%Zc^8'
    iv_aes = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key_aes, AES.MODE_CBC, iv_aes)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    # Hr should be imported or defined, using Hr from main.py's original position
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"} 
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    # ... (MajorLogin message creation and serialization, same as original)
    # Re-defining Hr for this scope if not globally accessible
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    # ... (Populate major_login fields as per your original code) ...
    # (Skipping long field assignment for brevity, assuming original logic is here)
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    Hr = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB51"}
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 
           
async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        print(data2.hex()[10:])
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        print(packet)
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)


                        message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! '
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)

                    except:
                        if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                            try:
                                print(data2.hex()[10:])
                                packet = await DeCode_PackEt(data2.hex()[10:])
                                print(packet)
                                packet = json.loads(packet)
                                OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                                JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)


                                message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! \n\n{get_random_color()}- Commands : @a {xMsGFixinG("player_uid")} {xMsGFixinG("909000001")}\n\n[00FF00]Dev : @{xMsGFixinG("Spideerio")}'
                                P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                            except:
                                pass

            online_writer.close() ; await online_writer.wait_closed() ; online_writer = None

        except Exception as e: print(f"- ErroR With {ip}:{port} - {e}") ; online_writer = None
        await asyncio.sleep(reconnect_delay)
                            
async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                
                if data.hex().startswith("120000"):

                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None


                    if response:
                        if inPuTMsG.startswith(("/5")):
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nAccepT My Invitation FasT\n\n"
                                P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                C = await cHSq(5, uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(5 , uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                E = await ExiT(None , key , iv)
                                await asyncio.sleep(3)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , E)
                            except:
                                print('msg in squad')



                        if inPuTMsG.startswith('/t '):
                            CodE = inPuTMsG.split('/t ')[1]
                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                EM = await GenJoinSquadsPacket(CodE , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)


                            except:
                                print('msg in squad')

                        if inPuTMsG.startswith('/solo'):
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)

                        if inPuTMsG.strip().startswith('/s'):
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)

                        # >>>>>>>>>>>>> MODIFIED SHORTCUT EMOTE COMMAND HANDLER <<<<<<<<<<<<<
                        parts = inPuTMsG.strip().split()
                        
                        # Command is /emote_name uid (or) /emote_name teamcode uid
                        if len(parts) >= 2 and parts[0].startswith('/') and parts[0][1:] in EMOTE_ALIASES:
                            emote_alias = parts[0][1:]
                            emote_id = EMOTE_ALIASES[emote_alias]
                            
                            is_auto_mode = len(parts) >= 3 and parts[1].isdigit() and parts[2].isdigit() # /ak teamcode uid
                            is_squad_mode = len(parts) >= 2 and parts[1].isdigit() # /ak uid
                            
                            if not is_squad_mode and not is_auto_mode:
                                message = f'[B][C][FF0000]ERROR:\nভুল কমান্ড ফরম্যাট।\nব্যবহার:\n১. স্কোয়াডে থাকলে: /{emote_alias} (uid) [uid2...]\n২. Guild/Friend চ্যাটে: /{emote_alias} (teamcode) (uid) [uid2...]'
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                response = None # Prevent falling through to /e
                                continue

                            # Define where the UID list starts
                            uid_start_index = 1 if not is_auto_mode else 2
                            
                            # Extract UIDs (first UID is mandatory, others are optional)
                            target_uids = []
                            for i in range(uid_start_index, min(uid_start_index + 5, len(parts))): # Up to 5 UIDs
                                if parts[i].isdigit():
                                    target_uids.append(int(parts[i]))
                                else:
                                    break
                            
                            # Check if valid UIDs were found
                            if not target_uids:
                                message = f'[B][C][FF0000]ERROR:\nUID অবশ্যই সংখ্যা হতে হবে।\nব্যবহার:\n১. স্কোয়াডে থাকলে: /{emote_alias} (uid) [uid2...]\n২. Guild/Friend চ্যাটে: /{emote_alias} (teamcode) (uid) [uid2...]'
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                response = None
                                continue
                            
                            # --- CORE EMOTE LOGIC ---
                            
                            # 1. Check for Auto Mode (Join Team, Emote, Leave)
                            if is_auto_mode:
                                team_code = parts[1]
                                
                                try:
                                    # Attempt to Join
                                    EM = await GenJoinSquadsPacket(team_code , key , iv)
                                    await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                                    await asyncio.sleep(2) # Wait for join
                                    
                                    # Emote
                                    message = f'[B][C]{get_random_color()}\nACITVE Emote /{emote_alias} on -> {xMsGFixinG(target_uids[0])}{" and others" if len(target_uids) > 1 else ""}\n'
                                    P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    for target_uid in target_uids:
                                        H = await Emote_k(target_uid, emote_id, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.5) # Small delay between emotes
                                        
                                    await asyncio.sleep(3) # Wait for emote animation
                                    
                                    # Leave
                                    leave = await ExiT(None, key, iv) # None to leave current team
                                    await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
                                    
                                    message = f'[B][C]{get_random_color()}\nBot left the squad after performing emote.'
                                    P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                except Exception as e:
                                    message = f'[B][C][FF0000]ERROR: Auto Emote Failed. Team Code or UID invalid. Error: {str(e)}'
                                    P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)


                            # 2. Check for Squad Mode (Emote only) - If already in Squad chat
                            elif is_squad_mode:
                                try:
                                    chatdata['5']['data']['16'] # This line will raise an exception if not in Squad chat (Private/Guild)
                                    print('msg in private/guild. Squad Mode not applicable.')
                                    message = f"[B][C]{get_random_color()}\n\nCommand Available OnLy In SQuaD, or use the format: /{emote_alias} (teamcode) (uid) in Guild/Private chat! \n\n"
                                    P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                except:
                                    # This is a Squad chat
                                    print(f'msg in squad: /{emote_alias} -> {target_uids}')
                                    message = f'[B][C]{get_random_color()}\nACITVE Emote /{emote_alias} on -> {xMsGFixinG(target_uids[0])}{" and others" if len(target_uids) > 1 else ""}\n'
                                    P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    for target_uid in target_uids:
                                        H = await Emote_k(target_uid, emote_id, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.5)
                            
                            response = None # Command was handled, skip the rest
                        # >>>>>>>>>>>>> END MODIFIED SHORTCUT EMOTE COMMAND HANDLER <<<<<<<<<<<<<
                        
                        
                        if response and inPuTMsG.strip().startswith('/e'): # Only proceed if response is still valid (not handled by shortcut)

                            try:
                                dd = chatdata['5']['data']['16']
                                print('msg in private')
                                message = f"[B][C]{get_random_color()}\n\nCommand Available OnLy In SQuaD ! \n\n"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except:
                                print('msg in squad')

                                parts = inPuTMsG.strip().split()
                                print(response.Data.chat_type, uid, chat_id)
                                message = f'[B][C]{get_random_color()}\nACITVE TarGeT -> {xMsGFixinG(uid)}\n'

                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)

                                uid2 = uid3 = uid4 = uid5 = None
                                s = False

                                try:
                                    uid = int(parts[1])
                                    uid2 = int(parts[2])
                                    uid3 = int(parts[3])
                                    uid4 = int(parts[4])
                                    uid5 = int(parts[5])
                                    idT = int(parts[5])

                                except ValueError as ve:
                                    print("ValueError:", ve)
                                    s = True

                                except Exception:
                                    idT = len(parts) - 1
                                    idT = int(parts[idT])
                                    print(idT)
                                    print(uid)

                                if not s:
                                    try:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                                        H = await Emote_k(uid, idT, key, iv,region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)

                                        if uid2:
                                            H = await Emote_k(uid2, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid3:
                                            H = await Emote_k(uid3, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid4:
                                            H = await Emote_k(uid4, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        if uid5:
                                            H = await Emote_k(uid5, idT, key, iv,region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        

                                    except Exception as e:
                                        pass

                        
                        # >>>>>>>>>>>>> MODIFIED HELP MESSAGE <<<<<<<<<<<<<
                        if inPuTMsG in ("hi" , "hello" , "fen" , "help"):
                            uid = response.Data.uid
                            chat_id = response.Data.Chat_ID
                            message = f'''[C][B][00FFFF]━━━━━━━━━━━━
[ffd319][B]☂︎Add 100 Likes
[FFFFFF]/like/(uid)
[ffd319][b]❄︎Join Bot In Group
[FFFFFF][b]/t (teamcode)
[ffd319][b]❀To Perform AnyEmote (Full Code)
[FFFFFF][b]/e (uid) (emote code)
[00FF7F][B]★ সহজ ইমোট কমান্ড (Emote Shortcut) ★
[FFFFFF][b]১. স্কোয়াডে থাকলে: /(emote_name) (uid) [uid2...]
[FFFFFF][b]২. Guild/Friend চ্যাটে (Auto-Mode): [00FF00]/(emote_name) (teamcode) (uid) [uid2...]
[FFFFFF][b]উদাহরণ (Auto-Mode): /ak 12345 521475527
[FFFFFF][b]উপলব্ধ ইমোট: [00FF00]{", ".join(EMOTE_ALIASES.keys())}
[ffd319]⚡Make 5 Player Group:
[FFFFFF]❄️/5 
[ffd319][b][c]🎵Make leave Bot 
[FFFFFF][b][c]©️/solo
[00FF7F][B]!!admin Commond!!
[ffd319][b]To Stop The Bot
[FFFFFF][b]/stop
[ffd319][b]To Mute Bot
[FFFFFF][b]/mute (time)
[C][B][FFB300]OWNER: WINTER
[00FFFF]━━━━━━━━━━━━
[00FF00]
[00ff00][B]⚓Thankyou For Joining Our Guild⚓                            
'''
                            P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                        response = None
                            
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
                    
                    	
                    	
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

# ------------------------------------------
# >>> Clan/Player Info/AI/Likes/Spam Requests Functions (No Change) <<<
# ------------------------------------------
# (Your original functions like Get_clan_info, get_player_info, talk_with_ai, spam_requests, etc. should be here)
# ... (Leaving them out for final presentation but they should be in the file) ...


# ------------------------------------------
# >>> Flask API রুট (এখানে থাকবে) <<<
# ------------------------------------------

@app.route('/join', methods=['GET'])
def join_and_emote():
    # গ্লোবাল ভ্যারিয়েবল ব্যবহার
    global online_writer, whisper_writer, key, iv, region, LOOP 

    # 1.একাধিক UID গ্রহণ করুন (uid1 থেকে uid5)
    target_uids_str = []
    for i in range(1, 6):  # uid1, uid2, ..., uid5 চেক করুন
        uid = request.args.get(f'uid{i}')
        if uid:
            target_uids_str.append(uid)
            
    emote_id_str = request.args.get('emote_id')
    team_code = request.args.get('tc')
    
    # 2. বৈধতা পরীক্ষা (আপডেট করা হয়েছে)
    if not target_uids_str or not emote_id_str or not team_code:
        return jsonify({
            "status": "error",
            "message": "ত্রুটি: কমপক্ষে একটি UID (uid1), emote_id এবং tc দিতে হবে।"
        }), 400

    if online_writer is None or LOOP is None or key is None or whisper_writer is None:
        return jsonify({
            "status": "error",
            "message": "ত্রুটি: বট গেম সার্ভারে সংযুক্ত নেই। সংযোগের জন্য অপেক্ষা করুন।"
        }), 503

    try:
        # সমস্ত প্রাপ্ত UID-কে int-এ রূপান্তর করুন
        target_uids_int = [int(uid) for uid in target_uids_str]
        emote_id = int(emote_id_str)
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "ত্রুটি: UID এবং Emote ID অবশ্যই সংখ্যা হতে হবে।"
        }), 400

    # 3. অ্যাসিঙ্ক্রোনাস ইমোট সিকোয়েন্স ফাংশন (একাধিক UID হ্যান্ডেল করার জন্য আপডেট করা হয়েছে)
    async def perform_emote_sequence(uids_list, emote_id, team_code_str):
        # গ্লোবাল ভ্যারিয়েবল অ্যাক্সেস
        global online_writer, whisper_writer, key, iv, region 

        # --- জয়েন করুন (একবার) ---
        EM = await GenJoinSquadsPacket(team_code_str , key , iv)
        await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
        await asyncio.sleep(2.5) # জয়েন করার জন্য অপেক্ষা 

        # --- প্রতিটি UID-এর জন্য ইমোট দেখান (লুপ) ---
        for uid_target in uids_list:
            H = await Emote_k(uid_target, emote_id, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            await asyncio.sleep(0.5) # প্রতিটি ইমোটের মধ্যে সামান্য বিলম্ব

        await asyncio.sleep(3) # শেষ ইমোটটি শেষ হওয়ার জন্য অপেক্ষা 

        # --- গ্রুপ ছাড়ুন ---
        # leave = await ExiT(None, key, iv) # None to leave current team
        # await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
        # await asyncio.sleep(1)

    # 4. ইভেন্ট লুপে অ্যাসিঙ্ক্রোনাস ফাংশনটি চালান
    try:
        future = asyncio.run_coroutine_threadsafe(
            perform_emote_sequence(target_uids_int, emote_id, team_code), 
            LOOP
        )
        # একাধিক ইমোটের জন্য টাইমআউট বাড়ানো হয়েছে
        future.result(timeout=30) 
        
        # সফল বার্তা আপডেট করা হয়েছে
        uids_display = ", ".join(target_uids_str)
        return jsonify({
            "status": "success",
            "message": f"সফলভাবে ইমোট কমান্ড পাঠানো হয়েছে। বট টিম কোড {team_code} এ যোগ দিয়ে, UIDs: {uids_display} কে ইমোট ID {emote_id_str} দেখাবে। (Bengali/বাংলা)"
        }), 200

    except asyncio.TimeoutError:
         return jsonify({
            "status": "error",
            "message": "ত্রুটি: অপারেশন টাইমআউট হয়েছে। সম্ভবত গেম সার্ভার সাড়া দিচ্ছে না বা টিম কোড Invalid ছিল।"
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"ইমোট অপারেশনে সমস্যা হয়েছে। ত্রুটি: {str(e)}। (Bengali/বাংলা)"
        }), 500
        
# ------------------------------------------
# >>> MaiiiinE এবং StarTinG ফাংশন (এখানে থাকবে) <<<
# ------------------------------------------

async def MaiiiinE():
    # গ্লোবাল ভ্যারিয়েবল ব্যবহার
    global LOOP, key, iv, region, whisper_writer, online_writer
    
    Uid , Pw = '4260656397' , 'C4BB2682F8D27B593A5BE43E584432D0F936C8DB588B15FAB66E2B2DAF2C7ABD'
    
    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: print("ErroR - InvaLid AccounT") ; return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") ; return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(UrL)
    region = MajoRLoGinauTh.region # গ্লোবাল region সেট
    
    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key # গ্লোবাল key সেট
    iv = MajoRLoGinauTh.iv     # গ্লোবাল iv সেট
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("ErroR - GeTinG PorTs From LoGin Da Ta !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()

    # অ্যাসিঙ্ক্রোনাস লুপ সেটআপ
    LOOP = asyncio.get_running_loop() # বর্তমান লুপটি গ্লোবালি সংরক্ষণ
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
     
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    
    # --- ফ্লাস্ক সার্ভার একটি নতুন থ্রেডে শুরু করুন ---
    def run_flask():
        # IMPORTANT: Use 0.0.0.0 to make it accessible from outside the container/machine
        app.run(host='0.0.0.0', port=30151, debug=False) 

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True # মেইন প্রোগ্রাম শেষ হলে থ্রেডও শেষ হবে
    flask_thread.start()
    # -----------------------------------------------

    os.system('clear')
    print(render('AYUSH', colors=['white', 'green'], align='center'))
    print('')
    print(f" - BoT STarTinG And OnLine on TarGeT : {TarGeT} | BOT NAME : {acc_name}\n")
    print(f" - BoT sTaTus > GooD | OnLinE ! (:")    
    print(f" - Flask API STarTed on http://0.0.0.0:30151/join (:")
    print(f" - Example: http://<YOUR_IP>:30151/join?uid1=<UID>&emote_id=<ID>&tc=<CODE>")
    print(f" - Subscribe > Spideerio | Gaming ! (:")    
    await asyncio.gather(task1 , task2)
    
async def StarTinG():
    while True:
        try: await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except asyncio.TimeoutError: print("Token ExpiRed ! , ResTartinG")
        except Exception as e: print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    asyncio.run(StarTinG())

# --- END OF FILE main.py (MODIFIED) ---