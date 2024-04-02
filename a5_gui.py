# THUY NGUYEN
# THUYN18@UCI.EDU
# 10087312

import time
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
from pathlib import Path
from ds_messenger import DirectMessenger
from Profile import Profile1


class Body(tk.Frame):
    '''create and draw widget'''
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self.contact_color_mapping = {}


        self._draw()

    def node_select(self, event):
        try:
            index = int(self.posts_tree.selection()[0])
            entry = self._contacts[index]
            if self._select_callback is not None:
                self._select_callback(entry)
        except IndexError:
            pass

    def _draw(self):
        self.root.configure(bg="#2D2E2E")

        posts_frame = tk.Frame(master=self, width=250, bg="#2D2E2E")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        style = ttk.Style()
        style.configure("Treeview", background="#2D2E2E", foreground="white",
                        fieldbackground="#2D2E2E", highlightthickness=0)
        style.configure("Treeview.Heading", font=('Calibri', 10, 'bold'))
        style.map("Treeview", background=[('selected', "#2D2E2E")])

        self.posts_tree = ttk.Treeview(posts_frame, style='Treeview')
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=10, pady=10)

        entry_frame = tk.Frame(master=self, bg="#2D2E2E")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="#2D2E2E")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="#2D2E2E", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="#2D2E2E")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5, bg="#4A4A4A")
        self.message_editor.tag_configure('entry-right', justify='left', font=('Helvetica', 20))
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
        expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=10, wrap=tk.WORD,
                                    highlightthickness=0, bg="#4A4A4A",
                                    padx=10,pady=10)
        self.entry_editor.tag_configure('entry-left', justify='left',
                                        font=('Arial', 20), foreground='white')
        self.entry_editor.tag_configure('entry-right', justify='right', font=('Segoe UI', 12, 'bold'),
                                        foreground='white', relief='flat',
                                        lmargin1=100, lmargin2=100,
                                        rmargin=10)
        self.entry_editor.pack(fill=tk.BOTH,
                               expand=True, padx=5, pady=5)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)

    def create_tag_for_contact(self, contact_name):
        '''
        generate random color from list of blue tone color
        '''
        if contact_name not in self.contact_color_mapping:
            color_list = [
            '#0D1B2A',  # Oxford Blue
            '#102A43',  # Yale Blue
            '#243B53',  # Dark Electric Blue
            '#334E68',  # Dark Cerulean
            '#486581',  # Queen Blue
            '#627D98']  # Shadow Blue
            color = color_list[len(self.contact_color_mapping) % len(color_list)]
            tag_name = f'contact_{contact_name}_message'

            self.entry_editor.tag_configure(tag_name,
                                            wrap=tk.WORD,
                                            font=('Segoe UI', 12),
                                            foreground='white',
                                            background=color,
                                            relief='flat',
                                            borderwidth=0,
                                            lmargin1=10, rmargin=100,
                                            lmargin2=10, spacing3=5)

            self.contact_color_mapping[contact_name] = tag_name

        return self.contact_color_mapping[contact_name]

    def insert_contact(self, contact: str):
        '''insert contact to main display'''
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        '''insert contact tree to main display'''
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)
    
    def clear_contact_tree(self):
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    def insert_contact_message(self, message: str, sender):
        '''insert message from contact to main display'''
        tag = self.create_tag_for_contact(sender)
        self.entry_editor.insert(tk.END, message + '\n', tag)

    def new_display_message(self, message):
        '''insert message of user to main display'''
        self.entry_editor.insert(tk.END, message + '\n', 'entry-right')

    def get_text_entry(self) -> str:
        '''get text entry from user'''
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text: str):
        '''display text entry'''
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.style = ttk.Style()
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        '''send click event'''
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        '''set and draw widget'''
        self.save_button = tk.Button(master=self,
                                     text="Send",
                                     width=20,
                                     command=self.send_click)
        self.save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # Apply dynamic styling based on button state using event bindings
        self.save_button.bind("<Enter>", self.on_enter)
        self.save_button.bind("<Leave>", self.on_leave)
        self.save_button.bind("<ButtonPress>", self.on_press)
        self.save_button.bind("<ButtonRelease>", self.on_release)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT,
                               padx=5)

    def on_enter(self, event):
        '''enter event'''
        event.widget.config(background='blue', foreground='red')

    def on_leave(self, event):
        '''enter event when leave button'''
        event.widget.config(background=self.root.cget('bg'),
                            foreground='black')

    def on_press(self, event):
        '''enter button when pressed'''
        event.widget.config(background='black',
                            foreground='red')

    def on_release(self, event):
        '''enter button when released'''
        # This will make the button return to its "enter" state after click
        self.on_enter(event)


class NewContactDialog(tk.simpledialog.Dialog):
    '''connect server dialog'''
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        # Initialize variables to store the input
        self.root = root
        self.server_var = tk.StringVar(value=server)
        self.user_var = tk.StringVar(value=user)
        self.pwd_var = tk.StringVar(value=pwd)
        
        super().__init__(root, title)

    def body(self, master):
        '''Create label to collect credentials from users'''
        tk.Label(master, text="Server:").grid(row=0)
        tk.Label(master, text="Username:").grid(row=1)
        tk.Label(master, text="Password:").grid(row=2)

        self.server_entry = tk.Entry(master,
                                     textvariable=self.server_var)
        self.username_entry = tk.Entry(master,
                                       textvariable=self.user_var)
        self.password_entry = tk.Entry(master,
                                       textvariable=self.pwd_var,
                                       show='*')

        self.server_entry.grid(row=0, column=1)
        self.username_entry.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)

    def apply(self):
        ''' Update the class attributes with the entered values '''
        self.server = self.server_entry.get()
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()


