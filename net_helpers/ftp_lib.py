#!/usr/bin/env/python
"""
Title:
    Python script for creating and ftp client and interacting with it

Author:
    Abhijit Bansal

"""

# **************************
# region GLOBAL IMPORTS

import ftplib
import logging
import os
import time
import keyring
from c_builder import log

# endregion
# **************************


# For logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class FTPUserNameNotFound(Exception):
    pass


class FTPAuthenticationFailed(Exception):
    pass


class FTPDownloadFailed(Exception):
    pass


class FTPUploadFailed(Exception):
    pass


class FTPHelper(object):
    def __init__(self, user_name, password, url, use_cred_manager=True, show_authentication=True):
        """A Helpful client that expands on the base ftp client library

        Args:
            use_cred_manager (bool): If specified, the password is taken out using user name from the
                                     host credential manager. Will also add/update the password if
                                     successfully authorized
            url (str): URL of the ftp client
            password (str): The password to the server
            user_name (str): user name for the ftp client
        """
        self.url = url
        self.user_name = user_name
        self.password = password
        self.ftp = ftplib.FTP(self.url)
        self.authenticated = False
        self.use_cred_mgr = use_cred_manager
        self.show_authentication = show_authentication
        self._service_name = "FTPHelper"

    def _login(self):
        """To login to the FTP Client"""
        try:
            if not self.password and self.use_cred_mgr:
                password = keyring.get_password(self._service_name, self.user_name)
                if not password:
                    raise FTPUserNameNotFound("{self.user_name} not found in credential manager".format(**locals()))
            else:
                password = self.password

            self.ftp.login(user=self.user_name, passwd=password)

        except Exception as e:
            logger.exception("Authentication Failed")
            raise FTPAuthenticationFailed

        else:
            if self.show_authentication:
                logger.info("Authentication succeeded")

            # Update the password in case it changed
            if self.use_cred_mgr:
                keyring.set_password(self._service_name, self.user_name, self.password)

            self.authenticated = True
            return True

    def download_file(self, server_file_path, dest_dir, block_size=102400):
        """
        To download file from server if needed

        Args:
            block_size (int): Size of the block, can be increase for copying
            dest_dir (str): Local directory to where to copy the file
            server_file_path (str): Path to the file on the server
        """
        file_dir, file_name = os.path.split(server_file_path)

        out_file = os.path.join(dest_dir, file_name)

        try:
            f = open(out_file, 'wb')
            self.ftp.cwd(file_dir)
            self.ftp.retrbinary("RETR " + file_name, f.write, block_size)

        except Exception as e:
            logger.exception("File could not be downloaded")
            raise FTPDownloadFailed

        else:

            logger.info("Successfully FTPed {file_path} to {dest_dir}".format(**locals()))
            return True

        finally:
            # Try to close the file if opened for reading
            try:
                f.close()
            except:
                pass

    def upload_file(self, file_path, dest_dir, block_size=102400):
        """
        To upload a local file to the FTP server

        Args:
            file_path (str): Local file path which needs to be upladed
            dest_dir (str): Server directory to where to copy the file
            block_size (int): The block size to use while uploading, higher size can result in faster upload
        """

        file_dir, file_name = os.path.split(file_path)

        try:
            logger.info("Uploading {file_name}".format(**locals()))
            self.ftp.cwd(dest_dir)
            start_time = time.time()
            # logger.info(start_time)
            self.ftp.storbinary("STOR " + file_name, open(file_path, 'rb'), block_size)
            # logger.info(time.time() - start_time)
        except Exception as e:
            logger.exception("Upload failed")
            raise FTPUploadFailed
        else:
            logger.info("Successfully FTPed {file_path} to {dest_dir}".format(**locals()))
            return True

    def __enter__(self):
        self._login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.ftp.quit()
        except Exception as e:
            pass


if __name__ == '__main__':

    logger.setLevel(logging.DEBUG)
    logger = log.setup_console_logger("FTP", logging.DEBUG)

    # Example
    with FTPHelper("abhijit.bansal", "password", "example.ftp.server") as ftp:
        ftp.upload_file(r'C:\Temp\sample.txt', '/ftp_server/docs/sample/')

