# msImpersonate v1.0

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M03Q2JN)

<p align="center">
  <img src="https://github.com/dievus/msimpersonate/blob/main/images/msimpersonate.jpg" />
</p>

msImpersonate is a Python-native user impersonation tool that is capable of impersonating local or network user accounts with valid credentials. The tool was built with internal penetration tests in mind, allowing for local authentication, or network and domain authentication from the tester's dropbox.  The tool utilizes Python's ctypes library to interact with the Windows operating system. Together with the CreateProcessWithLogonW function, it is possible to spawn Command Prompts, Powershell, and other services as the target user. 

msImpersonate will first attempt to authenticate on the local machine. If this is not successful, the tool will attempt to authenticate using netlogon from the CreateProcessWithLogonW function. I may or may not re-add functionality that allows the tester to determine whether to attempt local or network authentication. 

Note that the netlogon parameter cannot differentiate between valid and invalid credentials. As such, any network authentication and service spawn will require further inspection to ensure that the credentials utilized are indeed valid or not.

##### This tool is meant to be executed from WINDOWS and will require Python3 to be installed on the machine

## Usage
##### Installing msImpersonate
```Download the ZIP file from the repository and extract the contents where desired.```

##### Change directories to msImpersonate via command prompt and run:
```pip3 install -r requirements.txt```

##### Execute an impersonation attack
```python3 msimpersonate.py <username> <domain> <password> <command to run>```

##### Note that domain can be blank if authenticating locally using the following:

```python3 msimpersonate.py <username> ' ' <password> <command to run>```

##### Notes
Here is your obligatory don't do anything stupid with my tool. If you do it's your fault.
