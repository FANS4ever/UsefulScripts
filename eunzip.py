# Extract non unicode archives with specific encoding
import zipfile
import argparse

def unzip(file_path, new_zip_encoding, encoding_error_mode = 'replace'):
    zfile=zipfile.ZipFile(file_path,'r')
    zip_infos = zfile.infolist()
    text_decode = lambda text: text.encode('cp437').decode(new_zip_encoding, encoding_error_mode)
    for i, info in enumerate(zip_infos):
        decoded_filename = text_decode(info.filename)
        print(f'Extract progress {int(((i+1)/len(zip_infos))*100)}% Extracting file: {decoded_filename}')
        info.filename = decoded_filename
        zfile.extract(info)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True,  metavar='TEXT', help="File path")
    parser.add_argument("-e", "--encoding", default='shift-jis',  metavar='TEXT', help="Encoding to use when decoding file names (default: %(default)s)")
    args = parser.parse_args()
    try:
        unzip(args.path, args.encoding)
    except KeyboardInterrupt:
        print('[WARNING] Unzipping was interrupted. The last file being processed could be corrupted.')