# Self Sign the executable - https://themayor.notion.site/Certificate-Signing-Payloads-482f2b500abd42efaa0b17f74e3c73ce

from ctypes import Structure, byref, windll
from ctypes.wintypes import HANDLE, DWORD, LPWSTR, WORD, BYTE
import sys
import time

# https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information
# https://docs.python.org/3/library/ctypes.html#structures-and-unions
# https://docs.python.org/3/library/ctypes.html#ctypes.Structure
'''Here the PROCESS_INFORMATION structure is defined which will be needed for the new process and thread.'''
class PROCINFO(Structure):
    _fields_ = [('Process', HANDLE), ('Thread', HANDLE), ('ProcessId', DWORD), ('ThreadId', DWORD)]

#  https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-startupinfow
'''Here the STARTUPINFOW structure which defines the window station, desktop, handles and appearance. None of these are utilized in the tool,
but are required for functionality.'''
class STARTINFOW(Structure):
    _fields_ = [('cb', DWORD), ('Reserved', LPWSTR), ('Desktop', LPWSTR), ('Title', LPWSTR), ('X', DWORD), ('Y', DWORD), ('XSize', DWORD), ('YSize', DWORD), ('XCountChars', DWORD), ('YCountChars', DWORD), ('FillAttribute', DWORD), ('Flags', DWORD), ('ShowWindow', WORD), ('Reserved2', WORD), ('Reserved2', BYTE), ('StdInput', HANDLE), ('StdOutput', HANDLE), ('StdError', HANDLE)]

# https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createprocesswithlogonw
'''Here the CreateProcessWithLogonW function is defined which will be used to create the new process and thread.
   startupInfo is a pointer to the STARTINFOW structure which is defined above.
   proc_info is a pointer to the PROCINFO structure which is defined above.'''
def CreateProcessWithLogonW(Username, Domain, Password, LogonFlags, ApplicationName, CommandLine, CreationFlags, Environment, CurrentDirectory, startupInfo):
    startupInfo = STARTINFOW()
    proc_info = PROCINFO()
    valid = windll.advapi32.CreateProcessWithLogonW(Username, Domain, Password, LogonFlags, ApplicationName, CommandLine, CreationFlags, Environment, CurrentDirectory, startupInfo, byref(proc_info))
    if not valid:
        print('[!] Check the arguments and credentials and try again.\n')
        sys.exit(1)
    return proc_info

if __name__ == '__main__':
    try:
        user_name = sys.argv[1]
        domain = sys.argv[2]
        password = sys.argv[3]
        command = sys.argv[4]
    except Exception:
        print("[!] USAGE: tokenimpersonate.py <username> <domain> <password> <command>\n")
        sys.exit()
    time.sleep(5)
    '''Here we call the CreateProcessWithLogonW function with the arguments and credentials to create a new process with the impersonated token.'''
    proc = CreateProcessWithLogonW(user_name, domain, password, 0, None, command, 0, None, "C:\\", None)
    print("[+] Process created with PID: %d" % proc.ProcessId)
    print("[+] Thread created with TID: %d" % proc.ThreadId)
    print("[+] Closing process handle")
    close_proc = windll.kernel32.CloseHandle(proc.Process)
    print("[+] Closing thread handle")
    close_hand = windll.kernel32.CloseHandle(proc.Thread)
    print("[+] Done")
