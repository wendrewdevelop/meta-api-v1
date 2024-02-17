### TO-DO

- [x] If user's admin (is_staff) show all default folders (user.folder_name);
- [x] Use default folder (user.folder_name) as first folder in directory tree schema;
- [x] Implement uuid instead pk;
- <s>[ ] Implement email send;</s> <b style="color: blue;"><i>now its run in frontend</b></i>
- [x] Implement days to expire file;
    - <s style="color: green;">We will have two dates to define when user file will expire:
        1. days (in quantity not in date) to define when user start receiving notifications;
        2. date of file expiration;
        3. file expiration will start notifying when DATE OF FILE - DAYS.</s>