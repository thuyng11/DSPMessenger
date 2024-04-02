
# ICS 32 Distributed Social Messenger (DSM)

## Overview

ICS 32 DSM is a GUI-based application enabling ICS 32 students to communicate on the DSP server. It focuses on sending and receiving messages, managing contacts, and storing messages locally. When users load a `.dsu` file, it displays the messages associated with that user's profile.

## Entry Point

The program starts with `a5.py`. Running this script initiates the GUI for user interaction.

## Main Features

### Messaging
- **Send Messages:** Users can send messages to others in their contact list. 
- **Retrieve Messages:** The app retrieves messages from the DSP server, ensuring users can always access their conversation history.
- **Local Message Storage:** Messages are stored locally in the user profile (`.dsu` file), allowing for a persistent history across sessions.

### User Profiles
- **Profile Management:** Users can load and save their profiles, containing their DSP server credentials and message history, from and to a `.dsu` file.
- **Contact Management:** Users can add contacts, facilitating direct messaging with more individuals on the DSP server.

### GUI Components
- **Login & Configuration:** On startup, users enter DSP server credentials for authentication.
- **Messaging Interface:** Features a contact list and message display area for easy communication.
- **Interactive GUI Elements:** Includes buttons and menus for sending messages, managing contacts, and configuring server settings.

## How to Use

1. **Launch the App:** Start by running `a5.py`.
2. **Load Profile:** Select 'File' menu and open your `.dsu` profile file containing DSP server credentials and any existing message history.
3. **Send & Receive Messages:** Connect to DSP server via 'Settings' menu. After succesfully connected, select a contact to view and send messages. The application will automatically retrieve and display new messages.
4. **Manage Contacts:** Add new contacts via the 'Settings' menu to communicate with more users.

## Technical Details

- **Implementation Language:** Python, utilizing Tkinter for the GUI.
- **DSP Server Communication:** Uses protocols from `ds_protocol.py` for messaging.
- **Local Data Management:** Profiles and messages are stored locally in `.dsu` files, ensuring data persistence.

## Conclusion

ICS 32 DSM simplifies communication for ICS 32 students through an easy-to-use platform. It supports messaging, contact management, and local data storage, enhancing the communication experience within the ICS 32 community.