class MainApp(tk.Frame):
    '''main application frame'''
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.profile = Profile1()
        self.file_name = None
        self.username = None
        self.password = None
        self.server = '168.235.86.101'
        self.recipient = None
        self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                username=self.username,
                                                password=self.password)
        self.body = Body(self, self.recipient_selected)
        self.body.pack(fill=tk.BOTH, expand=True)

        self._draw()
        self.display_contact()

    def recipient_selected(self, recipient):
        '''Load messages for the selected contact'''
        self.recipient = recipient

        self.load_contact_messages()

    def display_contact(self):
        '''display contact list'''
        if self.profile is not None:
            for contact in self.profile.get_friends():
                self.body.insert_contact(contact)
    
    def clear_contact(self):
        '''clear contact tree before loading new file'''
        self.body.clear_contact_tree()


    def load_contact_messages(self):
        '''display message from other user'''
        try:
            if self.username is None:
                # Clear the entry editor before inserting new messages
                self.body.entry_editor.config(state='normal')
                self.body.entry_editor.delete('1.0', tk.END)

                # Fetch messages for the selected contact
                combined_list = self.profile.get_user_message() + self.profile.get_messages()
                sorted_list = sorted(combined_list, key=lambda x: float(x['timestamp']))
                for item in sorted_list:
                    message = item['message']
                    if item['sender'] == self.profile.username and item['recipient'] == self.recipient:
                        self.body.new_display_message(f'{message}\n')
                    elif item['sender'] == self.recipient and item['recipient'] == self.profile.username:
                        self.body.insert_contact_message(f'{message}\n', self.recipient)
            else:
                # Clear the entry editor before inserting new messages
                self.body.entry_editor.config(state='normal')
                self.body.entry_editor.delete('1.0', tk.END)

                # Fetch messages for the selected contact

                combined_list = self.profile.get_user_message() + self.profile.get_messages()
                sorted_list = sorted(combined_list, key=lambda x: float(x['timestamp']))
                for item in sorted_list:
                    message = item['message']
                    if item['sender'] == self.username and item['recipient'] == self.recipient:
                        self.body.new_display_message(f'{message}\n')
                    elif item['sender'] == self.recipient and item['recipient'] == self.username:
                        self.body.insert_contact_message(f'{message}\n', self.recipient)

            self.body.entry_editor.config(state='disabled')
        except TypeError as e:
            raise Exception('Invalid type.')

    def send_message(self):
        '''send message to selected recipient'''
        message_text = self.body.get_text_entry()
        if message_text and self.recipient:
            # Send the message through DirectMessenger
            sent_successfully = self.direct_messenger.send(message_text, self.recipient)
            if sent_successfully:
                # Clear the message entry field
                self.body.set_text_entry('')

                # Set new message in editor field
                self.body.entry_editor.config(state='normal')
                self.body.new_display_message(message_text)
                self.body.entry_editor.config(state='disabled')

                # save to local storage
                self.profile.add_user_message(self.direct_messenger.username,
                                              self.recipient,
                                              message_text, time.time())
                self.profile.save_profile(self.file_name)
            else:
                tk.messagebox.showerror("Error", "Failed to send the message.")
        else:
            tk.messagebox.showinfo("Info", "Please select a recipient and enter a message.")

    def add_contact(self):
        '''Implement adding a new contact'''
        new_contact = simpledialog.askstring("Add Contact", "Enter contact name:")
        if new_contact:  # Simple validation
            self.body.insert_contact(new_contact)
            # Update Profile
            self.profile.add_friend(new_contact)


    def configure_server(self):
        '''connect server'''
        try:
            ud = NewContactDialog(self.root, "Configure Account",
                                self.username, self.password, self.server)
            self.username = ud.user
            self.password = ud.pwd
            self.server = ud.server
            self.direct_messenger = DirectMessenger(dsuserver=self.server,
                                                    username=self.username,
                                                    password=self.password)

            self.direct_messenger.connect()
        except AttributeError:
            print('Failed to connect to server. Missing user information.')

    def load_profile(self):
        '''load profile using open'''
        file_path = filedialog.askopenfilename(initialdir=".",
                                                title="Select File",
                                                filetypes=[("DSU files", "*.dsu")])
        self.file_name = file_path
        self.profile.load_profile(Path(self.file_name))
        self.clear_contact()

        self.display_contact()
        self.load_contact_messages()

    def check_new(self):
        '''check new message while program is running'''
        if self.username is not None:
            new_messages = self.direct_messenger.retrieve_new()
            if new_messages is not None:
                for message in new_messages:
                    self.profile.add_messages(message.recipient,
                                              self.username, message.message,
                                              message.timestamp)
                    self.profile.save_profile(self.file_name)
                    self.body.insert_contact_message(f"{message.recipient}: {message.message}", message.recipient)
        else:
            pass
        # Schedule the next check
        self.after(2000, self.check_new)

    def _draw(self):
        '''Build a menu and add it to the root frame.'''
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='Open...', command=self.load_profile)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)
