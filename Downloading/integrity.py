import sys
import hashlib
import os

def file_hash(path):
	file = str(path) # Location of the file (can be set a different way)
	BLOCK_SIZE = 65536 # The size of each read from the file

	file_hash = hashlib.md5() # Create the hash object, can use something other than `.sha256()` if you wish
	with open(file, 'rb') as f: # Open the file to read it's bytes
	    fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
	    while len(fb) > 0: # While there is still data being read from the file
		file_hash.update(fb) # Update the hash
		fb = f.read(BLOCK_SIZE) # Read the next block from the file

	return str(file_hash.hexdigest()) # Get the hexadecimal digest of the hash


def folder_hash(path, verbose=0):
    SHAhash = hashlib.md5()
    if not os.path.exists (path):
        return -1

    try:
        for root, dirs, files in os.walk(path):
            for names in files:
                if verbose == 1:
                    print('Hashing', names)
                filepath = os.path.join(root,names)
                try:
                    f1 = open(filepath, 'rb')
                except:
                    # You can't open the file for some reason
                    f1.close()
                    continue

                while 1:
                    # Read file in as little chunks
                    buf = f1.read(4096)
                    if not buf : break
                    SHAhash.update(hashlib.md5(buf).hexdigest())
                f1.close()

    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2

    return str(SHAhash.hexdigest())



if __name__ == "__main__":
    sha_hash = sys.argv[1]
    sha_hash = sha_hash[-40:]
    stri = ""
    for i in sha_hash:
        if i == '.':
            break
        else:
            stri = stri + i
    path = None
    path = sys.argv[2]
    ch   = os.path.isdir(path)
    message_digest = None
    if ch == 1:
        message_digest = folder_hash(path)
    elif ch == 0:
        message_digest = file_hash(path)
    
    if message_digest == stri:
        print("The Data Integrity Check cleared!")
    else:
        raise ValueError("Oops the data is not the same!!")
