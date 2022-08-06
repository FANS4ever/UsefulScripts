#Convenient Base64 cmd tool for windows
import base64
import argparse
import subprocess
import binascii

def do_times(action, input, times, file_path):
    tmp = input if file_path else input.encode('utf-8')

    if file_path and action == base64.b64encode:
        tmp = read_file_bytes(file_path)
    
    for i in range(times):
        tmp = action(tmp)
   
    if file_path and action == base64.b64decode:
        write_file_bytes(file_path, tmp)
        return ''
        
    return tmp

def copy_to_clip(text):
    p = subprocess.Popen('clip', stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, shell=False)
    p.communicate(text)
    p.wait()
    
def write_file_bytes(path, bytes):
    with open(path, "wb") as f:
         f.write(bytes)
         
def read_file_bytes(path):
    with open(path, "rb") as f:
        return f.read()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("-e", "--encode",  metavar='TEXT', help="encode TEXT using Base64")
    action_group.add_argument("-d", "--decode", metavar='TEXT', help="decode TEXT using Base64")
    action_group.add_argument("-ef", "--encode-file", metavar='PATH', help="encode a file(bytes) at PATH using Base64")
    action_group.add_argument("-df", "--decode-file", metavar=('TEXT', 'PATH'), nargs=2, help="decode TEXT to bytes using Base64 and create a file at PATH")
    parser.add_argument("-t", "--times", type=int, default=1, metavar='NUMBER', help="how many times to encode/decode (default: %(default)s)")
    parser.add_argument("-c", "--copy-clipboard", action="store_true", help="copy encoded/decoded value to clipboard (does not work with -df argument)")
    args = parser.parse_args()
    
    #print(args)
    
    action = base64.b64decode
    input = ''
    file_path = None

    if(args.encode):
        action = base64.b64encode
        input = args.encode

    if(args.decode):
        action = base64.b64decode
        input = args.decode
        
    if(args.encode_file):
        action = base64.b64encode
        file_path = args.encode_file
    
    if(args.decode_file):
        action = base64.b64decode
        input = args.decode_file[0]
        file_path = args.decode_file[1]
    
    try:
        processed_input = do_times(action, input, args.times, file_path)
        
        if(not args.decode_file):
            processed_input = processed_input.decode('utf-8')
            print(processed_input)
        
        if(args.decode_file and args.copy_clipboard):
            print("Copy to clipboard is not supported for decoded files")
        elif (args.copy_clipboard):
            copy_to_clip(processed_input)
            print('Copied to clipboard!')

    except binascii.Error as err:
        print(f'ERROR: {err}')
        exit()
    
