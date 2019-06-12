import sys
import time
import libtorrent as lt
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
          print 'Hashing', names
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


def create_torrent(message_digest):
  #Create torrent
  name = str(message_digest) + ".torrent"
  fs = lt.file_storage()
  lt.add_files(fs, path)
  t = lt.create_torrent(fs)
  trackerList = ['udp://tracker.coppersurfer.tk:6969',
            'udp://tracker.opentrackr.org:1337/announce',
            'udp://torrent.gresille.org:80/announce',
            'udp://9.rarbg.me:2710/announce',
            'udp://p4p.arenabg.com:1337',
            'udp://tracker.internetwarriors.net:1337']

  for tracker in trackerList:        
    t.add_tracker(tracker, 0)
    t.set_creator('libtorrent %s' % lt.version)
    t.set_comment("Test")
    lt.set_piece_hashes(t, ".")
    torrent = t.generate()    
    f = open(name, "wb")
    f.write(lt.bencode(torrent))
    f.close()

    #Seed torrent
    ses = lt.session()
    ses.listen_on(6881, 6891)
    h = ses.add_torrent({'ti': lt.torrent_info(name), 'save_path': '.', 'seed_mode': True}) 
    print("Total size: " + str(h.status().total_wanted))
    print("Name: " + h.name())   
    while h.is_seed():
        s = h.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
          'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

        print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
          (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
        sys.stdout.flush()

        time.sleep(1)


if __name__ == "__main__":
  path = None
  path = input("Enter File/Folder Name within current Directory (~/Uploading):")
  ch   = os.path.isdir(path)
  message_digest = None
  if ch == 1:
    message_digest = folder_hash(path)
  elif ch == 0:
    message_digest = file_hash(path)
  create_torrent(message_digest)

  