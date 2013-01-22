**What if your laptop was stolen?**

Tracker could help you to find your stolen laptop. You can make your laptop send output of certain commands to a remote server. The server will save the output of commands and client's ip address.

The message that is sent to server is encrypted with AES with Cipher-block chaining mode.

Tracker consists of client(laptop) and server.
Server can be any public webserver that can run PHP.

Installing
----------

1. Install PyCrypto package to your server and laptop with:

    sudo pip install PyCrypto

It may need python-dev packages or something.

2. Move tracker folder to your webserver's public directory, for example */var/www/tracker/*.

3. Give permissions for your web server to write in */var/www/tracker/* directory.

    chmod 775 /var/www/tracker
    chgrp www-data /var/www/tracker

Where you should replace www-data with the correct group. On Apache www-data is default group.

4. Modify *client.py* to your needs:

    server_address = 'http://kimmobrunfeldt.com'

    request_address = server_address + '/tracker/server.php'

    # Cyrpt key for sended text
    crypt_key = 'b794aefd-63bb-11e2-9592-705681c24ac3'

    # Each command is subprocess.Popen's list format.
    # Use absolute paths!
    commands = [['/sbin/ifconfig']]

Change these lines to your needs in the beginning of *client.py*.

*If you change the crypt_key, change it to **tracker/decrypt.py** also.*

5. Add execution of *client.py* to your laptop's crontab.

Execute:

    env EDITOR=nano crontab -e

And add the following line:

    */5 *    *   *   *   python /Users/kimmo/code/python/tracker/client.py &> /dev/null

Where you should replace the *client.py* path with your own. This will execute the client.py every 5 minutes.


6. Done! Now your laptop will send output of certain commands to your server every 5 minutes. Because the message is encrypted, you can now print the message.txt by executing:

    python decrypt.py message.txt

In your server's *tracker/* directory.
